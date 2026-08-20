"""Draws the social card and the icon set from the site's own palette.

    python tools/build_brand_assets.py

Writes og.jpg (1200x630), favicon.svg, favicon-32.png, apple-touch-icon.png,
icon-192.png and icon-512.png into the repo root. Rerun after any change to
the headline claim so the card and the page never disagree.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = Path("C:/Windows/Fonts")

HARBOR = (13, 34, 49)
HARBOR_2 = (22, 57, 78)
PAPER = (243, 240, 231)
VERDIGRIS = (72, 164, 141)
ON_DARK_2 = (169, 188, 198)

# The card repeats the hero claim word for word. If one changes, both change.
KICKER = "SYOSSET  \u00b7  NORTH SHORE LONG ISLAND"
HEADLINE = ["Five of my last nine listings", "sold above the asking price."]
NAME = "Margie Horowitz"
ROLE = "Licensed Real Estate Salesperson  \u00b7  19 years on the North Shore"


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def build_og():
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), HARBOR)
    d = ImageDraw.Draw(img)

    # A soft vertical lift so the flat navy does not read as a placeholder.
    for y in range(h):
        t = y / h
        d.line([(0, y), (w, y)], fill=tuple(
            round(a + (b - a) * (t ** 1.4)) for a, b in zip(HARBOR, HARBOR_2)))

    d.rectangle([0, 0, 10, h], fill=VERDIGRIS)

    d.text((78, 92), KICKER, font=font("seguisb.ttf", 21), fill=VERDIGRIS)

    y = 168
    serif = font("georgiab.ttf", 60)
    for line in HEADLINE:
        d.text((76, y), line, font=serif, fill=PAPER)
        y += 82

    d.line([(78, 396), (250, 396)], fill=VERDIGRIS, width=2)

    d.text((76, 436), NAME, font=font("georgia.ttf", 38), fill=PAPER)
    d.text((78, 496), ROLE, font=font("segoeui.ttf", 22), fill=ON_DARK_2)

    out = ROOT / "og.jpg"
    img.save(out, "JPEG", quality=88, optimize=True, progressive=True)
    print(f"og.jpg          {out.stat().st_size // 1024} KB  1200x630")


def build_icons():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="12" fill="rgb{HARBOR}"/>
  <path d="M14 46V18h5.6l12.4 18 12.4-18H50v28h-5.4V27.4L32.6 44h-1.2L19.4 27.4V46z"
        fill="rgb{PAPER}"/>
  <rect x="14" y="50" width="36" height="3" rx="1.5" fill="rgb{VERDIGRIS}"/>
</svg>
"""
    (ROOT / "favicon.svg").write_text(svg, encoding="utf-8")
    print("favicon.svg     monogram")

    for size, name in [(32, "favicon-32.png"), (180, "apple-touch-icon.png"),
                       (192, "icon-192.png"), (512, "icon-512.png")]:
        s = size * 4  # draw big, downsample, so the M stays crisp at 32px
        img = Image.new("RGB", (s, s), HARBOR)
        d = ImageDraw.Draw(img)
        f = font("georgiab.ttf", int(s * 0.56))
        box = d.textbbox((0, 0), "M", font=f)
        d.text(((s - box[2] - box[0]) / 2, (s - box[3] - box[1]) / 2 - s * 0.03),
               "M", font=f, fill=PAPER)
        d.rectangle([s * 0.22, s * 0.78, s * 0.78, s * 0.83], fill=VERDIGRIS)
        img.resize((size, size), Image.LANCZOS).save(ROOT / name, "PNG", optimize=True)
        print(f"{name:<15} {size}x{size}")


if __name__ == "__main__":
    build_og()
    build_icons()
