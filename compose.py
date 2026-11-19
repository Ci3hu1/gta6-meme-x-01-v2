# compose.py — renders meme.jpg (1200x675) for gta6-meme-x-01-v2.
# Ghost: the REAL make.fun ghost, rendered at high resolution from the
# official vector logo (assets/ghost-logo.svg, light variant, magenta coin
# removed — the money bag already carries the paid angle and the coin would
# collide with it). The old splash flood-fill cut is gone: no flat vertical
# edge, the full ghost outline survives on every side.
# Scene: Vice City sunset drawn in code (PIL gradients + silhouettes). No photos.
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, 'assets')
W, H = 1200, 675
PALM = (28, 11, 51)
SKYLINE = (36, 16, 64)

# ---------------------------------------------------------------- ghost
def cut_ghost():
    # Pre-rendered from assets/ghost-logo.svg (cairosvg, 2400 px wide,
    # cropped to the opaque bbox + margin). Full figure, clean outline.
    g = Image.open(os.path.join(ASSETS, 'ghost.png')).convert('RGBA')
    print('ghost.png', g.size)
    return g

# ---------------------------------------------------------------- scene helpers
def vgrad(w, h, stops):
    """stops: list of (pos0..1, (r,g,b)). Returns RGB image."""
    ys = np.linspace(0, 1, h)
    cols = np.zeros((h, 3))
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        m = (ys >= p0) & (ys <= p1)
        t = np.clip((ys[m] - p0) / max(p1 - p0, 1e-9), 0, 1)[:, None]
        cols[m] = np.array(c0) * (1 - t) + np.array(c1) * t
    cols[ys < stops[0][0]] = stops[0][1]
    cols[ys > stops[-1][0]] = stops[-1][1]
    return Image.fromarray(np.tile(cols[:, None, :], (1, w, 1)).astype(np.uint8), 'RGB')

def palm(d, bx, by, s, flip=1):
    pts = []
    for t in np.linspace(0, 1, 24):
        x = (1 - t) ** 2 * bx + 2 * (1 - t) * t * (bx + flip * 70 * s) + t * t * (bx + flip * 45 * s)
        y = (1 - t) ** 2 * by + 2 * (1 - t) * t * (by - 120 * s) + t * t * (by - 250 * s)
        pts.append((x, y))
    d.line(pts, fill=PALM, width=max(8, int(15 * s)), joint='curve')
    cx, cy = pts[-1]
    for k, ang in enumerate((-170, -135, -100, -65, -30, 5, 40)):
        a = np.radians(ang)
        ex = cx + np.cos(a) * 120 * s * (1 if flip > 0 else -1)
        ey = cy + np.sin(a) * 55 * s + 55 * s
        mx = cx + np.cos(a) * 60 * s * (1 if flip > 0 else -1)
        my = cy + np.sin(a) * 30 * s - 25 * s
        fpts = []
        for t in np.linspace(0, 1, 16):
            fpts.append(((1 - t) ** 2 * cx + 2 * (1 - t) * t * mx + t * t * ex,
                         (1 - t) ** 2 * cy + 2 * (1 - t) * t * my + t * t * ey))
        d.line(fpts, fill=PALM, width=max(5, int(9 * s)), joint='curve')
    d.ellipse([cx - 12 * s, cy - 12 * s, cx + 12 * s, cy + 12 * s], fill=PALM)

def skyline(d, rng):
    # Art-deco Vice City silhouette along the horizon (y base 472).
    x = -10
    while x < W + 10:
        bw = rng.integers(55, 130)
        bh = rng.integers(28, 95)
        top = 472 - bh
        d.rectangle([x, top, x + bw, 472], fill=SKYLINE)
        if bh > 70:  # stepped deco crown + spire
            d.rectangle([x + bw * 0.25, top - 16, x + bw * 0.75, top], fill=SKYLINE)
            d.rectangle([x + bw * 0.45, top - 34, x + bw * 0.55, top - 16], fill=SKYLINE)
        for _ in range(int(bw * bh / 900)):
            wx = x + rng.integers(6, max(7, bw - 10))
            wy = top + rng.integers(8, max(9, bh - 10))
            d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 215, 106))
        x += bw + rng.integers(4, 26)

def text_center(d, y, s, font, fill, stroke=7):
    tw = d.textlength(s, font=font)
    d.text(((W - tw) / 2, y), s, font=font, fill=fill,
           stroke_width=stroke, stroke_fill=(10, 5, 20))
    return tw

