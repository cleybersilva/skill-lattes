"""Orquestra execução, verificação e reconciliação de um lote aprovado."""
import argparse
import json
import sys
from pathlib import Path

try:
    from openpyxl import load_workbook
except ImportError:
    load_workbook = None


def reconcile_verified(source: Path, output: Path, verified_items: list[dict]) -> dict:
    if load_workbook is None:
        raise RuntimeError("Instale openpyxl.")
    source = source.resolve()
    output = output.resolve()
    if output.exists() or output == source:
        raise ValueError("Escolha uma cópia XLSX nova.")

    import shutil
    shutil.copy2(source, output)
    workbook = load_workbook(output)
    changes = []
    for item in verified_items:
        if item.get("state") != "verificado":
            continue
        for change in item.get("xlsx_changes", []):
            sheet = workbook[change["sheet"]]
            before = sheet[change["cell"]].value
            sheet[change["cell"]] = change["value"]
            changes.append({
                "sheet": change["sheet"],
                "cell": change["cell"],
                "before": before,
                "after": change["value"],
                "key": item["key"],
            })
    workbook.save(output)
    workbook.close()
    return {"output": str(output), "changes": changes}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("execution_report", type=Path)
    parser.add_argument("--xlsx", type=Path)
    parser.add_argument("--xlsx-output", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = json.loads(args.execution_report.read_text(encoding="utf-8"))
    verified = report.get("results", [])
    reconciliation = None
    if args.xlsx:
        if not args.xlsx_output:
            parser.error("--xlsx-output é obrigatório com --xlsx.")
        reconciliation = reconcile_verified(args.xlsx, args.xlsx_output, verified)
    final = {
        "schema": "lattes-batch-report-v1",
        "execution": report,
        "reconciliation": reconciliation,
    }
    if args.output.exists():
        parser.error("Escolha um arquivo de relatório novo.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(final, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(final, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
