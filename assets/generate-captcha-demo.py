from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "captcha-demo.gif"

W, H = 1200, 650
BG = (8, 11, 18)
PANEL = (17, 22, 32)
CHROME = (18, 23, 33)
LINE = (55, 65, 82)
PAPER = (248, 249, 251)
FIELD = (255, 255, 255)
BORDER = (205, 212, 224)
TEXT = (24, 29, 39)
MUTED = (112, 123, 140)
WHITE = (255, 255, 255)
ORANGE = (255, 180, 84)
GREEN = (63, 208, 155)
BLUE = (55, 118, 210)
CLAUDE = (221, 162, 111)


def load_font(size, bold=False):
    name = "segoeuib.ttf" if bold else "segoeui.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size)


F12 = load_font(12)
F13 = load_font(13)
F14 = load_font(14)
F16 = load_font(16)
F18 = load_font(18)
F20 = load_font(20)
F22 = load_font(22)
F24 = load_font(24, True)
F30 = load_font(30, True)


def box(draw, bounds, fill, radius=10, outline=None, width=1):
    draw.rounded_rectangle(bounds, radius=radius, fill=fill, outline=outline, width=width)


def draw_text(draw, xy, value, font=F14, fill=TEXT, anchor=None):
    draw.text(xy, value, font=font, fill=fill, anchor=anchor)


