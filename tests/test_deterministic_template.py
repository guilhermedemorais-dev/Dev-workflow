import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins/dev-workflow-standard/scripts/render_deterministic_template.py"
SPEC = importlib.util.spec_from_file_location("render_deterministic_template", SCRIPT)
renderer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(renderer)
CONTEXT_SCRIPT = ROOT / "plugins/dev-workflow-standard/scripts/derive_context.py"
CONTEXT_SPEC = importlib.util.spec_from_file_location("derive_context_for_renderer_tests", CONTEXT_SCRIPT)
derive_context = importlib.util.module_from_spec(CONTEXT_SPEC)
CONTEXT_SPEC.loader.exec_module(derive_context)


class DeterministicTemplateTests(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads((ROOT / "plugins/sdd-spec-factory/templates/task-template.schema.json").read_text(encoding="utf-8"))
        self.template = (ROOT / "plugins/sdd-spec-factory/templates/task-template.md").read_text(encoding="utf-8")
        self.values = {"task_id": "TASK-058", "task_title": "Revisão Unicode, ação & exceção"}

    def test_existing_task_template_renders_with_fixed_text_unchanged(self):
        rendered = renderer.render(self.template, self.schema, self.values)
        expected = self.template.replace("{{task_id}}", "TASK\\-058").replace("{{task_title}}", "Revisão Unicode, ação &amp; exceção")
        self.assertEqual(rendered.encode("utf-8"), expected.encode("utf-8"))
        self.assertTrue(rendered.startswith("# TASK\\-058: Revisão Unicode, ação &amp; exceção\n"))
        self.assertIn("A GitHub Issue é o card humano completo", rendered)

    def test_repeated_rendering_is_byte_deterministic(self):
        first = renderer.render(self.template, self.schema, self.values).encode("utf-8")
        second = renderer.render(self.template, self.schema, self.values).encode("utf-8")
        self.assertEqual(first, second)

    def test_only_allowlisted_fields_are_accepted(self):
        with self.assertRaisesRegex(renderer.TemplateError, "field set mismatch"):
            renderer.render("{{task_id}} {{task_title}}", self.schema, {"task_id": "TASK-1"})
        with self.assertRaisesRegex(renderer.TemplateError, "field set mismatch"):
            renderer.render("{{task_id}} {{task_title}}", self.schema, {**self.values, "extra": "x"})

    def test_invalid_pattern_and_length_fail(self):
        with self.assertRaisesRegex(renderer.TemplateError, "declared format"):
            renderer.render(self.template, self.schema, {**self.values, "task_id": "not-a-task"})
        with self.assertRaisesRegex(renderer.TemplateError, "max_length"):
            renderer.render(self.template, self.schema, {**self.values, "task_title": "x" * 121})

    def test_inserted_values_are_not_processed_as_templates(self):
        result = renderer.render("Fix: {{message}}", {
            "schema_version": 1,
            "destination": "plain",
            "fields": {"message": {"type": "string", "escape": "plain"}},
        }, {"message": "literal {{message}} stays literal"})
        self.assertEqual(result, "Fix: literal {{message}} stays literal")

    def test_validation_failure_does_not_replace_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            output = base / "out.md"
            output.write_bytes(b"existing complete output\n")
            template_path, schema_path, values_path = base / "template.md", base / "schema.json", base / "values.json"
            template_path.write_text("{{task_id}} {{task_title}}", encoding="utf-8")
            schema_path.write_text(json.dumps(self.schema), encoding="utf-8")
            values_path.write_text(json.dumps({"task_id": "bad", "task_title": "new"}), encoding="utf-8")
            result = subprocess.run([
                sys.executable, str(SCRIPT), "--template", str(template_path),
                "--schema", str(schema_path), "--values", str(values_path), "--output", str(output),
            ], capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(output.read_bytes(), b"existing complete output\n")

    def test_output_cannot_overwrite_any_input_file(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            template_path, schema_path, values_path = base / "template.md", base / "schema.json", base / "values.json"
            template_path.write_text("{{task_id}} {{task_title}}", encoding="utf-8")
            schema_path.write_text(json.dumps(self.schema), encoding="utf-8")
            values_path.write_text(json.dumps(self.values, ensure_ascii=False), encoding="utf-8")
            snapshots = {path: path.read_bytes() for path in (template_path, schema_path, values_path)}
            for output in snapshots:
                result = subprocess.run([
                    sys.executable, str(SCRIPT), "--template", str(template_path),
                    "--schema", str(schema_path), "--values", str(values_path), "--output", str(output),
                ], capture_output=True, text=True, check=False)
                self.assertEqual(result.returncode, 2)
                self.assertIn("must not overwrite", result.stderr)
                self.assertEqual(output.read_bytes(), snapshots[output])

    def test_malformed_or_unused_tokens_fail_closed(self):
        with self.assertRaisesRegex(renderer.TemplateError, "mismatch"):
            renderer.render("{{task_id}} {{unknown}}", self.schema, self.values)
        with self.assertRaisesRegex(renderer.TemplateError, "malformed"):
            renderer.render("{{task_id}} {{task_title", self.schema, self.values)

    def test_markdown_field_escapes_markup_and_unicode_survives(self):
        title = "Olá <script>alert(1)</script> | *título*"
        output = renderer.render("# {{title}}", {
            "schema_version": 1,
            "destination": "markdown",
            "fields": {"title": {"type": "string", "escape": "markdown_inline"}},
        }, {"title": title})
        self.assertNotIn("<script>", output)
        self.assertNotIn("*título*", output)
        self.assertIn("Olá", output)
        self.assertIn("\\|", output)

    def test_newline_normalization_for_markdown_block(self):
        output = renderer.render("{{body}}", {
            "schema_version": 1,
            "destination": "markdown",
            "fields": {"body": {"type": "string", "escape": "markdown_block"}},
        }, {"body": "primeira\r\nsegunda"})
        self.assertIn("primeira\nsegunda", output)
        self.assertNotIn("\r", output)

    def test_destination_requires_matching_string_escape_and_json_remains_valid(self):
        schema = {
            "schema_version": 1,
            "destination": "json",
            "fields": {"name": {"type": "string", "escape": "plain"}},
        }
        with self.assertRaisesRegex(renderer.TemplateError, "incompatible with json"):
            renderer.render('{"name":"{{name}}"}', schema, {"name": '"unsafe"'})
        schema["fields"]["name"]["escape"] = "json_string"
        output = renderer.render('{"name":"{{name}}"}', schema, {"name": '"safe" \\ path'})
        self.assertEqual(json.loads(output), {"name": '"safe" \\ path'})

    def test_tampered_context_artifact_does_not_verify(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source = base / "source.md"
            source.write_text("Conteúdo aprovado.\n" + "linha sem regra.\n" * 20, encoding="utf-8")
            plan = base / "plan.json"
            plan.write_text(json.dumps({
                "schema_version": 1,
                "sources": [{"path": "source.md", "selections": [{"start": 1, "end": 1, "purpose": "texto"}]}],
                "cases": [{"id": "positive", "query": "qual texto?", "must_include": ["Conteúdo aprovado"]}],
                "negative_controls": [
                    {"id": "remove", "operation": "remove", "target": "Conteúdo aprovado", "must_fail_cases": ["positive"]},
                    {"id": "invert", "operation": "replace", "target": "aprovado", "replacement": "rejeitado", "must_fail_cases": ["positive"]},
                ],
            }, ensure_ascii=False), encoding="utf-8")
            artifact, _ = derive_context.build_artifact(plan)
            artifact_path = base / "derived.json"
            artifact["plan_reference"] = plan.name
            artifact["evaluation"]["semantic_equivalence_claim"] = True
            artifact_path.write_text(json.dumps(artifact, ensure_ascii=False), encoding="utf-8")
            valid, message, _ = derive_context.verify_artifact(artifact_path)
            self.assertFalse(valid)
            self.assertIn("evaluation changed", message)


if __name__ == "__main__":
    unittest.main()
