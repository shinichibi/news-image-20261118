#!/usr/bin/env python3
"""Draw the entry image: a broadsheet front page summing up the world news of
Wednesday 18 November 2026, saved as entry.png (1024x1024) beside this file.

Everything is drawn with PIL primitives -- no external images -- so the page
is fully reproducible from this script alone.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 231)
INK = (22, 20, 18)
RED = (163, 22, 33)
DARKRED = (128, 16, 26)
GREY = (92, 86, 78)
RULE = (40, 38, 34)
FAINT = (190, 182, 166)
SEA = (38, 74, 92)
SKY = (216, 208, 188)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- icons
def icon_globe(d, x, y, s):
    d.ellipse([x, y, x + s, y + s], outline=INK, width=3)
    d.ellipse([x + s * 0.32, y, x + s * 0.68, y + s], outline=INK, width=2)
    d.line([x, y + s * 0.5, x + s, y + s * 0.5], fill=INK, width=2)
    d.arc([x, y + s * 0.12, x + s, y + s * 0.55], 0, 180, fill=INK, width=2)
    d.arc([x, y + s * 0.45, x + s, y + s * 0.88], 180, 360, fill=INK, width=2)


def icon_bridge(d, x, y, s):
    deck = y + s * 0.6
    d.line([x, deck, x + s, deck], fill=INK, width=4)
    for tx in (x + s * 0.2, x + s * 0.8):
        d.line([tx, y + s * 0.12, tx, deck], fill=INK, width=4)
        d.line([tx, y + s * 0.12, x + s * 0.5, deck], fill=INK, width=2)
    d.line([x + s * 0.2, y + s * 0.12, x + s * 0.8, y + s * 0.12], fill=INK, width=2)
    d.line([x, y + s * 0.88, x + s, y + s * 0.88], fill=SEA, width=3)
    d.line([x + s * 0.12, y + s * 0.78, x + s * 0.42, y + s * 0.78], fill=SEA, width=2)


def icon_trade(d, x, y, s):
    # two flags facing each other over a baseline
    for fx, col in ((x + s * 0.08, RED), (x + s * 0.58, SEA)):
        d.line([fx, y + s * 0.1, fx, y + s * 0.78], fill=INK, width=3)
        d.polygon([(fx, y + s * 0.1), (fx + s * 0.3, y + s * 0.2),
                   (fx, y + s * 0.32)], fill=col)
    d.line([x + s * 0.1, y + s * 0.88, x + s * 0.9, y + s * 0.88], fill=INK, width=3)


def icon_cyclone(d, x, y, s):
    cx, cy = x + s / 2, y + s / 2
    for r, a0 in ((0.46, 20), (0.34, 150), (0.23, 280)):
        box = [cx - s * r, cy - s * r, cx + s * r, cy + s * r]
        d.arc(box, a0, a0 + 250, fill=SEA, width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)


def icon_rocket(d, x, y, s):
    cx = x + s / 2
    d.polygon([(cx, y + s * 0.05), (cx + s * 0.16, y + s * 0.3),
               (cx + s * 0.16, y + s * 0.62), (cx - s * 0.16, y + s * 0.62),
               (cx - s * 0.16, y + s * 0.3)], outline=INK, width=3)
    d.ellipse([cx - s * 0.07, y + s * 0.3, cx + s * 0.07, y + s * 0.46],
              outline=RED, width=3)
    d.polygon([(cx - s * 0.16, y + s * 0.55), (cx - s * 0.32, y + s * 0.78),
               (cx - s * 0.16, y + s * 0.72)], fill=INK)
    d.polygon([(cx + s * 0.16, y + s * 0.55), (cx + s * 0.32, y + s * 0.78),
               (cx + s * 0.16, y + s * 0.72)], fill=INK)
    d.polygon([(cx - s * 0.08, y + s * 0.66), (cx, y + s * 0.95),
               (cx + s * 0.08, y + s * 0.66)], fill=RED)


def icon_trophy(d, x, y, s):
    d.polygon([(x + s * 0.3, y + s * 0.1), (x + s * 0.7, y + s * 0.1),
               (x + s * 0.66, y + s * 0.44), (x + s * 0.34, y + s * 0.44)],
              outline=INK, width=3)
    d.arc([x + s * 0.1, y + s * 0.12, x + s * 0.33, y + s * 0.4], 90, 270, fill=INK, width=3)
    d.arc([x + s * 0.67, y + s * 0.12, x + s * 0.9, y + s * 0.4], 270, 90, fill=INK, width=3)
    d.rectangle([x + s * 0.45, y + s * 0.44, x + s * 0.55, y + s * 0.64], fill=INK)
    d.rectangle([x + s * 0.3, y + s * 0.64, x + s * 0.7, y + s * 0.76], fill=RED)


def icon_sport(d, x, y, s):
    # cricket bat (long blade, short handle) and ball
    d.polygon([(x + s * 0.34, y + s * 0.3), (x + s * 0.48, y + s * 0.24),
               (x + s * 0.78, y + s * 0.82), (x + s * 0.6, y + s * 0.92),
               (x + s * 0.5, y + s * 0.84)], outline=INK, width=3)
    d.line([x + s * 0.38, y + s * 0.28, x + s * 0.26, y + s * 0.1], fill=INK, width=6)
    d.ellipse([x + s * 0.6, y + s * 0.04, x + s * 0.86, y + s * 0.3], fill=RED)


def icon_columns(d, x, y, s):
    d.polygon([(x + s * 0.5, y + s * 0.06), (x + s * 0.94, y + s * 0.3),
               (x + s * 0.06, y + s * 0.3)], outline=INK, width=3)
    for i in range(3):
        cx = x + s * (0.2 + 0.24 * i)
        d.rectangle([cx, y + s * 0.4, cx + s * 0.1, y + s * 0.78], outline=INK, width=3)
    d.rectangle([x + s * 0.08, y + s * 0.84, x + s * 0.92, y + s * 0.92], fill=INK)


# ---------------------------------------------------------------- panels
PANELS = [
    ("ASIA DIPLOMACY", icon_globe,
     "TRUMP IN MANILA FOR QUAD TALKS",
     "Modi pitches free e-visas at the ASEAN-India summit; bloc adopts an AI plan for small firms."),
    ("UKRAINE WAR", icon_bridge,
     "UKRAINE HITS CRIMEAN BRIDGE AGAIN",
     "Second day of strikes as Russia pounds Kyiv's bridges; UN: 372 civilians died in October."),
    ("TRADE", icon_trade,
     "CANADA & CHINA EXTEND TRADE DEALS",
     "Xi meets PM Carney as both sides widen their pacts ahead of the APEC summit."),
    ("WEATHER", icon_cyclone,
     "CYCLONE AKVAN BEARS DOWN ON INDIA",
     "Andhra and Odisha coasts on high alert; flights cancelled as the storm intensifies."),
    ("SPACE", icon_rocket,
     "SPACEX CATCHES A FALLING STARSHIP",
     "Booster snatched from the sky -- a step toward a fully reusable rocket."),
    ("CULTURE", icon_trophy,
     "RAYE LEADS GRAMMY NOMINATIONS",
     "The 2027 nods land with a bang -- and a surprise snub for Harry Styles."),
    ("SPORT", icon_sport,
     "DHONI CALLS TIME ON THE IPL",
     "Chennai icon retires to mentor CSK; India lift a record 10th SAFF title."),
    ("EUROPE", icon_columns,
     "LATVIA BACKS KULBERGS GOVERNMENT",
     "Parliament approves the new cabinet in a confidence vote in Riga."),
]


def draw_lead_scene(d, x, y, w, h):
    """Flat scene for the lead: a domed capitol under red radar rings at
    left, a US carrier on Gulf water at right, drone marks in the sky."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    base = y + h - 12
    # capitol: steps, body, dome
    dx = x + w * 0.10
    dw = w * 0.17
    d.rectangle([dx - 6, base - 8, dx + dw + 6, base], fill=INK)
    d.rectangle([dx, base - 26, dx + dw, base - 8], fill=INK)
    d.pieslice([dx + dw * 0.14, base - 58, dx + dw * 0.86, base - 12], 180, 360, fill=INK)
    d.rectangle([dx + dw * 0.46, base - 68, dx + dw * 0.54, base - 50], fill=INK)
    # radar rings centred over the dome
    cx, cy = dx + dw / 2, base - 62
    for r in (11, 20, 29):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=2)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
    # sea strip
    d.rectangle([x, base, x + w, y + h], fill=SEA)
    # carrier
    hx, hy = x + w * 0.52, base - 4
    d.polygon([(hx, hy), (hx + w * 0.4, hy), (hx + w * 0.36, hy + 11),
               (hx + w * 0.05, hy + 11)], fill=INK)
    d.rectangle([hx + w * 0.26, hy - 15, hx + w * 0.33, hy], fill=INK)
    d.line([hx + w * 0.295, hy - 26, hx + w * 0.295, hy - 15], fill=INK, width=3)
    # drones
    for fx, fy in ((0.56, 0.18), (0.64, 0.1), (0.72, 0.22)):
        px, py = x + w * fx, y + h * fy
        d.line([px - 7, py, px + 7, py], fill=INK, width=3)
        d.line([px, py - 5, px, py + 5], fill=INK, width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36                      # page margin
    CW = W - 2 * M              # content width
    cx = W / 2

    # strap line
    centered(d, cx, 22, "ALL THE DAY'S NEWS ON ONE PAGE  ·  No. 18  ·  DRAWN BY AN AI AGENT",
             font(SANS_B, 17), GREY)
    d.line([M, 50, W - M, 50], fill=RULE, width=2)

    # masthead
    centered(d, cx, 58, "THE WORLD IN A DAY", font(SERIF_B, 84), INK)
    d.line([M, 150, W - M, 150], fill=RULE, width=5)
    d.line([M, 159, W - M, 159], fill=RULE, width=1)

    # date band
    d.rectangle([M, 168, W - M, 222], fill=DARKRED)
    centered(d, cx, 176, "WEDNESDAY 18 NOVEMBER 2026", font(SANS_B, 39), (255, 255, 255))

    # ---------------- lead story
    y = 236
    d.text((M, y), "MIDDLE EAST — THE LEAD", font=font(SANS_B, 19), fill=RED)
    y += 27
    head_f = font(SERIF_B, 41)
    for line in wrap(d, "TRUMP: IRAN 'DIRTY BOMB' PLOT TAKEN 'VERY SERIOUSLY'", head_f, CW):
        d.text((M, y), line, font=head_f, fill=INK)
        y += 46
    deck_f = font(SERIF, 20)
    deck = ("Bahrain issues, then lifts, a threat all-clear overnight as Kuwait "
            "intercepts drones -- the Gulf on edge, a third US carrier in the region.")
    for line in wrap(d, deck, deck_f, CW):
        d.text((M, y), line, font=deck_f, fill=(52, 48, 44))
        y += 25
    y += 4
    draw_lead_scene(d, M, y, CW, 74)
    y += 74 + 10
    d.line([M, y, W - M, y], fill=RULE, width=2)
    y += 10

    # ---------------- panel grid: 2 columns x 4 rows
    gap = 10
    colgap = 16
    pw = (CW - colgap) // 2
    ph = 108
    pk_f = font(SANS_B, 14)
    ph_f = font(SERIF_B, 23)
    ps_f = font(SANS, 16)
    for i, (kicker, icon, head, summ) in enumerate(PANELS):
        col, row = i % 2, i // 2
        px = M + col * (pw + colgap)
        py = y + row * (ph + gap)
        if col == 1:
            d.line([px - colgap // 2, py + 2, px - colgap // 2, py + ph - 2],
                   fill=FAINT, width=1)
        icon(d, px + 2, py + 24, 58)
        tx = px + 74
        tw = pw - 74
        d.text((tx, py), kicker, font=pk_f, fill=RED)
        hy = py + 19
        for line in wrap(d, head, ph_f, tw)[:2]:
            d.text((tx, hy), line, font=ph_f, fill=INK)
            hy += 26
        for line in wrap(d, summ, ps_f, tw)[:2]:
            d.text((tx, hy), line, font=ps_f, fill=(52, 48, 44))
            hy += 19
        if row < 3:
            ry = py + ph + gap // 2
            d.line([px, ry, px + pw, ry], fill=FAINT, width=1)
    y += 4 * ph + 3 * gap + 8
    d.line([M, y, W - M, y], fill=RULE, width=2)
    y += 7

    # ---------------- in brief footer
    brief_f = font(SANS, 16)
    brief = ("IN BRIEF  ·  Board of Peace warns Gaza's ceasefire could collapse without urgent action  ·  "
             "New York: Asif Merchant gets 27.5 years over a plot to assassinate US officials")
    for line in wrap(d, brief, brief_f, CW):
        d.text((M, y), line, font=brief_f, fill=(52, 48, 44))
        y += 20

    img.save("entry.png", optimize=True)
    print("wrote entry.png, content ends at y =", y)


if __name__ == "__main__":
    main()
