"""Haven Tashkent YouTube banner (2560x1440), same hand-built vector scene as the pfp."""
import sys, pathlib
from playwright.sync_api import sync_playwright
from build import (A, b64, LIME, CARROT, BANANA, PUMPKIN, FADED, UMBER, LUCKY, CREAM,
                   star8, tv_tower, dome, madrasa, minaret, hotel_uzbekistan, chinar, leaf, doppi)

HERE = pathlib.Path(__file__).parent
W, H = 2560, 1440
SAFE = (507, 508, 2053, 931)          # YouTube safe area (1546x423)
HZ = 880                               # horizon line, inside the desktop-visible band
TURQ = "#2E9C9A"

def towers_at(spec, col, light, base=HZ):
    out = []
    for x, h, w, kind in spec:
        if kind == 1:
            out.append(f'<path d="M{x},{base} L{x},{base-h+40} L{x+w},{base-h} L{x+w},{base} Z" fill="{col}"/>')
        elif kind == 2:
            out.append(f'<path d="M{x},{base} L{x},{base-h+w/2} Q{x+w/2},{base-h-w*0.15} {x+w},{base-h+w/2} L{x+w},{base} Z" fill="{col}"/>')
        else:
            out.append(f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" fill="{col}"/>')
        for yy in range(int(base-h+50), base-16, 32):
            out.append(f'<rect x="{x+10}" y="{yy}" width="{w-20}" height="6" fill="{light}" opacity="0.35"/>')
    return "\n".join(out)

def chip(x, y, text, fill, fg, w):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="62" rx="31" fill="{fill}" stroke="{UMBER}" stroke-width="5"/>'
            f'<text x="{x+w/2}" y="{y+43}" text-anchor="middle" font-family="Jua" font-size="36" fill="{fg}">{text}</text>')

