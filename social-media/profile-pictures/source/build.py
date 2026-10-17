"""Haven Tashkent profile picture — rendered from vector shapes + official brand assets.
No AI imagery: every Tashkent element is hand-built SVG geometry.
Run: pip install playwright && python build.py   (writes out/master-orange.png)
YouTube banner: python banner.py   (writes out/banner.png)"""
import base64, sys, pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
# Brand assets: uses ./assets if present, otherwise the team repo's brand-kit/ folders
_KIT = HERE.parents[2] / "brand-kit"
_DIRS = [HERE / "assets", _KIT / "logos", _KIT / "fonts", _KIT / "daven-pudding"]
class _Assets:
    def __truediv__(self, name):
        for d in _DIRS:
            if (d / name).exists(): return d / name
        raise FileNotFoundError(name)
A = _Assets()
def b64(p): return base64.b64encode((A / p).read_bytes()).decode()

S = 2048
# brand palette
LIME, CARROT = "#B8C11F", "#FC8616"
BANANA, PUMPKIN, FADED = "#F9DD60", "#E87136", "#DFA063"
UMBER, LUCKY = "#783D2B", "#A8A237"
CREAM = "#FFF4E0"

def variant_colors(v):
    if v == "orange":
        return dict(sky_top=CARROT, sky_mid="#FDA23F", sky_glow=BANANA, back=FADED, back_op=0.85)
    else:  # green sky variant
        return dict(sky_top=LUCKY, sky_mid=LIME, sky_glow=BANANA, back="#D9D27A", back_op=0.9)

def star8(cx, cy, r, fill, op=1.0):
    """Uzbek 8-point star (two overlapping squares)."""
    s = r * 0.72
    return (f'<g opacity="{op}" fill="{fill}">'
            f'<rect x="{cx-s}" y="{cy-s}" width="{2*s}" height="{2*s}" rx="{s*0.12}"/>'
            f'<rect x="{cx-s}" y="{cy-s}" width="{2*s}" height="{2*s}" rx="{s*0.12}" transform="rotate(45 {cx} {cy})"/></g>')

def tv_tower(x, base, top, col, accent):
    """Tashkent TV Tower: tripod legs, slender shaft, observation pod, antenna."""
    h = base - top
    leg_top = base - h * 0.30
    pod_y = base - h * 0.62
    out = []
    # three splayed legs (front view: two outer, one middle)
    for dx in (-95, 95):
        out.append(f'<path d="M{x+dx},{base} Q{x+dx*0.35},{base-h*0.12} {x+dx*0.08},{leg_top}" '
                   f'stroke="{col}" stroke-width="22" fill="none" stroke-linecap="round"/>')
    out.append(f'<rect x="{x-11}" y="{leg_top}" width="22" height="{base-leg_top}" fill="{col}"/>')
    # shaft tapering
    out.append(f'<path d="M{x-24},{leg_top+4} L{x-13},{pod_y} L{x+13},{pod_y} L{x+24},{leg_top+4} Z" fill="{col}"/>')
    # ring platform at leg top
    out.append(f'<rect x="{x-40}" y="{leg_top-10}" width="80" height="22" rx="8" fill="{col}"/>')
    # observation pod (stacked discs)
    out.append(f'<ellipse cx="{x}" cy="{pod_y+18}" rx="62" ry="24" fill="{col}"/>')
    out.append(f'<rect x="{x-52}" y="{pod_y-34}" width="104" height="52" rx="18" fill="{col}"/>')
    out.append(f'<rect x="{x-46}" y="{pod_y-20}" width="92" height="12" rx="5" fill="{accent}"/>')
    out.append(f'<ellipse cx="{x}" cy="{pod_y-36}" rx="44" ry="16" fill="{col}"/>')
    # upper shaft + antenna with red/white bands feel
    out.append(f'<path d="M{x-12},{pod_y-40} L{x-6},{top+h*0.12} L{x+6},{top+h*0.12} L{x+12},{pod_y-40} Z" fill="{col}"/>')
    out.append(f'<rect x="{x-3.5}" y="{top}" width="7" height="{h*0.13}" fill="{col}"/>')
    out.append(f'<circle cx="{x}" cy="{top-4}" r="8" fill="{accent}"/>')
    return "\n".join(out)