# ---------------------------------------------------------------- build
def main():
    ghost = cut_ghost()
    sky = vgrad(W, 472, [(0.0, (43, 16, 85)), (0.45, (255, 46, 136)),
                         (0.85, (255, 122, 61)), (1.0, (255, 170, 90))])
    img = Image.new('RGB', (W, H))
    img.paste(sky, (0, 0))
    d = ImageDraw.Draw(img, 'RGBA')
    rng = np.random.default_rng(7)
    # stars up top + birds
    for _ in range(26):
        x, y = rng.integers(0, W), rng.integers(8, 120)
        d.ellipse([x, y, x + 3, y + 3], fill=(255, 255, 255))
    for bx, by in [(880, 90), (930, 70), (1010, 110)]:
        d.line([bx - 12, by, bx, by - 7, bx + 12, by], fill=(30, 10, 50), width=3)
    # sun (outrun slats) left of centre so the white ghost never sits on it
    sx, sy, sr = 330, 400, 108
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 233, 168))
    for i, (yy, th) in enumerate([(sy + 18, 7), (sy + 42, 10), (sy + 68, 13)]):
        d.rectangle([sx - sr - 2, yy, sx + sr + 2, yy + th], fill=(255, 122, 61))
    skyline(d, rng)
    # ocean + sun reflection
    oc = vgrad(W, 92, [(0.0, (64, 20, 96)), (1.0, (122, 38, 110))])
    img.paste(oc, (0, 472))
    d = ImageDraw.Draw(img, 'RGBA')
    for i, wdt in enumerate((150, 110, 80, 55, 36)):
        yy = 486 + i * 13
        d.rectangle([sx - wdt // 2, yy, sx + wdt // 2, yy + 5], fill=(255, 233, 168, 200))
    # beach
    bc = vgrad(W, 115, [(0.0, (247, 200, 135)), (1.0, (214, 138, 75))])
    img.paste(bc, (0, 564))
    d = ImageDraw.Draw(img, 'RGBA')
    d.rectangle([0, 564, W, 572], fill=(190, 110, 60))
    # palms frame the scene
    palm(d, 55, 690, 1.05, flip=1)
    palm(d, 1150, 700, 1.15, flip=-1)
    # ---- ghost, centre-right, large
    gh = 400
    gw = int(ghost.width * gh / ghost.height)
    g2 = ghost.resize((gw, gh), Image.LANCZOS)
    gx, gy = 795 - gw // 2, 245
    img.paste(g2, (gx, gy), g2)
    # ---- sick note in the ghost's left hand (rotated white paper, red cross)
    note = Image.new('RGBA', (170, 210), (0, 0, 0, 0))
    nd = ImageDraw.Draw(note)
    nd.rounded_rectangle([6, 6, 164, 204], radius=10, fill=(255, 255, 255),
                         outline=(20, 10, 30), width=5)
    nd.rectangle([78, 26, 92, 66], fill=(220, 40, 60))
    nd.rectangle([58, 40, 112, 54], fill=(220, 40, 60))
    for i, yy in enumerate((88, 112, 136, 160)):
        nd.line([28, yy, 142 if i < 2 else 110, yy], fill=(120, 120, 130), width=6)
    note = note.rotate(-10, resample=Image.BICUBIC, expand=True)
    img.paste(note, (gx - 118, gy + 175), note)
    # ---- green money bag at the ghost's right
    bag = Image.new('RGBA', (190, 200), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bag)
    bd.ellipse([15, 55, 175, 195], fill=(39, 174, 96), outline=(16, 80, 45), width=6)
    bd.polygon([(78, 62), (112, 62), (128, 18), (62, 18)], fill=(39, 174, 96),
               outline=(16, 80, 45))
    bd.line([62, 18, 128, 18], fill=(16, 80, 45), width=6)
    bd.arc([28, 70, 90, 150], start=110, end=250, fill=(120, 230, 160), width=8)
    bf = ImageFont.truetype(os.path.join(ASSETS, 'Anton.ttf'), 78)
    bd.text((95, 108), '$', font=bf, fill=(255, 255, 255), anchor='mm',
            stroke_width=4, stroke_fill=(16, 80, 45))
    img.paste(bag, (gx + gw - 92, gy + 215), bag)
    # ---- caption, huge Anton, white + black outline
    d = ImageDraw.Draw(img)
    cap = ImageFont.truetype(os.path.join(ASSETS, 'Anton.ttf'), 76)
    l1, l2 = 'MY SICK NOTE SAYS GTA 6', 'MY BOSS SIGNED IT.'
    if d.textlength(l1, font=cap) > 1140:
        cap = ImageFont.truetype(os.path.join(ASSETS, 'Anton.ttf'), 68)
    text_center(d, 26, l1, cap, (255, 255, 255))
    text_center(d, 106, l2, cap, (255, 255, 255))
    # ---- make.fun wordmark, bottom-left
    wm = ImageFont.truetype(os.path.join(ASSETS, 'Anton.ttf'), 46)
    d.text((26, 612), 'make.fun', font=wm, fill=(255, 255, 255),
           stroke_width=5, stroke_fill=(10, 5, 20))
    img.save(os.path.join(HERE, 'meme.jpg'), quality=90)
    print('saved meme.jpg', img.size)

if __name__ == '__main__':
    main()
