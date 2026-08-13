# Blog implementation notes

Maintainer notes for the blog. For *writing* a post, see the "Writing a blog
post" section of `CONTRIBUTING.md`. This file covers why the implementation
looks the way it does, and which parts will break silently if changed.

## Why it works this way

Zensical 0.0.51 ships no blog functionality. Its build core is a compiled Rust
binary (`zensical.abi3.so`); Python is called back only to parse config and
render Markdown. **There is no plugin system and no build hooks**, so Python
cannot emit pages.

What made a blog possible without any of that: MiniJinja templates — both page
templates and `extra_templates` — receive the full `nav` tree, and every node
carries `meta` (its front matter), `title`, `url`, and `canonical_url`. **`nav`
is therefore the post database.** Listings, archives, and the feed are all
produced by walking `nav` and filtering on front matter. No Python, no code
generation, no generated files in version control.

A `zensical.extensions.macros` Markdown extension does exist (mkdocs-macros
compatible, `define_env` in a root `main.py`). It is deliberately unused — see
"Escape hatch" below.

## Rules that break things silently

These caused real failures during implementation. Each fails without an error,
or with an error that points somewhere unhelpful.

**The `nav` tree has to contain every post.** Zensical is perfectly happy with a
top-level `nav` key in `zensical.toml`; this is a constraint of the
implementation above, not of Zensical. Because the templates read `nav` as the
post database, a post the tree does not reach is a post the listings and the
feed cannot see.

Leaving navigation directory-derived satisfies that by construction, which is
why there is no `nav` list. Adding one satisfies it only for as long as somebody
keeps it in step, and the failure is silent: with a three-entry `nav` the feed
drops from three entries to none, the blog index stops being built at all, and
all three posts still build and stay reachable by URL, with `--strict` reporting
success throughout.

So an explicit `nav` is a maintenance question rather than a prohibition. It
would need every post listed in it, and something in `just ci` to fail when one
is missing, before it could be relied on. (`nav_order` and friends under
`[project.extra]` are unrelated custom keys and are fine.)

Related, and equally silent: a directory reference (`{ "Blog" = "blog" }`), a
glob (`"blog/2026/*.md"`), and a directory nested in a list all expand to
**nothing** — no error, no warning, just an empty section.

**MiniJinja autoescape is OFF.** Nothing is escaped without an explicit `| e`.
A post titled `Prompting Q&A` produced `<title>Prompting Q&A</title>` and broke
the entire feed for every subscriber (`not well-formed (invalid token)`). A quote
in a `description` closed an HTML `content="` attribute early. Every interpolation
of author-supplied text in `src/feed.xml`, `overrides/main.html`, and
`overrides/partials/post-item.html` carries `| e` for this reason. **Do not
remove them.** URLs are deliberately left unescaped — escaping those corrupts the
links.

**MiniJinja has no `dateformat` filter and no `fromjson` filter.** Two
consequences, both load-bearing:
- The feed is **Atom, not RSS**. Atom uses RFC 3339, which the ISO front-matter
  dates already satisfy via a literal `T00:00:00Z` suffix. RSS needs RFC 822,
  which cannot be produced here.
- A macro cannot return a list, only rendered text. This is why the
  `walk(items, ns)` traversal macro is **duplicated** across
  `overrides/main.html`, `src/feed.xml`, and `overrides/partials/nav.html`. The
  duplication is forced, not laziness. A shared collector is not expressible.

**`page.meta` may be undefined, and attribute access on it fails the build.**
Guard with `page.meta and page.meta.x`, or bind
`{%- set meta = page.meta if page.meta else {} -%}` first (as the `extrahead`
block does). Containment checks need the same care: `page.meta.tag in
post.meta.tags` breaks on a post written without a `tags:` key.

**`date` front matter must be exactly `YYYY-MM-DD`.** The feed appends the
literal `T00:00:00Z`; a fuller datetime corrupts it.

**`site_url` must end with a trailing slash.** The feed and `og:image`
concatenate paths onto it directly.

**`nav_order` matches rendered page titles character for character** — the
homepage is `"Satyrn AI — AI Our Way"`, em dash and all, not "Home". A mismatch
does not error; the item silently drops to the end of the sidebar. Items absent
from `nav_order` are appended rather than hidden, so a new page never vanishes.

## Client-side dates: the non-obvious part

`src/javascripts/blog-dates.js` localises ISO dates. Three details are each
deliberate and were each arrived at by a failure:

- **`document$.subscribe(...)`, not `DOMContentLoaded`.** `navigation.instant` is
  enabled, so a plain listener fires once and never again after in-site
  navigation.
- **`Date.UTC(y, m - 1, d)` *and* `timeZone: "UTC"` on the formatter.** Both are
  required. `Date.UTC` builds the correct instant, but `Intl.DateTimeFormat`
  otherwise renders it in the *viewer's* zone — at UTC−4 that is 20:00 the
  previous day, so every date displayed one day early. This is invisible to a
  build and to code review; it only appears in a browser at a negative offset.
  The locale argument stays `undefined` so viewers keep their own locale; only
  the time zone is pinned.
- **The `/^\d{4}-\d{2}-\d{2}$/` guard**, so a full timestamp elsewhere on the
  site is never corrupted.

The server-rendered text stays ISO, which is the no-JavaScript fallback. Do not
pre-format it.

## Referential integrity: authors are enforced, tags are not

Asymmetric, and worth knowing:

