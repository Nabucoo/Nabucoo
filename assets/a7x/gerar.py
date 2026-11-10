"""Gera os SVGs do tema preto e branco com caveiras (doodle) para o README.

Uso: python3 gerar.py <pasta_saida> <fonte_gotica.woff2>
"""
import os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

OUT = sys.argv[1]
FONT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)

W = "#FFFFFF"
K = "#000000"

font = TTFont(FONT)
gs = font.getGlyphSet()
cmap = font.getBestCmap()
upm = font["head"].unitsPerEm
hmtx = font["hmtx"]


def text_path(txt, size, cx, baseline, fill, extra=""):
    s = size / upm
    parts, x = [], 0
    for ch in txt:
        g = cmap.get(ord(ch)) or cmap.get(ord(" "))
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


# ---------------- doodles (caixa 100x100, centro 50,50) ----------------
def place(inner, x, y, size, rot=0):
    k = size / 100
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({k}) translate(-50 -50)">{inner}</g>'


def skull():
    return (
        f'<path d="M50 10 C27 10 13 27 15 47 C16 58 22 64 30 67 L31 79 C31 87 69 87 69 79 L70 67 '
        f'C78 64 84 58 85 47 C87 27 73 10 50 10 Z" fill="{W}" stroke="{K}" stroke-width="4.5" stroke-linejoin="round"/>'
        f'<ellipse cx="36" cy="47" rx="9.5" ry="10.5" fill="{K}"/>'
        f'<ellipse cx="64" cy="47" rx="9.5" ry="10.5" fill="{K}"/>'
        f'<path d="M50 57 L45 66 Q50 68 55 66 Z" fill="{K}"/>'
        f'<path d="M37 73 L63 73 M43 70 L43 82 M50 70 L50 84 M57 70 L57 82" stroke="{K}" stroke-width="3" stroke-linecap="round" fill="none"/>'
        f'<path d="M63 16 L58 25 L64 30" stroke="{K}" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
    )


def mohawk():
    crest = (f'<path d="M33 26 C29 16 31 7 35 0 L41 11 L45 -4 L51 9 L57 -4 L61 11 L67 0 C72 10 71 19 67 26 Z" '
             f'fill="{W}" stroke="{K}" stroke-width="3.5" stroke-linejoin="round"/>'
             f'<path d="M41 11 L44 22 M51 9 L51 22 M61 11 L58 22" stroke="{K}" stroke-width="2.5" stroke-linecap="round"/>')
    return crest + place(skull(), 50, 58, 86)


def bones():
    segs = [((14, 96), (86, 28)), ((86, 96), (14, 28))]
    out = []
    for w, r, c in [(14, 8, K), (7, 4.8, W)]:
        for (x1, y1), (x2, y2) in segs:
            dx, dy = x2 - x1, y2 - y1
            n = (dx * dx + dy * dy) ** 0.5
            px, py = -dy / n * 5.5, dx / n * 5.5
            out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>')
            for ex, ey in ((x1, y1), (x2, y2)):
                out.append(f'<circle cx="{ex+px:.1f}" cy="{ey+py:.1f}" r="{r}" fill="{c}"/>')
                out.append(f'<circle cx="{ex-px:.1f}" cy="{ey-py:.1f}" r="{r}" fill="{c}"/>')
    return "".join(out)


def skull_bones(head=None):
    return bones() + place((head or skull)(), 50, 46, 78)


def lightning():
    return f'<path d="M58 4 L24 56 L46 56 L36 96 L78 38 L54 38 L68 4 Z" fill="{W}" stroke="{K}" stroke-width="3" stroke-linejoin="round"/>'


def star():
    return "".join(
        f'<line x1="50" y1="50" x2="{x}" y2="{y}" stroke="{W}" stroke-width="9" stroke-linecap="round"/>'
        for x, y in ((50, 12), (50, 88), (17, 31), (83, 69), (17, 69), (83, 31)))


