"""Gera uma planilha XLSX vazia seguindo o contrato da skill-lattes."""
import argparse
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation


HEADERS = [
    "Ano", "Tipo", "Subtipo", "SubSubtipo", "Local", "Aluno", "Obs",
    "Link", "Solicitado", "Atualizado", "Qualis",
] + [f"Coluna {index}" for index in range(4, 25)]


def generate(output: Path) -> None:
    if output.exists():
        raise ValueError("Escolha um arquivo de saída novo.")

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Página1"

    header_fill = PatternFill("solid", fgColor="1F4E78")
    header_font = Font(color="FFFFFF", bold=True)
    thin = Side(style="thin", color="C7D1DE")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    for column, header in enumerate(HEADERS, start=1):
        cell = sheet.cell(row=1, column=column, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border

    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = f"A1:{sheet.cell(row=1, column=len(HEADERS)).coordinate}"
    sheet.row_dimensions[1].height = 32
    for row in range(2, 502):
        sheet.row_dimensions[row].height = 22
        for column in range(1, len(HEADERS) + 1):
            sheet.cell(row=row, column=column).border = border
            sheet.cell(row=row, column=column).alignment = Alignment(
                vertical="top",
                wrap_text=column in (6, 7, 8),
            )

    width_by_header = {
        "Ano": 10,
        "Tipo": 18,
        "Subtipo": 18,
        "SubSubtipo": 18,
        "Local": 24,
        "Aluno": 34,
        "Obs": 45,
        "Link": 42,
        "Solicitado": 14,
        "Atualizado": 14,
        "Qualis": 12,
    }
    for column, header in enumerate(HEADERS, start=1):
        sheet.column_dimensions[chr(64 + column) if column <= 26 else sheet.cell(row=1, column=column).column_letter].width = width_by_header.get(header, 18)

    boolean_validation = DataValidation(
        type="list",
        formula1='"Sim,Não"',
        allow_blank=True,
    )
    sheet.add_data_validation(boolean_validation)
    boolean_validation.add("I2:I501")
    boolean_validation.add("J2:J501")

    instructions = workbook.create_sheet("Instruções")
    instructions.append(["Campo", "Como preencher"])
    instruction_rows = [
        ("Ano", "Ano principal da atividade."),
        ("Tipo/Subtipo/SubSubtipo", "Preserve a classificação original e não invente campos."),
        ("Local", "Instituição, evento, periódico ou plataforma."),
        ("Aluno", "Nome do aluno, pessoa ou texto realmente associado à atividade."),
        ("Obs", "Título, observação ou contexto adicional."),
        ("Link", "Um ou mais comprovantes, separados por quebra de linha."),
        ("Solicitado", "Controle de solicitação: use Sim/Não ou deixe vazio."),
        ("Atualizado", "Só use após reabrir e verificar o registro no Lattes."),
        ("Qualis", "Use somente com área, período e classificação comprovados."),
    ]
    for row in instruction_rows:
        instructions.append(row)
    instructions.column_dimensions["A"].width = 24
    instructions.column_dimensions["B"].width = 78
    instructions.freeze_panes = "A2"
    for cell in instructions[1]:
        cell.fill = header_fill
        cell.font = header_font
    for row in instructions.iter_rows(min_row=1, max_row=instructions.max_row):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = border

    workbook.save(output)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("examples/Planilha-Padrao-Zerada-Lattes.xlsx"))
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    generate(args.output)
    print(f"Modelo criado em {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
