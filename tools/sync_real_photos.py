"""Compress whatever real listing photography is in img/real/ and tell the page about it.

Two jobs, and the second one is the important one. The carousel shows a "Representative
image" badge on any slide whose photograph is a generated stand-in rather than Margie's own.
That badge has to track the folder, not somebody's memory of it, so this rewrites the REAL
set in index.html from what is actually on disk every time it runs.

  python tools/sync_real_photos.py
"""
import io
import os
import re

from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REAL_DIR = os.path.join(ROOT, "img", "real")
INDEX = os.path.join(ROOT, "index.html")

MAX_W = 1400
QUALITY = 84
MIN_KEEP = 40_000   # smaller than this is a portal placeholder, not a photograph


def main():
    if not os.path.isdir(REAL_DIR):
        os.makedirs(REAL_DIR, exist_ok=True)

    keys = []
    for name in sorted(os.listdir(REAL_DIR)):
        if not name.endswith(".jpg"):
            continue
        path = os.path.join(REAL_DIR, name)
        if os.path.getsize(path) < MIN_KEEP:
            print(f"  {name}: {os.path.getsize(path) // 1024}K, too small to be a photo, skipped")
            continue

        before = os.path.getsize(path)
        im = Image.open(path).convert("RGB")
        if im.width > MAX_W:
            im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
            im.save(path, "JPEG", quality=QUALITY, optimize=True, progressive=True)
        elif before > 300_000:
            im.save(path, "JPEG", quality=QUALITY, optimize=True, progressive=True)

        keys.append(name[:-4])
        print(f"  {name}: {im.width}x{im.height}  {before // 1024}K -> "
              f"{os.path.getsize(path) // 1024}K")

    html = io.open(INDEX, encoding="utf-8").read()
    listed = ", ".join(f'"{k}"' for k in keys)
    new = f"const REAL = new Set([{listed}]);"
    html, n = re.subn(r"const REAL = new Set\(\[[^\]]*\]\);", new, html, count=1)
    if not n:
        raise SystemExit("could not find the REAL set in index.html")
    io.open(INDEX, "w", encoding="utf-8").write(html)

    print(f"\n{len(keys)} real photo(s): {', '.join(keys) or 'none'}")
    print("index.html REAL set updated; every other slide keeps its representative badge")


if __name__ == "__main__":
    main()