def flame():
    return (f'<path d="M50 96 C26 96 16 76 22 60 C26 50 33 45 31 30 C41 38 43 47 45 53 C49 37 46 22 56 4 '
            f'C61 25 79 39 81 63 C83 83 71 96 50 96 Z" fill="{W}" stroke="{K}" stroke-width="3"/>'
            f'<path d="M50 90 C38 90 33 80 37 70 C40 64 44 62 46 55 C50 62 52 66 54 64 C58 70 64 76 62 82 '
            f'C60 88 56 90 50 90 Z" fill="{K}"/>')


def crown():
    return (f'<path d="M14 78 L12 30 L32 54 L50 18 L68 54 L88 30 L86 78" fill="none" stroke="{W}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<path d="M8 90 L92 87" stroke="{W}" stroke-width="6" stroke-linecap="round"/>'
            f'<circle cx="12" cy="24" r="5" fill="{W}"/><circle cx="50" cy="11" r="5" fill="{W}"/><circle cx="88" cy="24" r="5" fill="{W}"/>')


HEART = ("M50 88 C20 66 8 50 10 34 C12 20 26 12 38 16 C44 18 48 22 50 28 C52 22 56 18 62 16 "
         "C74 12 88 20 90 34 C92 50 80 66 50 88 Z")


def heart():
    return (f'<path d="{HEART}" fill="none" stroke="{W}" stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M50 28 L43 44 L54 52 L45 66 L51 78" fill="none" stroke="{W}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>')


def flaming_heart():
    return (place(flame(), 30, 34, 52, -18) + place(flame(), 70, 34, 52, 18) + place(flame(), 50, 26, 62)
            + place(f'<path d="{HEART}" fill="{W}" stroke="{K}" stroke-width="7" stroke-linejoin="round"/>', 50, 64, 70))


def xmark():
    return f'<path d="M20 22 L80 82 M78 20 L24 84" stroke="{W}" stroke-width="13" stroke-linecap="round"/>'


def guitar():
    return (
        f'<path d="M50 58 C44 58 42 52 36 52 C26 52 24 64 30 70 C22 76 22 92 36 96 C44 98 48 94 50 94 '
        f'C52 94 58 98 66 96 C78 92 78 76 70 70 C76 64 74 52 64 52 C58 52 56 58 50 58 Z" fill="{W}" stroke="{K}" stroke-width="3"/>'
        f'<rect x="46" y="10" width="8" height="58" fill="{W}" stroke="{K}" stroke-width="2.5"/>'
        f'<path d="M44 1 L56 1 L57 14 L43 14 Z" fill="{W}" stroke="{K}" stroke-width="2.5" stroke-linejoin="round"/>'
        f'<g fill="{W}" stroke="{K}" stroke-width="1.5"><circle cx="40" cy="4" r="2.6"/><circle cx="40" cy="10" r="2.6"/>'
        f'<circle cx="60" cy="4" r="2.6"/><circle cx="60" cy="10" r="2.6"/></g>'
        f'<path d="M46 22 L54 22 M46 30 L54 30 M46 38 L54 38 M46 46 L54 46 M46 54 L54 54" stroke="{K}" stroke-width="1.6"/>'
        f'<rect x="42" y="68" width="16" height="4" rx="1.5" fill="{K}"/><rect x="42" y="76" width="16" height="4" rx="1.5" fill="{K}"/>'
        f'<rect x="40" y="85" width="20" height="3.5" rx="1.5" fill="{K}"/>'
        f'<line x1="50" y1="12" x2="50" y2="86" stroke="{K}" stroke-width="0.9"/>'
        f'<circle cx="66" cy="88" r="2.6" fill="{K}"/><circle cx="70" cy="81" r="2.2" fill="{K}"/>'
    )


