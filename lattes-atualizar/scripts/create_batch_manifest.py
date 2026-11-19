"""Cria um manifesto JSON para um lote explicitamente aprovado."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


VALID_STATES = {
    "inventariado",
    "conciliado",
    "comprovado",
    "proposto",
    "aprovado",
    "preenchido",
    "salvo",
    "verificado",
    "publicado",
    "reconciliado",
    "pendente",
    "bloqueado",
    "timeout",
    "sessao_expirada",
    "falha_de_reconciliacao",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("items", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    with args.items.open("r", encoding="utf-8") as source:
        items = json.load(source)
    if not isinstance(items, list):
        raise ValueError("O arquivo de itens deve conter uma lista.")
    if not items:
        raise ValueError("O lote aprovado não pode estar vazio.")

    approved = []
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Cada item deve ser um objeto.")
        required = {"key", "sheet", "row", "proposal"}
        missing = sorted(required.difference(item))
        if missing:
            raise ValueError(f"Campos obrigatórios ausentes: {', '.join(missing)}")
        approved.append({
            "key": item["key"],
            "sheet": item["sheet"],
            "row": item["row"],
            "proposal": item["proposal"],
            "state": "aprovado",
            "authorized": True,
        })

    manifest = {
        "schema": "lattes-batch-v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "items": approved,
    }
    if args.output.exists():
        raise ValueError("Escolha um arquivo de manifesto novo.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as output:
        json.dump(manifest, output, ensure_ascii=False, indent=2)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