def build(show_guide=False):
    fd = (A / "DarumadropOne-Regular.ttf").as_uri(); fj = (A / "Jua-Regular.ttf").as_uri()
    sky = f'''<radialGradient id="sky" cx="0.5" cy="0.62" r="0.62" gradientTransform="translate(0.5 0.62) scale(1 1.25) translate(-0.5 -0.62)">
        <stop offset="0" stop-color="{BANANA}"/><stop offset="0.35" stop-color="#FDA23F"/><stop offset="1" stop-color="{CARROT}"/></radialGradient>'''
    sun = f'<circle cx="1280" cy="{HZ}" r="420" fill="{BANANA}" opacity="0.5"/>'

    stars = "".join(star8(x, y, r, CREAM, o) for x, y, r, o in
                    [(260, 380, 26, .7), (700, 300, 18, .6), (1500, 250, 22, .6), (2050, 330, 28, .7),
                     (2350, 520, 18, .6), (420, 640, 16, .55), (1980, 560, 14, .55), (1180, 430, 14, .5)])

    # background layer: Hotel Uzbekistan + Tashkent City, kept low behind the text
    back = (f'<g opacity="0.85">'
            + hotel_uzbekistan(40, HZ, 230, 330, FADED, CREAM)
            + towers_at([(1150, 190, 90, 0), (1255, 250, 85, 1), (1355, 175, 80, 0), (1450, 215, 85, 2),
                         (1550, 160, 75, 0)], FADED, CREAM)
            + hotel_uzbekistan(2250, HZ, 200, 280, FADED, CREAM)
            + '</g>')

    # foreground landmarks — outside/edges of the safe area so text stays clean
    front = (tv_tower(450, HZ + 20, 300, UMBER, PUMPKIN)
             + dome(250, HZ + 20, 200, 130, TURQ, ribs=8, rib_col=UMBER)
             + f'<rect x="140" y="{HZ-8}" width="220" height="30" fill="{UMBER}"/>'
             + madrasa(2090, HZ + 20, 360, 210, UMBER, TURQ, CREAM)
             + minaret(2500, HZ + 20, 220, UMBER, TURQ))

    ground = (f'<path d="M0,{HZ+30} C400,{HZ-10} 800,{HZ+40} 1280,{HZ+15} C1750,{HZ-10} 2150,{HZ+35} 2560,{HZ+5} L2560,{H} L0,{H} Z" fill="{LIME}"/>'
              f'<path d="M0,{HZ+170} C450,{HZ+120} 900,{HZ+200} 1400,{HZ+160} C1900,{HZ+120} 2250,{HZ+190} 2560,{HZ+150} L2560,{H} L0,{H} Z" fill="{LUCKY}" opacity="0.55"/>')
    path = (f'<path d="M1180,{H} C1240,1300 1120,1180 1300,1080 C1420,1010 1480,960 1420,{HZ+18} L1500,{HZ+18} C1570,960 1530,1030 1410,1100 C1270,1180 1400,1300 1380,{H} Z" fill="{BANANA}" opacity="0.85"/>')
    trees = (chinar(40, HZ - 70, 110, CARROT, BANANA, UMBER) + chinar(330, HZ + 220, 130, CARROT, BANANA, UMBER)
             + chinar(2300, HZ + 250, 140, PUMPKIN, "#FDA23F", UMBER) + chinar(900, HZ + 330, 95, PUMPKIN, BANANA, UMBER)
             + chinar(1850, HZ + 360, 105, CARROT, BANANA, UMBER))
    leaves = (leaf(140, 560, 1.0, -30, LIME) + leaf(980, 200, 0.9, 25, BANANA) + leaf(1700, 420, 0.8, -40, LIME)
              + leaf(2450, 250, 1.0, 35, BANANA) + leaf(620, 1240, 1.1, 60, CARROT) + leaf(1650, 1250, 0.9, -20, PUMPKIN)
              + leaf(2050, 1050, 0.8, 40, BANANA) + leaf(1000, 1050, 0.9, -50, LIME))

    # --- safe-area content ---
    lh = 300; lw = lh * 762 / 491
    logo = (f'<image href="data:image/png;base64,{b64("haven-logo.png")}" x="545" y="540" '
            f'width="{lw}" height="{lh}" filter="url(#lshadow)"/>')
    tx = 1045
    text = (f'<text x="{tx}" y="690" font-family="Daru" font-size="150" fill="#fff" stroke="{UMBER}" stroke-width="30" '
            f'stroke-linejoin="round" paint-order="stroke" letter-spacing="5">Tashkent</text>'
            f'<text x="{tx+8}" y="760" font-family="Jua" font-size="44" fill="#fff" stroke="{UMBER}" stroke-width="12" '
            f'stroke-linejoin="round" paint-order="stroke">Two days. One game. Made by you.</text>'
            + chip(tx + 4, 795, "Nov 14–15", BANANA, UMBER, 220)
            + chip(tx + 240, 795, "Ages 13–18", LIME, UMBER, 230)
            + chip(tx + 486, 795, "100% free", CREAM, UMBER, 210))

    ds = 0.46; dx, dy = 1745, 570
    daven = (f'<g transform="translate({dx} {dy}) scale({ds})" filter="url(#sticker)">'
             f'<image href="data:image/png;base64,{b64("sketchy-daven.png")}" x="0" y="0" width="641" height="728"/>'
             + doppi() + '</g>')

    guide = ''
    if show_guide:
        x0, y0, x1, y1 = SAFE
        guide = (f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="none" stroke="red" stroke-width="5"/>'
                 f'<rect x="0" y="{y0}" width="{W}" height="{y1-y0}" fill="none" stroke="blue" stroke-width="4" stroke-dasharray="20 12"/>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
    <defs>{sky}
      <filter id="lshadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="10" stdDeviation="8" flood-color="{UMBER}" flood-opacity="0.55"/></filter>
      <filter id="sticker" x="-15%" y="-15%" width="130%" height="130%">
        <feMorphology in="SourceAlpha" operator="dilate" radius="14" result="d"/>
        <feFlood flood-color="#ffffff"/><feComposite in2="d" operator="in" result="w"/>
        <feDropShadow in="w" dx="0" dy="10" stdDeviation="8" flood-color="{UMBER}" flood-opacity="0.4" result="ws"/>
        <feMerge><feMergeNode in="ws"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    </defs>
    <rect width="{W}" height="{H}" fill="url(#sky)"/>
    {sun}{stars}{back}{front}{ground}{path}{trees}{leaves}{logo}{text}{daven}{guide}
    </svg>'''
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
      @font-face {{ font-family: Daru; src: url("{fd}"); }}
      @font-face {{ font-family: Jua; src: url("{fj}"); }}
      html,body {{ margin:0; padding:0; }}
    </style></head><body>{svg}</body></html>'''

if __name__ == "__main__":
    out = HERE / "out"; out.mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H})
        for g in (False, True):
            f = out / "_banner.html"; f.write_text(build(g))
            pg.goto(f.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
            pg.screenshot(path=str(out / f"banner{'-guide' if g else ''}.png"), clip={"x": 0, "y": 0, "width": W, "height": H})
        b.close()
