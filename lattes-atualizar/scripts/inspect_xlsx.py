"""Extrai células XLSX em JSON sem dependências e sem modificar a origem."""
import argparse
import hashlib
import json
import posixpath
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile

NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
REL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'


def text_content(element):
    return ''.join(t.text or '' for t in element.findall('.//s:t', NS))


def inspect(path):
    path = Path(path)
    result = {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'sheets': []}
    with ZipFile(path) as book:
        strings = []
        if 'xl/sharedStrings.xml' in book.namelist():
            strings = [text_content(s) for s in ET.fromstring(book.read('xl/sharedStrings.xml'))]
        rels = {r.attrib['Id']: r.attrib['Target'] for r in ET.fromstring(book.read('xl/_rels/workbook.xml.rels'))}
        workbook = ET.fromstring(book.read('xl/workbook.xml'))
        for sheet in workbook.findall('s:sheets/s:sheet', NS):
            target = rels[sheet.attrib[f'{{{REL}}}id']]
            target = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/' + target)
            root = ET.fromstring(book.read(target))
            rows = []
            for row in root.findall('s:sheetData/s:row', NS):
                cells = {}
                for cell in row.findall('s:c', NS):
                    kind = cell.get('t')
                    value = cell.findtext('s:v', default=None, namespaces=NS)
                    if kind == 'inlineStr':
                        value = text_content(cell)
                    elif kind == 's' and value is not None:
                        value = strings[int(value)]
                    elif kind == 'b' and value is not None:
                        value = value == '1'
                    elif kind not in ('str', 'e') and value is not None:
                        value = float(value)
                        if value.is_integer():
                            value = int(value)
                    formula = cell.findtext('s:f', default=None, namespaces=NS)
                    if value is not None or formula is not None:
                        cells[cell.attrib['r']] = {'value': value, **({'formula': formula} if formula is not None else {})}
                if cells:
                    rows.append({'row': int(row.attrib['r']), 'cells': cells})
            links = []
            relpath = posixpath.join(posixpath.dirname(target), '_rels', posixpath.basename(target) + '.rels')
            sheetrels = {}
            if relpath in book.namelist():
                sheetrels = {r.attrib['Id']: r.attrib['Target'] for r in ET.fromstring(book.read(relpath))}
            for link in root.findall('s:hyperlinks/s:hyperlink', NS):
                links.append({'cell': link.get('ref'), 'target': sheetrels.get(link.get(f'{{{REL}}}id'), link.get('location'))})
            result['sheets'].append({'name': sheet.get('name'), 'rows': rows, 'hyperlinks': links})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('xlsx', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.resolve() == args.xlsx.resolve() or args.output.exists():
        parser.error('A saída deve ser um arquivo novo, diferente da origem.')
    result = inspect(args.xlsx)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as output:
        json.dump(result, output, ensure_ascii=False, indent=2)
    print(f'{len(result["sheets"])} aba(s) extraída(s). Origem preservada.')


if __name__ == '__main__':
    main()
