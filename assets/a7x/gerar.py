"""Gera os SVGs do tema Avenged Sevenfold + caveiras (doodle) para o README."""
import os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

OUT = sys.argv[1]
FONT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)

LIGHT = "#FFFFFF"   # osso / caveira
DARK = "#000000"    # contorno / olhos
LAV = "#FFFFFF"     # doodles sobre o banner
MID = "#FFFFFF"     # elementos sobre fundo transparente (claro e escuro)

font = TTFont(FONT)
gs = font.getGlyphSet()
cmap = font.getBestCmap()
upm = font["head"].unitsPerEm
hmtx = font["hmtx"]


def text_path(txt, size, cx, baseline, fill, extra=""):
    s = size / upm
    parts, x = [], 0
    for ch in txt:
        g = cmap.get(ord(ch))
        if g is None:
            g = cmap.get(ord(" "))
        pen = SVGPathPen(gs)
        gs[g].draw(pen)
        d = pen.getCommands()
        if d:
            parts.append(f'<path transform="translate({x:.1f} 0)" d="{d}"/>')
        x += hmtx[g][0]
    width = x * s
    x0 = cx - width / 2
    return (f'<g transform="translate({x0:.1f} {baseline}) scale({s:.5f} {-s:.5f})" fill="{fill}" {extra}>'
            + "".join(parts) + "</g>"), width


# ---------- doodles (caixa 100x100) ----------
def place(inner, x, y, size, rot=0):
    k = size / 100
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({k}) translate(-50 -50)">{inner}</g>'


def skull():
    return (
        f'<path d="M50 10 C27 10 13 27 15 47 C16 58 22 64 30 67 L31 79 C31 87 69 87 69 79 L70 67 '
        f'C78 64 84 58 85 47 C87 27 73 10 50 10 Z" fill="{LIGHT}" stroke="{DARK}" stroke-width="4.5" stroke-linejoin="round"/>'
        f'<ellipse cx="36" cy="47" rx="9.5" ry="10.5" fill="{DARK}"/>'
        f'<ellipse cx="64" cy="47" rx="9.5" ry="10.5" fill="{DARK}"/>'
        f'<path d="M50 57 L45 66 Q50 68 55 66 Z" fill="{DARK}"/>'
        f'<path d="M37 73 L63 73 M43 70 L43 82 M50 70 L50 84 M57 70 L57 82" stroke="{DARK}" stroke-width="3" stroke-linecap="round" fill="none"/>'
        f'<path d="M63 16 L58 25 L64 30" stroke="{DARK}" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
    )


def bones():
    segs = [((14, 96), (86, 28)), ((86, 96), (14, 28))]
    out = []
    for layer, (w, r, c) in enumerate([(14, 8, DARK), (7, 4.8, LIGHT)]):
        for (x1, y1), (x2, y2) in segs:
            dx, dy = x2 - x1, y2 - y1
            n = (dx * dx + dy * dy) ** 0.5
            px, py = -dy / n * 5.5, dx / n * 5.5
            out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>')
            for ex, ey in ((x1, y1), (x2, y2)):
                out.append(f'<circle cx="{ex+px:.1f}" cy="{ey+py:.1f}" r="{r}" fill="{c}"/>')
                out.append(f'<circle cx="{ex-px:.1f}" cy="{ey-py:.1f}" r="{r}" fill="{c}"/>')
    return "".join(out)


def skull_bones():
    return bones() + place(skull(), 50, 46, 78)


def lightning(c=LAV):
    return f'<path d="M58 4 L24 56 L46 56 L36 96 L78 38 L54 38 L68 4 Z" fill="{c}" stroke="{DARK}" stroke-width="3" stroke-linejoin="round"/>'


def star(c=LAV):
    return "".join(
        f'<line x1="50" y1="50" x2="{x}" y2="{y}" stroke="{c}" stroke-width="9" stroke-linecap="round"/>'
        for x, y in ((50, 12), (50, 88), (17, 31), (83, 69), (17, 69), (83, 31)))


def flame(c=LAV):
    return (f'<path d="M50 96 C26 96 16 76 22 60 C26 50 33 45 31 30 C41 38 43 47 45 53 C49 37 46 22 56 4 '
            f'C61 25 79 39 81 63 C83 83 71 96 50 96 Z" fill="{c}"/>'
            f'<path d="M50 90 C38 90 33 80 37 70 C40 64 44 62 46 55 C50 62 52 66 54 64 C58 70 64 76 62 82 '
            f'C60 88 56 90 50 90 Z" fill="{DARK}"/>')


def crown(c=LAV):
    return (f'<path d="M14 78 L12 30 L32 54 L50 18 L68 54 L88 30 L86 78" fill="none" stroke="{c}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<path d="M8 90 L92 87" stroke="{c}" stroke-width="6" stroke-linecap="round"/>')


def heart(c=LAV):
    return (f'<path d="M50 88 C20 66 8 50 10 34 C12 20 26 12 38 16 C44 18 48 22 50 28 C52 22 56 18 62 16 '
            f'C74 12 88 20 90 34 C92 50 80 66 50 88 Z" fill="none" stroke="{c}" stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M50 28 L43 44 L54 52 L45 66 L51 78" fill="none" stroke="{c}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>')


def xmark(c=LAV):
    return (f'<path d="M20 22 L80 82 M78 20 L24 84" stroke="{c}" stroke-width="13" stroke-linecap="round"/>')


