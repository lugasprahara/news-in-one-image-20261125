#!/usr/bin/env python3
"""Render entry.png — the world news of Wednesday 25 November 2026 in one image.

Standing format (approved by lugas): 1024x1024, teal / coral / paper palette,
date huge at top-left, coral story-count block, one wide hero panel, story
panels with short briefs, a dark world map with numbered location dots, and a
sources footer. All stories verified against the sources named in the footer
on the morning of 25 Nov 2026 (WIB).
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 240, 226)
CARD = (255, 253, 246)
INK = (25, 25, 22)
TEAL = (14, 95, 92)
TEAL_DARK = (8, 59, 60)
CORAL = (255, 107, 87)
CORAL_DARK = (214, 69, 44)
LINE = (216, 207, 187)
MAP_BG = (13, 43, 51)
MAP_LAND = (64, 145, 140)
GREY = (70, 66, 58)

SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
CHUNK = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
OUT = "/home/hatch/workspace/makefun-wave4/news25/repo/entry.png"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, width, leading):
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ------------------------------------------------------------------ stories
HERO = {
    "kicker": "NEW YORK · TECH, TRADE & LAW",
    "headline": "HUAWEI CONVICTED IN U.S. CRIMINAL TRIAL",
    "brief": ("A Brooklyn jury convicted the Chinese tech giant on 10 of 12 counts — stealing "
              "trade secrets, bank fraud and hiding its Iran business. Cleared of racketeering, "
              "it still faces billions of dollars in penalties when sentenced in September 2027."),
}

# (number, kicker, headline, brief)
PANELS = [
    ("1", "CHINA · SPACE", "SHENZHOU-24 LIFTS OFF WITH FIRST FOREIGN ASTRONAUT",
     "China's crewed ship rose Wednesday with three astronauts — one the first foreign crew member — bound for the Tiangong station."),
    ("2", "PACIFIC · DIPLOMACY", "AUSTRALIA SIGNS SECURITY PACT WITH SOLOMON ISLANDS",
     "Canberra becomes Honiara's defence partner of choice, as the islands' earlier Beijing deal is reported scrapped."),
    ("3", "UKRAINE · WAR AT SEA", "KYIV HITS RUSSIAN SHIPS IN TWO SEAS",
     "Zelenskyy confirmed the Gulf of Finland drone strike; a Russian warship was also sunk in Benghazi harbour, Libya."),
    ("4", "YEMEN · GULF", "DRONE STRIKES RIYADH TOWER, 11 WOUNDED",
     "Saudi officials say a Houthi drone hit the capital's tallest tower. Britain sanctioned the group and four officials."),
    ("5", "FRANCE · JUSTICE", "SARKOZY ORDERED TO TRIAL OVER LIBYA CASE",
     "Judges sent the ex-president and Carla Bruni to trial over alleged Libyan funding of his 2007 campaign."),
    ("6", "UNITED STATES · TRADE", "WASHINGTON READIES NEW TARIFFS ON PARTNERS",
     "Washington is preparing fresh levies on many of its biggest trading partners, China and the EU among them."),
    ("7", "FOOTBALL · EUROPE", "REAL MADRID ROUT PSV 5-1 IN CHAMPIONS LEAGUE",
     "Mbappé scored twice and Bellingham hit a stunner as Madrid came from behind to overwhelm PSV Eindhoven."),
    ("8", "SOUTH KOREA · SEOUL", "METRO STRIKE CALLED OFF AT THE LAST MINUTE",
     "Seoul Metro and its unions reached a wage deal on Wednesday, averting a general strike on the subway."),
    ("9", "COLOMBIA · CARTAGENA", "GUNMEN HOLD DOZENS HOSTAGE IN SUPERMARKET",
     "Armed men seized shoppers after a botched armoured-car robbery; police surrounded the store."),
    ("10", "BUSINESS · TECH", "DELL LIFTS FORECAST ON AI SERVER BOOM",
     "A record quarter, driven by surging demand for AI servers, pushed Dell to raise its annual forecasts."),
]

BRIEFS = [
    "Iraq orders seizure of Kurdish oilfields",
    "CIA & ODNI breached — unclassified data hit",
    "Trump gives Giuliani the Medal of Freedom",
    "Trump pardons turkeys Freedom & Feathers",
    "Senegal's AFCON title restored by CAS",
    "Xiamen Airlines to buy 50 Boeing 737-8s",
    "Iran's medicine shortage deepens — DW",
    "Colombia car bomb injures at least 23",
    "Shortwave lessons for Afghan girls return",
    "Seoul shares slide on U.S. tech losses",
    "Fort Hood gunman seeks stay of execution",
    "Study: 700,000 Russian dead in Ukraine",
]

SOURCES = ("Sources: Reuters · AP · U.S. Dept. of Justice · BBC · SCMP · Korea Times · "
           "Yonhap · DW · RFE/RL — as reported on 25 November 2026")

# map markers: (label, lon, lat) — numbers match the panels; the star is the hero
MARKERS = [
    ("*", -74.0, 40.7), ("1", 100.0, 41.0), ("2", 159.9, -9.4),
    ("3", 26.0, 60.0), ("3", 20.1, 32.1), ("4", 46.7, 24.6),
    ("5", 2.35, 48.9), ("6", -77.0, 38.9), ("7", -3.7, 40.4),
    ("8", 127.0, 37.6), ("9", -75.5, 10.4), ("10", -97.7, 30.3),
]

# blobby continents as (lon, lat, rx, ry) ellipses for the dot-matrix map
LAND = [
    (-102, 46, 30, 13), (-152, 65, 10, 5), (-85, 38, 14, 8), (-42, 72, 11, 6),
    (-86, 13, 8, 3), (-95, 22, 8, 5),
    (-61, -12, 11, 16), (-70, -32, 5, 10),
    (20, 6, 15, 20), (25, -18, 10, 10), (47, -19, 3, 6),
    (12, 49, 15, 7), (20, 55, 12, 6), (16, 63, 9, 6), (-4, 40, 6, 4), (-2, 53, 3, 4),
    (45, 27, 10, 7), (88, 50, 40, 13), (60, 55, 18, 9), (78, 22, 7, 8),
    (101, 16, 6, 8), (108, 32, 13, 9), (127, 37, 4, 3), (138, 37, 4, 5),
    (113, -1, 13, 3), (140, -4, 6, 3),
    (134, -25, 12, 7), (172, -42, 3, 4),
]


def on_land(lon, lat):
    return any(((lon - cx) / rx) ** 2 + ((lat - cy) / ry) ** 2 <= 1.0
               for cx, cy, rx, ry in LAND)


def draw_map(draw, x0, y0, x1, y1):
    draw.rounded_rectangle([x0, y0, x1, y1], 10, fill=MAP_BG)
    draw.text((x0 + 14, y0 + 7), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=(180, 220, 214))
    lon_min, lon_max, lat_max, lat_min = -168, 192, 84, -58
    mx0, my0, mx1, my1 = x0 + 10, y0 + 27, x1 - 10, y1 - 6

    def px(lon):
        return mx0 + (lon - lon_min) / (lon_max - lon_min) * (mx1 - mx0)

    def py(lat):
        return my0 + (lat_max - lat) / (lat_max - lat_min) * (my1 - my0)

    lat = lat_max
    while lat >= lat_min:
        lon = lon_min
        while lon <= lon_max:
            if on_land(lon, lat):
                draw.ellipse([px(lon) - 1.8, py(lat) - 1.8, px(lon) + 1.8, py(lat) + 1.8], fill=MAP_LAND)
            lon += 3.4
        lat -= 3.4
    for label, lon, lat in MARKERS:
        cx, cy = px(lon), py(lat)
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=CORAL, outline=(255, 255, 255), width=1)
        f = font(SANS_B, 10 if len(label) > 1 else 11)
        w_ = draw.textlength(label, font=f)
        draw.text((cx - w_ / 2, cy - 6), label, font=f, fill=(255, 255, 255))


def panel(draw, x, y, w_, h, num, kicker, headline, brief):
    draw.rounded_rectangle([x, y, x + w_, y + h], 8, fill=CARD, outline=LINE, width=1)
    draw.ellipse([x + 10, y + 9, x + 31, y + 30], fill=CORAL)
    f = font(SANS_B, 11 if len(num) > 1 else 12)
    draw.text((x + 20.5 - draw.textlength(num, font=f) / 2, y + 13), num, font=f, fill=(255, 255, 255))
    draw.text((x + 40, y + 12), kicker, font=font(SANS_B, 11), fill=TEAL)
    text_block(draw, x + 12, y + 36, headline, font(SANS_B, 17), INK, w_ - 24, 19)
    text_block(draw, x + 12, y + 76, brief, font(SANS, 13), GREY, w_ - 24, 14)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28

    # ------------------------------------------------------------- header
    d.text((M, 14), "THE WORLD IN ONE IMAGE", font=font(SANS_B, 15), fill=TEAL)
    tag = "DAILY NEWS POSTER · MAKE.FUN"
    d.text((W - M - d.textlength(tag, font=font(SANS_B, 15)), 14), tag, font=font(SANS_B, 15), fill=TEAL)
    d.text((M - 4, 32), "25", font=font(CHUNK, 104), fill=INK)
    d.text((M + 148, 42), "NOVEMBER 2026", font=font(SANS_B, 45), fill=INK)
    d.text((M + 150, 98), "W E D N E S D A Y", font=font(SANS_B, 27), fill=CORAL_DARK)
    bx0, by0, bx1, by1 = 796, 34, W - M, 146
    d.rounded_rectangle([bx0, by0, bx1, by1], 10, fill=CORAL)
    d.text((bx0 + 14, by0 + 12), "23", font=font(CHUNK, 48), fill=(255, 255, 255))
    d.text((bx0 + 92, by0 + 22), "STORIES", font=font(SANS_B, 20), fill=(255, 255, 255))
    d.text((bx0 + 92, by0 + 50), "ONE DAY", font=font(SANS_B, 13), fill=(255, 255, 255))
    d.text((bx0 + 14, by1 - 24), "SIX CONTINENTS · ONE IMAGE", font=font(SANS_B, 11), fill=(255, 255, 255))
    d.line([M, 156, W - M, 156], fill=INK, width=2)

    # ------------------------------------------------------------- hero
    hy0, hy1 = 166, 366
    d.rounded_rectangle([M, hy0, W - M, hy1], 10, fill=TEAL_DARK)
    d.ellipse([M + 16, hy0 + 15, M + 43, hy0 + 42], fill=CORAL)
    fs = font(SANS_B, 16)
    d.text((M + 29.5 - d.textlength("*", font=fs) / 2, hy0 + 20), "*", font=fs, fill=(255, 255, 255))
    d.text((M + 54, hy0 + 19), HERO["kicker"], font=font(SANS_B, 15), fill=CORAL)
    text_block(d, M + 24, hy0 + 46, HERO["headline"], font(SERIF_B, 41), (255, 255, 255), W - 2 * M - 48, 46)
    text_block(d, M + 24, hy0 + 134, HERO["brief"], font(SANS, 17), (226, 238, 232), W - 2 * M - 48, 22)

    # ------------------------------------------------------------- panel rows
    cw = (W - 2 * M - 2 * 12) // 3  # 314
    for i, p in enumerate(PANELS[0:3]):
        panel(d, M + i * (cw + 12), 376, cw, 120, *p)
    draw_map(d, M, 506, M + 640, 626)
    panel(d, M + 652, 506, W - M - (M + 652), 120, *PANELS[3])
    for i, p in enumerate(PANELS[4:7]):
        panel(d, M + i * (cw + 12), 636, cw, 120, *p)
    for i, p in enumerate(PANELS[7:10]):
        panel(d, M + i * (cw + 12), 766, cw, 120, *p)

    # ------------------------------------------------------------- briefs strip
    by = 898
    d.text((M, by), "MORE OF THE DAY", font=font(SANS_B, 14), fill=CORAL_DARK)
    col_w = (W - 2 * M) // 3
    bf = font(SANS, 13)
    for i, b in enumerate(BRIEFS):
        cx = M + (i % 3) * col_w
        cy = by + 20 + (i // 3) * 16
        d.text((cx, cy), "· " + b, font=bf, fill=GREY)

    # ------------------------------------------------------------- footer
    d.line([M, 984, W - M, 984], fill=INK, width=1)
    sw = d.textlength(SOURCES, font=font(SANS, 12))
    d.text(((W - sw) / 2, 992), SOURCES, font=font(SANS, 12), fill=GREY)

    img.save(OUT)
    print("saved", OUT)


if __name__ == "__main__":
    main()
