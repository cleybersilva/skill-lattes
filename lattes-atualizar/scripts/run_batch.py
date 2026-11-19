"""Executa um ciclo seguro e sequencial sobre um manifesto aprovado."""
import argparse
import json
from pathlib import Path


def run_batch(manifest: dict, observed: list[dict] | None = None) -> dict:
    if manifest.get("schema") != "lattes-batch-v1":
        raise ValueError("Manifesto incompatível.")
    observed = observed or []
    results = []
    for index, item in enumerate(manifest.get("items", [])):
        if item.get("authorized") is not True:
            results.append({"key": item.get("key"), "state": "bloqueado", "reason": "sem autorizacao"})
            continue
        state = "preenchido"
        if index < len(observed):
            actual = observed[index]
            mismatches = []
            expected = item.get("proposal", {})
            for field, value in expected.items():
                if actual.get(field) != value:
                    mismatches.append(field)
            state = "verificado" if not mismatches else "pendente"
        results.append({
            "key": item.get("key"),
            "state": state,
            "proposal": item.get("proposal"),
        })
    return {
        "batch": manifest.get("created_at"),
        "summary": {
            "total": len(results),
            "verificados": sum(r["state"] == "verificado" for r in results),
            "pendentes": sum(r["state"] in {"pendente", "bloqueado"} for r in results),
        },
        "items": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--observed", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    observed = None
    if args.observed:
        observed = json.loads(args.observed.read_text(encoding="utf-8"))
        if not isinstance(observed, list):
            raise ValueError("observed deve ser uma lista.")
    report = run_batch(manifest, observed)
    if args.output.exists():
        parser.error("Escolha um arquivo de saída novo.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
