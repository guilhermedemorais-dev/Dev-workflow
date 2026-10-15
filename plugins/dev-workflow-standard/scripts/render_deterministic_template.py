#!/usr/bin/env python3
"""Render a UTF-8 template with explicitly declared, validated fields."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any


TOKEN = re.compile(r"\{\{([A-Za-z][A-Za-z0-9_]*)\}\}")
FIELD_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
DESTINATION_ESCAPES = {
    "markdown": {"markdown_inline", "markdown_block"},
    "plain": {"plain"},
    "json": {"json_string"},
}


class TemplateError(ValueError):
    pass


def _load_json(path: Path, label: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise TemplateError(f"cannot read {label}: {exc}") from exc


def _escape(value: str, mode: str) -> str:
    if mode == "plain":
        if any(ord(char) < 32 for char in value):
            raise TemplateError("plain field contains a control character")
        return value
    if mode == "markdown_inline":
        if "\n" in value or "\r" in value:
            raise TemplateError("markdown_inline fields cannot contain line breaks")
        value = html.escape(value, quote=False)
        return re.sub(r"([\\`*_{}\[\]()#+\-.!|>~])", r"\\\1", value)
    if mode == "markdown_block":
        value = value.replace("\r\n", "\n").replace("\r", "\n")
        value = html.escape(value, quote=False)
        return re.sub(r"([\\`*_{}\[\]()#+\-.!|>~])", r"\\\1", value)
    if mode == "json_string":
        return json.dumps(value, ensure_ascii=False)[1:-1]
    raise TemplateError(f"unsupported escape mode: {mode}")


def render(template: str, schema: dict[str, Any], values: dict[str, Any]) -> str:
    fields = schema.get("fields")
    if schema.get("schema_version") != 1 or not isinstance(fields, dict) or not fields:
        raise TemplateError("schema must declare schema_version 1 and fields")
    if schema.get("destination") not in ("markdown", "plain", "json"):
        raise TemplateError("schema must declare destination markdown, plain, or json")
    if set(values) != set(fields):
        missing, extra = sorted(set(fields) - set(values)), sorted(set(values) - set(fields))
        details = []
        if missing:
            details.append("missing: " + ", ".join(missing))
        if extra:
            details.append("extra: " + ", ".join(extra))
        raise TemplateError("field set mismatch (" + "; ".join(details) + ")")
    tokens = TOKEN.findall(template)
    if "{{" in TOKEN.sub("", template) or "}}" in TOKEN.sub("", template):
        raise TemplateError("malformed template token")
    if set(tokens) != set(fields):
        unknown = sorted(set(tokens) - set(fields))
        unused = sorted(set(fields) - set(tokens))
        raise TemplateError(f"template/schema mismatch (unknown={unknown}, unused={unused})")

    rendered: dict[str, str] = {}
    for name, rule in fields.items():
        if not FIELD_NAME.fullmatch(name) or not isinstance(rule, dict):
            raise TemplateError("invalid field declaration")
        value = values[name]
        kind = rule.get("type", "string")
        if kind == "string":
            if not isinstance(value, str):
                raise TemplateError(f"{name} must be a string")
            maximum = rule.get("max_length", 4000)
            if not isinstance(maximum, int) or isinstance(maximum, bool) or maximum < 0:
                raise TemplateError(f"{name} has an invalid max_length schema")
            if len(value) > maximum:
                raise TemplateError(f"{name} exceeds max_length")
            enum = rule.get("enum")
            if enum is not None:
                if not isinstance(enum, list) or not all(isinstance(item, str) for item in enum):
                    raise TemplateError(f"{name} has an invalid enum schema")
                if value not in enum:
                    raise TemplateError(f"{name} is not an allowed enum value")
            pattern = rule.get("pattern")
            if pattern is not None:
                if not isinstance(pattern, str):
                    raise TemplateError(f"{name} has an invalid pattern schema")
                try:
                    matched = re.fullmatch(pattern, value)
                except re.error as exc:
                    raise TemplateError(f"{name} has an invalid pattern schema: {exc}") from exc
                if matched is None:
                    raise TemplateError(f"{name} does not match its declared format")
            escape_mode = rule.get("escape", "plain")
            if escape_mode not in DESTINATION_ESCAPES[schema["destination"]]:
                raise TemplateError(f"{name} escape mode is incompatible with {schema['destination']} destination")
            rendered[name] = _escape(value, escape_mode)
        elif kind == "integer":
            if not isinstance(value, int) or isinstance(value, bool):
                raise TemplateError(f"{name} must be an integer")
            minimum, maximum = rule.get("min"), rule.get("max")
            if ((minimum is not None and (not isinstance(minimum, int) or isinstance(minimum, bool))) or
                    (maximum is not None and (not isinstance(maximum, int) or isinstance(maximum, bool)))):
                raise TemplateError(f"{name} has an invalid range schema")
            if minimum is not None and value < minimum or maximum is not None and value > maximum:
                raise TemplateError(f"{name} is outside its allowed range")
            rendered[name] = str(value)
        elif kind == "boolean":
            if not isinstance(value, bool):
                raise TemplateError(f"{name} must be a boolean")
            rendered[name] = "true" if value else "false"
        else:
            raise TemplateError(f"unsupported field type: {kind}")

    # A single substitution pass means inserted values are never interpreted again.
    return TOKEN.sub(lambda match: rendered[match.group(1)], template)


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o600
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    stream = os.fdopen(fd, "wb")
    try:
        os.fchmod(stream.fileno(), mode)
        with stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except Exception:
        stream.close()
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--values", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        output_path = args.output.resolve()
        input_paths = {args.template.resolve(), args.schema.resolve(), args.values.resolve()}
        if output_path in input_paths:
            raise TemplateError("output path must not overwrite the template, schema, or values file")
        template = args.template.read_text(encoding="utf-8")
        schema = _load_json(args.schema, "schema")
        values = _load_json(args.values, "values")
        if not isinstance(schema, dict) or not isinstance(values, dict):
            raise TemplateError("schema and values must be JSON objects")
        result = render(template, schema, values)
        atomic_write(args.output, result.encode("utf-8"))
        print("template rendered deterministically")
        return 0
    except (OSError, UnicodeError, TemplateError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