def eye():
    lashes = "".join(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="{W}" stroke-width="4.5" stroke-linecap="round"/>'
                     for a, b, c, d in ((22, 34, 14, 23), (36, 26, 32, 13), (50, 23, 50, 9), (64, 26, 68, 13), (78, 34, 86, 23)))
    return (lashes + f'<path d="M6 52 Q50 12 94 52 Q50 92 6 52 Z" fill="{W}" stroke="{K}" stroke-width="4"/>'
            f'<circle cx="50" cy="52" r="17" fill="{K}"/><circle cx="56" cy="46" r="5" fill="{W}"/>')


def note():
    return (f'<g fill="{W}" stroke="{K}" stroke-width="2.5"><ellipse cx="31" cy="78" rx="12" ry="8.5" transform="rotate(-20 31 78)"/>'
            f'<ellipse cx="73" cy="70" rx="12" ry="8.5" transform="rotate(-20 73 70)"/>'
            f'<path d="M39 76 L39 22 L83 12 L83 68 L77 68 L77 26 L45 33 L45 76 Z"/></g>')


def diamond():
    return (f'<path d="M18 38 L34 18 L66 18 L82 38 L50 88 Z" fill="none" stroke="{W}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M18 38 L82 38 M34 18 L42 38 L50 88 M66 18 L58 38 L50 88" fill="none" stroke="{W}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M50 2 L50 10 M24 6 L29 12 M76 6 L71 12" stroke="{W}" stroke-width="3.5" stroke-linecap="round"/>')


def rose():
    return (f'<path d="M50 62 C34 60 16 70 6 88 C26 92 42 82 50 62 Z" fill="{W}" stroke="{K}" stroke-width="3"/>'
            f'<path d="M50 62 C66 60 84 70 94 88 C74 92 58 82 50 62 Z" fill="{W}" stroke="{K}" stroke-width="3"/>'
            f'<path d="M28 82 L18 84 M72 82 L82 84" stroke="{K}" stroke-width="2.5" stroke-linecap="round"/>'
            f'<path d="M50 70 C24 70 18 50 24 34 C28 22 40 14 50 18 C60 14 72 22 76 34 C82 50 76 70 50 70 Z" fill="{W}" stroke="{K}" stroke-width="3.5"/>'
            f'<path d="M50 44 C56 42 56 36 50 35 C43 34 40 43 44 49 C50 56 62 52 64 42 C66 31 55 24 45 26 '
            f'C33 29 29 44 35 54 M24 40 C30 48 40 54 50 52" fill="none" stroke="{K}" stroke-width="3" stroke-linecap="round"/>')


def chain_link(vertical):
    if vertical:
        return f'<rect x="38" y="20" width="24" height="60" rx="12" fill="none" stroke="{W}" stroke-width="7"/>'
    return f'<rect x="20" y="38" width="60" height="24" rx="12" fill="none" stroke="{W}" stroke-width="7"/>'


ROUGH = ('<filter id="rough" x="-5%" y="-5%" width="110%" height="110%">'
         '<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7"/>'
         '<feDisplacementMap in="SourceGraphic" scale="3.5"/></filter>')
GLOW = ('<filter id="glow" x="-20%" y="-40%" width="140%" height="180%">'
        '<feGaussianBlur stdDeviation="6" result="b"/><feFlood flood-color="#FFFFFF" flood-opacity="0.35"/>'
        '<feComposite in2="b" operator="in" result="g"/><feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')


def svg(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<defs>{ROUGH}{GLOW}{defs}</defs>{body}</svg>\n')


def card(w, h, doodles, r=22):
    return svg(w, h, f'<rect x="2" y="2" width="{w-4}" height="{h-4}" rx="{r}" fill="{K}" stroke="{W}" stroke-width="3"/>'
                     f'<g filter="url(#rough)">{"".join(doodles)}</g>')


def write(name, content):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)


