#!/usr/bin/env python3
"""
Build a self-contained slide-deck HTML file by inlining fonts/logo/screenshots
as base64 into a template. See ../SKILL.md for the full workflow this fits into.

Usage:
  python3 build_deck.py --template deck-template.html --manifest manifest.json --out slides.html

manifest.json maps every __TOKEN__ placeholder used in the template to a file
on disk, e.g.:

  {
    "__FONT_DISPLAY__": "fonts/inter-var.woff2",
    "__FONT_MONO__": "fonts/jetbrains-mono.woff2",
    "__LOGO__": "assets/logo.png",
    "__IMG_STEP_1__": "screenshots/step-1.webp",
    "__IMG_STEP_2__": "screenshots/step-2.webp"
  }

Re-run this after every edit to the template or every new/replaced screenshot.
Never hand-edit the generated --out file directly — see the Gotchas section
in SKILL.md for why that gets silently undone.
"""
import argparse
import base64
import json
import re
import sys


def b64_of(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--template", default="deck-template.html", help="Template with __TOKEN__ placeholders")
    ap.add_argument("--manifest", default="manifest.json", help="JSON map of token -> file path")
    ap.add_argument("--out", default="slides.html", help="Output path for the self-contained deck")
    args = ap.parse_args()

    html = open(args.template, encoding="utf-8").read()
    manifest = json.load(open(args.manifest, encoding="utf-8"))

    for token, path in manifest.items():
        if token not in html:
            print(f"WARNING: {token} not found in template (unused manifest entry?)", file=sys.stderr)
            continue
        try:
            html = html.replace(token, b64_of(path))
        except FileNotFoundError:
            print(f"ERROR: {token} -> {path} does not exist", file=sys.stderr)
            sys.exit(1)

    leftover = sorted(set(re.findall(r"__[A-Z0-9_]+__", html)))
    if leftover:
        print(f"ERROR: unresolved placeholders, add these to the manifest: {leftover}", file=sys.stderr)
        sys.exit(1)

    open(args.out, "w", encoding="utf-8").write(html)
    slide_count = html.count("<!-- SLIDE")
    print(f"wrote {args.out} ({len(html):,} bytes, {slide_count} slides)")


if __name__ == "__main__":
    main()
