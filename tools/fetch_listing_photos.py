"""Pull Margie's listing photography from the portals that mirror the OneKey MLS photo set.

Rights to this photography come from Margie and her brokerage. This only automates retrieval.

Two sources, tried in order:

  Zillow   photos.zillowstatic.com, `cc_ft_1536` variant, the largest on offer.
  Redfin   ssl.cdn-redfin.com `bigphoto`, about 1280px. `genMid` is 623px and too small.

Homes.com has the best masters (1900px) but blocks every non-browser client at the edge and
refuses cross-origin reads, so it cannot be scripted at all.

Both portals throttle hard: roughly eight quick requests and the IP starts getting empty 202s
and 403s. PAGE_DELAY is deliberately slow. Let it run in the background rather than tightening it.

  python tools/fetch_listing_photos.py               everything still missing
  python tools/fetch_listing_photos.py glen-head     just one
  python tools/fetch_listing_photos.py --force       re-fetch even what is already on disk
"""
import os
import re
import subprocess
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "img", "real")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

PAGE_DELAY = 75      # between property pages
RETRY_DELAY = 120    # after a throttled response
MIN_BYTES = 40_000   # anything smaller is a placeholder, not a photograph

# key -> (zillow zpid or None, redfin path or None). Keys match `img` in the SALES array.
LISTINGS = {
    "p-glen-head":  (None,       None),
    "p-brooklyn":   (None,       "/NY/Brooklyn/1542-84th-St-11228/home/40829288"),
    "p-seaford":    (None,       "/NY/Seaford/2631-Irene-Ln-11783/home/20224158"),
    "p-albertson":  (None,       "/NY/Albertson/6-Wood-Ave-11507/home/20543441"),
    "p-islip":      ("82666298", None),
    "p-lawrence":   (None,       "/NY/Glen-Cove/214-Lawrence-Ln-11542/home/20492521"),
    "p-tyrconnell": (None,       None),
    "p-bryce":      (None,       "/NY/Glen-Cove/8-Bryce-Ave-11542/home/20478563"),
    "p-robinwood":  ("31218306", None),
    "p-perry":      ("31163872", "/NY/Bayville/44-Perry-Ave-11709/home/20485500"),
}

SLUG = {
    "p-glen-head":  "22-Lincoln-Ave-Glen-Head-NY-11545",
    "p-brooklyn":   "1542-84th-St-Brooklyn-NY-11228",
    "p-seaford":    "2631-Irene-Ln-Seaford-NY-11783",
    "p-albertson":  "6-Wood-Ave-Albertson-NY-11507",
    "p-islip":      "98-Cortelyou-St-Islip-NY-11751",
    "p-lawrence":   "214-Lawrence-Ln-Glen-Cove-NY-11542",
    "p-tyrconnell": "44-Tyrconnell-Ave-Massapequa-Park-NY-11762",
    "p-bryce":      "8-Bryce-Ave-Glen-Cove-NY-11542",
    "p-robinwood":  "61-Robinwood-Ave-Hempstead-NY-11550",
    "p-perry":      "44-Perry-Ave-Bayville-NY-11709",
}


# Python cannot complete a TLS handshake on this machine (the AV breaks revocation checking),
# so every request goes out through curl, same as the other tools in here.
def curl(url, dest=None):
    cmd = ["curl", "-sL", "--ssl-no-revoke", "-m", "60", "-A", UA,
           "-H", "Accept-Language: en-US,en;q=0.9"]
    if dest:
        cmd += ["-o", dest, "-w", "%{http_code}"]
        return subprocess.run(cmd + [url], capture_output=True, text=True).stdout.strip()
    return subprocess.run(cmd + [url], capture_output=True).stdout.decode("utf-8", "replace")


def page(url):
    """Fetch a portal page, giving a throttled response one long second chance."""
    html = curl(url)
    if len(html) < 20_000:
        time.sleep(RETRY_DELAY)
        html = curl(url)
    return html if len(html) >= 20_000 else ""


def zillow_photos(html):
    """Largest Zillow variant per photo id, in page order."""
    hits = re.findall(r"https://photos\.zillowstatic\.com/fp/([a-f0-9]{20,})-cc_ft_\d+\.jpg", html)
    seen, ordered = set(), []
    for h in hits:
        if h not in seen:
            seen.add(h)
            ordered.append(f"https://photos.zillowstatic.com/fp/{h}-cc_ft_1536.jpg")
    return ordered


def redfin_photos(html):
    hits = re.findall(r"https://ssl\.cdn-redfin\.com/photo/\d+/bigphoto/\d+/[\w.]+\.jpg", html)
    seen, ordered = set(), []
    for h in hits:
        if h not in seen:
            seen.add(h)
            ordered.append(h)
    return ordered


def grab(key, zpid, redfin):
    dest = os.path.join(OUT, key + ".jpg")
    attempts = []
    if zpid:
        attempts.append(("zillow",
                         f"https://www.zillow.com/homedetails/{SLUG[key]}/{zpid}_zpid/",
                         zillow_photos))
    if redfin:
        attempts.append(("redfin", "https://www.redfin.com" + redfin, redfin_photos))

    for name, url, extract in attempts:
        html = page(url)
        if not html:
            print(f"  {key:14s} {name}: throttled", flush=True)
            continue
        urls = extract(html)
        if not urls:
            print(f"  {key:14s} {name}: page loaded but no photos on it", flush=True)
            continue
        code = curl(urls[0], dest)
        size = os.path.getsize(dest) if os.path.exists(dest) else 0
        if code == "200" and size >= MIN_BYTES:
            print(f"  {key:14s} {name}: {len(urls)} photos, primary {size // 1024}K", flush=True)
            return True
        print(f"  {key:14s} {name}: primary HTTP {code} {size // 1024}K, too small", flush=True)
    return False


def main():
    os.makedirs(OUT, exist_ok=True)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv

    todo = []
    for key, (zpid, redfin) in LISTINGS.items():
        if args and not any(a in key for a in args):
            continue
        if not force and os.path.exists(os.path.join(OUT, key + ".jpg")):
            continue
        if not zpid and not redfin:
            print(f"  {key:14s} no source URL known yet", flush=True)
            continue
        todo.append((key, zpid, redfin))

    print(f"{len(todo)} to fetch, about {PAGE_DELAY}s apart", flush=True)
    for n, (key, zpid, redfin) in enumerate(todo):
        if n:
            time.sleep(PAGE_DELAY)
        grab(key, zpid, redfin)
    print("done", flush=True)


if __name__ == "__main__":
    main()
