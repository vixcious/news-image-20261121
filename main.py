#!/usr/bin/env python3
"""news-image-20261121 — Saturday 21 November 2026: the world today in 28 stories.

One-page newspaper front page, drawn with PIL only (stdlib). No network, no
randomness: every run produces a byte-identical PNG.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "/output/entry.png"

CREAM = (247, 241, 227)
PAPER = (252, 248, 238)
INK = (26, 26, 26)
RED = (163, 18, 18)
RED_DK = (122, 12, 12)
MUTED = (107, 98, 87)
RULE = (26, 26, 26)
CHIP_BG = (238, 228, 210)
NAVY = (16, 24, 46)
NAVY2 = (30, 44, 78)

FD = "/usr/share/fonts/truetype/dejavu"


def f_serif(size, bold=True):
    return ImageFont.truetype(
        os.path.join(FD, "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"), size)


def f_sans(size, bold=False):
    return ImageFont.truetype(
        os.path.join(FD, "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)


def tw(draw, text, font):
    return draw.textlength(text, font=font)


def trunc(draw, text, font, max_w):
    if tw(draw, text, font) <= max_w:
        return text
    ell = "\u2026"
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if tw(draw, text[:mid] + ell, font) <= max_w:
            lo = mid
        else:
            hi = mid - 1
    return text[:lo] + ell


def wrap2(draw, text, font, max_w):
    """Wrap text into at most 2 lines; truncate the second with an ellipsis."""
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = (cur + " " + word).strip()
        if tw(draw, trial, font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
            if len(lines) == 1:
                break
    if len(lines) < 2 and cur:
        lines.append(cur)
    elif len(lines) == 1 and cur:
        lines[0] = trunc(draw, lines[0] + " " + cur, font, max_w)
    if len(lines) > 2:
        lines = lines[:2]
    if len(lines) == 2:
        lines[1] = trunc(draw, lines[1], font, max_w)
    assert len(lines) <= 2
    return lines


# ---------------------------------------------------------------- stories
HERO = {
    "tag": "GULF CRISIS  \u00b7  HERO",
    "head": "IRAN STRIKES BAHRAIN",
    "deck": ("Missiles and drones at US positions: the Guards claim two Patriot "
             "radars hit at al-Riffa and Awali. Bahrain says an industrial site "
             "burned \u2014 and no one was hurt."),
    "chips": [("2", "US bases named"), ("0", "injured in Bahrain"),
              ("1", "tanker hit near Hormuz")],
}

FEATURES = [
    # tag, headline, deck, art kind, art palette
    ("BALTIC SEA", "Russian ship ablaze after drone strike",
     "Sanctioned ship hit at sea; all 16 crew escaped.",
     "ship", ((30, 44, 78), (214, 158, 64))),
    ("UKRAINE", "Triple-tap strike kills a boy, 7, and a paramedic",
     "Restaurant hit; drones then struck rescuers. 60 hurt.",
     "missile", ((26, 26, 26), (163, 18, 18))),
    ("MEXICO", "\u2018El Chapo Isidro\u2019 captured; 11 dead in Sinaloa",
     "Most-wanted boss seized in Guasave; 4 soldiers dead.",
     "raid", ((58, 44, 30), (214, 158, 64))),
    ("CLIMATE", "COP31 close to a final deal at last",
     "Past deadline, the summit nears a deal all can accept.",
     "summit", ((30, 74, 52), (214, 158, 64))),
    ("UNITED STATES", "FBI crime database hacked, scope unclear",
     "Fugitive, warrant records at risk. Trump: \u201cnot good.\u201d",
     "lock", ((16, 24, 46), (163, 18, 18))),
    ("DIPLOMACY", "Zelensky: Putin is a killer, not a friend",
     "Trump: \u201cgreat relationship\u201d. Kyiv: \u201che is an enemy.\u201d",
     "talks", ((74, 52, 30), (214, 158, 64))),
    ("HEALTH", "Mosquitoes bred to beat dengue cut cases 69%",
     "Trial in 5,700 children; effect held in 2024 outbreak.",
     "mosquito", ((30, 74, 52), (26, 26, 26))),
    ("SPACE", "BepiColombo reaches Mercury after 8 years",
     "Twin orbiters fire thrusters, enter Mercury orbit.",
     "space", ((16, 24, 46), (214, 158, 64))),
    ("BRITAIN", "Princess Catherine reveals secret cancer film",
     "Trailer drops: Three Peaks in 24 hours. BBC, 29 Nov.",
     "royal", ((74, 30, 52), (214, 158, 64))),
]

BRIEFS = [
    "Zelensky offers local ceasefires on Dnipro",
    "Gaza: food-vehicle strike kills 3",
    "Houthi missiles at Riyadh intercepted",
    "Basra power-station fire kills 4, hurts 35",
    "Bolsonaro in ICU with bowel obstruction",
    "France sentences 3 officers over Zecler",
    "Cost-of-living protests hit France, Berlin",
    "Virginia child dies of measles, first of 2026",
    "EU, Indonesia sign trade deal",
    "Japan felt \u201cleft out\u201d at Shenzhen summit",
    "England 37\u201312 All Blacks, record margin",
    "Alcaraz beats Shelton, faces Zverev",
    "Harden scores 51, passes Kobe",
    "Verstappen on pole in Las Vegas",
    "BTS win five awards at MAMA in Osaka",
    "Tanzania convicts Lissu of sedition",
    "Fighting widens in eastern Congo",
    "CERN finds first evidence of rare decay",
]

# Dotted world map: 64 cols x 32 rows, '#' = land. Coarse equirectangular mask.
LAND = [
    ".................##......##.....................................",
    "............#########...#####...................................",
    "...#####..#############......#################################..",
    "..######.###############....###################################.",
    "...#####.##############.#...###################################.",
    ".....##..#############......##################################..",
    "...........###########..########################################",
    "...........##########...######################################..",
    "...........##########...#####################################...",
    "............#########...####################################....",
    "............########.....##############################.........",
    ".............#######......############################..........",
    "..............####.........##########################...........",
    "...............###..........#########################...........",
    "................####.........######################.............",
    ".................####.........####################..............",
    "....................####.......##################...............",
    "....................#####.......#################...............",
    ".....................####........###############................",
    ".....................#####........##############................",
    "......................####.........#############................",
    "......................####.........############.................",
    "......................###..........###########..................",
    "......................##...........##########...................",
    "......................##........................................",
    "......................##........................................",
    "................................................................",
    "................................................................",
    "................................................................",
    "................................................................",
    "................................................................",
    "................................................................",
]

# (story number, display lon, display lat) — a few pins nudged a few degrees
# so neighbouring pins (London/Brussels, Kyiv/Antalya) stay readable.
PINS = [
    (1, 50.5, 26.2), (2, 21.0, 62.0), (3, 33.4, 47.9), (4, -108.5, 25.6),
    (5, 38.0, 32.0), (6, -77.0, 38.9), (7, 27.0, 53.0), (8, -43.9, -19.9),
    (9, 4.35, 50.85), (10, -5.0, 54.0),
]


def draw_hero_art(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=NAVY)
    # sky bands
    for i in range(6):
        d.rectangle([x0, y0 + i * h // 6, x0 + w, y0 + (i + 1) * h // 6],
                    fill=(NAVY[0] + i * 2, NAVY[1] + i * 3, NAVY[2] + i * 5))
    # fixed stars
    stars = [(18, 14), (64, 26), (120, 10), (180, 30), (240, 12), (300, 24),
             (360, 14), (420, 28), (470, 12), (90, 44), (210, 48), (330, 44)]
    for sx, sy in stars:
        d.ellipse([x0 + sx - 1, y0 + sy - 1, x0 + sx + 1, y0 + sy + 1],
                  fill=(240, 236, 220))
    # missile arcs (red-orange trails)
    d.line([(x0 + 40, y0 + h - 30), (x0 + 150, y0 + 70), (x0 + 250, y0 + 40)],
           fill=(232, 90, 40), width=4)
    d.line([(x0 + 300, y0 + h - 20), (x0 + 380, y0 + 90), (x0 + 460, y0 + 60)],
           fill=(232, 120, 50), width=4)
    for cx, cy, r in [(250, 40, 6), (460, 60, 6)]:
        d.ellipse([x0 + cx - r, y0 + cy - r, x0 + cx + r, y0 + cy + r],
                  fill=(255, 200, 90))
    # fire glow, low behind the skyline, bottom right (stays inside the panel)
    for r in (26, 20, 13, 7):
        d.ellipse([x0 + w - 70 - r, y0 + h - 30 - r, x0 + w - 70 + r,
                   y0 + h - 30 + r], fill=(232 - r, 120 - r // 2, 30))
    # city silhouette
    base = y0 + h
    for bx, bw, bh in [(0, 46, 52), (52, 34, 78), (92, 40, 60), (138, 30, 88),
                       (174, 44, 56), (224, 36, 70), (266, 40, 50),
                       (312, 34, 80), (352, 42, 58), (400, 36, 72),
                       (442, 44, 54), (488, 44, 66)]:
        d.rectangle([x0 + bx, base - bh, x0 + bx + bw, base], fill=(10, 14, 28))
        for wy in range(base - bh + 8, base - 8, 14):
            for wx in range(x0 + bx + 7, x0 + bx + bw - 4, 13):
                d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 205, 110))
    # searchlight beams (narrow)
    d.polygon([(x0 + 120, base - 60), (x0 + 78, y0 + 20), (x0 + 92, y0 + 20)],
              fill=(240, 236, 210))
    d.polygon([(x0 + 380, base - 72), (x0 + 436, y0 + 24), (x0 + 448, y0 + 24)],
              fill=(240, 236, 210))


def draw_tile_art(d, x0, y0, w, h, kind, palette):
    bg, accent = palette
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=bg)
    if kind == "ship":
        d.rectangle([x0, y0 + h - 14, x0 + w, y0 + h], fill=(214, 158, 64))
        d.polygon([(x0 + 20, y0 + h - 14), (x0 + 150, y0 + h - 14),
                   (x0 + 132, y0 + h - 30), (x0 + 38, y0 + h - 30)],
                  fill=(240, 236, 220))
        d.rectangle([x0 + 70, y0 + h - 44, x0 + 82, y0 + h - 30],
                    fill=(240, 236, 220))
        for fx in (170, 196, 222):
            d.polygon([(x0 + fx, y0 + h - 30), (x0 + fx + 14, y0 + h - 30),
                       (x0 + fx + 7, y0 + h - 52)], fill=(232, 90, 40))
    elif kind == "missile":
        d.line([(x0 + 14, y0 + h - 8), (x0 + 120, y0 + 16)], fill=accent, width=4)
        d.line([(x0 + 130, y0 + 14), (x0 + 150, y0 + 10)], fill=(255, 200, 90),
               width=6)
        d.ellipse([x0 + 180, y0 + 8, x0 + 200, y0 + 28], fill=(255, 200, 90))
        d.rectangle([x0 + 220, y0 + h - 26, x0 + 300, y0 + h - 8],
                    fill=(240, 236, 220))
    elif kind == "raid":
        d.rectangle([x0, y0 + h - 12, x0 + w, y0 + h], fill=(26, 26, 26))
        d.ellipse([x0 + 26, y0 + 8, x0 + 66, y0 + 48], fill=(255, 205, 110))
        d.rectangle([x0 + 120, y0 + 12, x0 + 200, y0 + 34], fill=(240, 236, 220))
        d.rectangle([x0 + 220, y0 + 20, x0 + 290, y0 + 40], fill=(163, 18, 18))
    elif kind == "summit":
        for i, cx in enumerate((40, 100, 160, 220, 280)):
            d.ellipse([x0 + cx - 16, y0 + 8 + (i % 2) * 8, x0 + cx + 16,
                       y0 + 40 + (i % 2) * 8],
                      outline=(240, 236, 220), width=3)
        d.rectangle([x0, y0 + h - 10, x0 + w, y0 + h], fill=(214, 158, 64))
    elif kind == "lock":
        d.rectangle([x0 + 120, y0 + 12, x0 + 190, y0 + 44], outline=accent,
                    width=5)
        d.rectangle([x0 + 128, y0 + 24, x0 + 182, y0 + 44], fill=accent)
        d.rectangle([x0 + 150, y0 + 28, x0 + 160, y0 + 40], fill=bg)
        d.line([(x0 + 20, y0 + 30), (x0 + 90, y0 + 30)], fill=(240, 236, 220),
               width=2)
        d.line([(x0 + 230, y0 + 30), (x0 + 300, y0 + 30)], fill=(240, 236, 220),
               width=2)
    elif kind == "talks":
        d.polygon([(x0 + 60, y0 + 10), (x0 + 110, y0 + 10), (x0 + 85, y0 + 44)],
                  fill=(240, 236, 220))
        d.polygon([(x0 + 200, y0 + 10), (x0 + 250, y0 + 10), (x0 + 225, y0 + 44)],
                  fill=(214, 158, 64))
        d.line([(x0 + 85, y0 + 44), (x0 + 225, y0 + 44)], fill=accent, width=3)
    elif kind == "mosquito":
        d.ellipse([x0 + 130, y0 + 10, x0 + 180, y0 + 34], fill=(240, 236, 220))
        d.line([(x0 + 130, y0 + 22), (x0 + 60, y0 + 8)], fill=(240, 236, 220),
               width=2)
        d.line([(x0 + 130, y0 + 22), (x0 + 60, y0 + 36)], fill=(240, 236, 220),
               width=2)
        d.line([(x0 + 180, y0 + 22), (x0 + 250, y0 + 8)], fill=(240, 236, 220),
               width=2)
        d.line([(x0 + 180, y0 + 22), (x0 + 250, y0 + 36)], fill=(240, 236, 220),
               width=2)
        d.ellipse([x0 + 250, y0 + 6, x0 + 290, y0 + 38], outline=(255, 200, 90),
                  width=3)
    elif kind == "space":
        d.ellipse([x0 + 230, y0 + 6, x0 + 296, y0 + 40], fill=(214, 158, 64))
        d.ellipse([x0 + 238, y0 + 12, x0 + 258, y0 + 26], fill=(190, 130, 40))
        d.polygon([(x0 + 40, y0 + 22), (x0 + 120, y0 + 22), (x0 + 80, y0 + 40)],
                  fill=(240, 236, 220))
        d.rectangle([x0 + 70, y0 + 14, x0 + 90, y0 + 22], fill=(240, 236, 220))
    elif kind == "royal":
        d.polygon([(x0 + 120, y0 + 6), (x0 + 150, y0 + 22), (x0 + 180, y0 + 6),
                   (x0 + 168, y0 + 40), (x0 + 132, y0 + 40)],
                  fill=(214, 158, 64))
        d.rectangle([x0 + 220, y0 + 18, x0 + 290, y0 + 36], fill=(240, 236, 220))
        d.rectangle([x0 + 20, y0 + 30, x0 + 90, y0 + 40], fill=(240, 236, 220))


def draw_map(d, x0, y0, w, h):
    # Use mask rows 2..27 (lat ~79 to ~-62); lat range mapped 80..-60.
    # Double the mask horizontally so the dot field reads as a map, not bars.
    rows = ["".join(ch * 2 for ch in row) for row in LAND[2:28]]
    cols = 128
    cw, ch = w / cols, h / len(rows)
    for r, row in enumerate(rows):
        assert len(row) == 128
        for c, ch_ in enumerate(row):
            if ch_ == "#":
                cx, cy = x0 + (c + 0.5) * cw, y0 + (r + 0.5) * ch
                d.ellipse([cx - 1.3, cy - 1.3, cx + 1.3, cy + 1.3],
                          fill=(120, 110, 96))
    for num, lon, lat in PINS:
        px = x0 + (lon + 180) / 360 * w
        py = y0 + (80 - lat) / 140 * h
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=(252, 248, 238), width=2)
        f = f_sans(9, bold=True)
        t = str(num)
        d.text((px - tw(d, t, f) / 2, py - 5), t, font=f, fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # kicker band
    d.rectangle([0, 0, W, 26], fill=RED)
    fk = f_sans(12, bold=True)
    d.text((28, 7), "ONE DAY, THE WHOLE WORLD, ON ONE PAGE", font=fk,
           fill=(255, 255, 255))
    right = "28 STORIES"
    d.text((W - 28 - tw(d, right, fk), 7), right, font=fk, fill=(255, 255, 255))

    # masthead
    fm = f_serif(46, bold=True)
    title = "THE WORLD IN ONE DAY"
    d.text(((W - tw(d, title, fm)) / 2, 34), title, font=fm, fill=INK)
    fd_ = f_sans(15, bold=True)
    date = "S A T U R D A Y   2 1   N O V E M B E R   2 0 2 6"
    d.text(((W - tw(d, date, fd_)) / 2, 88), date, font=fd_, fill=RED)
    d.line([(28, 112), (W - 28, 112)], fill=RULE, width=2)
    d.line([(28, 116), (W - 28, 116)], fill=RULE, width=1)

    # hero
    hx, hy, hw, hh = 28, 126, 532, 200
    draw_hero_art(d, hx, hy, hw, hh)
    tx = hx + hw + 16
    tw_ = W - 28 - tx
    ft = f_sans(11, bold=True)
    d.text((tx, hy + 2), HERO["tag"], font=ft, fill=RED)
    fh = f_serif(27, bold=True)
    head_lines = wrap2(d, HERO["head"], fh, tw_)
    assert len(head_lines) == 1
    d.text((tx, hy + 22), head_lines[0], font=fh, fill=INK)
    fdeck = f_sans(13)
    deck_lines = []
    words = HERO["deck"].split()
    cur = ""
    for word in words:
        trial = (cur + " " + word).strip()
        if tw(d, trial, fdeck) <= tw_:
            cur = trial
        else:
            deck_lines.append(cur)
            cur = word
    deck_lines.append(cur)
    assert len(deck_lines) <= 5, deck_lines
    yy = hy + 60
    for line in deck_lines:
        d.text((tx, yy), line, font=fdeck, fill=(60, 54, 46))
        yy += 17
    # stat chips
    cy = hy + 152
    cw_ = (tw_ - 16) // 3
    for i, (num, label) in enumerate(HERO["chips"]):
        cx = tx + i * (cw_ + 8)
        d.rectangle([cx, cy, cx + cw_, cy + 44], fill=CHIP_BG,
                    outline=(200, 188, 164))
        fn = f_serif(20, bold=True)
        d.text((cx + 8, cy + 3), num, font=fn, fill=RED)
        fl = f_sans(10)
        d.text((cx + 8, cy + 27), trunc(d, label, fl, cw_ - 16), font=fl,
               fill=MUTED)

    # map strip
    my = 338
    fcap = f_sans(11, bold=True)
    d.text((28, my), "WHERE THE DAY HAPPENED", font=fcap, fill=RED)
    d.text((W - 28 - tw(d, "PINS ARE NUMBERED BY STORY", fcap), my),
           "PINS ARE NUMBERED BY STORY", font=fcap, fill=MUTED)
    draw_map(d, 28, my + 18, W - 56, 88)

    # features
    fy = 452
    d.text((28, fy), "THE DAY IN NINE MORE STORIES", font=fcap, fill=RED)
    d.line([(28, fy + 18), (W - 28, fy + 18)], fill=RULE, width=1)
    gy = fy + 26
    t_w, t_h, gap = 317, 114, 8
    for i, (tag, head, deck, kind, palette) in enumerate(FEATURES):
        r_, c_ = divmod(i, 3)
        x0 = 28 + c_ * (t_w + gap)
        y0 = gy + r_ * (t_h + gap)
        d.rectangle([x0, y0, x0 + t_w, y0 + t_h], fill=PAPER,
                    outline=(214, 204, 186))
        draw_tile_art(d, x0 + 1, y0 + 1, t_w - 2, 44, kind, palette)
        d.text((x0 + 8, y0 + 50), tag, font=f_sans(10, bold=True), fill=RED)
        fhh = f_serif(14, bold=True)
        lines = wrap2(d, head, fhh, t_w - 16)
        assert len(lines) <= 2
        ly = y0 + 64
        for line in lines:
            d.text((x0 + 8, ly), line, font=fhh, fill=INK)
            ly += 17
        fdd = f_sans(11)
        shown_deck = trunc(d, deck, fdd, t_w - 16)
        assert shown_deck == deck, shown_deck
        d.text((x0 + 8, y0 + 100), shown_deck, font=fdd, fill=(60, 54, 46))

    # briefs
    by = gy + 3 * t_h + 2 * gap + 12
    d.text((28, by), "IN BRIEF \u2014 18 MORE STORIES", font=fcap, fill=RED)
    d.line([(28, by + 18), (W - 28, by + 18)], fill=RULE, width=1)
    fb = f_sans(12, bold=True)
    bcol_w = t_w
    for i, brief in enumerate(BRIEFS):
        c_, r_ = divmod(i, 6)
        x0 = 28 + c_ * (bcol_w + gap)
        y0 = by + 26 + r_ * 16
        num = "%d." % (i + 11)
        d.text((x0, y0), num, font=fb, fill=RED)
        nx = x0 + tw(d, num + " ", fb)
        shown = trunc(d, brief, fb, bcol_w - (nx - x0))
        assert shown == brief, shown
        d.text((nx, y0), shown, font=fb, fill=INK)

    # footer
    foy = by + 26 + 6 * 16 + 8
    d.line([(28, foy), (W - 28, foy)], fill=RULE, width=1)
    ff = f_sans(10)
    foot = [
        "Reported Saturday 21 November 2026. Claims by governments and armed groups are labelled as claims; "
        "unverified figures are not stated as fact.",
        "Sources: Reuters, AP, CNN, ISW, ESA, Xinhua, BBC, USA Today. "
        "All artwork is original illustration, drawn for this page.",
    ]
    yy = foy + 6
    for line in foot:
        d.text((28, yy), trunc(d, line, ff, W - 56), font=ff, fill=MUTED)
        yy += 13

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG")
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
