"""Atualiza uma copia da planilha sem modificar o arquivo original."""
import argparse
import json
import shutil
import sys
from pathlib import Path

try:
    from openpyxl import load_workbook
except ImportError:
    print("Instale openpyxl: python -m pip install openpyxl", file=sys.stderr)
    raise


def reconcile(source: Path, output: Path, changes: list[dict]) -> dict:
    source = source.resolve()
    output = output.resolve()
    if not source.is_file():
        raise ValueError("Arquivo XLSX de origem não encontrado.")
    if output == source:
        raise ValueError("A origem não pode ser sobrescrita.")
    if output.exists():
        raise ValueError("Escolha um arquivo de saída novo.")

    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, output)
    workbook = load_workbook(output)
    applied = []

    for change in changes:
        sheet_name = change["sheet"]
        cell_name = change["cell"].upper()
        value = change["value"]
        if sheet_name not in workbook.sheetnames:
            raise ValueError(f"Aba inexistente: {sheet_name}")
        sheet = workbook[sheet_name]
        if not cell_name or not isinstance(cell_name, str):
            raise ValueError("Cada alteração exige uma célula válida.")
        before = sheet[cell_name].value
        sheet[cell_name] = value
        applied.append({
            "sheet": sheet_name,
            "cell": cell_name,
            "before": before,
            "after": value,
        })

    workbook.save(output)
    workbook.close()
    return {"source": str(source), "output": str(output), "applied": applied}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xlsx", type=Path)
    parser.add_argument("--changes", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with args.changes.open("r", encoding="utf-8") as source:
        changes = json.load(source)
    if not isinstance(changes, list):
        raise ValueError("O JSON de alterações deve ser uma lista.")
    report = reconcile(args.xlsx, args.output, changes)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
