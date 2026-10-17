# Blog implementation notes

Maintainer notes for the blog.
For *writing* a post, see the "Writing a blog post" section of `CONTRIBUTING.md`.
This file covers why the implementation looks the way it does,
and which parts will break silently if changed.

## How it works

The blog is Zensical 0.0.71's native blog.
These plugins in `zensical.toml` do the work:

| Plugin | Role |
| --- | --- |
| `blog` | Reads `src/blog/posts/`, builds the listing, archive, category and author pages, and removes posts from the `nav` tree. |
| `tags` | Builds the tags index from the `<!-- material/tags -->` marker in `src/tags/index.md`. |
| `rss` | Writes the feed. |
| `macros` | Lets `src/index.md` run Jinja, for the landing page cards. |

The theme templates are shadowed only where the stock markup is missing something the design needs.
Each is listed in the file map below.

## Posts and URLs

A post is `src/blog/posts/<file>.md`.
It builds to `/blog/<year>/<file>/`, from these settings:

```toml
post_url_format = "{date}/{file}"
post_url_date_format = "yyyy"
```

`{file}` is the filename without its extension, so the filename is part of the URL.
Renaming a post moves it.

`post_excerpt = "required"` makes a post without a `<!-- more -->` break fail the build.
`categories_allowed` is a closed list, and only those values build.
A post with `draft: true` is left out of the build, the listing, the feed and the landing page.

## Authors

`src/blog/.authors.yml` holds `name`, `avatar` and a one-line `description` for each author.
Zensical requires all three.
`description` renders as plain text in the author card of a post's sidebar.

The bio is markdown at `src/blog/author/<slug>.md`.
With `authors_profiles = true` it renders on the generated profile page, above that author's posts.

`url` is deliberately absent from `.authors.yml`.
Zensical links an author's name to `url` when it is set, so setting it sends every name off-site and leaves nothing linking to the profile.
Without it, every author name links to the profile.

Listing rows show up to `post_excerpt_max_authors` authors, set to 4 in `zensical.toml`.
The plugin's default is 1, which leaves a co-author off the listing.
The post byline and each author's profile list all of them.

## The handwritten author name

Author names are set in Triple Charm Script through the `--satyrn-font-author` token in `src/stylesheets/satyrn.css`.
It is applied in each place a name appears, and each needs its own hook because they come from different templates:

| Where | Hook | Template |
| --- | --- | --- |
| Post byline | `.satyrn-byline__link` | `partials/content.html` includes `partials/post-byline.html` |
| Listing rows | `.satyrn-post-author` | `partials/post.html` |
| Landing cards | `.satyrn-card__byline` | `src/index.md` |

The card byline is plain text, because the whole card is one link and a nested link is invalid.
Another site can point `--satyrn-font-author` at another face.

`partials/post.html` is a copy of the stock listing row.
The stock row shows only the avatar, so the copy adds the name beside it.
`partials/content.html` is the stock partial plus the byline and the layered title:
a post's `<h1>` is always ours, carrying its text in `data-title`, and a leading `#` heading in the markdown is dropped.

## Landing page cards

The `macros` plugin runs with `render_by_default = false`.
Only `src/index.md` has `render_macros: true`, so no other page is rendered as Jinja.

The cards need the latest posts, and the blog plugin has removed them from `nav`.
`main.py` reads them from `src/blog/posts/` instead, and exposes `latest_posts` to the page.
`home_posts_count` in `[project.extra]` sets how many show.

`main.py` builds each URL itself:

```python
f"blog/{date.year}/{path.stem}/"
```

That restates `post_url_format`.
The URL is relative to the landing page, so a branch preview's cards open that preview's posts.
Change one without the other and the cards link to pages that do not exist, with a green build.
`just check-blog` asserts that every card link resolves to a built post, which is what catches the drift.

## Feed

The `rss` plugin writes RSS 2.0 to `/feed.xml`.
Its default name is renamed through `feeds_filenames`.
It also emits `feed_rss_updated.xml` and `rss.xsl`, which are expected.

`match_path = "blog/posts/.*"` is what keeps the feed to posts.
Without it every page on the site becomes an entry.
`categories = ["categories", "tags"]` publishes both fields as RSS categories.

`overrides/main.html` adds the autodiscovery `<link>` to every page.

## Tags

There is one tags page, `src/tags/index.md`, holding the `<!-- material/tags -->` marker.
A tag chip links to `tags/#tag:<name>` on that page.
Tags need no per-tag file, and a tag in front matter cannot dead-link.

