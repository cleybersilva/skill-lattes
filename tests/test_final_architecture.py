import importlib.util
import tempfile
import unittest
import json
import subprocess
import sys
from pathlib import Path
from xml.etree.ElementTree import Element, ElementTree


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    path = ROOT / "lattes-atualizar" / "scripts" / name
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FinalArchitectureTests(unittest.TestCase):
    def test_browser_adapter_builds_safe_plan_and_requires_authorization(self):
        module = load("lattes_browser_adapter.py")
        manifest = {
            "schema": "lattes-batch-v1",
            "items": [
                {"key": "1", "sheet": "Página1", "row": 2, "proposal": {"title": "A"}, "authorized": True},
                {"key": "2", "sheet": "Página1", "row": 3, "proposal": {"title": "B"}, "authorized": False},
            ],
        }
        plan = module.build_plan(manifest)
        self.assertEqual(plan[0]["state"], "aprovado")
        self.assertEqual(plan[1]["state"], "bloqueado")

    def test_browser_adapter_rejects_unsupported_manifest(self):
        module = load("lattes_browser_adapter.py")
        with self.assertRaisesRegex(ValueError, "Manifesto incompatível"):
            module.build_plan({"schema": "outro", "items": []})

    def test_browser_launcher_supports_three_engine_names(self):
        script = ROOT / "lattes-atualizar" / "scripts" / "live_lattes_session.py"
        text = script.read_text(encoding="utf-8")
        self.assertIn('"chrome"', text)
        self.assertIn('"edge"', text)
        self.assertIn('"firefox"', text)
        self.assertIn("find_browser_executable", text)

    def test_blank_xlsx_template_is_generated_without_personal_data(self):
        script = ROOT / "lattes-atualizar" / "scripts" / "generate_template_xlsx.py"
        spec = importlib.util.spec_from_file_location("template", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "modelo.xlsx"
            module.generate(output)
            from openpyxl import load_workbook
            workbook = load_workbook(output)
            sheet = workbook["Página1"]
            self.assertEqual(sheet["A1"].value, "Ano")
            self.assertEqual(sheet["I1"].value, "Solicitado")
            self.assertEqual(sheet["J1"].value, "Atualizado")
            self.assertIsNone(sheet["A2"].value)
            self.assertIn("Instruções", workbook.sheetnames)
            self.assertIn("Exemplo fictício", workbook.sheetnames)
            example = workbook["Exemplo fictício"]
            self.assertEqual(example["A2"].value, 2026)
            self.assertEqual(example["B2"].value, "Artigo")
            self.assertEqual(example["I2"].value, "Sim")
            self.assertEqual(example["J2"].value, "Não")

    def test_approved_batch_manifest_is_schema_bound(self):
        script = ROOT / "lattes-atualizar" / "scripts" / "create_batch_manifest.py"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            items = root / "items.json"
            output = root / "manifest.json"
            items.write_text(json.dumps([{
                "key": "linha-2",
                "sheet": "Página1",
                "row": 2,
                "proposal": {"Atualizado": True},
            }]), encoding="utf-8")
            subprocess.run(
                [sys.executable, str(script), str(items), "--output", str(output)],
                check=True,
                capture_output=True,
                text=True,
            )
            manifest = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(manifest["schema"], "lattes-batch-v1")
            self.assertTrue(manifest["items"][0]["authorized"])
            self.assertEqual(manifest["items"][0]["state"], "aprovado")

    def test_xml_export_is_parsed(self):
        module = load("inspect_lattes_xml.py")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "curriculo.xml"
            root = Element("CURRICULO-VITAE")
            general = Element("DADOS-GERAIS", {"NOME-COMPLETO": "Cleyber Silva"})
            root.append(general)
            production = Element("ARTIGO-PUBLICADO", {"DOI": "10.0000/test"})
            root.append(production)
            ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
            result = module.inspect(path)
            self.assertEqual(result["identity"]["NOME-COMPLETO"], "Cleyber Silva")
            self.assertEqual(len(result["productions"]), 1)

    def test_deduplication_uses_doi_and_title(self):
        module = load("deduplicate.py")
        self.assertTrue(module.duplicate(
            {"doi": "10.1000/test", "title": "Outro"},
            {"doi": "10.1000/test", "title": "Diferente"},
        ))
        self.assertTrue(module.duplicate(
            {"title": "Minha produção acadêmica"},
            {"title": "Minha produção acadêmica"},
        ))

    def test_evidence_evaluator_blocks_missing_field(self):
        module = load("evidence_evaluator.py")
        result = module.evaluate(
            {"fields": {"title": "Artigo", "doi": "10.1000/x"}},
            [{"title": "Artigo", "doi": "outro"}],
        )
        self.assertEqual(result["status"], "bloqueado")
        self.assertIn("doi", [item["field"] for item in result["missing"]])

    def test_saved_record_verification(self):
        module = load("verify_saved_record.py")
        self.assertTrue(module.verify({"title": "Artigo"}, {"title": "Artigo"})["verified"])
        self.assertFalse(module.verify({"title": "Artigo"}, {"title": "Outro"})["verified"])

    def test_batch_is_sequential_and_verifies_observed_records(self):
        module = load("run_batch.py")
        manifest = {
            "schema": "lattes-batch-v1",
            "created_at": "2026-11-19T00:00:00Z",
            "items": [
                {"key": "1", "authorized": True, "proposal": {"title": "A"}},
                {"key": "2", "authorized": True, "proposal": {"title": "B"}},
            ],
        }
        report = module.run_batch(manifest, [{"title": "A"}, {"title": "Outra"}])
        self.assertEqual(report["summary"]["total"], 2)
        self.assertEqual(report["summary"]["verificados"], 1)
        self.assertEqual(report["summary"]["pendentes"], 1)

    def test_e2e_fixture_has_save_reopen_timeout_and_captcha(self):
        html = (ROOT / "assets" / "lattes-e2e.html").read_text(encoding="utf-8")
        for text in ("ReCAPTCHA", "SALVO:", "REABRIR", "TIMEOUT:", "Registro existente"):
            self.assertIn(text, html) if text != "REABRIR" else self.assertIn("Reabrir", html)


if __name__ == "__main__":
    unittest.main()
