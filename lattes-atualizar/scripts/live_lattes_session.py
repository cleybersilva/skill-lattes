"""Abre uma sessão real do Lattes e aguarda intervenção humana."""
import argparse
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="https://lattes.cnpq.br/")
    parser.add_argument("--profile", type=str, default=None)
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Instale: python -m pip install playwright && python -m playwright install chromium", file=sys.stderr)
        return 2

    with sync_playwright() as playwright:
        if args.profile:
            context = playwright.chromium.launch_persistent_context(
                args.profile, headless=False
            )
        else:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(args.url, wait_until="domcontentloaded")
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
