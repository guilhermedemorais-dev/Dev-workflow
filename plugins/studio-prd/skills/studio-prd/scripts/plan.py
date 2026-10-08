#!/usr/bin/env python3
"""Validate a Studio planning document and render its equivalent human Markdown.

Read-only, stdlib-only. No network calls, approvals or project writes.
"""
import argparse
import html
import json
import math
from pathlib import Path
import posixpath
import re
import sys
from urllib.parse import quote, urlsplit


def require(condition, message):
    if not condition:
        raise ValueError(message)


def required(obj, keys, context):
    require(isinstance(obj, dict), f"{context}: expected object")
    require(set(keys) <= obj.keys(), f"{context}: missing required fields")


def text(value):
    return isinstance(value, str) and bool(value.strip())


def number(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def strings(value):
    return isinstance(value, list) and all(text(item) for item in value)


def source_link(value):
    require(text(value) and not any(ord(c) < 32 for c in value), "invalid source link")
    parsed = urlsplit(value)
    require(parsed.scheme in ("", "https", "http"), "unsafe source link scheme")
    require(not parsed.netloc or parsed.scheme in ("https", "http"), "protocol-relative source link forbidden")
    if parsed.scheme:
        require(bool(parsed.netloc) and parsed.username is None and parsed.password is None, "invalid URL or embedded credential")
    else:
        require(bool(parsed.path), "source path required")
    return value


def estimate(value, context):
    required(value, ("effort_hours", "calendar_days", "confidence", "assumptions"), context)
    require(value["confidence"] in ("UNKNOWN", "LOW", "MEDIUM", "HIGH"), f"{context}: confidence")
    require(strings(value["assumptions"]), f"{context}: assumptions")
    for key in ("effort_hours", "calendar_days"):
        interval = value[key]
        if interval is not None:
            required(interval, ("min", "max"), f"{context}.{key}")
            require(number(interval["min"]) and number(interval["max"])
                    and interval["min"] <= interval["max"], f"{context}: invalid {key} range")


def validate(plan):
    required(plan, ("schema_version", "revision", "project", "status", "sources",
                   "capacity_hours_per_week", "module_count", "modules", "stages",
                   "orders", "parallel_groups", "total_estimate", "resources",
                   "decisions", "change_log"), "plan")
    require(type(plan["schema_version"]) is int and plan["schema_version"] == 1, "unsupported schema_version")
    require(type(plan["revision"]) is int and plan["revision"] > 0, "revision must be positive integer")
    require(text(plan["project"]), "project required")
    require(plan["status"] in ("DRAFT", "IN_REVIEW", "APPROVED"), "invalid plan status")
    required(plan["sources"], ("briefing", "prd"), "sources")
    require(all(text(plan["sources"][k]) for k in ("briefing", "prd")), "source paths required")
    for key in ("briefing", "prd"):
        source_link(plan["sources"][key])
    capacity = plan["capacity_hours_per_week"]
    require(capacity is None or (number(capacity) and capacity > 0), "capacity must be positive or null")
    modules = plan["modules"]
    require(isinstance(modules, list) and modules, "modules required")
    require(type(plan["module_count"]) is int and plan["module_count"] == len(modules), "module_count mismatch")
    ids, task_ids, dependencies = [], [], {}
    for module in modules:
        required(module, ("id", "name", "task_id", "status", "scope", "existing_state",
                          "actors", "dependencies", "urgency", "estimate", "actual_hours",
                          "deliverables", "entry_conditions", "exit_conditions", "resources",
                          "risks", "blockers", "prompt"), "module")
        require(all(text(module[k]) for k in ("id", "name", "task_id", "status", "scope", "existing_state")), "module identity/scope required")
        ids.append(module["id"])
        task_ids.append(module["task_id"])
        for key in ("actors", "deliverables", "entry_conditions", "exit_conditions", "risks", "blockers"):
            require(strings(module[key]), f"{module['id']}: {key} must be string list")
        require(isinstance(module["resources"], list), "module resources must be list")
        require(module["actual_hours"] is None or number(module["actual_hours"]), "invalid actual hours")
        estimate(module["estimate"], module["id"])
        required(module["urgency"], ("level", "reason", "desired_date", "impact", "decision"), "urgency")
        require(all(text(module["urgency"][k]) for k in ("level", "reason", "impact", "decision")), "urgency rationale required")
        require(isinstance(module["dependencies"], list), "dependencies must be list")
        dependencies[module["id"]] = []
        for dependency in module["dependencies"]:
            required(dependency, ("module_id", "capability", "reason"), "dependency")
            require(all(text(dependency[k]) for k in ("module_id", "capability", "reason")), "dependency capability/reason required")
            dependencies[module["id"]].append(dependency["module_id"])
        prompt = module["prompt"]
        required(prompt, ("mode", "task_url", "contract_path", "notes"), "prompt")
        require(prompt["mode"] in ("specification", "execution"), "invalid prompt mode")
        require(strings(prompt["notes"]) and 2 <= len(prompt["notes"]) <= 3, "prompt needs 2-3 contextual notes")
        for key in ("task_url", "contract_path"):
            require(prompt[key] is None or text(prompt[key]), f"invalid prompt {key}")
            if prompt[key] is not None:
                source_link(prompt[key])
        if prompt["mode"] == "execution":
            require(text(prompt["task_url"]) and text(prompt["contract_path"]), "execution prompt requires actual task/contract links")
    require(len(ids) == len(set(ids)), "duplicate module ID")
    require(len(task_ids) == len(set(task_ids)), "one distinct complete task per module required")
    for module_id, deps in dependencies.items():
        require(len(deps) == len(set(deps)), "duplicate dependency")
        require(all(dep in ids and dep != module_id for dep in deps), "unknown/self dependency")
    required(plan["orders"], ("specification", "execution", "integration"), "orders")
    for phase in ("specification", "execution", "integration"):
        order = plan["orders"][phase]
        require(strings(order) and len(order) == len(ids) and set(order) == set(ids), f"{phase}: each module must occur once")
        if phase != "specification":
            for module_id, deps in dependencies.items():
                require(all(order.index(dep) < order.index(module_id) for dep in deps), f"{phase}: dependency order/cycle violation")
    stages = plan["stages"]
    require(isinstance(stages, list) and stages, "stages required")
    covered, stage_ids = [], []
    for stage in stages:
        required(stage, ("id", "title", "module_ids", "entry_conditions", "exit_conditions", "estimate"), "stage")
        require(text(stage["id"]) and text(stage["title"]), "stage identity required")
        require(strings(stage["module_ids"]) and stage["module_ids"], "stage modules required")
        require(strings(stage["entry_conditions"]) and strings(stage["exit_conditions"]), "stage conditions must be lists")
        estimate(stage["estimate"], stage["id"])
        stage_ids.append(stage["id"])
        covered.extend(stage["module_ids"])
    require(len(stage_ids) == len(set(stage_ids)), "duplicate stage ID")
    require(len(covered) == len(ids) and set(covered) == set(ids), "each module must belong to one stage")
    stage_index = {module_id: index for index, stage in enumerate(stages) for module_id in stage["module_ids"]}
    for module_id, deps in dependencies.items():
        require(all(stage_index[dep] <= stage_index[module_id] for dep in deps), "stage dependency order violation")
    estimate(plan["total_estimate"], "total_estimate")
    for key in ("resources", "decisions", "change_log", "parallel_groups"):
        require(isinstance(plan[key], list), f"{key} must be list")
    for group in plan["parallel_groups"]:
        required(group, ("module_ids", "rationale"), "parallel group")
        members = group["module_ids"]
        require(strings(members) and len(members) >= 2 and len(set(members)) == len(members)
                and set(members) <= set(ids) and text(group["rationale"]), "invalid parallel group")
        for member in members:
            pending, seen = list(dependencies[member]), set()
            while pending:
                dep = pending.pop()
                if dep not in seen:
                    seen.add(dep)
                    pending.extend(dependencies[dep])
            require(not (seen & set(members)), "dependent modules cannot run in parallel")
    return plan


LABELS = {
    "schema_version": "Versão do formato", "revision": "Revisão", "project": "Projeto",
    "status": "Estado", "sources": "Fontes", "briefing": "Briefing", "prd": "PRD",
    "capacity_hours_per_week": "Capacidade (horas/semana)", "module_count": "Quantidade de módulos",
    "modules": "Módulos e tasks", "id": "ID", "name": "Nome", "task_id": "Task",
    "scope": "Fronteira funcional", "existing_state": "Estado encontrado", "actors": "Atores",
    "dependencies": "Dependências", "module_id": "Módulo", "capability": "Capacidade necessária",
    "reason": "Motivo", "urgency": "Urgência", "level": "Nível", "desired_date": "Data desejada",
    "impact": "Impacto", "decision": "Decisão", "estimate": "Estimativa", "effort_hours": "Esforço (horas)",
    "calendar_days": "Duração de calendário (dias)", "min": "Mínimo", "max": "Máximo",
    "confidence": "Confiança", "assumptions": "Premissas", "actual_hours": "Horas realizadas",
    "deliverables": "Entregáveis", "entry_conditions": "Condições de entrada", "exit_conditions": "Condições de saída",
    "resources": "Recursos/custos", "risks": "Riscos", "blockers": "Bloqueios", "prompt": "Recado para novo chat",
    "stages": "Etapas", "title": "Título", "module_ids": "Módulos", "orders": "Sequências",
    "specification": "Especificação", "execution": "Execução", "integration": "Integração",
    "parallel_groups": "Paralelismo proposto", "rationale": "Justificativa e conflitos avaliados",
    "total_estimate": "Estimativa total", "decisions": "Decisões", "change_log": "Histórico de alterações",
    "mode": "Modo", "task_url": "Link da task", "contract_path": "Contrato", "notes": "Cuidados específicos",
}


def escaped(value):
    value = html.escape(str(value), quote=False).replace("\n", " ").replace("\r", " ")
    return re.sub(r"([\\`*\[\]_])", r"\\\1", value)


def link(label, value):
    source_link(value)
    parsed = urlsplit(value)
    target = value
    if not parsed.scheme and not value.startswith("/"):
        # Canonical plan location is docs/planejamento/. Inputs are project-root relative.
        target = posixpath.relpath(parsed.path, "docs/planejamento")
        if parsed.query:
            target += "?" + parsed.query
        if parsed.fragment:
            target += "#" + parsed.fragment
    return "[" + escaped(label) + "](<" + quote(target, safe="/:?#=&%") + ">)"


def bullets(value, indent=0):
    prefix = "  " * indent + "- "
    if isinstance(value, dict):
        result = []
        for key, child in value.items():
            label = escaped(LABELS.get(key, key))
            if isinstance(child, (dict, list)) and child:
                result.append(prefix + label + ":")
                result.extend(bullets(child, indent + 1))
            else:
                result.append(prefix + label + ": " + ("Não informado" if child is None else "Nenhum registrado" if child == [] or child == {} else escaped(child)))
        return result
    if isinstance(value, list):
        result = []
        for index, child in enumerate(value, 1):
            if isinstance(child, (dict, list)):
                result.append(prefix + str(index) + ".")
                result.extend(bullets(child, indent + 1))
            else:
                result.append(prefix + escaped(child))
        return result
    return [prefix + escaped(value)]


def render(plan):
    validate(plan)
    lines = ["# Planejamento interno: " + escaped(plan["project"]), "",
             "Documento interno do desenvolvedor. Estimativas não são garantias. Aprovação do PRD não autoriza implementação, merge ou deploy.", ""]
    for key, value in plan.items():
        lines += ["## " + escaped(LABELS.get(key, key)), ""]
        lines += bullets(value) if isinstance(value, (dict, list)) else ["Não informado" if value is None else escaped(value)]
        lines.append("")
    lines += ["## Prompts curtos por task", ""]
    for module in plan["modules"]:
        prompt = module["prompt"]
        action = ("Use sdd-spec-factory para especificar este módulo; implementação não está liberada."
                  if prompt["mode"] == "specification" else
                  "Confira estágio, contrato, receipt de equivalência e autorizações antes de executar a lista autorizada.")
        lines += ["### " + escaped(module["task_id"] + " — " + module["name"]), "",
                  "> Trabalhe na " + escaped(module["task_id"]) + ". " + action,
                  ">", "> Atenção: " + escaped("; ".join(prompt["notes"])) + ". Se surgir lacuna de negócio ou conflito entre módulos, pergunte antes de assumir.",
                  ">", "> Referências: " + link("briefing", plan["sources"]["briefing"]) + "; " + link("PRD", plan["sources"]["prd"]) +
                  "; " + (link("task", prompt["task_url"]) if prompt["task_url"] else "task ainda não vinculada") + "; " + (link("contrato", prompt["contract_path"]) if prompt["contract_path"] else "contrato ainda não criado") + ".", ""]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "render", "check"))
    parser.add_argument("plan", type=Path)
    parser.add_argument("markdown", nargs="?", type=Path)
    args = parser.parse_args(argv)
    try:
        plan = validate(json.loads(args.plan.read_text(encoding="utf-8")))
        if args.command == "render":
            sys.stdout.write(render(plan))
        elif args.command == "check":
            require(args.markdown is not None, "check requires Markdown path")
            require(args.markdown.read_text(encoding="utf-8") == render(plan), "MD/JSON divergence: reconcile and render same revision")
            print("OK: MD/JSON equivalent")
        else:
            print("OK: plan structure valid; approvals and sources NOT VALIDATED")
    except (ValueError, OSError, TypeError) as error:
        print(f"INVALID: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
