import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "lattes-atualizar" / "scripts" / "simulate_captcha.py"


class CaptchaSimulationTests(unittest.TestCase):
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
