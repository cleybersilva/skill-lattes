import importlib.util
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile
import json
import importlib.util

SCRIPT = Path(__file__).resolve().parents[1] / 'lattes-atualizar/scripts/inspect_xlsx.py'
spec = importlib.util.spec_from_file_location('reader', SCRIPT)
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)

WRITER = Path(__file__).resolve().parents[1] / 'lattes-atualizar/scripts/reconcile_xlsx.py'
writer_spec = importlib.util.spec_from_file_location('writer', WRITER)
writer = importlib.util.module_from_spec(writer_spec)
writer_spec.loader.exec_module(writer)

MANIFEST = Path(__file__).resolve().parents[1] / 'lattes-atualizar/scripts/create_batch_manifest.py'


class ReaderTests(unittest.TestCase):
    def test_reconcile_creates_copy_without_changing_source(self):
        try:
            from openpyxl import Workbook, load_workbook
        except ImportError:
            self.skipTest('openpyxl não está instalado')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'input.xlsx'
            output = root / 'reconciliado.xlsx'
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = 'Página1'
            sheet['J2'] = False
            workbook.save(source)
            before = source.read_bytes()

            report = writer.reconcile(source, output, [
                {'sheet': 'Página1', 'cell': 'J2', 'value': True},
            ])

            self.assertEqual(source.read_bytes(), before)
            self.assertTrue(output.is_file())
            self.assertTrue(load_workbook(output)['Página1']['J2'].value)
            self.assertEqual(report['applied'][0]['before'], False)

    def test_reconcile_rejects_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'input.xlsx'
            output = root / 'existing.xlsx'
            source.write_bytes(b'fixture')
            output.write_bytes(b'existing')
            with self.assertRaisesRegex(ValueError, 'novo'):
                writer.reconcile(source, output, [])

    def test_sparse_booleans_strings_formula_and_hyperlink(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.xlsx'
            ns = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
            with ZipFile(path, 'w') as z:
                z.writestr('xl/workbook.xml', f'<workbook xmlns="{ns}" xmlns:r="{reader.REL}"><sheets><sheet name="Página1" r:id="r1"/></sheets></workbook>')
                z.writestr('xl/_rels/workbook.xml.rels', '<Relationships><Relationship Id="r1" Target="worksheets/sheet1.xml"/></Relationships>')
                z.writestr('xl/sharedStrings.xml', f'<sst xmlns="{ns}"><si><t>Atualizado</t></si></sst>')
                z.writestr('xl/worksheets/sheet1.xml', f'<worksheet xmlns="{ns}" xmlns:r="{reader.REL}"><sheetData><row r="1"><c r="J1" t="s"><v>0</v></c></row><row r="2"><c r="I2" t="b"><v>0</v></c><c r="J2" t="b"><v>1</v></c><c r="K2"><f>1+1</f><v>2</v></c></row><row r="3"><c r="A3"/></row><row r="4"><c r="F4" t="inlineStr"><is><t>ação</t></is></c></row></sheetData><hyperlinks><hyperlink ref="F4" r:id="h1"/></hyperlinks></worksheet>')
                z.writestr('xl/worksheets/_rels/sheet1.xml.rels', '<Relationships><Relationship Id="h1" Target="https://example.org/proof"/></Relationships>')
            before = path.read_bytes()
            data = reader.inspect(path)['sheets'][0]
            self.assertEqual([r['row'] for r in data['rows']], [1, 2, 4])
            self.assertEqual(data['rows'][0]['cells']['J1']['value'], 'Atualizado')
            self.assertIs(data['rows'][1]['cells']['I2']['value'], False)
            self.assertIs(data['rows'][1]['cells']['J2']['value'], True)
            self.assertEqual(data['rows'][1]['cells']['K2']['formula'], '1+1')
            self.assertEqual(data['rows'][2]['cells']['F4']['value'], 'ação')
            self.assertEqual(data['hyperlinks'][0]['target'], 'https://example.org/proof')
            self.assertEqual(before, path.read_bytes())


if __name__ == '__main__':
    unittest.main()