# ---------------- header ----------------
HW, HH = 1000, 340
name, _ = text_path("Lucas", 150, HW / 2, 212, W, 'filter="url(#glow)"')
d = [
    place(guitar(), 62, 175, 150, -28), place(guitar(), 938, 175, 150, 28),
    place(skull_bones(), 195, 175, 165, -10), place(skull_bones(mohawk), 805, 168, 170, 10),
    place(skull(), 46, 46, 56, -18), place(skull(), 954, 46, 56, 18),
    place(skull(), 46, 296, 56, 14), place(skull(), 954, 296, 56, -14),
    place(crown(), 500, 50, 62),
    place(note(), 418, 46, 36, -10), place(note(), 584, 46, 36, 10),
    place(lightning(), 322, 74, 52, -12), place(lightning(), 678, 74, 52, 12),
    place(eye(), 300, 292, 48, -6), place(eye(), 700, 292, 48, 6),
    place(skull(), 405, 290, 40, -8), place(skull(), 595, 290, 40, 8), place(skull(), 500, 300, 38),
    place(flame(), 452, 296, 30, -6), place(flame(), 548, 296, 30, 6),
    place(heart(), 268, 36, 34, -12), place(heart(), 732, 36, 34, 12),
    place(star(), 128, 318, 22), place(star(), 872, 24, 22), place(star(), 372, 26, 18),
    place(star(), 628, 26, 18), place(star(), 222, 300, 18), place(star(), 778, 300, 18),
    place(diamond(), 128, 28, 30), place(xmark(), 875, 318, 20),
]
write("header.svg", svg(HW, HH,
      f'<rect x="2" y="2" width="{HW-4}" height="{HH-4}" rx="22" fill="{K}" stroke="{W}" stroke-width="3"/>'
      f'<g filter="url(#rough)">{"".join(d)}</g>{name}'))

# ---------------- linha animada ----------------
lines = ["Estudante de Análise e Desenvolvimento de Sistemas", "Desenvolvedor em formação", "São Paulo - SP, Brasil"]
TW, TH, DUR = 1000, 70, 12
parts, clips = [], []
for i, ln in enumerate(lines):
    g, w = text_path(ln, 36, TW / 2, 48, W)
    x0 = TW / 2 - w / 2
    a, b = i / 3, (i + 1) / 3
    kt = sorted({0, a, a + 0.1, b - 0.05, b, 1})
    vals = [(w + 10) if (a + 0.1 - 1e-9) <= t <= (b - 0.05 + 1e-9) else 0 for t in kt]
    clips.append(f'<clipPath id="c{i}"><rect x="{x0-5:.1f}" y="0" width="0" height="{TH}">'
                 f'<animate attributeName="width" dur="{DUR}s" repeatCount="indefinite" calcMode="linear" '
                 f'keyTimes="{";".join(f"{t:.4f}" for t in kt)}" values="{";".join(f"{v:.1f}" for v in vals)}"/></rect></clipPath>')
    parts.append(f'<g clip-path="url(#c{i})">{g}</g>')
side = place(skull(), 36, 35, 40, -12) + place(skull(), 964, 35, 40, 12)
write("typing.svg", svg(TW, TH, f'<rect x="1" y="1" width="{TW-2}" height="{TH-2}" rx="14" fill="{K}"/>'
                        f'<g filter="url(#rough)">{side}</g>' + "".join(parts), "".join(clips)))

# ---------------- separadores (cada um diferente) ----------------
DW, DH = 1000, 60


def strip(doodles, line=True):
    ln = f'<path d="M60 30 L395 30 M605 30 L940 30" stroke="{W}" stroke-width="3" stroke-linecap="round"/>' if line else ""
    return svg(DW, DH, f'<rect x="0" y="0" width="{DW}" height="{DH}" rx="14" fill="{K}"/>{ln}'
                       f'<g filter="url(#rough)">{"".join(doodles)}</g>')


write("divider-1.svg", strip([place(skull_bones(), 500, 30, 54), place(skull(), 440, 30, 30, -12), place(skull(), 560, 30, 30, 12),
                              place(star(), 380, 30, 16), place(star(), 620, 30, 16),
                              place(lightning(), 34, 30, 24, 20), place(lightning(), 966, 30, 24, -20)]))
