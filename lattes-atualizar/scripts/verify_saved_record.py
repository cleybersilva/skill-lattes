"""Verifica campos observados após salvar contra o manifesto aprovado."""
import argparse
import json
from pathlib import Path


def verify(expected: dict, observed: dict) -> dict:
    mismatches = []
    for field, value in expected.items():
        actual = observed.get(field)
        if actual != value:
            mismatches.append({"field": field, "expected": value, "observed": actual})
    return {
        "verified": not mismatches,
        "mismatches": mismatches,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("expected", type=Path)
    parser.add_argument("observed", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    expected = json.loads(args.expected.read_text(encoding="utf-8"))
    observed = json.loads(args.observed.read_text(encoding="utf-8"))
    result = verify(expected, observed)
    if args.output.exists():
        parser.error("Escolha um arquivo de saída novo.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