def dome(cx, base, w, h, col, ribs=None, rib_col=None, finial=True):
    """Ribbed melon dome on a drum."""
    out = [f'<path d="M{cx-w/2},{base} C{cx-w/2},{base-h*0.75} {cx-w*0.18},{base-h} {cx},{base-h} '
           f'C{cx+w*0.18},{base-h} {cx+w/2},{base-h*0.75} {cx+w/2},{base} Z" fill="{col}"/>']
    if ribs:
        for i in range(1, ribs):
            t = i / ribs
            rx = cx - w/2 + w*t
            out.append(f'<path d="M{rx},{base} Q{cx + (rx-cx)*0.55},{base-h*0.78} {cx},{base-h+4}" '
                       f'stroke="{rib_col}" stroke-width="5" fill="none" opacity="0.55"/>')
    if finial:
        out.append(f'<rect x="{cx-3}" y="{base-h-34}" width="6" height="36" fill="{col}"/>')
        out.append(f'<circle cx="{cx}" cy="{base-h-36}" r="7" fill="{col}"/>')
    return "\n".join(out)

def madrasa(x0, base, w, h, col, dome_col, light):
    """Kukeldash-style madrasa: big pishtaq portal with pointed arch + corner guldasta towers + domes."""
    out = []
    cx = x0 + w/2
    # side wings
    out.append(f'<rect x="{x0}" y="{base-h*0.55}" width="{w}" height="{h*0.55}" fill="{col}"/>')
    # wing arches (small niches)
    for i in range(4):
        for side in (-1, 1):
            nx = cx + side*(w*0.23 + i*w*0.065)
            if abs(nx-cx) > w/2-30: continue
            out.append(f'<path d="M{nx-16},{base-30} L{nx-16},{base-h*0.36} Q{nx},{base-h*0.46} {nx+16},{base-h*0.36} L{nx+16},{base-30} Z" fill="{light}" opacity="0.35"/>')
    # domes behind the portal
    out.append(dome(cx - w*0.30, base - h*0.55, w*0.22, h*0.30, dome_col, ribs=6, rib_col=col))
    out.append(dome(cx + w*0.30, base - h*0.55, w*0.22, h*0.30, dome_col, ribs=6, rib_col=col))
    # portal (pishtaq)
    pw = w*0.42
    out.append(f'<rect x="{cx-pw/2}" y="{base-h}" width="{pw}" height="{h}" fill="{col}"/>')
    # pointed arch recess
    aw = pw*0.58
    out.append(f'<path d="M{cx-aw/2},{base} L{cx-aw/2},{base-h*0.55} Q{cx-aw/2},{base-h*0.80} {cx},{base-h*0.88} '
               f'Q{cx+aw/2},{base-h*0.80} {cx+aw/2},{base-h*0.55} L{cx+aw/2},{base} Z" fill="{FADED}" opacity="0.9"/>')
    # tile band frame
    out.append(f'<path d="M{cx-pw/2+18},{base} L{cx-pw/2+18},{base-h+18} L{cx+pw/2-18},{base-h+18} L{cx+pw/2-18},{base}" '
               f'stroke="{dome_col}" stroke-width="9" fill="none"/>')
    # corner guldasta towers
    for gx in (cx-pw/2-14, cx+pw/2+14):
        out.append(f'<rect x="{gx-17}" y="{base-h*1.08}" width="34" height="{h*1.08}" rx="6" fill="{col}"/>')
        out.append(f'<path d="M{gx-24},{base-h*1.08} Q{gx},{base-h*1.26} {gx+24},{base-h*1.08} Z" fill="{dome_col}"/>')
        out.append(f'<rect x="{gx-24}" y="{base-h*1.08}" width="48" height="12" rx="4" fill="{col}"/>')
    return "\n".join(out)

