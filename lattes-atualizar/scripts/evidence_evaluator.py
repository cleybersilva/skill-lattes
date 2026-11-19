"""Avalia uma proposta contra evidências locais sem acessar o Lattes."""
import argparse
import json
from pathlib import Path


def evaluate(proposal: dict, evidence: list[dict]) -> dict:
    fields = proposal.get("fields", {})
    proven = []
    missing = []
    for field, value in fields.items():
        matches = [
            item for item in evidence
            if str(item.get(field, "")).strip().lower() == str(value).strip().lower()
        ]
        if matches:
            proven.append({"field": field, "value": value, "evidence": matches})
        else:
            missing.append({"field": field, "value": value})
    status = "comprovado" if fields and not missing else ("bloqueado" if fields else "pendente")
    return {
        "status": status,
        "fields": proven,
        "missing": missing,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("proposal", type=Path)
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    proposal = json.loads(args.proposal.read_text(encoding="utf-8"))
    evidence = json.loads(args.evidence.read_text(encoding="utf-8"))
    if not isinstance(evidence, list):
        raise ValueError("A evidência deve ser uma lista.")
    result = evaluate(proposal, evidence)
    if args.output.exists():
        parser.error("Escolha um arquivo de saída novo.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
