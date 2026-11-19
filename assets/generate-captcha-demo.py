from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "captcha-demo.gif"

W, H = 1200, 650
BG = (8, 11, 18)
SIDE = (17, 22, 32)
BROWSER = (249, 250, 252)
LINE = (55, 65, 82)
BORDER = (211, 217, 228)
TEXT = (25, 31, 42)
MUTED = (118, 128, 145)
WHITE = (255, 255, 255)
ORANGE = (255, 180, 84)
GREEN = (63, 208, 155)
BLUE = (55, 118, 210)
CLAUDE = (221, 162, 111)


def font(size, bold=False):
    name = "segoeuib.ttf" if bold else "segoeui.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size)


F12 = font(12)
F13 = font(13)
F14 = font(14)
F16 = font(16)
F18 = font(18)
F20 = font(20)
F22 = font(22)
F24 = font(24, True)
F30 = font(30, True)


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text(draw, xy, value, fnt=F14, fill=TEXT, anchor=None):
    draw.text(xy, value, font=fnt, fill=fill, anchor=anchor)


def draw_cursor(draw, x, y):
    points = [(x, y), (x + 2, y + 27), (x + 8, y + 20), (x + 13, y + 31),
              (x + 17, y + 29), (x + 12, y + 18), (x + 21, y + 17)]
    draw.polygon(points, fill=(18, 24, 36))
    draw.line(points + [points[0]], fill=WHITE, width=2)


def draw_claude(draw, phase):
    rounded(draw, (28, 28, 338, 622), 18, SIDE, LINE, 2)
    rounded(draw, (46, 48, 320, 86), 12, (26, 33, 47), LINE)
    draw.ellipse((64, 62, 82, 80), fill=CLAUDE)
    text(draw, (94, 67), "Claude Code", F18, WHITE)
    text(draw, (46, 118), "Skill: lattes-atualizar", F14, MUTED)

    command = "Preparar 1 atividade autorizada"
    if phase >= 8:
        command = "Navegar no formulário do Lattes"
    if phase >= 14:
        command = "Aguardar CAPTCHA/MFA"
    if phase >= 18:
        command = "Preencher campos aprovados"
    if phase >= 23:
        command = "Reabrir e verificar registro"

    rounded(draw, (46, 150, 320, 210), 10, (13, 17, 26), LINE)
    text(draw, (58, 166), "> " + command, F14, WHITE)
    text(draw, (58, 188), "lote: 1 · externa: aguardando", F12, MUTED)

    steps = [
        ("Inventariar planilha", phase >= 4),
        ("Conferir evidência", phase >= 7),
        ("Abrir formulário", phase >= 10),
        ("Resolver desafio", phase >= 15 and phase < 19),
        ("Preencher campos", phase >= 19),
        ("Verificar registro", phase >= 23),
    ]
    y = 242
    for label, done in steps:
        color = GREEN if done else MUTED
        mark = "✓" if done else "○"
        text(draw, (58, y), mark, F16, color)
        text(draw, (82, y), label, F14, WHITE if done else MUTED)
        y += 42

    if 14 <= phase < 19:
        rounded(draw, (46, 510, 320, 584), 10, (48, 42, 28), (150, 117, 61), 2)
        text(draw, (58, 528), "PAUSADO", F12, ORANGE)
        text(draw, (58, 552), "Usuário assume CAPTCHA/MFA", F13, WHITE)
    elif phase >= 19:
        rounded(draw, (46, 510, 320, 584), 10, (22, 47, 44), (52, 135, 108), 2)
        text(draw, (58, 528), "CONTROLE RESTABELECIDO", F12, GREEN)
        text(draw, (58, 552), "Somente o lote autorizado", F13, WHITE)