def minaret(x, base, h, col, accent):
    out = [f'<path d="M{x-30},{base} L{x-20},{base-h} L{x+20},{base-h} L{x+30},{base} Z" fill="{col}"/>']
    for k in (0.3, 0.55, 0.8):
        out.append(f'<rect x="{x-27+k*8}" y="{base-h*k}" width="{54-k*16}" height="9" fill="{accent}" opacity="0.8"/>')
    out.append(f'<rect x="{x-34}" y="{base-h-18}" width="68" height="20" rx="6" fill="{col}"/>')
    out.append(f'<rect x="{x-24}" y="{base-h-62}" width="48" height="46" fill="{col}"/>')
    out.append(f'<path d="M{x-28},{base-h-60} Q{x},{base-h-118} {x+28},{base-h-60} Z" fill="{accent}"/>')
    out.append(f'<rect x="{x-3}" y="{base-h-140}" width="6" height="26" fill="{col}"/>')
    return "\n".join(out)

def hotel_uzbekistan(x0, base, w, h, col, light):
    """The brutalist Hotel Uzbekistan slab with its lattice facade."""
    out = [f'<path d="M{x0},{base} L{x0},{base-h} Q{x0+w/2},{base-h-26} {x0+w},{base-h} L{x0+w},{base} Z" fill="{col}"/>']
    cols, rows = 7, 9
    for r in range(rows):
        for c in range(cols):
            px = x0 + 14 + c*(w-28)/cols
            py = base - h + 30 + r*(h-60)/rows
            cw, ch = (w-28)/cols - 8, (h-60)/rows - 10
            out.append(f'<path d="M{px},{py+ch} L{px},{py+ch*0.35} Q{px+cw/2},{py-ch*0.15} {px+cw},{py+ch*0.35} L{px+cw},{py+ch} Z" fill="{light}" opacity="0.32"/>')
    return "\n".join(out)