ROUGH = ('<filter id="rough" x="-5%" y="-5%" width="110%" height="110%">'
         '<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7"/>'
         '<feDisplacementMap in="SourceGraphic" scale="3.5"/></filter>')


def svg(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<defs>{ROUGH}{defs}</defs>{body}</svg>\n')


def write(name, content):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)


BG = ('<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
      '<stop offset="0" stop-color="#000000"/><stop offset="1" stop-color="#000000"/></linearGradient>'
      '<filter id="glow" x="-20%" y="-40%" width="140%" height="180%">'
      '<feGaussianBlur stdDeviation="6" result="b"/><feFlood flood-color="#FFFFFF" flood-opacity="0.35"/>'
      '<feComposite in2="b" operator="in" result="g"/><feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')

# ---------- header ----------
W, H = 1000, 320
name, _ = text_path("Lucas", 150, W / 2, 205, LIGHT, 'filter="url(#glow)"')
d = [
    place(skull_bones(), 175, 165, 170, -10), place(skull_bones(), 825, 165, 170, 10),
    place(skull(), 48, 48, 62, -18), place(skull(), 952, 48, 62, 18),
    place(skull(), 48, 272, 62, 14), place(skull(), 952, 272, 62, -14),
    place(skull(), 335, 268, 44, -8), place(skull(), 665, 268, 44, 8),
    place(skull(), 500, 286, 40, 0),
    place(crown(), 500, 52, 64, 0),
    place(lightning(), 330, 70, 58, -12), place(lightning(), 670, 70, 58, 12),
    place(flame(), 418, 280, 38, -6), place(flame(), 582, 280, 38, 6),
    place(star(), 120, 300, 26), place(star(), 880, 22, 26), place(star(), 250, 40, 22),
    place(star(), 750, 300, 22), place(star(), 400, 36, 18), place(star(), 600, 36, 18),
    place(heart(), 70, 165, 40, -10), place(heart(), 930, 165, 40, 10),
    place(xmark(), 260, 290, 22), place(xmark(), 740, 32, 22),
]
body = (f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="22" fill="url(#bg)" stroke="{MID}" stroke-width="3"/>'
        f'<g filter="url(#rough)">{"".join(d)}</g>{name}')
write("header.svg", svg(W, H, body, BG))

# ---------- typing ----------
lines = ["Estudante de Análise e Desenvolvimento de Sistemas", "Desenvolvedor em formação", "São Paulo - SP, Brasil"]
TW, TH, DUR = 1000, 70, 12
parts, clips = [], []
for i, ln in enumerate(lines):
    g, w = text_path(ln, 36, TW / 2, 48, "#FFFFFF")
    x0 = TW / 2 - w / 2
    a, b = i / 3, (i + 1) / 3
    kt = sorted({0, a, a + 0.1, b - 0.05, b, 1})
    vals = [0 if t in (0, a, b, 1) and not (t == a + 0.1 or t == b - 0.05) else w + 10 for t in kt]
    vals = [(w + 10) if (a + 0.1 - 1e-9) <= t <= (b - 0.05 + 1e-9) else 0 for t in kt]
    clips.append(f'<clipPath id="c{i}"><rect x="{x0-5:.1f}" y="0" width="0" height="{TH}">'
                 f'<animate attributeName="width" dur="{DUR}s" repeatCount="indefinite" calcMode="linear" '
                 f'keyTimes="{";".join(f"{t:.4f}" for t in kt)}" values="{";".join(f"{v:.1f}" for v in vals)}"/></rect></clipPath>')
    parts.append(f'<g clip-path="url(#c{i})">{g}</g>')
write("typing.svg", svg(TW, TH, f'<rect x="1" y="1" width="{TW-2}" height="{TH-2}" rx="14" fill="#000000"/>' + "".join(parts), "".join(clips)))

# ---------- divider ----------
DW, DH = 1000, 60
body = (f'<rect x="0" y="0" width="{DW}" height="{DH}" rx="14" fill="#000000"/><path d="M45 30 L410 30 M590 30 L955 30" stroke="{MID}" stroke-width="3" stroke-linecap="round"/>'
        f'<g filter="url(#rough)">'
        + place(skull_bones(), 500, 30, 54) + place(skull(), 440, 30, 30, -12) + place(skull(), 560, 30, 30, 12)
        + place(star(MID), 380, 30, 16) + place(star(MID), 620, 30, 16)
        + place(lightning(MID), 30, 30, 22, 20) + place(lightning(MID), 970, 30, 22, -20)
        + "</g>")
write("divider.svg", svg(DW, DH, body))

# ---------- ícone de caveira para títulos ----------
write("skull.svg", svg(100, 100, f'<g filter="url(#rough)">{skull()}</g>'))

# ---------- footer ----------
FW, FH = 1000, 150
row = []
for k in range(9):
    x = 70 + k * 107.5
    if k % 2 == 0:
        row.append(place(skull_bones(), x, 70, 82, (-8 if k % 4 == 0 else 8)))
    else:
        row.append(place(flame(), x, 78, 52, 0))
body = (f'<rect x="2" y="2" width="{FW-4}" height="{FH-4}" rx="22" fill="url(#bg)" stroke="{MID}" stroke-width="3"/>'
        f'<g filter="url(#rough)">{"".join(row)}'
        + place(star(), 30, 130, 16) + place(star(), 970, 20, 16) + "</g>")
write("footer.svg", svg(FW, FH, body, BG.replace('x1="0" y1="0" x2="1" y2="1"', 'x1="1" y1="1" x2="0" y2="0"')))
print("ok")
