"""Abre ou acompanha uma sessão real do Lattes com interação humana."""
import argparse
import sys
import time
from pathlib import Path


def find_browser_executable(browser: str = "auto") -> str | None:
    candidates = {
        "chrome": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            str(Path.home() / "AppData/Local/Google/Chrome/Application/chrome.exe"),
        ],
        "edge": [
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            str(Path.home() / "AppData/Local/Microsoft/Edge/Application/msedge.exe"),
        ],
        "firefox": [
            str(Path.home() / "AppData/Local/Programs/Firefox/firefox.exe"),
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
        ],
    }
    order = candidates[browser] if browser in candidates else (
        candidates["chrome"] + candidates["edge"] + candidates["firefox"]
    )
    return next((candidate for candidate in order if Path(candidate).is_file()), None)


def monitor_page(page) -> None:
    captcha_was_reported = False
    security_was_reported = False
    try:
        while True:
            try:
                body = page.locator("body").inner_text(timeout=2_000).lower()
                security_page = (
                    "código de segurança" in body
                    or "currículo não encontrado" in body
                )
                if security_page and not security_was_reported:
                    print("VALIDAÇÃO EXTERNA: resolva o desafio na aba aberta.")
                    security_was_reported = True
                elif not security_page and security_was_reported:
                    print("DESAFIO CONCLUÍDO: confira o currículo correto.")
                    security_was_reported = False

                has_captcha = page.locator(
                    "iframe[src*='recaptcha'], iframe[title*='reCAPTCHA']"
                ).count()
                if has_captcha and not captcha_was_reported:
                    print("DESAFIO DETECTADO: resolva manualmente.")
                    captcha_was_reported = True
                elif not has_captcha and captcha_was_reported:
                    captcha_was_reported = False
                page.wait_for_timeout(5_000)
            except Exception:
                break
            if page.is_closed():
                break
    except KeyboardInterrupt:
        pass


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="https://lattes.cnpq.br/")
    parser.add_argument("--profile", type=str, default=str(Path(".work/browser-lattes-profile").resolve()))
    parser.add_argument("--screenshot", type=Path, default=Path(".work/live-lattes.png"))
    parser.add_argument("--debug-port", type=int, default=9222)
    parser.add_argument("--use-open-browser", action="store_true")
    parser.add_argument("--browser", choices=["auto", "chrome", "edge", "firefox"], default="auto")
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Instale: python -m pip install playwright", file=sys.stderr)
        return 2

    with sync_playwright() as playwright:
        executable = find_browser_executable(args.browser)
        browser_name = args.browser
        if browser_name == "auto":
            if executable and "edge" in executable.lower():
                browser_name = "edge"
            elif executable and "firefox" in executable.lower():
                browser_name = "firefox"
            elif executable:
                browser_name = "chrome"
            else:
                browser_name = "chromium"

        if browser_name == "firefox":
            browser = playwright.firefox.launch(
                headless=False,
                executable_path=executable,
            )
            context = browser.new_context(locale="pt-BR", viewport={"width": 1440, "height": 900})
            page = context.pages[0] if context.pages else context.new_page()
            page.goto(args.url, wait_until="domcontentloaded", timeout=45_000)
        elif args.use_open_browser:
            try:
                browser = playwright.chromium.connect_over_cdp(
                    f"http://127.0.0.1:{args.debug_port}"
                )
            except Exception as error:
                print("O navegador aberto não está em modo de depuração.", file=sys.stderr)
                print("Reinicie Chrome ou Edge com --remote-debugging-port=9222.", file=sys.stderr)
                print(str(error), file=sys.stderr)
                return 2
            context = browser.contexts[0]
            candidates = [
                page for page in context.pages
                if "lattes.cnpq.br" in page.url or "buscatextual.cnpq.br" in page.url
            ]
            page = candidates[-1] if candidates else (
                context.pages[-1] if context.pages else context.new_page()
            )
        else:
            launch_options = {
                "headless": False,
                "locale": "pt-BR",
                "viewport": {"width": 1440, "height": 900},
                "device_scale_factor": 1,
                "args": [
                    "--disable-dev-shm-usage",
                    "--disable-backgrounding-occluded-windows",
                    "--disable-renderer-backgrounding",
                    "--window-size=1440,900",
                    f"--remote-debugging-port={args.debug_port}",
                ],
            }
            if executable:
                launch_options["executable_path"] = executable
            Path(args.profile).mkdir(parents=True, exist_ok=True)
            context = playwright.chromium.launch_persistent_context(
                args.profile, **launch_options
            )
            page = context.pages[0] if context.pages else context.new_page()
            for attempt in range(1, 4):
                try:
                    response = page.goto(args.url, wait_until="domcontentloaded", timeout=45_000)
                    page.wait_for_timeout(1_500)
                    if response and response.status >= 500:
                        raise RuntimeError(f"HTTP {response.status}")
                    break
                except Exception as error:
                    print(f"Tentativa {attempt}/3 falhou: {error}")
                    if attempt == 3:
                        print("Não foi possível renderizar a página.")
                        return 1
                    time.sleep(2)

        args.screenshot.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(args.screenshot), full_page=True)
        print(f"Navegador: {browser_name}")
        print(f"URL ativa: {page.url}")
        print(f"Diagnóstico visual: {args.screenshot}")
        print("PAUSA HUMANA: resolva login, CAPTCHA e MFA na janela aberta.")
        print("Não compartilhe senha ou código no chat.")
        monitor_page(page)
        if browser_name != "firefox" and not args.use_open_browser:
            context.close()
        elif browser_name == "firefox":
            context.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