- A post naming an **unregistered author slug** raises and **fails the build**.
  Free integrity. Note the error reads `undefined value (in <file>:<line>)` and
  does *not* name the offending slug.
- A **missing optional field** on a registered author (`avatar`, `title`,
  `fediverse`) is merely falsy — it degrades quietly, which is what those guards
  in `post-byline.html` are for.
- A **tag with no `src/tags/<tag>.md`** is caught by nothing at build time. The
  tag chip still renders as a live `<a>` to a dead URL. `just check-blog` is the
  only guard, which is why it runs in `just ci`.

Also note Zensical prints `No issues found` *before* reporting a template error.
Trust the exit code, not that message.

## File map

| Path | Role |
| --- | --- |
| `overrides/main.html` | `extrahead` (OpenGraph, `fediverse:creator`, feed autodiscovery) and `content` (byline → prose → listing). Holds a `walk` macro. |
| `overrides/partials/post-item.html` | One listing row. Expects the loop variable to be named `post`. |
| `overrides/partials/post-byline.html` | Author attribution and date on post pages. |
| `overrides/partials/tags.html` | Shadows Zensical's shipped partial. Needed because the `tags` variable arrives as `[{"name": ...}]` with **no `url` key**, so the stock partial renders inert `<span>`s. |
| `overrides/partials/nav.html` | Shadows the shipped partial. Orders top-level items, collapses archive sections, lists recent posts newest-first. |
| `src/feed.xml` | Atom 1.0, rendered via `extra_templates`. |
| `src/javascripts/blog-dates.js` | Date localisation. |
| `src/stylesheets/satyrn.css` | The `block: blog` section. Everything it adds is prefixed `satyrn-`, like the rest of the site's own markup. |
| `justfile` | `check-blog` verifies posts and feed. Runs as part of `just ci`. |

Two things in that CSS are worth knowing before editing it. The blog's lists
render inside `.md-typeset`, where the theme's own list rules are written as
`.md-typeset ul:not([hidden])` and `[dir=ltr] .md-typeset ul li` — both of
which outrank a two-class selector, so the resets carry a `[dir]` prefix purely
to win. And the byline is inline rather than flex: as flex items the author
list and the date wrapped independently, which put the date between two
authors.

`src/blog/index.md`, `src/authors/index.md`, and `src/tags/index.md` are **not
decorative** — the sidebar collapse targets each section's index page, and a
section without one renders expanded instead.

## Config reference (`[project.extra]`)

| Key | Purpose |
| --- | --- |
| `nav_order` | Top-level sidebar order, by exact rendered title. |
| `nav_collapse` | Sections rendered as a single link (`Authors`, `Tags`). |
| `nav_recent` | Sections rendered as a link plus recent posts (`Blog`). |
| `nav_recent_count` | How many recent posts to show. |
| `og_image` | Fallback social image, relative to `site_url`. |
| `authors.<slug>` | `name`, optional `title`, `avatar`, `url` (homepage), `fediverse` (`@user@instance`). |

`url` and `fediverse` are independent: `url` is linked from the byline;
`fediverse` only builds the meta tag and is never rendered as a link. `rel="me"`
is deliberately not used anywhere — it solves profile verification, a different
problem from link-preview attribution.

`fediverse:creator` is **singular by design** — Mastodon credits one creator per
page — so `authors[0]` is credited. **Author order in front matter is therefore
meaningful.**

## Outstanding before launch

1. **Each author must enable attribution on Mastodon** (Preferences → Public
   Profile → Verification → Author Attribution, adding this domain). Until then
   `fediverse:creator` has no visible effect, and it only applies to links shared
   afterward. There is also a reported Mastodon issue where the tag suppresses
   the site description in preview cards
   ([mastodon#32758](https://github.com/mastodon/mastodon/issues/32758)).

An account decision rather than a code one, and it can wait for a real author.

The blog currently has no posts, which shows in two places until the first one
lands: `/blog/` renders its introduction with nothing beneath it, and the feed's
`<updated>` falls back to `1970-01-01T00:00:00Z` because it is the newest post
date and there is none. Both correct themselves on the first post; neither is
worth an empty-state branch in the templates for the days in between.

Two entries came off this list rather than being deferred. The example posts and
authors were reverted whole, in the commit shaped to allow it. And the
previous/next links pointing at `Tags` are fixed in
`overrides/partials/footer.html`, which filters both directions on `nav_hide`
rather than turning `navigation.footer` off.

`site_url` used to be a fourth entry here, because `navigation.instant` fetches
`sitemap.xml` from the absolute URL and the browser refuses that request
cross-origin, so `just serve` filled the console with CORS errors and degraded
to full page loads. `just serve` now builds from a generated copy of the config
with `site_url` pointed at the dev address — see the comment above `dev_config`
in the justfile for why a copy is the only option available.

## Escape hatch

If date formatting or tag validation ever becomes painful, the fallback is a root
`main.py` exposing macros via `define_env` (Zensical watches it, so live reload
keeps working). That moves listing logic from `nav` to filesystem globbing, at the
cost of hand-computed URLs that can drift from `use_directory_urls`. Not worth
reaching for preemptively.

## Removal path

When Zensical ships native blog support: delete `overrides/`, `src/feed.xml`,
`src/javascripts/blog-dates.js`, and the `extra_templates` /
`[project.extra.authors]` / `nav_*` / `og_image` config. Deleting
`overrides/partials/nav.html` restores the stock sidebar. The posts themselves are
plain Markdown with conventional front matter — the format any future blog plugin
would read anyway.