def fit_text(draw, box_bounds, value, font, fill):
    left, top, right, bottom = box_bounds
    max_width = right - left - 24
    probe = value
    while probe:
        bbox = draw.textbbox((0, 0), probe, font=font)
        if bbox[2] <= max_width:
            break
        probe = probe[:-1]
    if len(probe) < len(value):
        probe = probe[:-1].rstrip() + "..."
    draw_text(draw, (left + 12, (top + bottom) // 2), probe, font, fill, "lm")


def draw_cursor(draw, x, y):
    points = [
        (x, y),
        (x + 3, y + 30),
        (x + 10, y + 22),
        (x + 16, y + 34),
        (x + 21, y + 32),
        (x + 15, y + 20),
        (x + 25, y + 19),
    ]
    draw.polygon(points, fill=(18, 24, 36))
    draw.line(points + [points[0]], fill=WHITE, width=2)


def draw_claude(draw, phase):
    box(draw, (28, 28, 330, 622), PANEL, 18, LINE, 2)
    box(draw, (46, 48, 312, 88), (26, 33, 47), 12, LINE)
    draw.ellipse((64, 62, 82, 80), fill=CLAUDE)
    draw_text(draw, (94, 68), "Claude Code", F18, WHITE)
    draw_text(draw, (46, 112), "Skill: lattes-atualizar", F13, MUTED)

    command = "Preparar atividade autorizada"
    if phase >= 7:
        command = "Abrir formulário do Lattes"
    if phase >= 12:
        command = "Detectar CAPTCHA/MFA"
    if phase >= 16:
        command = "Aguardar intervenção humana"
    if phase >= 20:
        command = "Preencher campos aprovados"
    if phase >= 26:
        command = "Reabrir e verificar registro"

    box(draw, (46, 142, 312, 202), (13, 17, 26), 10, LINE)
    draw_text(draw, (58, 158), "> " + command, F13, WHITE)
    draw_text(draw, (58, 182), "lote: 1  ·  externa: autorizada", F12, MUTED)

    steps = [
        ("Inventariar planilha", phase >= 3),
        ("Conferir evidência", phase >= 5),
        ("Abrir formulário", phase >= 8),
        ("Resolver desafio", 12 <= phase < 16),
        ("Preencher campos", phase >= 17),
        ("Verificar registro", phase >= 26),
    ]
    y = 224
    for label, done in steps:
        color = GREEN if done else MUTED
        mark = "✓" if done else "○"
        draw_text(draw, (58, y), mark, F16, color)
        draw_text(draw, (82, y), label, F13, WHITE if done else MUTED)
        y += 42

    if 12 <= phase < 16:
        box(draw, (46, 510, 312, 584), (48, 42, 28), 10, (150, 117, 61), 2)
        draw_text(draw, (58, 528), "PAUSADO", F12, ORANGE)
        draw_text(draw, (58, 552), "Usuário assume CAPTCHA/MFA", F12, WHITE)
    elif phase >= 16:
        box(draw, (46, 510, 312, 584), (22, 47, 44), 10, (52, 135, 108), 2)
        draw_text(draw, (58, 528), "CONTROLE RESTABELECIDO", F12, GREEN)
        draw_text(draw, (58, 552), "Somente o lote autorizado", F12, WHITE)


def draw_browser(draw, phase):
    box(draw, (350, 28, 1172, 622), CHROME, 18, LINE, 2)

    for cx, color in ((388, (255, 97, 89)), (414, (255, 194, 75)), (440, (41, 201, 65))):
        draw.ellipse((cx, 48, cx + 16, 64), fill=color)
    box(draw, (470, 46, 1140, 82), (10, 13, 20), 18, LINE)
    draw_text(draw, (488, 64), "lattes.cnpq.br/curriculo/editar", F13, MUTED)

    box(draw, (370, 94, 1152, 602), PAPER, 12, (214, 219, 228), 1)
    box(draw, (370, 94, 1152, 142), (43, 76, 145), 12)
    draw_text(draw, (394, 118), "Currículo Lattes", F18, WHITE)

    draw_text(draw, (394, 162), "Adicionar produção bibliográfica", F20, TEXT)
    draw_text(draw, (394, 184), "Artigo publicado", F13, MUTED)

    fields = [
        ("Título", "Automação segura de currículos acadêmicos", 214),
        ("Autores", "Cleyber Silva; equipe colaboradora", 278),
        ("Ano", "2026", 342),
        ("DOI", "10.0000/demo.lattes.2026", 406),
        ("Natureza", "Artigo completo publicado", 470),
    ]

    cursor_x, cursor_y = 0, 0
    for index, (label, value, y) in enumerate(fields):
        draw_text(draw, (394, y - 12), label, F12, MUTED)
        box(draw, (394, y, 1128, y + 42), FIELD, 8, BORDER, 2)

        visible = ""
        if phase >= 20:
            local = phase - 20
            count = max(0, min(len(value), local * 5 - index * 2))
            visible = value[:count]
        if phase >= 27:
            visible = value
        fit_text(draw, (394, y, 1128, y + 42), visible, F14, TEXT)

        if 20 <= phase < 27 and index == min(max(0, (phase - 20) // 1), len(fields) - 1):
            local = phase - 20
            count = max(0, min(len(value), local * 5 - index * 2))
            probe = value[:count]
            bbox = draw.textbbox((0, 0), probe, font=F14)
            cursor_x = 406 + bbox[2]
            cursor_y = y + 21

    if 12 <= phase < 16:
        box(draw, (610, 238, 918, 430), WHITE, 12, (190, 197, 208), 2)
        draw_text(draw, (636, 268), "Verificação de segurança", F18, TEXT)
        box(draw, (636, 300, 892, 350), (242, 245, 249), 8, BORDER)
        draw_text(draw, (650, 318), "CAPTCHA / MFA", F16, TEXT)
        draw_text(draw, (650, 338), "Aguardando ação do usuário", F12, MUTED)
        box(draw, (636, 368, 892, 408), (255, 247, 223), 8, (230, 200, 120), 2)
        draw_text(draw, (650, 388), "Resolver manualmente", F14, TEXT)
        cursor_x, cursor_y = 750, 388

    if phase >= 27:
        box(draw, (394, 526, 1128, 574), (229, 247, 239), 8, (120, 205, 171), 1)
        draw_text(draw, (408, 550), "✓ Campos conferidos  ·  registro pronto para revisão", F14, (31, 121, 88))

    return cursor_x, cursor_y


def make_frame(phase):
    im = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(im)
    draw_claude(draw, phase)
    cursor_x, cursor_y = draw_browser(draw, phase)

    if 12 <= phase < 16:
        draw_cursor(draw, cursor_x, cursor_y)
    elif 20 <= phase < 27:
        draw_cursor(draw, cursor_x, cursor_y)

    box(draw, (350, 606, 1172, 632), (31, 38, 53), 12, LINE)
    label = "Navegação em pausa" if 12 <= phase < 16 else "Execução controlada"
    color = ORANGE if 12 <= phase < 16 else GREEN
    draw.ellipse((366, 614, 378, 626), fill=color)
    draw_text(draw, (390, 620), label, F12, WHITE)
    return im


frames = [make_frame(phase) for phase in range(32)]
frames[0].save(
    OUTPUT,
    save_all=True,
    append_images=frames[1:],
    duration=420,
    loop=0,
    optimize=True,
)
