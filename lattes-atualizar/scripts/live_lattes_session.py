"""Abre uma sessão real do Lattes e aguarda intervenção humana."""
import argparse
import sys
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="https://lattes.cnpq.br/")
    parser.add_argument(
        "--profile",
        type=str,
        default=str(Path(".work/chrome-lattes-profile").resolve()),
        help="Perfil persistente para manter sessão, login e CAPTCHA resolvido",
    )
    parser.add_argument("--screenshot", type=Path, default=Path(".work/live-lattes.png"))
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Instale: python -m pip install playwright && python -m playwright install chromium", file=sys.stderr)
        return 2

    with sync_playwright() as playwright:
        chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        launch_options = {
            "headless": False,
            "executable_path": chrome,
            "locale": "pt-BR",
            "viewport": {"width": 1440, "height": 900},
            "device_scale_factor": 1,
            "args": [
                "--disable-dev-shm-usage",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding",
                "--window-size=1440,900",
            ],
        }
        Path(args.profile).mkdir(parents=True, exist_ok=True)
        context = playwright.chromium.launch_persistent_context(
            args.profile, **launch_options
        )
        page = context.pages[0] if context.pages else context.new_page()
        response = None
        for attempt in range(1, 4):
            try:
                response = page.goto(
                    args.url,
                    wait_until="domcontentloaded",
                    timeout=45_000,
                )
                page.wait_for_timeout(1_500)
                if response and response.status >= 500:
                    raise RuntimeError(f"HTTP {response.status}")
                break
            except Exception as error:
                print(f"Tentativa {attempt}/3 falhou: {error}")
                if attempt == 3:
                    print("Não foi possível renderizar a página. Verifique o navegador e sua conexão.")
                    return 1
                time.sleep(2)

        args.screenshot.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(args.screenshot), full_page=True)
        print(f"URL ativa: {page.url}")
        print(f"Diagnóstico visual: {args.screenshot}")
        print("PAUSA HUMANA: faça login, CAPTCHA e MFA na janela.")
        print("Não compartilhe senha ou código no chat.")
        print("A janela ficará aberta até você fechá-la.")
        print("Feche o navegador quando terminar. Não envie senha ou código no chat.")
        captcha_was_reported = False
        try:
            while True:
                try:
                    if page.locator("iframe[src*='recaptcha'], iframe[title*='reCAPTCHA']").count():
                        if not captcha_was_reported:
                            print("DESAFIO DETECTADO: resolva a grade manualmente e clique em Verificar.")
                            captcha_was_reported = True
                    elif captcha_was_reported:
                        print("DESAFIO CONCLUÍDO OU NAVEGOU: confira a próxima página antes de continuar.")
                        captcha_was_reported = False
                    page.wait_for_timeout(5_000)
                except Exception:
                    break
                if page.is_closed():
                    break
        except KeyboardInterrupt:
            pass
        finally:
            context.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
