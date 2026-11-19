"""Extrai dados estruturados de uma exportação XML ou ZIP do Currículo Lattes."""
import argparse
import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


def xml_bytes(path: Path) -> bytes:
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            candidates = [
                name for name in archive.namelist()
                if name.lower().endswith(".xml")
            ]
            if not candidates:
                raise ValueError("O ZIP não contém arquivo XML.")
            return archive.read(candidates[0])
    return path.read_bytes()


def inspect(path: Path) -> dict:
    root = ET.fromstring(xml_bytes(path))
    identity = root.find(".//DADOS-GERAIS")
    identity_data = {} if identity is None else dict(identity.attrib)

    productions = []
    for element in root.iter():
        tag = element.tag.split("}")[-1]
        if tag not in {
            "ARTIGO-PUBLICADO",
            "LIVRO-PUBLICADO",
            "CAPITULO-DE-LIVRO-PUBLICADO",
            "TRABALHO-EM-EVENTOS",
            "PATENTE",
        }:
            continue
        record = dict(element.attrib)
        for child in element.iter():
            if child is element:
                continue
            child_tag = child.tag.split("}")[-1]
            if child.attrib:
                record.setdefault(child_tag, []).append(dict(child.attrib))
        productions.append({"category": tag, "data": record})

    return {
        "identity": identity_data,
        "productions": productions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xml", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Escolha um arquivo de saída novo.")
    result = inspect(args.xml)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"productions": len(result["productions"]), "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