The old `/tags/<tag>/` and `/authors/<slug>/` URLs are not redirected, and now 404.
They were archive pages reached only from on-site links, and those links now point at the new pages.
Post URLs and `/feed.xml` did not change.

## Sidebar

Posts are out of `nav`, so the sidebar cannot list them.
Blog shows the sections the plugin generates: Archive, Categories and Authors.
`partials/nav.html` handles `nav_order`, `nav_hide` and `nav_collapse`, and has no blog-specific branch.

## Rules that break things silently

**MiniJinja autoescape is off.**
Nothing is escaped without an explicit `| e`.
A post titled `Prompting Q&A` otherwise produces `<title>Prompting Q&A</title>`, and a quote in a `description` closes an HTML `content="` attribute early.
Every interpolation of author-supplied text in `overrides/main.html`, `overrides/partials/post.html`, `overrides/partials/post-byline.html`, `overrides/partials/content.html` and `src/index.md` carries `| e`.
Do not remove them.
URLs are left unescaped, because escaping corrupts the links.

**`page.meta` may be undefined, and attribute access on it fails the build.**
Guard with `page.meta and page.meta.x`, or bind `{%- set meta = page.meta if page.meta else {} -%}` first, as the `extrahead` block does.

**`main.py` restates the URL format.**
See "Landing page cards".

**A `match_path` that stops matching changes the feed without an error.**
`just check-blog` fails if the feed's item count differs from the post count.

**`site_url` must end with a trailing slash.**
The feed, `og:image` and `main.py` concatenate paths onto it directly.

**`nav_order` matches rendered page titles character for character.**
The homepage is `"Satyrn — Open, local-first agents for Python developers"`, em dash and all, not "Home".
A mismatch does not error, and the item drops to the end of the sidebar.
Items absent from `nav_order` are appended rather than hidden, so a new page never vanishes.

## File map

| Path | Role |
| --- | --- |
| `main.py` | `define_env` for the `macros` plugin. Reads posts from disk for the landing cards. |
| `overrides/main.html` | `extrahead` (OpenGraph, `article:*` tags, feed autodiscovery) and the emptied `tabs` block. |
| `overrides/partials/content.html` | Stock `content.html` plus the post byline and the layered title. |
| `overrides/partials/post-byline.html` | Author attribution and date on post pages. |
| `overrides/partials/post.html` | The listing row, copied from the stock partial to add the author name. |
| `overrides/partials/nav.html` | The sidebar and mobile drawer. |
| `src/blog/.authors.yml` | Author name, avatar and one-line description. |
| `src/blog/author/<slug>.md` | Author bio, rendered on the generated profile. |
| `src/blog/posts/` | Posts. |
| `src/tags/index.md` | The tags page. |
| `src/stylesheets/satyrn.css` | Its `block: blog` section styles Zensical's `.md-post`, `.md-meta`, `.md-tag`, `.md-pagination` and `.md-profile`, plus our `.satyrn-post-author` and `.satyrn-byline*`. Its links take their underline and focus ring from the shared lists near the end of the file. |
| `justfile` | `check-blog` verifies posts, the feed and the landing cards. Runs as part of `just ci`. |

## Config reference

`[project.plugins.blog]`:

| Key | Value | Purpose |
| --- | --- | --- |
| `post_url_format` | `"{date}/{file}"` | URL shape of a post. |
| `post_url_date_format` | `"yyyy"` | Year only in the URL. |
| `post_excerpt` | `"required"` | A `<!-- more -->` break must be present. |
| `authors_profiles` | `true` | Generate a profile page per author. |
| `categories_allowed` | `["Announcements"]` | The only categories that build. |

`[project.plugins.rss]`:

| Key | Purpose |
| --- | --- |
| `match_path` | Keeps non-post pages out of the feed. |
| `date_from_meta` | Takes the entry date from the `date` front matter. |
| `feeds_filenames` | Renames the feed to `feed.xml`. |
| `json_feed_enabled` | Off, so only RSS is written. |

`[project.extra]`:

| Key | Purpose |
| --- | --- |
| `nav_order` | Top-level sidebar order, by exact rendered title. |
| `nav_collapse` | Sections rendered as a single link. |
| `nav_hide` | Sections left out of the sidebar, drawer and previous/next links. |
| `home_posts_count` | How many cards the landing page shows. |
| `og_image` | Fallback social image, relative to `site_url`. |

## Remaining work

The blog's `fediverse:creator` meta tag is gone, along with the author-attribution step it needed on Mastodon.
Add it back to `extrahead` if attribution is wanted.
