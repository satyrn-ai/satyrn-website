"""Macros for src/index.md: the latest posts, read from disk.

The blog plugin keeps posts out of the nav tree, so the landing page reads
them here instead. Post URLs repeat the blog plugin's `post_url_format`
(`{date}/{file}`, year only) rather than asking it; `just check-blog` is what
catches the two drifting apart. They are relative to the landing page, so a
branch preview links to its own posts, not production's.
"""

import pathlib

import yaml

POSTS = pathlib.Path("src/blog/posts")


def front_matter(path):
    _, _, rest = path.read_text().partition("---")
    block, _, _ = rest.partition("\n---")
    return yaml.safe_load(block) or {}


def define_env(env):
    authors = yaml.safe_load((POSTS.parent / ".authors.yml").read_text())["authors"]
    posts = []
    for path in sorted(POSTS.rglob("*.md")):
        meta = front_matter(path)
        if meta.get("draft"):
            continue
        date = meta["date"]
        posts.append({
            "title": meta["title"],
            "date": date,
            "description": meta.get("description", ""),
            "url": f"blog/{date.year}/{path.stem}/",
            "authors": [{"name": authors[slug]["name"]} for slug in meta.get("authors", [])],
        })
    env.variables["latest_posts"] = sorted(posts, key=lambda p: p["date"], reverse=True)
