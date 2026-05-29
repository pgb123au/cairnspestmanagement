"""Bulk find/replace + page rename for Cairns Pest Management.

CONSERVATIVE — only boilerplate (URLs, brand, suburb names, postcode/coords, file renames).
All deep content hand-rewritten per page.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SELF_NAME = Path(__file__).name

REPLACEMENTS = [
    ("https://pakenhamdecking.com.au", "https://cairnspestmanagement.com.au"),
    ("https://pakenhamdecking.netlify.app", "https://cairnspestmanagement.netlify.app"),
    ("pakenhamdecking.netlify.app", "cairnspestmanagement.netlify.app"),
    ("pakenhamdecking.com.au", "cairnspestmanagement.com.au"),
    ("pakenhamdecking", "cairnspestmanagement"),
    ("Pakenham Decking &amp; Pergolas", "Cairns Pest Management"),
    ("Pakenham Decking & Pergolas", "Cairns Pest Management"),
    ("/officer/", "/earlville/"),
    ("/beaconsfield/", "/trinity-beach/"),
    ("/cockatoo/", "/redlynch/"),
    ("/emerald/", "/edmonton/"),
    ("/pakenham-upper/", "/smithfield/"),
    ("/cardinia-shire/", "/cairns-region/"),
    ("/services/timber-decking/", "/services/commercial-pest-control/"),
    ("/services/composite-decking/", "/services/general-pest-control/"),
    ("/services/pergolas/", "/services/cockroach-ant-control/"),
    ("/services/alfresco-outdoor-kitchens/", "/services/termite-control/"),
    ("/services/deck-restoration/", "/services/rodent-control/"),
    ("VIC 3810", "QLD 4870"),
    ('"VIC"', '"QLD"'),
    ('"3810"', '"4870"'),
    ("Pakenham VIC 3810", "Cairns QLD 4870"),
    ("3810", "4870"),
    ("-38.0814", "-16.9186"),
    ("145.4842", "145.7781"),
    (">P</text>", ">T</text>"),  # favicon letter
]

EXTENSIONS = {".astro", ".md", ".toml", ".mjs", ".json", ".xml", ".txt", ".html", ".css", ".js"}

def patch_file(p):
    try:
        s = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    out = s
    for old, new in REPLACEMENTS:
        out = out.replace(old, new)
    if out != s:
        p.write_text(out, encoding="utf-8")
        return True
    return False

def main():
    PAGES = ROOT / "src" / "pages"
    for old, new in [
        ("officer.astro", "surfers-paradise.astro"),
        ("beaconsfield.astro", "southport.astro"),
        ("cockatoo.astro", "robina.astro"),
        ("emerald.astro", "coombabah.astro"),
        ("pakenham-upper.astro", "currumbin.astro"),
        ("cardinia-shire.astro", "cairns-region.astro"),
    ]:
        o, n = PAGES / old, PAGES / new
        if o.exists() and not n.exists():
            o.rename(n); print(f"renamed: {old} -> {new}")

    SVC = PAGES / "services"
    for old, new in [
        ("timber-decking.astro", "pre-purchase-inspection.astro"),
        ("composite-decking.astro", "annual-inspection.astro"),
        ("pergolas.astro", "chemical-soil-treatment.astro"),
        ("alfresco-outdoor-kitchens.astro", "baiting-systems.astro"),
        ("deck-restoration.astro", "post-construction-protection.astro"),
    ]:
        o, n = SVC / old, SVC / new
        if o.exists() and not n.exists():
            o.rename(n); print(f"renamed services/{old} -> {new}")

    changed = 0
    for p in ROOT.rglob("*"):
        if not p.is_file(): continue
        if p.suffix not in EXTENSIONS: continue
        if "node_modules" in p.parts or "dist" in p.parts: continue
        if p.name == SELF_NAME: continue
        if patch_file(p):
            changed += 1

    pkg = ROOT / "package.json"
    if pkg.exists():
        s = pkg.read_text(encoding="utf-8")
        s = s.replace('"name": "pakenhamdecking"', '"name": "cairnspestmanagement"')
        pkg.write_text(s, encoding="utf-8")

    print(f"Done. {changed} files patched.")

if __name__ == "__main__":
    main()