def towers(col, light):
    """Tashkent City modern towers (background)."""
    spec = [(1250, 300, 120, 0), (1385, 380, 110, 1), (1505, 270, 95, 0), (1610, 330, 105, 2)]
    out = []
    for x, h, w, kind in spec:
        base = 1560
        if kind == 1:   # slanted top
            out.append(f'<path d="M{x},{base} L{x},{base-h+40} L{x+w},{base-h} L{x+w},{base} Z" fill="{col}"/>')
        elif kind == 2: # rounded top
            out.append(f'<path d="M{x},{base} L{x},{base-h+w/2} Q{x+w/2},{base-h-w*0.15} {x+w},{base-h+w/2} L{x+w},{base} Z" fill="{col}"/>')
        else:
            out.append(f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" fill="{col}"/>')
        for yy in range(int(base-h+60), base-20, 36):
            out.append(f'<rect x="{x+12}" y="{yy}" width="{w-24}" height="7" fill="{light}" opacity="0.35"/>')
    return "\n".join(out)

def chinar(cx, cy, r, c1, c2, trunk):
    """Autumn chinar (plane) tree — Tashkent's street tree, in Haven's autumn style."""
    out = [f'<path d="M{cx-14},{cy+r*1.55} L{cx-8},{cy+r*0.2} L{cx+8},{cy+r*0.2} L{cx+14},{cy+r*1.55} Z" fill="{trunk}"/>']
    blobs = [(-0.55, 0.25, 0.62), (0.55, 0.22, 0.6), (0, -0.25, 0.72), (-0.3, -0.55, 0.5), (0.35, -0.5, 0.52), (0, 0.35, 0.6)]
    for bx, by, br in blobs:
        out.append(f'<circle cx="{cx+bx*r}" cy="{cy+by*r}" r="{br*r}" fill="{c1}"/>')
    for bx, by, br in [(-0.25, -0.35, 0.32), (0.3, -0.15, 0.28), (-0.5, 0.15, 0.22)]:
        out.append(f'<circle cx="{cx+bx*r}" cy="{cy+by*r}" r="{br*r}" fill="{c2}" opacity="0.9"/>')
    return "\n".join(out)

def leaf(x, y, s, rot, col):
    return (f'<path transform="translate({x} {y}) rotate({rot}) scale({s})" '
            f'd="M0,-40 C26,-24 26,22 0,40 C-26,22 -26,-24 0,-40 Z" fill="{col}"/>'
            f'<path transform="translate({x} {y}) rotate({rot}) scale({s})" d="M0,-34 L0,34" stroke="{UMBER}" stroke-width="3" opacity="0.35"/>')

def doppi():
    """Chust doppi skullcap for Daven, drawn in his sketchy outline style.
    Coordinates are in Daven's own image space (641x728)."""
    ol = "#A9502F"; ink = "#2B2321"
    out = ['<g transform="rotate(-7 310 170)">']
    body = "M192,240 C188,172 200,122 226,100 C272,82 352,80 396,96 C420,118 432,170 428,234 C352,214 270,216 192,240 Z"
    out.append(f'<path d="{body}" fill="{ink}" stroke="{ol}" stroke-width="16" stroke-linejoin="round"/>')
    # seams at the cap's four corners (white stitched lines)
    out.append(f'<path d="M244,94 C252,140 258,186 262,222" stroke="{CREAM}" stroke-width="4" fill="none" stroke-dasharray="7 6"/>')
    out.append(f'<path d="M378,92 C370,138 364,184 362,216" stroke="{CREAM}" stroke-width="4" fill="none" stroke-dasharray="7 6"/>')
    def pepper(x, y, rot, sx=1.0, sy=1.0):
        # qalampir (chili-pepper / almond) motif with a curled tip
        return (f'<path transform="translate({x} {y}) rotate({rot}) scale({sx} {sy})" '
                f'd="M-4,34 C-30,22 -34,-10 -14,-30 C-6,-38 6,-44 10,-52 C14,-40 12,-30 8,-24 C26,-12 26,18 8,32 C4,35 0,36 -4,34 Z" fill="{CREAM}"/>'
                f'<path transform="translate({x} {y}) rotate({rot}) scale({sx} {sy})" d="M-2,24 C-14,14 -14,-6 -4,-16" stroke="{ink}" stroke-width="4" fill="none"/>')
    out.append(pepper(312, 162, 8, 1.15, 1.1))          # front face — the big one
    out.append(pepper(220, 176, -10, 0.45, 0.9))        # side faces, foreshortened
    out.append(pepper(404, 168, 14, 0.45, 0.9))
    # scalloped arch band along the brim
    x = 200
    while x < 420:
        y = 236 - (x-200)*0.022
        out.append(f'<path d="M{x},{y} q10,-14 20,0" stroke="{CREAM}" stroke-width="5" fill="none"/>')
        x += 20
    out.append('</g>')
    return "\n".join(out)

def build(v, show_guide=False):
    c = variant_colors(v)
    font_d = (A / "DarumadropOne-Regular.ttf").as_uri()
    sky = f'''<radialGradient id="sky" cx="0.5" cy="0.74" r="0.75">
        <stop offset="0" stop-color="{c['sky_glow']}"/>
        <stop offset="0.38" stop-color="{c['sky_mid']}"/>
        <stop offset="1" stop-color="{c['sky_top']}"/></radialGradient>'''
    sun = f'<circle cx="1024" cy="1500" r="430" fill="{BANANA}" opacity="0.55"/>'

    stars = "".join([star8(330, 1020, 22, CREAM, 0.7), star8(1760, 980, 26, CREAM, 0.7),
                     star8(1650, 1180, 14, CREAM, 0.6), star8(420, 1230, 14, CREAM, 0.55)])

    back = (f'<g opacity="{c["back_op"]}">' + hotel_uzbekistan(470, 1560, 300, 420, c["back"], CREAM)
            + towers(c["back"], CREAM) + '</g>')

    TURQ = "#2E9C9A"
    front = (tv_tower(330, 1580, 760, UMBER, PUMPKIN)
             + madrasa(860, 1580, 520, 300, UMBER, TURQ, CREAM)
                          + dome(700, 1580, 230, 150, TURQ, ribs=8, rib_col=UMBER)  # Chorsu-style dome
             + f'<rect x="575" y="1548" width="250" height="34" fill="{UMBER}"/>')

    ground = (f'<path d="M0,1600 C300,1545 620,1580 1024,1560 C1400,1545 1750,1580 2048,1555 L2048,2048 L0,2048 Z" fill="{LIME}"/>'
              f'<path d="M0,1700 C350,1660 700,1720 1100,1690 C1500,1660 1800,1710 2048,1680 L2048,2048 L0,2048 Z" fill="{LUCKY}" opacity="0.55"/>')
    path = (f'<path d="M760,2048 C820,1900 700,1800 880,1720 C1000,1668 1060,1640 1010,1592 L1090,1592 C1150,1640 1110,1690 1000,1740 C860,1810 980,1920 960,2048 Z" fill="{BANANA}" opacity="0.85"/>'
            f'<path d="M800,2048 C850,1910 760,1810 900,1740" stroke="{FADED}" stroke-width="8" fill="none" opacity="0.6"/>')
    trees = (chinar(250, 1520, 120, CARROT, BANANA, UMBER) + chinar(470, 1600, 95, PUMPKIN, "#FDA23F", UMBER)
             + chinar(1830, 1530, 110, PUMPKIN, BANANA, UMBER))
    leaves = (leaf(250, 830, 0.9, -30, LIME) + leaf(1820, 720, 1.0, 35, BANANA)
              + leaf(560, 1880, 1.1, 60, CARROT) + leaf(420, 1760, 0.9, -15, PUMPKIN) + leaf(1240, 1960, 0.8, 40, BANANA) + leaf(1700, 1460, 0.8, -50, LIME) + leaf(170, 1320, 0.75, 20, BANANA))

    # official white logo (must keep the Hack Club mark)
    lw = 1280; lh = lw * 491 / 762
    logo = (f'<image href="data:image/png;base64,{b64("haven-logo.png")}" x="{1024-lw/2+20}" y="{230}" width="{lw}" height="{lh}" filter="url(#lshadow)"/>')

    # Daven in a doppi, thumbs up — bottom right, inside the circle crop
    ds = 0.82; dx, dy = 1140, 1300
    daven = (f'<g transform="translate({dx} {dy}) scale({ds})" filter="url(#sticker)">'
             f'<image href="data:image/png;base64,{b64("sketchy-daven.png")}" x="0" y="0" width="641" height="728"/>'
             + doppi() + '</g>')

    city = (f'<text x="1024" y="1095" text-anchor="middle" font-family="Daru" font-size="220" '
            f'fill="#fff" stroke="{UMBER}" stroke-width="34" stroke-linejoin="round" paint-order="stroke" letter-spacing="6">Tashkent</text>')

    guide = ('<circle cx="1024" cy="1024" r="1024" fill="none" stroke="red" stroke-width="6"/>' if show_guide else '')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">
    <defs>{sky}
      <filter id="lshadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="14" stdDeviation="10" flood-color="{UMBER}" flood-opacity="0.55"/></filter>
      <filter id="sticker" x="-15%" y="-15%" width="130%" height="130%">
        <feMorphology in="SourceAlpha" operator="dilate" radius="14" result="d"/>
        <feFlood flood-color="#ffffff"/><feComposite in2="d" operator="in" result="w"/>
        <feDropShadow in="w" dx="0" dy="10" stdDeviation="8" flood-color="{UMBER}" flood-opacity="0.4" result="ws"/>
        <feMerge><feMergeNode in="ws"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      <filter id="dshadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="10" stdDeviation="8" flood-color="{UMBER}" flood-opacity="0.35"/></filter>
    </defs>
    <rect width="{S}" height="{S}" fill="url(#sky)"/>
    {sun}{stars}{back}{front}{ground}{path}{trees}{leaves}{logo}{city}{daven}{guide}
    </svg>'''
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
      @font-face {{ font-family: Daru; src: url("{font_d}"); }}
      html,body {{ margin:0; padding:0; background:#000; }}
    </style></head><body>{svg}</body></html>'''

if __name__ == "__main__":
    out = HERE / "out"; out.mkdir(exist_ok=True)
    variants = sys.argv[1:] or ["orange", "green"]
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": S, "height": S})
        for v in variants:
            for g in (False, True):
                html = out / f"_{v}.html"; html.write_text(build(v, g))
                pg.goto(html.as_uri()); pg.wait_for_timeout(400)
                pg.evaluate("document.fonts.ready")
                pg.screenshot(path=str(out / f"master-{v}{'-guide' if g else ''}.png"),
                              clip={"x": 0, "y": 0, "width": S, "height": S})
        b.close()
