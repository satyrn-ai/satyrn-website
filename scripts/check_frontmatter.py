"""Fail when a page's front matter does not parse as a YAML mapping.

Zensical parses front matter inside `except Exception: pass`, so a stray
colon silently discards the whole block -- taking `template:` with it --
and the build still reports success. --strict cannot see this because
nothing is ever emitted. Hence checking it here.

Run by `just check-frontmatter` and by the prek hook of the same name.
"""

import pathlib
import sys

import yaml

bad = []
for page in sorted(pathlib.Path("src").rglob("*.md")):
    text = page.read_text()
    if not text.startswith("---"):
        continue
    _, _, rest = text.partition("---")
    block, sep, _ = rest.partition("\n---")
    if not sep:
        bad.append((page, "front matter is never closed"))
        continue
    try:
        meta = yaml.safe_load(block)
    except yaml.YAMLError as e:
        bad.append((page, str(e).split("\n")[0]))
        continue
    if not isinstance(meta, dict):
        bad.append((page, f"parsed as {type(meta).__name__}, not a mapping"))
for page, why in bad:
    print(f"{page}: {why}")
print(f"{len(bad)} page(s) with unparseable front matter")
sys.exit(1 if bad else 0)
