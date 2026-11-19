"""Executa as células Python do treinamento em diretório temporário, sem Jupyter."""
import contextlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class NotebookTests(unittest.TestCase):
    def test_sequential_python_execution(self):
        notebook = json.loads((ROOT / 'treinamento-lattes.ipynb').read_text(encoding='utf-8'))
        self.assertEqual((notebook['nbformat'], notebook['nbformat_minor']), (4, 5))
        ids = [cell['id'] for cell in notebook['cells']]
        self.assertEqual(len(ids), len(set(ids)))
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            shutil.copytree(ROOT / 'lattes-atualizar', workspace / 'lattes-atualizar',
                            ignore=shutil.ignore_patterns('__pycache__'))
            namespace = {'__name__': '__main__'}
            code_count = 0
            for cell in notebook['cells']:
                self.assertIn(cell['cell_type'], ('markdown', 'code'))
                self.assertIsInstance(cell['source'], list)
                if cell['cell_type'] != 'code':
                    continue
                self.assertEqual(cell['outputs'], [])
                self.assertIsNone(cell['execution_count'])
                source = ''.join(cell['source'])
                source = source.replace('RAIZ_PROJETO = Path.cwd().resolve()',
                                        f'RAIZ_PROJETO = Path({str(workspace)!r}).resolve()')
                with contextlib.redirect_stdout(io.StringIO()):
                    exec(compile(source, cell['id'], 'exec'), namespace)
                code_count += 1
            self.assertEqual(code_count, 11)
            report = json.loads(namespace['destino'].read_text(encoding='utf-8'))
            self.assertFalse(report['inventario_real'])
            self.assertEqual(len(report['triagem']), 5)
            self.assertEqual(len(report['linhas_parciais']), 1)
            self.assertEqual(report['operacoes_reais_no_lattes'], 0)
            self.assertEqual(report['escritas_em_xlsx'], 0)
            self.assertTrue(report['exercicio_ficticio']['resultado']['simulacao'])


if __name__ == '__main__':
    unittest.main()
