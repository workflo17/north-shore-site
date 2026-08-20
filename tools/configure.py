"""The two switches that turn a design concept into a public website.

    python tools/configure.py --status
    python tools/configure.py --url https://margiehorowitz.com
    python tools/configure.py --live
    python tools/configure.py --concept

--url rewrites every absolute reference to the site in one pass: the canonical
tag, the Open Graph URL and image, the JSON-LD @id and url fields, the sitemap
entry, and the Sitemap line in robots.txt. Miss one of those by hand and Google
indexes the preview domain instead of the real one.

--live removes the "design concept" bar, swaps the noindex meta for an
indexable one, and opens robots.txt. --concept puts all three back. Nothing
else on the page changes, so the switch is safe to throw both ways.
"""

import argparse
import datetime
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
ROBOTS = ROOT / "robots.txt"
SITEMAP = ROOT / "sitemap.xml"

NOINDEX = '<meta name="robots" content="noindex, nofollow">'
INDEXABLE = '<meta name="robots" content="index, follow, max-image-preview:large">'

ROBOTS_CLOSED = """# INDEXING:BEGIN concept
# The site is not public yet. Nothing is crawlable while the brokerage line and
# the New York disclosures are unconfirmed. Flip with: python tools/configure.py --live
User-agent: *
Disallow: /
# INDEXING:END"""

ROBOTS_OPEN = """# INDEXING:BEGIN live
User-agent: *
Allow: /

# The generators do not buy houses on Long Island, and they cost bandwidth.
User-agent: GPTBot
Disallow: /
User-agent: CCBot
Disallow: /
# INDEXING:END"""


def read(path):
    return path.read_text(encoding="utf-8")


def write(path, text):
    path.write_text(text, encoding="utf-8")


def current_url():
    m = re.search(r'<link rel="canonical" href="([^"]+)"', read(INDEX))
    return m.group(1).rstrip("/") if m else None


def current_state():
    html = read(INDEX)
    indexed = INDEXABLE in html
    bar_hidden = "<!-- CONCEPTBAR:BEGIN hidden" in html
    robots_open = "INDEXING:BEGIN live" in read(ROBOTS)
    return indexed, bar_hidden, robots_open


def set_url(new_url):
    new_url = new_url.rstrip("/")
    if not re.match(r"^https://[a-z0-9.-]+$", new_url):
        sys.exit(f"Refusing: {new_url!r} is not an https origin with no path.")

    old = current_url()
    if not old:
        sys.exit("Refusing: no canonical tag found in index.html.")
    if old == new_url:
        print(f"Already set to {new_url}. Nothing to do.")
        return

    for path in (INDEX, ROBOTS, SITEMAP):
        text = read(path)
        hits = text.count(old)
        if hits:
            write(path, text.replace(old, new_url))
        print(f"  {path.name:<14} {hits} reference{'s' if hits != 1 else ''} rewritten")

    today = datetime.date.today().isoformat()
    write(SITEMAP, re.sub(r"<lastmod>[^<]+</lastmod>", f"<lastmod>{today}</lastmod>", read(SITEMAP)))
    print(f"  sitemap.xml    lastmod set to {today}")
    print(f"\n{old}  ->  {new_url}")


def set_mode(live):
    html = read(INDEX)

    html = html.replace(INDEXABLE if not live else NOINDEX,
                        NOINDEX if not live else INDEXABLE)

    # The concept bar is commented out rather than deleted, so --concept can
    # put the exact same markup back.
    if live:
        html = re.sub(
            r"<!-- CONCEPTBAR:BEGIN -->\n(.*?)\n<!-- CONCEPTBAR:END -->",
            lambda m: f"<!-- CONCEPTBAR:BEGIN hidden\n{m.group(1)}\nCONCEPTBAR:END -->",
            html, flags=re.S)
    else:
        html = re.sub(
            r"<!-- CONCEPTBAR:BEGIN hidden\n(.*?)\nCONCEPTBAR:END -->",
            lambda m: f"<!-- CONCEPTBAR:BEGIN -->\n{m.group(1)}\n<!-- CONCEPTBAR:END -->",
            html, flags=re.S)

    write(INDEX, html)

    robots = read(ROBOTS)
    robots = re.sub(r"# INDEXING:BEGIN.*?# INDEXING:END",
                    ROBOTS_OPEN if live else ROBOTS_CLOSED, robots, flags=re.S)
    write(ROBOTS, robots)

    status()
    if live:
        print("\nBefore you push this: the brokerage name, the office address, the")
        print("Fair Housing notice and the New York Standard Operating Procedures")
        print("all have to be on the page. New York requires them on advertising.")
        print("Check with: grep -n tofill index.html")


def status():
    indexed, bar_hidden, robots_open = current_state()
    tofill = read(INDEX).count('class="tofill"')
    mode = "LIVE" if (indexed and robots_open and bar_hidden) else "CONCEPT"
    if indexed != robots_open or indexed != bar_hidden:
        mode = "MIXED, which is a bug"
    print(f"\n  mode          {mode}")
    print(f"  site url      {current_url()}")
    print(f"  meta robots   {'index, follow' if indexed else 'noindex, nofollow'}")
    print(f"  robots.txt    {'crawlable' if robots_open else 'closed'}")
    print(f"  concept bar   {'hidden' if bar_hidden else 'showing'}")
    print(f"  .tofill spots {tofill} left on the page\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", help="set the site's public origin, e.g. https://margiehorowitz.com")
    ap.add_argument("--live", action="store_true", help="publish: indexable, no concept bar")
    ap.add_argument("--concept", action="store_true", help="unpublish: noindex, concept bar back")
    ap.add_argument("--status", action="store_true", help="report the current state")
    args = ap.parse_args()

    if args.live and args.concept:
        sys.exit("Pick one of --live or --concept.")
    if args.url:
        set_url(args.url)
    if args.live or args.concept:
        set_mode(args.live)
    if args.status or not (args.url or args.live or args.concept):
        status()