write("divider-2.svg", strip([place(chain_link(k % 2 == 0), 40 + k * 23.5, 30, 34) for k in range(40) if not 18 <= k <= 21]
                             + [place(mohawk(), 500, 30, 50)], line=False))
write("divider-3.svg", strip([place(flame() if k % 2 else skull(), 40 + k * 46, 31, 34 if k % 2 else 30, (k % 3 - 1) * 8)
                              for k in range(21)], line=False))
write("divider-4.svg", strip([place(eye(), 500, 30, 56), place(lightning(), 445, 30, 30, -15), place(lightning(), 555, 30, 30, 15),
                              place(xmark(), 380, 30, 14), place(xmark(), 620, 30, 14),
                              place(skull(), 34, 30, 30, -10), place(skull(), 966, 30, 30, 10)]))
write("divider-5.svg", strip([place(rose(), 500, 30, 54), place(heart(), 445, 30, 30, -12), place(heart(), 555, 30, 30, 12),
                              place(diamond(), 380, 30, 20), place(diamond(), 620, 30, 20),
                              place(note(), 34, 30, 28), place(note(), 966, 30, 28)]))

# ---------------- ícones dos títulos (selo preto, funciona no tema claro e escuro) ----------------
def badge(inner, size=72):
    return svg(100, 100, f'<circle cx="50" cy="50" r="47" fill="{K}" stroke="{W}" stroke-width="3"/>'
                         f'<g filter="url(#rough)">{place(inner, 50, 52, size)}</g>')


write("icon-ola.svg", badge(skull()))
write("icon-sobre.svg", badge(mohawk(), 70))
write("icon-tech.svg", badge(guitar(), 74))
write("icon-objetivo.svg", badge(crown(), 62))
write("icon-estudo.svg", badge(eye(), 72))
write("icon-contato.svg", badge(flaming_heart(), 74))

# ---------------- ilustrações laterais ----------------
write("card-sobre.svg", card(220, 260, [
    place(skull_bones(mohawk), 110, 120, 170, -6), place(lightning(), 34, 40, 40, -15), place(star(), 190, 36, 24),
    place(note(), 188, 222, 36, 10), place(flame(), 34, 222, 36), place(star(), 112, 234, 16)]))
write("card-objetivo.svg", card(200, 200, [
    place(crown(), 100, 46, 70), place(skull(), 100, 118, 100), place(diamond(), 30, 168, 30, -10),
    place(diamond(), 170, 168, 30, 10), place(star(), 28, 34, 18), place(star(), 172, 34, 18)]))
write("card-estudo.svg", card(200, 200, [
    place(eye(), 100, 64, 110), place(guitar(), 64, 140, 90, -30), place(rose(), 140, 146, 66, 8),
    place(star(), 26, 182, 16), place(star(), 176, 22, 16)]))

# ---------------- rodapé ----------------
FW, FH = 1000, 180
fx = [place(guitar(), 470, 92, 150, -32), place(guitar(), 530, 92, 150, 32), place(skull_bones(), 500, 78, 96),
      place(skull_bones(), 82, 90, 96, -8), place(flame(), 185, 96, 58), place(rose(), 285, 92, 70, -8),
      place(flaming_heart(), 380, 92, 64),
      place(flaming_heart(), 620, 92, 64), place(rose(), 715, 92, 70, 8), place(flame(), 815, 96, 58),
      place(skull_bones(mohawk), 918, 90, 100, 8),
      place(star(), 30, 158, 16), place(star(), 970, 22, 16), place(star(), 250, 26, 14), place(star(), 750, 158, 14),
      place(eye(), 400, 160, 34), place(eye(), 600, 160, 34)]
write("footer.svg", svg(FW, FH, f'<rect x="2" y="2" width="{FW-4}" height="{FH-4}" rx="22" fill="{K}" stroke="{W}" stroke-width="3"/>'
                                f'<g filter="url(#rough)">{"".join(fx)}</g>'))
