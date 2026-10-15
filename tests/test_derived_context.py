import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "plugins/dev-workflow-standard/scripts/derive_context.py"
SPEC = importlib.util.spec_from_file_location("derive_context", SCRIPT)
derive_context = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(derive_context)


class DerivedContextTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "canonical.md"
        self.source.write_text(
            "Regra: merge exige aprovação humana.\n"
            "Exceção: merge automático é proibido mesmo se os testes passarem.\n"
            "Negação: credencial não pode ser gravada em texto.\n"
            + "\n".join(f"Contexto secundário sem regra aplicável {index}." for index in range(40))
            + "\n",
            encoding="utf-8",
        )
        self.plan = self.root / "plan.json"
        self.plan.write_text(json.dumps({
            "schema_version": 1,
            "sources": [{
                "path": "canonical.md",
                "selections": [
                    {"start": 1, "end": 3, "purpose": "regras e exceções relevantes"}
                ],
            }],
            "cases": [
                {"id": "approval", "query": "Qual é a regra de merge?", "must_include": ["merge exige aprovação humana"]},
                {"id": "exception", "query": "O merge automático pode ser liberado?", "must_include": ["merge automático é proibido"]},
                {"id": "secret", "query": "Como tratar credenciais?", "must_include": ["credencial não pode ser gravada em texto"]},
            ],
            "negative_controls": [
                {"id": "remove-exception", "operation": "remove", "target": "Exceção: merge automático é proibido", "must_fail_cases": ["exception"]},
                {"id": "invert-negation", "operation": "replace", "target": "credencial não pode", "replacement": "credencial pode", "must_fail_cases": ["secret"]},
            ],
        }, ensure_ascii=False), encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_artifact_has_exact_excerpt_hash_and_no_semantic_claim(self):
        artifact, selected = derive_context.build_artifact(self.plan)
        self.assertEqual(selected, "".join(self.source.read_text(encoding="utf-8").splitlines(keepends=True)[:3]))
        self.assertEqual(artifact["sources"][0]["sha256"], derive_context.sha256(self.source.read_bytes()))
        self.assertEqual(artifact["evaluation"]["result"], "PASS")
        self.assertFalse(artifact["evaluation"]["semantic_equivalence_claim"])
        self.assertEqual(artifact["evaluation"]["negative_controls"], 2)
        sizes = artifact["evaluation"]["size_measurement"]
        self.assertLess(sizes["derived_context_bytes"], sizes["canonical_source_bytes"])
        self.assertGreater(sizes["reduction_ratio"], 0)

    def test_mutation_controls_fail_if_their_case_does_not_detect_mutation(self):
        plan = json.loads(self.plan.read_text(encoding="utf-8"))
        plan["negative_controls"][0]["must_fail_cases"] = ["approval"]
        text = self.source.read_text(encoding="utf-8")
        failures = derive_context.evaluate(text, plan)
        self.assertTrue(any("mutation was not detected" in failure for failure in failures))

    def test_mutation_detects_one_missing_fact_even_when_another_remains(self):
        plan = json.loads(self.plan.read_text(encoding="utf-8"))
        plan["cases"].append({
            "id": "two-facts",
            "query": "What governs merge and its exception?",
            "must_include": ["merge exige aprovação humana", "merge automático é proibido"],
        })
        plan["negative_controls"].append({
            "id": "remove-one-fact",
            "operation": "remove",
            "target": "merge exige aprovação humana",
            "must_fail_cases": ["two-facts"],
        })
        failures = derive_context.evaluate(self.source.read_text(encoding="utf-8"), plan)
        self.assertFalse(any("remove-one-fact: mutation was not detected" in failure for failure in failures))

    def test_source_change_invalidates_and_returns_canonical_text(self):
        artifact_path = self.root / "derived.json"
        artifact, _ = derive_context.build_artifact(self.plan)
        artifact["plan_reference"] = self.plan.name
        artifact_path.write_text(json.dumps(artifact), encoding="utf-8")
        self.source.write_text("Fonte canônica revisada.\n", encoding="utf-8")
        valid, message, fallback = derive_context.verify_artifact(artifact_path)
        self.assertFalse(valid)
        self.assertIn("source changed", message)
        self.assertEqual(fallback, self.source.read_text(encoding="utf-8"))

    def test_source_change_with_possible_secret_suppresses_fallback(self):
        artifact, _ = derive_context.build_artifact(self.plan)
        artifact["plan_reference"] = self.plan.name
        artifact_path = self.root / "derived.json"
        artifact_path.write_text(json.dumps(artifact), encoding="utf-8")
        self.source.write_text("token = 'ghp_abcdefghijklmnopqrstuvwxyz1234567890'\n", encoding="utf-8")
        valid, message, fallback = derive_context.verify_artifact(artifact_path)
        self.assertFalse(valid)
        self.assertIn("source changed", message)
        self.assertEqual(fallback, "")

    def test_plan_change_invalidates_artifact(self):
        artifact, _ = derive_context.build_artifact(self.plan)
        artifact["plan_reference"] = self.plan.name
        artifact_path = self.root / "derived.json"
        artifact_path.write_text(json.dumps(artifact), encoding="utf-8")
        plan = json.loads(self.plan.read_text(encoding="utf-8"))
        plan["cases"][0]["query"] = "pergunta alterada"
        self.plan.write_text(json.dumps(plan), encoding="utf-8")
        valid, message, fallback = derive_context.verify_artifact(artifact_path)
        self.assertFalse(valid)
        self.assertIn("plan changed", message)
        self.assertEqual(fallback, self.source.read_text(encoding="utf-8"))

    def test_plan_requires_exception_and_negation_controls(self):
        plan = json.loads(self.plan.read_text(encoding="utf-8"))
        plan["negative_controls"] = plan["negative_controls"][:1]
        self.plan.write_text(json.dumps(plan), encoding="utf-8")
        with self.assertRaisesRegex(derive_context.ContextError, "inversion control"):
            derive_context.build_artifact(self.plan)

    def test_possible_secret_source_is_blocked(self):
        self.source.write_text("api_key = 'abcdefghijklmnop123456'\n", encoding="utf-8")
        with self.assertRaisesRegex(derive_context.ContextError, "possible secret"):
            derive_context.build_artifact(self.plan)

    def test_possible_secret_in_plan_purpose_is_blocked_before_artifact_return(self):
        plan = json.loads(self.plan.read_text(encoding="utf-8"))
        plan["sources"][0]["selections"][0]["purpose"] = "owner token ghp_abcdefghijklmnopqrstuvwxyz1234567890"
        self.plan.write_text(json.dumps(plan), encoding="utf-8")
        with self.assertRaisesRegex(derive_context.ContextError, "possible secret detected in derived artifact"):
            derive_context.build_artifact(self.plan)

    def test_evaluation_failure_returns_canonical_source_fallback(self):
        plan = json.loads(self.plan.read_text(encoding="utf-8"))
        plan["cases"][1]["must_include"] = ["Contexto secundário sem regra aplicável 39."]
        self.plan.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        with self.assertRaisesRegex(derive_context.ContextError, "evaluation failed") as caught:
            derive_context.build_artifact(self.plan)
        self.assertEqual(caught.exception.fallback_text, self.source.read_text(encoding="utf-8"))

    def test_query_case_must_be_answerable_from_canonical_source(self):
        plan = json.loads(self.plan.read_text(encoding="utf-8"))
        plan["cases"][0]["must_include"] = ["answer absent from original"]
        self.plan.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        with self.assertRaisesRegex(derive_context.ContextError, "not answerable from the canonical source") as caught:
            derive_context.build_artifact(self.plan)
        self.assertEqual(caught.exception.fallback_text, self.source.read_text(encoding="utf-8"))

    def test_source_traversal_outside_root_is_rejected(self):
        plan = json.loads(self.plan.read_text(encoding="utf-8"))
        plan["sources"][0]["path"] = "../../etc/passwd"
        self.plan.write_text(json.dumps(plan), encoding="utf-8")
        with self.assertRaisesRegex(derive_context.ContextError, "outside the allowed root"):
            derive_context.build_artifact(self.plan, self.root)

    def test_tampered_artifact_path_traversal_is_rejected(self):
        artifact_path = self.root / "derived.json"
        artifact, _ = derive_context.build_artifact(self.plan, self.root)
        artifact["plan_reference"] = "../../etc/passwd"
        artifact_path.write_text(json.dumps(artifact), encoding="utf-8")
        valid, message, fallback = derive_context.verify_artifact(artifact_path, self.root)
        self.assertFalse(valid)
        self.assertIn("outside the allowed root", message)
        self.assertEqual(fallback, "")

    def test_malformed_artifact_shapes_fail_without_traceback(self):
        artifact_path = self.root / "derived.json"
        for value in ("[]", "null", '{"schema_version":1,"sources":"bad"}'):
            artifact_path.write_text(value, encoding="utf-8")
            valid, message, fallback = derive_context.verify_artifact(artifact_path, self.root)
            self.assertFalse(valid)
            self.assertTrue(message)
            self.assertEqual(fallback, "")

    def test_output_cannot_overwrite_plan_or_canonical_source(self):
        plan_before = self.plan.read_bytes()
        source_before = self.source.read_bytes()
        for output in (self.plan, self.source):
            result = subprocess.run([
                sys.executable, str(SCRIPT), "--plan", str(self.plan), "--root", str(self.root),
                "--output", str(output),
            ], capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 2)
            self.assertIn("must not overwrite", result.stderr)
        self.assertEqual(self.plan.read_bytes(), plan_before)
        self.assertEqual(self.source.read_bytes(), source_before)


if __name__ == "__main__":
    unittest.main()
