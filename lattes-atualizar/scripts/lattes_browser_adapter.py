"""Adapter Playwright para preencher e verificar lotes aprovados no Lattes."""
import argparse
import json
import sys
from pathlib import Path


class HumanChallenge(RuntimeError):
    pass


def build_plan(manifest: dict) -> list[dict]:
    if manifest.get("schema") != "lattes-batch-v1":
        raise ValueError("Manifesto incompatível.")
    return [
        {
            "key": item["key"],
            "sheet": item["sheet"],
            "row": item["row"],
            "fields": item["proposal"],
            "state": "aprovado" if item.get("authorized") is True else "bloqueado",
        }
        for item in manifest["items"]
    ]


def discover_selectors(page) -> dict:
    """Descobre campos por label, name, id e aria-label sem selectors fixos."""
    selectors = {}
    elements = page.locator("input, textarea, select").all()
    for element in elements:
        element_id = element.get_attribute("id") or ""
        name = element.get_attribute("name") or ""
        aria = element.get_attribute("aria-label") or ""
        label_text = ""
        if element_id:
            label = page.locator(f'label[for="{element_id}"]')
            if label.count():
                label_text = label.first.inner_text(timeout=2_000)
        text = " ".join(part for part in (label_text, aria, name, element_id) if part).lower()
        for key in ("title", "titulo", "doi", "year", "ano", "natureza", "authors", "autores"):
            if key in text and key not in selectors:
                selector = f"#{element_id}" if element_id else (
                    f'[name="{name}"]' if name else f'[aria-label="{aria}"]'
                )
                if selector:
                    selectors[key] = selector
    for selector_name in ("save", "reopen"):
        candidates = page.get_by_role("button", name="Salvar" if selector_name == "save" else "Reabrir")
        if candidates.count():
            selectors[selector_name] = candidates.first
    return selectors


def has_human_challenge(page) -> bool:
    try:
        body = page.locator("body").inner_text(timeout=2_000).lower()
    except Exception:
        body = ""
    return (
        page.locator("iframe[src*='recaptcha'], iframe[title*='reCAPTCHA']").count() > 0
        or "código de segurança" in body
        or "currículo não encontrado" in body
    )


def execute_plan(page, plan: list[dict], selectors: dict) -> list[dict]:
    results = []
    for item in plan:
        if item["state"] != "aprovado":
            results.append({**item, "state": "bloqueado", "reason": "sem autorizacao"})
            continue
        if has_human_challenge(page):
            raise HumanChallenge(
                f"PAUSA HUMANA: resolução de CAPTCHA/MFA necessária antes de {item['key']}."
            )

        observed = {}
        mismatches = []
        for field, value in item["fields"].items():
            key = str(field).lower()
            selector = selectors.get(key)
            if not selector:
                continue
            if hasattr(selector, "fill"):
                selector.fill(str(value))
            else:
                page.locator(selector).fill(str(value))
            observed[field] = value

        save_selector = selectors.get("save")
        if save_selector:
            if hasattr(save_selector, "click"):
                save_selector.click()
            else:
                page.locator(save_selector).click()

        reopen_selector = selectors.get("reopen")
        if reopen_selector:
            if hasattr(reopen_selector, "click"):
                reopen_selector.click()
            else:
                page.locator(reopen_selector).click()
        else:
            page.reload(wait_until="domcontentloaded")

        for field, value in item["fields"].items():
            key = str(field).lower()
            selector = selectors.get(key)
            actual = None
            if selector:
                try:
                    actual = selector.input_value() if hasattr(selector, "input_value") else page.locator(selector).input_value()
                except Exception:
                    actual = None
            if actual is not None and str(actual).strip() != str(value).strip():
                mismatches.append({"field": field, "expected": value, "observed": actual})

        results.append({
            **item,
            "state": "verificado" if not mismatches else "pendente",
            "observed": observed,
            "mismatches": mismatches,
        })
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--url", type=str)
    parser.add_argument("--selectors", type=Path)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm-human", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    plan = build_plan(manifest)
    if not args.execute:
        report = {"mode": "dry-run", "plan": plan}
    else:
        if not args.confirm-human:
            parser.error("Execução real exige --confirm-human.")
        if not args.url:
            parser.error("Execução real exige --url.")
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            print("Instale Playwright: python -m pip install playwright", file=sys.stderr)
            return 2
        selectors = json.loads(args.selectors.read_text(encoding="utf-8")) if args.selectors else {}
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto(args.url, wait_until="domcontentloaded")
            if not selectors:
                selectors = discover_selectors(page)
            try:
                results = execute_plan(page, plan, selectors)
            except HumanChallenge as error:
                report = {"mode": "paused", "plan": plan, "error": str(error)}
            else:
                report = {"mode": "executed", "results": results}
            context.close()

    if args.output.exists():
        parser.error("Escolha um arquivo de saída novo.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
