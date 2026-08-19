# Satyrn AI website

The site behind [satyrn.ai](https://satyrn.ai/):
the landing page, the blog, and the project documentation.
It's a static site built with [Zensical](https://zensical.org/),
so what ships is plain HTML, CSS and a little JavaScript.

## What you need

Two tools:
[`uv`](https://docs.astral.sh/uv/) and [`just`](https://just.systems).
Every recipe shells out to `uv`,
which handles Python and Zensical for you,
so there's nothing else to install and no virtualenv to activate.

## Using it

`just` on its own lists every command:

```bash
just          # show the commands
just serve    # dev server with live reload on http://localhost:8000
just build    # production build into ./site
just ci       # everything CI runs
```

Writing a page means adding a markdown file under `src/`.
The navigation picks it up from the directory tree,
and `just serve` reloads as you save.

Not a `just` user?
The commands underneath are `uv run zensical serve` and `uv run zensical build --strict`.
`just serve` additionally points `site_url` at localhost first,
without which instant navigation degrades to full page loads locally.

### Docker

Run the app in the container instead:

```bash
uv run just docker-serve
```

runs the dev server in a container instead, still with live reload at
<http://localhost:8000>, since the repo is bind-mounted in.

To see the commands underneath, see the `docker-serve` command in the [justfile](https://github.com/satyrn-ai/satyrn-website/blob/main/justfile)

It's dev-only, and this image isn't what ships to production.

## How it gets deployed

Cloudflare Pages builds the site from `main` and publishes it.
Its build command is `uv run zensical build --strict`
and its output directory is `site`.
The `--strict` matters: without it a broken link ships instead of failing.

Those settings live in the Cloudflare dashboard rather than in this repo,
which is worth knowing before you go looking for a deploy config that isn't here.
GitHub Actions only runs checks;
it deliberately doesn't publish, so the two can't fight over the same output.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
Worth reading before your first change:
a handful of this site's choices are deliberate,
and two of them break silently if you undo them,
with a green build and no error message.

## Credits

Artwork by [Georgi Ker](https://georgiker.com/).