# ---------------- projetos ----------------
def gift():
    return (f'<path d="M38 34 C22 20 16 34 30 38 Z M62 34 C78 20 84 34 70 38 Z" fill="none" stroke="{W}" stroke-width="5" stroke-linejoin="round"/>'
            f'<rect x="20" y="50" width="60" height="42" fill="{W}" stroke="{K}" stroke-width="3"/>'
            f'<rect x="14" y="36" width="72" height="16" fill="{W}" stroke="{K}" stroke-width="3"/>'
            f'<rect x="45" y="36" width="10" height="56" fill="{K}"/>'
            f'<path d="M50 36 L44 26 M50 36 L56 26" stroke="{W}" stroke-width="4" stroke-linecap="round"/>')


def chart():
    return (f'<path d="M12 90 L92 90 M12 90 L12 10" stroke="{W}" stroke-width="5" stroke-linecap="round"/>'
            f'<g fill="{W}" stroke="{K}" stroke-width="3"><rect x="20" y="64" width="14" height="26"/>'
            f'<rect x="40" y="50" width="14" height="40"/><rect x="60" y="36" width="14" height="54"/></g>'
            f'<path d="M18 52 L40 34 L56 42 L86 14" fill="none" stroke="{W}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M72 13 L87 13 L87 28" fill="none" stroke="{W}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')


def coins():
    out = []
    for i, y in enumerate((80, 66, 52, 38)):
        out.append(f'<ellipse cx="50" cy="{y+6}" rx="32" ry="11" fill="{W}" stroke="{K}" stroke-width="3"/>'
                   f'<ellipse cx="50" cy="{y}" rx="32" ry="11" fill="{W}" stroke="{K}" stroke-width="3"/>')
    out.append(f'<text x="50" y="44" font-family="Georgia,serif" font-size="18" font-weight="bold" text-anchor="middle" fill="{K}">$</text>')
    return "".join(out)


def project_card(fname, title, left, right, extras):
    PW, PH = 480, 190
    size = 66
    _, w = text_path(title, size, PW / 2, 0, W)
    if w > 270:
        size = size * 270 / w
    t, _ = text_path(title, size, PW / 2, 96 + size * 0.33, W, 'filter="url(#glow)"')
    body = (f'<rect x="2" y="2" width="{PW-4}" height="{PH-4}" rx="22" fill="{K}" stroke="{W}" stroke-width="3"/>'
            f'<g filter="url(#rough)">{place(left, 58, 92, 82, -8)}{place(right, 422, 92, 82, 8)}{"".join(extras)}</g>{t}')
    write(fname, svg(PW, PH, body))


project_card("projeto-queroae.svg", "QueroAê", gift(), skull_bones(), [
    place(heart(), 150, 160, 26, -10), place(heart(), 330, 160, 26, 10), place(star(), 120, 30, 18),
    place(star(), 360, 28, 16), place(xmark(), 240, 30, 14), place(star(), 240, 166, 14),
    place(flaming_heart(), 190, 34, 30), place(flaming_heart(), 290, 34, 30)])
project_card("projeto-simulafin.svg", "SimulaFin", chart(), coins(), [
    place(lightning(), 150, 160, 28, -12), place(lightning(), 330, 160, 28, 12), place(skull(), 240, 162, 30),
    place(star(), 120, 30, 18), place(star(), 360, 28, 16), place(diamond(), 200, 30, 22), place(diamond(), 280, 30, 22)])
write("icon-projetos.svg", badge(gift(), 70))
write("divider-6.svg", strip([place(gift(), 500, 30, 46), place(chart(), 440, 30, 30), place(coins(), 560, 30, 30),
                              place(star(), 380, 30, 16), place(star(), 620, 30, 16),
                              place(flame(), 34, 30, 28), place(flame(), 966, 30, 28)]))
print("ok")
