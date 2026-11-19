"""Detecta possíveis duplicatas entre propostas e registros do currículo."""
import argparse
import json
import re
import unicodedata
from pathlib import Path


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", str(value))
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return re.sub(r"\W+", " ", value.lower()).strip()


def duplicate(candidate: dict, existing: dict) -> bool:
    doi_a = normalize(candidate.get("doi", ""))
    doi_b = normalize(existing.get("doi", ""))
    if doi_a and doi_b:
        return doi_a == doi_b
    title_a = normalize(candidate.get("title", candidate.get("titulo", "")))
    title_b = normalize(existing.get("title", existing.get("titulo", "")))
    if title_a and title_b:
        return title_a == title_b
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("proposal", type=Path)
    parser.add_argument("existing", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    proposal = json.loads(args.proposal.read_text(encoding="utf-8"))
    existing = json.loads(args.existing.read_text(encoding="utf-8"))
    candidates = proposal if isinstance(proposal, list) else [proposal]
    records = existing if isinstance(existing, list) else [existing]
    matches = []
    for index, candidate in enumerate(candidates):
        found = [record for record in records if duplicate(candidate, record)]
        matches.append({"index": index, "duplicates": found, "action": "evitar_recadastro" if found else "preparar"})
    if args.output.exists():
        parser.error("Escolha um arquivo de saída novo.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(matches, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(matches, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
