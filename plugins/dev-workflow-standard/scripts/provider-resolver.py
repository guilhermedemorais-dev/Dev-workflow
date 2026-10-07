#!/usr/bin/env python3
"""Resolve configured LLM providers/models without persisting credentials."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "skills" / "dev-workflow-standard" / "references" / "provider-registry.json"


def load_registry(path: Path = REGISTRY_PATH) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("providers"), list):
        raise ValueError("invalid provider registry")
    ids = [item.get("id") for item in data["providers"] if isinstance(item, dict)]
    if any(not isinstance(item, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", item) for item in ids):
        raise ValueError("invalid provider id")
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate provider id")
    return data


def provider_by_id(registry: dict, provider_id: str) -> dict:
    matches = [p for p in registry["providers"] if p.get("id") == provider_id]
    if len(matches) != 1:
        raise ValueError("provider missing or ambiguous")
    return matches[0]


def configuration_state(provider: dict) -> str:
    env_key = provider.get("env_key")
    if not isinstance(env_key, str) or not env_key:
        return "UNCONFIGURED"
    return "CONFIGURED" if os.environ.get(env_key) else "UNCONFIGURED"


def safe_provider(provider: dict) -> dict:
    return {
        key: value
        for key, value in provider.items()
        if key not in {"secret", "token", "api_key"}
    }


def models_url(provider: dict) -> str:
    base = provider.get("base_url")
    path = provider.get("models_path", "/models")
    if not isinstance(base, str) or not base.startswith("https://"):
        raise ValueError("provider has no safe HTTPS base_url")
    if not isinstance(path, str) or not path.startswith("/"):
        raise ValueError("invalid models_path")
    return base.rstrip("/") + path


def request_models(provider: dict, timeout: float = 12.0) -> list[str]:
    if provider.get("direct_probe_supported") is False:
        raise RuntimeError("ADAPTER_REQUIRED")
    env_key = provider.get("env_key")
    token = os.environ.get(env_key or "")
    if not token:
        raise RuntimeError("UNCONFIGURED")
    request = Request(
        models_url(provider),
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        method="GET",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        raise RuntimeError(f"HTTP_{error.code}") from None
    except (URLError, TimeoutError, OSError, ValueError):
        raise RuntimeError("UNAVAILABLE") from None

    raw = payload.get("data", payload.get("models", [])) if isinstance(payload, dict) else []
    result: list[str] = []
    for item in raw if isinstance(raw, list) else []:
        model_id = item.get("id") if isinstance(item, dict) else item
        if isinstance(model_id, str) and model_id and model_id not in result:
            result.append(model_id)
    return sorted(result)


def infer_capabilities(provider: dict, model_id: str) -> list[str]:
    hints = provider.get("technology_model_hints", {})
    if not isinstance(hints, dict):
        return []
    normalized = model_id.lower()
    found: list[str] = []
    for capability, patterns in hints.items():
        if not isinstance(capability, str) or not isinstance(patterns, list):
            continue
        if any(isinstance(pattern, str) and pattern.lower() in normalized for pattern in patterns):
            found.append(capability)
    return sorted(found)


def status(registry: dict) -> dict:
    providers = []
    for provider in sorted(registry["providers"], key=lambda p: p.get("priority", 9999)):
        state = configuration_state(provider)
        if provider.get("direct_probe_supported") is False and state == "CONFIGURED":
            state = "ADAPTER_REQUIRED"
        providers.append({
            "id": provider["id"],
            "name": provider.get("name", provider["id"]),
            "state": state,
            "env_key": provider.get("env_key"),
            "docs_url": provider.get("docs_url"),
            "setup_url": provider.get("setup_url"),
        })
    configured = [p for p in providers if p["state"] in {"CONFIGURED", "AVAILABLE"}]
    return {
        "mode": "MULTI_PROVIDER_READY" if len(configured) > 1 else "SINGLE_AGENT_OR_UNVERIFIED",
        "providers": providers,
    }


def discover(provider: dict) -> dict:
    state = configuration_state(provider)
    if state == "UNCONFIGURED":
        return {"provider": provider["id"], "state": state, "models": []}
    if provider.get("direct_probe_supported") is False:
        return {"provider": provider["id"], "state": "ADAPTER_REQUIRED", "models": []}
    try:
        models = request_models(provider)
    except RuntimeError as error:
        return {"provider": provider["id"], "state": str(error), "models": []}
    return {
        "provider": provider["id"],
        "state": "AVAILABLE",
        "models": [
            {"id": model_id, "capabilities": infer_capabilities(provider, model_id)}
            for model_id in models
        ],
    }


def select(registry: dict, capability: str, provider_id: str | None = None,
           model_id: str | None = None, perform_discovery: bool = False) -> dict:
    candidates = sorted(registry["providers"], key=lambda p: p.get("priority", 9999))
    if provider_id:
        candidates = [provider_by_id(registry, provider_id)]

    for provider in candidates:
        if configuration_state(provider) != "CONFIGURED":
            continue
        if provider.get("direct_probe_supported") is False:
            continue

        if model_id:
            inferred = infer_capabilities(provider, model_id)
            if capability in inferred or not inferred:
                return {
                    "state": "SELECTED_UNVERIFIED",
                    "provider": provider["id"],
                    "model": model_id,
                    "capability": capability,
                    "next_action": "probe the exact model/runtime before execution",
                }
            continue

        if not perform_discovery:
            return {
                "state": "NEEDS_DISCOVERY",
                "provider": provider["id"],
                "capability": capability,
                "next_action": "run discover/probe before routing execution",
            }

        result = discover(provider)
        if result.get("state") != "AVAILABLE":
            continue
        matching = [m for m in result["models"] if capability in m.get("capabilities", [])]
        if matching:
            return {
                "state": "SELECTED",
                "provider": provider["id"],
                "model": matching[0]["id"],
                "capability": capability,
                "evidence": "provider model discovery",
            }

    return {
        "state": "BLOCKED",
        "capability": capability,
        "reason": "no configured compatible provider/model was verified",
        "next_action": "configure a provider or approve a compatible fallback",
    }


def codex_template(registry: dict) -> str:
    blocks = []
    for provider in sorted(registry["providers"], key=lambda p: p.get("priority", 9999)):
        if provider.get("api_style") != "openai-compatible" or not provider.get("base_url"):
            continue
        pid = provider["id"]
        blocks.extend([
            f"[model_providers.{pid}]",
            f'name = "{provider.get("name", pid)}"',
            f'base_url = "{provider["base_url"]}"',
            f'env_key = "{provider["env_key"]}"',
            "# Verify the current host wire/API compatibility before enabling this provider.",
            "",
        ])
    return "\n".join(blocks).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("catalog", "status", "discover", "select", "codex-template"))
    parser.add_argument("--provider")
    parser.add_argument("--model")
    parser.add_argument("--capability", default="coding")
    parser.add_argument("--discover", action="store_true")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()

    registry = load_registry(args.registry)
    if args.action == "catalog":
        output = {"providers": [safe_provider(p) for p in registry["providers"]]}
    elif args.action == "status":
        output = status(registry)
    elif args.action == "discover":
        if not args.provider:
            parser.error("--provider is required for discover")
        output = discover(provider_by_id(registry, args.provider))
    elif args.action == "select":
        output = select(registry, args.capability, args.provider, args.model, args.discover)
    else:
        sys.stdout.write(codex_template(registry))
        return 0

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
