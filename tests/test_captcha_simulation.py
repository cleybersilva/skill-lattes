import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "lattes-atualizar" / "scripts" / "simulate_captcha.py"
DEMO = ROOT / "assets" / "captcha-demo.html"
GIF = ROOT / "assets" / "captcha-demo.gif"


class CaptchaSimulationTests(unittest.TestCase):
    def test_readme_animation_asset_exists_and_is_animated(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("assets/captcha-demo.gif", readme)
        self.assertTrue(GIF.is_file())
        self.assertGreater(GIF.stat().st_size, 1000)

    def test_interactive_demo_has_takeover_and_reset_controls(self):
        html = DEMO.read_text(encoding="utf-8")
        self.assertIn("Executar simulação", html)
        self.assertIn("Confirmar resolução", html)
        self.assertIn("Reiniciar", html)
        self.assertIn("takeover", html)
        self.assertIn("Retomando lote autorizado", html)

    def test_simulation_never_opens_browser_or_sends_data(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            check=True,
            capture_output=True,
            text=True,
        )
        events = [json.loads(line) for line in result.stdout.splitlines()
                  if line.startswith("{") and '"estado"' in line]
        self.assertEqual(
            [event["estado"] for event in events],
            [
                "preparando",
                "navegando",
                "desafio_detectado",
                "takeover_humano",
                "confirmado",
                "continuando",
            ],
        )
        self.assertTrue(all(not event["navegador_aberto"] for event in events))
        self.assertTrue(all(not event["dados_reais_enviados"] for event in events))


if __name__ == "__main__":
    unittest.main()
