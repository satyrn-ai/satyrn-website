# Satyrn AI website

The site behind [satyrn.ai](https://satyrn.ai/):
the landing page, the blog, and the project documentation.
It's a static site built with [Zensical](https://zensical.org/).

## Getting started

You need [`uv`](https://docs.astral.sh/uv/).
Every recipe runs through it, so there's no virtualenv to activate.
[`just`](https://just.systems) is a project dependency too,
so `uv run just` works if you don't have it installed.

```bash
just          # list the recipes
just serve    # dev server with live reload on http://localhost:8000
just ci       # everything CI runs
```

A page is a markdown file under `src/`, and the navigation follows the directory tree.
Posts and authors are covered in [CONTRIBUTING.md](CONTRIBUTING.md).

Without `just`, the commands underneath are `uv run zensical serve`
and `uv run zensical build --strict`.
Plain `zensical serve` leaves `site_url` pointing at production,
so instant navigation falls back to full page loads locally.

`just docker-serve` runs the same dev server in a container.
It's for local use only; it isn't what ships.

## Deployment

Cloudflare Pages builds the site from `main` and publishes it,
with build command `uv run zensical build --strict` and output directory `site`.
Those settings live in the Cloudflare dashboard, not in this repo.
GitHub Actions only runs checks and never publishes.

## Contributors

The avatar carousel on the homepage is generated from `.all-contributorsrc`.
`just sync-contributors` adds new committers but never removes anyone.
To take someone off, add their GitHub login to `exclude` in `.all-contributorsrc`
and run `just contributors`;
that also stops `sync-contributors` from adding them back.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before your first change.
A few of its rules guard against failures that still build green.

## Credits

Artwork by [Laura Summers](https://github.com/summerscope).
