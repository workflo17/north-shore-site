"""Convert the rendered PNGs in img/ to web-weight JPEGs.

ComfyUI writes lossless PNGs, which came to 22 MB for fourteen images. Nobody is going to
wait for that on a phone in a driveway. JPEG at quality 84 holds up fine for architectural
photography and cuts the set to roughly a tenth of the size.

Usage:  python tools/optimise.py [--keep-png]
"""
import os
import sys

from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMG = os.path.join(ROOT, "img")
QUALITY = 84

# Nothing is displayed wider than about 700 CSS pixels, so 1400 covers a 2x screen.
MAX_W = 1400


def main():
    keep = "--keep-png" in sys.argv
    before = after = 0
    for name in sorted(os.listdir(IMG)):
        if not name.endswith(".png"):
            continue
        src = os.path.join(IMG, name)
        dst = os.path.join(IMG, name[:-4] + ".jpg")
        before += os.path.getsize(src)

        im = Image.open(src).convert("RGB")
        if im.width > MAX_W:
            im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
        im.save(dst, "JPEG", quality=QUALITY, optimize=True, progressive=True)

        after += os.path.getsize(dst)
        print(f"  {name} -> {os.path.basename(dst)} "
              f"{os.path.getsize(src)//1024}K to {os.path.getsize(dst)//1024}K")
        if not keep:
            os.remove(src)

    print(f"total {before // 1024}K -> {after // 1024}K")


if __name__ == "__main__":
    main()