def draw_browser(draw, phase):
    rounded(draw, (360, 28, 1172, 622), 18, (18, 23, 33), LINE, 2)

    for cx, color in ((398, (255, 97, 89)), (424, (255, 194, 75)), (450, (41, 201, 65))):
        draw.ellipse((cx, 48, cx + 16, 64), fill=color)
    rounded(draw, (480, 46, 1140, 82), 18, (10, 13, 20), LINE)
    text(draw, (498, 64), "lattes.cnpq.br/curriculo/editar", F14, MUTED)

    rounded(draw, (380, 94, 1152, 602), 12, BROWSER, (214, 219, 228), 1)
    rounded(draw, (380, 94, 1152, 142), 12, (43, 76, 145))
    text(draw, (404, 118), "Currículo Lattes", F18, WHITE)

    text(draw, (404, 164), "Adicionar produção bibliográfica", F20, TEXT)
    text(draw, (404, 188), "Artigo publicado", F14, MUTED)

    fields = [
        ("Título", "Automação segura de currículos acadêmicos", 228),
        ("Autores", "Cleyber Silva; equipe colaboradora", 296),
        ("Ano", "2026", 364),
        ("DOI", "10.0000/demo.lattes.2026", 432),
        ("Natureza", "Artigo completo publicado", 500),
    ]

    cursor_x, cursor_y = 0, 0
    for index, (label, value, y) in enumerate(fields):
        text(draw, (404, y - 26), label, F13, MUTED)
        rounded(draw, (404, y, 1128, y + 48), 8, WHITE, BORDER, 2)
        visible = ""
        if phase >= 19:
            fill_count = min(len(value), max(0, (phase - 19) * 6 - index * 3))
            visible = value[:fill_count]
        text(draw, (418, y + 24), visible if visible else value if phase >= 23 else "", F16, TEXT)
        if 19 <= phase <= 22 and index == min(phase - 19, len(fields) - 1):
            cursor_x = 418 + min(len(value), max(0, (phase - 19) * 6 - index * 3)) * 8
            cursor_y = y + 24

    if 14 <= phase < 19:
        rounded(draw, (610, 198, 922, 410), 12, WHITE, (190, 197, 208), 2)
        text(draw, (640, 224), "Verificação de segurança", F18, TEXT)
        rounded(draw, (640, 258, 892, 322), 8, (242, 245, 249), BORDER)
        text(draw, (660, 276), "CAPTCHA / MFA", F16, TEXT)
        text(draw, (660, 300), "Aguardando ação do usuário", F13, MUTED)
        rounded(draw, (640, 344, 892, 382), 8, (255, 247, 223), (230, 200, 120), 2)
        text(draw, (660, 363), "Resolver manualmente", F14, TEXT)
        cursor_x, cursor_y = 782, 363

    if phase >= 23:
        rounded(draw, (404, 558, 1128, 590), 8, (229, 247, 239), (120, 205, 171), 1)
        text(draw, (418, 574), "✓ Campos conferidos · registro pronto para revisão", F14, (31, 121, 88))

    return cursor_x, cursor_y


def make_frame(phase):
    im = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(im)
    draw_claude(draw, phase)
    cursor_x, cursor_y = draw_browser(draw, phase)

    if 18 <= phase <= 22:
        draw_cursor(draw, cursor_x, cursor_y)
    elif 14 <= phase < 19:
        draw_cursor(draw, cursor_x, cursor_y)

    if phase >= 10:
        draw.rounded_rectangle((360, 606, 1172, 632), radius=12, fill=(31, 38, 53), outline=LINE)
        label = "Navegação em pausa" if 14 <= phase < 19 else "Execução controlada"
        color = ORANGE if 14 <= phase < 19 else GREEN
        draw.ellipse((378, 614, 390, 626), fill=color)
        text(draw, (402, 620), label, F13, WHITE)

    return im


frames = [make_frame(phase) for phase in range(26)]
frames[0].save(
    OUTPUT,
    save_all=True,
    append_images=frames[1:],
    duration=420,
    loop=0,
    optimize=True,
)
