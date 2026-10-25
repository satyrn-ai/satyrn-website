# Contributing Guidelines

Almost everything below is a decision someone already made for a reason
that isn't visible in the code.
A few of them fail silently,
so it's worth a skim before your first change.

Run `just ci` before opening a pull request.
CI runs the same recipe:
a strict build, a navigation check, the blog checks,
an asset-reference check, the linters, and the page weight report.

Strict means `zensical build --strict`,
which turns Zensical's warnings into a non-zero exit.
Link and anchor checking is on by default;
`--strict` is what makes it fail rather than warn.
`[project.validation]` in `zensical.toml` only adds the reference and footnote
checks, which ship off.

## Pre-commit hooks

`prek.toml` defines the checks that run on source files rather than on the built site:
markdownlint, cspell, editorconfig-checker,
and the whitespace, line-ending and config-syntax hooks.
Install them once with `uv run prek install`,
and they run on the files in each commit.
The installed hook calls the prek in `.venv`,
so run `uv sync` again if you delete `.venv`.
The first commit after installing is slow
while prek sets up the environments its hooks need.

`just lint` runs the same hooks over every tracked file,
so a new post or page is skipped until it has been staged with `git add`.
`just ci` calls `just lint`, and CI runs `just ci`,
so a markdownlint or spelling failure shows up at commit time
instead of in a pull request's CI run.

The whitespace and end-of-file hooks fix the file and fail the commit.
Stage the fixed file and commit again.

[prek](https://prek.j178.dev/) is a drop-in replacement for pre-commit.
`prek.toml` is its own format, which plain `pre-commit` cannot read.
`uv run prek` uses the version pinned in `pyproject.toml`,
and `prek.toml` pins each hook repository to a commit.

`check-nav`, `check-blog`, `check-assets`, `check-placeholders` and `weigh`
read the built site, so they stay in the justfile
and only `just ci` runs them.

## Where things live

| Path | What it is |
| --- | --- |
| `src/index.md` | The landing page. All of its copy is here as markdown. |
| `src/mission.md`, `src/local-first.md`, `src/get-involved.md` | Top-level pages. Unfinished sections carry a "Still being written" admonition. |
| `src/blog/posts/` | Posts, one markdown file each. |
| `src/blog/.authors.yml`, `src/blog/author/` | The author registry, and one bio page per author. |
| `src/tags/index.md` | The tags page. Chips on posts link into it. |
| `main.py` | Reads the posts from disk for the landing page cards. |
| `src/stylesheets/satyrn.css` | Brand palette, landing page layout, blog styling. |
| `src/assets/` | Logos, mascot artwork, favicon, and the generated social card. |
| `overrides/main.html` | Head additions and link previews, applied to every page. |
| `overrides/home.html` | The landing page shell: its own footer, and the wrapper that keeps its sidebar to the mobile drawer. |
| `overrides/partials/` | The chrome, shadowed from the theme (`tabs.html`, `nav.html`, `footer.html`), plus the blog's `content.html`, `post-byline.html` and `post.html`. |
| `justfile` | Every command. `just` with no argument lists them. |

`docs/BLOG.md` covers the blog's implementation:
how the plugins and our overrides fit together,
and which parts of it break without saying so.
Read that before changing anything under `overrides/`.

## Language and spelling

Write in British English.
"behaviour", "colour", "organisation".
`just lint` checks this with cspell and CI runs it,
so an American spelling fails a pull request rather than being a matter of taste.
New technical words go in `.vscode/cspell.json`.

`theme.language` stays `en`, not `en-GB`, and that is deliberate.
Nothing on this site consumes the region subtag:
there is no `hyphens: auto`, no `:lang()` selector in the theme CSS,
no `<q>` element, and no text input for a browser to spell-check.
WCAG only asks that the page language be programmatically determinable,
which `en` satisfies,
and search engines take regional targeting from `hreflang`, not `<html lang>`.
The one real difference is screen reader accent.

If you do change it, note the theme ships no English regional variants,
and setting `theme.language` to a code it does not have fails the build.
That is the good case: it is loud rather than silent.

Navigation comes from the directory tree.
There's no `nav` list in `zensical.toml` on purpose:
a hand-written list would have to name every page to stay correct,
and says nothing when it stops doing so.
The blog does not read it: the blog plugin builds its own sections.

## Voice

The site should sound like the people building Satyrn, talking to developers.
Think Django and the kernel's contributor docs, not a foundation press release.
These rules come from comparing the writing of projects developers trust
and talk about (Django, Ladybird, Buzz, Biome, Lightpanda and others).

**Be concrete.**
Name what the reader actually deals with, not an abstraction.
"A provider outage is someone else's bad day" beats "resilient and reliable".
Cut "trust", "innovative", "seamless" and "enterprise scale" unless something specific follows.

**Say what it isn't.**
A short negative ("Not a hosted service.") lands faster than another claim.
Only use one you would still stand by in a year.

**Say what isn't finished.**
Keep "Where it's at" on the home page true.
If something moves from "Being built" to "Works today", move it there too.

**Claims need proof.**
Never publish a number without its method: hardware, dataset, what it lost on.
Never promise a behaviour (telemetry, data, governance) the code or the
Team Compass doesn't already back up.

**Buttons say what happens next.**
"Run an experiment" or "Browse open issues", not "Learn more" or "Get started".

**Humour is dry and rare, and never carries a fact.**
A joke only works when everything around it is exact.
If a line needs context or a shared idiom to land, it doesn't carry anything
important: that's why the hero says "a foundation created in the EU"
rather than "Cherry on top? European."
No emoji bullet lists, no "vibrant community", no cosmic mission copy.

## Things that fail quietly

Each of these has already cost someone an afternoon.

### A page title that stops matching

These settings in `[project.extra]` address pages by their rendered title:
`nav_order`, `nav_collapse`, `nav_hide` and `nav_menu`.
The match is character for character, em dash included.

None of them error on a title that matches nothing.
An unmatched `nav_order` entry drops the page to the end of the sidebar;
an unmatched `nav_menu` entry removes the menu item altogether.
Both build clean.

So renaming a page means grepping `zensical.toml` for its old title.
`just check-nav` covers the menu bar,
by comparing what the built page renders against the configured list.
The rest are on you.

### Built-in palette colour names

The theme ships rules like `[data-md-color-scheme=slate][data-md-color-primary=indigo]`,
whose specificity beats the brand tokens.
`zensical.toml` sets `primary` and `accent` to `"custom"` so none of them match.
Put a real colour name back and dark mode returns to indigo links.

## Accessibility

Treat this as part of the definition of done, not a later pass.
`just lint` catches missing alt text, and that is roughly all it catches.
Everything else here is on you.

### Images

Every `<img>` needs an `alt`, and the right value depends on the job it does:

- Content, like the mascot: describe what it shows.
  "Illustration of a curly-haired girl holding a balloon shaped like a ringed
  planet, the Satyrn mascot", not "mascot" and not "image".
- Decorative, like the mark beside the mission text: `alt=""`.
  Empty, not missing. An absent `alt` makes a screen reader read the filename.
- Repeated: if the same idea is already in adjacent text, use `alt=""`
  rather than saying it twice.

`width` and `height` must match the file's real pixel dimensions.
They're what reserves the right box before the image loads,
and getting them wrong shifts the layout under the reader.
This has been wrong here before:
the logo declared `480x334` while the file was `480x480`.

### Links

Colour alone can't be the thing that marks a link.
Inside a sentence a link needs an underline,
which is why `.satyrn-footer__link--inline` carries one.
In dark mode the gold sits at 1.48:1 against body text,
nowhere near the 3:1 that WCAG 1.4.1 asks for when colour does the work by itself.

Standalone links in a nav row are fine without it.
Position already says they're links.

Every link needs a discernible name.
An icon-only link needs `aria-label`;
an image inside a link needs `alt` describing the destination, not the picture.

### Names, roles and landmarks

Reach for a real element before an ARIA attribute.
`<nav>`, `<main>` and `<footer>` already carry the right roles,
and no ARIA is better than wrong ARIA.

Where several regions share a role, label them.
Three `<nav>` landmarks are on a page at once —
the tab bar, the sidebar and the breadcrumbs —
and the theme names each of them,
so anything you add alongside needs a name too.
The pillar cards are a list,
so a screen reader announces them as one and they don't each need naming.

### Keyboard and pointer

Interactive targets are at least 24x24px.
That's why `.md-tabs__link` and `.satyrn-footer__link--standalone`
carry padding and `min-height`.
The text alone is only about 14px tall.
Links sitting inline in a sentence are exempt.

Focus has to stay visible.
The custom links define their own `:focus-visible` ring
because the theme's default washes out against the brand backgrounds.
Tab through anything you add.

### Before you call it done

- Both colour schemes, not just the one you're working in.
- 320px up to desktop, checking nothing overflows sideways.
- Tab through it.
- Measure contrast, don't eyeball it.

## Marking unfinished work

Use an admonition, not an HTML comment.
A comment is invisible to whoever is reading the page:

```markdown
!!! warning "Still being written"

    What is provisional, and what will change.
```

Zensical supports thirteen types (`note`, `info`, `tip`, `warning`, `danger`
and so on), collapsible variants with `???`,
and custom titles in quotes.
Body text indents four spaces.

## Writing a blog post

A post is a markdown file at `src/blog/posts/<file>.md`,
with front matter in `yaml` format:

```yaml
---
title: Your Post Title
date: 2026-08-15
authors:
  - example
categories:
  - Announcements
tags:
  - engineering
description: One sentence. It carries the listing row, the link preview and the feed.
---

The opening paragraph, which is the excerpt in the listing.

<!-- more -->

The rest of the post.
```

The post builds to `/blog/<year>/<file>/`.
The filename is part of the URL, so renaming a post moves it.

### Frontmatter notes

Lists go one item per line, not `[example]`.
`unresolved_references` validation reads a flow sequence as a markdown
reference link and fails the build looking for a definition of `[example]`.
The rest of the site writes them this way too.

`<!-- more -->` is required.
It ends the excerpt shown in the listing, and a post without one fails the build.

`date` is a plain `YYYY-MM-DD`; `just check-blog` fails on a time or any other form.

`authors` are slugs from `src/blog/.authors.yml`.
An unregistered slug fails the build.
List every author on the post;
the byline and each profile show all of them,
and the listing rows show up to `post_excerpt_max_authors` from `zensical.toml`.

`categories` must come from `categories_allowed` in `zensical.toml`.
A value outside that list does not build.

`tags` are free text.
They need no file: each chip links to `tags/#tag:<name>` on the tags page.

`description` is optional to the build and load-bearing everywhere else.
Without it the listing row and the feed entry both come out empty,
and `just check-blog` fails.

`draft: true` leaves the post out of the build, the listing, the feed and the landing page.

An `image:` key overrides the link preview image for that post.
Without one the post falls back to the site-wide card at `extra.og_image`,
which `just og-image` builds.

The feed is RSS 2.0 at `/feed.xml`.
`match_path = "blog/posts/.*"` on the `rss` plugin is what keeps other pages out of it,
so a post has to live under `src/blog/posts/` to appear there.

The landing page cards read the posts from `main.py`,
which builds each URL itself and so repeats `post_url_format`.
Change that setting and `just check-blog` fails until `main.py` agrees.

### Adding a blog author

Each author needs:

- `src/blog/.authors.yml` needs an entry under `authors:`,
  with `name`, `avatar` and a one-line `description`.
  All three are required.
  The description is plain text, shown in the author card on the post.
- `src/blog/author/<slug>.md` holds the bio in markdown.
  It renders on the author's profile page, above their posts.
  Its front matter needs a quoted `description`, such as `"Posts by Carol Willing."`,
  which becomes the profile's link-preview text.

Leave `url` out of the yml entry.
When it is set, author names link to that address instead of the profile,
and nothing on the site links to the profile.

### Blog and tags indexes

`src/blog/index.md` is the blog's landing page,
and `src/tags/index.md` holds the `<!-- material/tags -->` marker the tags plugin fills.
The Blog sidebar section shows the generated Archive, Categories and Authors pages.
Old `/tags/<tag>/` and `/authors/<slug>/` URLs are not redirected.

## Pages and layout

The landing page opts out of the docs layout in its front matter:

```yaml
---
template: home.html
---
```

Every other page uses the stock Zensical layout,
sidebar and search,
with the same brand palette over it.

The landing page is hand-written HTML wrapped around markdown,
and `.markdownlint.jsonc` allows the elements it needs.
That includes `<section>`, used for the latest-post cards as a labelled region.
Any other element, `<br>` or `<b>` say, is still flagged by `just lint`.

Note what is *not* there.
`hide: navigation` looks like the way to give the landing page its full width,
and it is a trap:
it puts `hidden` on the primary sidebar,
and below 1220px the primary sidebar is the mobile drawer,
with nothing in the theme's CSS bringing it back.
The hamburger then opens onto an empty panel.
`overrides/home.html` wraps the sidebar in a class instead,
and one media query hides it above the same width the tab bar appears at.

### Navigation

The menu bar, the sidebar and the previous/next links are configured separately.

The menu bar is `[[project.extra.nav_menu]]`,
rendered by `overrides/partials/tabs.html`.
It is an editorial list, not a mirror of the top level:
adding `src/whatever.md` does not earn it a menu item.
Entries resolve against the nav tree rather than carrying their own URLs,
so links and active states stay the theme's job.

The sidebar is `overrides/partials/nav.html`,
walking the tree Zensical derives from `src/`.
Above 1220px the theme's `md-nav--lifted` narrows it
to whichever tab you are in,
which is why the sidebar shows page headings rather than the whole sitemap.
Below 1220px there is no tab bar,
the same markup becomes the drawer,
and it holds everything.

That split is why `nav_hide` keeps an item
when the item is the page you are on:
on desktop lifted has already hidden it everywhere else,
so the only thing `nav_hide` really removes is a drawer entry.
Drop it unconditionally and the page loses its own navigation.

The previous/next links are `overrides/partials/footer.html`.
The theme builds them from the directory tree in document order,
which knows nothing about `nav_order` or `nav_hide`,
so the override filters out anything inside a hidden section —
in both directions, so those sections neither appear as a destination
nor offer links back out of themselves.
`nav_hide` is what all three read,
so adding a section to it removes it from the chrome everywhere at once.

There is deliberately no `nav` list in `zensical.toml`.

The pillar cards use the theme's own `grid cards`:
a markdown list inside `<div class="grid cards satyrn-pillars" markdown>`,
so the card styling comes from Zensical and only the column counts are ours.
The grid deliberately doesn't use `auto-fit`.
`auto-fit` packs in as many columns as happen to fit,
which means it passes through a 3+1 layout and strands one card alone on a row.
Column counts are declared per breakpoint instead,
so you get 4 across, 2x2, or 1, and nothing else.
Add a fifth card and those numbers need revisiting.

## CSS conventions

Zensical's stylesheet is BEM (`.md-header__button`, `.md-nav__link--active`),
and `src/stylesheets/satyrn.css` follows it where it can.
Three kinds of selector live in that file:

| Kind | Example | For |
| --- | --- | --- |
| Block / element | `.satyrn-footer__link` | Markup we hand-write in `overrides/*.html` |
| Scoped descendant | `.satyrn-mission h2` | Tags the markdown parser emits |
| Token | `--satyrn-mark-filter` | Values that differ per colour scheme |

The middle row is the interesting one.
Giving those elements BEM classes would mean annotating the copy:

```markdown
### Open Source { .satyrn-pillars__title }
```

That drags styling hooks into the content,
which is the thing the markdown-drives-the-page approach exists to avoid,
and it has to be repeated for every new card.
Descendant selectors are the better trade,
as long as they stay one level deep and scoped to a block.

So: if you wrote the tag, give it a class.
If markdown wrote the tag, match it by name inside its block.

Two things that save time:

Most rules don't need a `.md-typeset` prefix to beat the theme.
Material's typeset rules are single-class specificity
and this stylesheet loads after them,
so `.satyrn-hero__text h1` already wins.
Reach for more specificity only after watching a rule actually lose.

Style the concept, not the instance.
The dark-mode logo halo and the display font were both first written
against the two elements that happened to need them,
and both then missed every other place the same thing showed up.

## Images and fonts

Regenerate artwork with `just encode-assets <dir>` rather than by hand.
The choices below are easy to undo by accident.

There's one logo file, not two.
Light and dark variants used to be swapped in CSS,
which made every visitor download both,
since a `display: none` image is still fetched.
The dark artwork also sat in more transparent padding,
so the same CSS width rendered it about 40% smaller than its counterpart.
One file plus a halo in dark mode is smaller and behaves the same in both schemes.

The social card is JPEG, and generated rather than drawn.
`just og-image` renders `artwork/satyrn-square-dark.svg` onto the brand charcoal at 1200x630,
so it stays in step with the logo instead of drifting from it.
It runs through `uv` with a pinned SVG renderer, so it needs no ImageMagick.
The logo sits inside the centre square, so unfurlers that crop to 1:1 keep all of it.
JPEG because the page never loads that file — only the crawlers building
link previews do, and their format support is narrower
and harder to verify than a browser's.
It carries no typeset text: the title and description travel as their own meta tags,
and the wordmark in the logo is drawn as outlines, so nothing depends on installed fonts.

AVIF is used for the mascot only.
It saves 13 KB there and has exactly one consumer.
The logo stays WebP-only because `theme.logo` renders as a bare `<img>`
with no `<picture>` around it,
so an AVIF would ship the same artwork twice: 24 KB instead of 15 KB.

Fredoka is fetched at a single weight.
Asking for `wght@500;600;700` pulls a separate file per weight
and only 600 is ever rendered,
so anything using the display font needs an explicit `font-weight: 600`.
Inherit some other weight and it snaps to the nearest declared one,
quietly pulling a second file.

JetBrains Mono is loaded even though today's pages have no code blocks.
That's deliberate. This is a documentation site,
and the pages that need it are coming.

Zensical's font config only accepts a text face and a code face,
so Fredoka arrives through an overridden `fonts` block in `overrides/main.html`.
There is no supported config key for a third face.

If you ever need a light and dark version of the same image,
Zensical has `#only-light` and `#only-dark` URL fragments for it.
Prefer those over hand-rolling a CSS swap.

## Colour and contrast

The palette comes from the design team's brand colours:
a greige light background (`#ced0c3`) and a warm charcoal dark one (`#383330`).
Each Satyrn surface owns one hue, and the main site's is yellow.
For now yellow is the only hue in the UI;
pink, blue and green belong to other surfaces.

Yellow comes in three tiers, and each is only valid for the job it was checked against:

| Token | Hex | Use | Contrast |
| --- | --- | --- | --- |
| `--satyrn-yellow-dark` | `#e3d678` | Text and logo on dark | 8.40:1 |
| `--satyrn-yellow-ui` | `#7f7435` | Large text, icons, borders on light | 3.02:1 |
| `--satyrn-yellow-text` | `#423c1b` | Body-size text on light | 7.09:1 |

The UI tier is not for body text.
Blocks shouldn't reach for a tier directly:
`--satyrn-accent` and `--satyrn-accent-text` pick the right one per scheme.

A yellow fill on greige is 1.06:1 and all but disappears,
so the primary button is charcoal with a yellow label in light mode
and yellow with a charcoal label in dark mode.

Borders that are the only thing marking out a control,
like the secondary button's, use `--satyrn-control-border` (3:1 or better),
not the faint `--satyrn-border` used for dividers and cards.
Footers sit on the page background:
the yellow wordmark is only 3.02:1 on greige, and a darker band pushes it under 3:1.

## Layout and breakpoints

The landing page follows the theme's own breakpoints,
so it changes layout in step with the header and tab bar:
above 1220px is full desktop, at 960px the hero drops to one column and the planet scene moves under the buttons,
and at 480px buttons go full width.
They're written in `em`, which in a media query is the 16px browser default,
not the site's 125% root size.

The one decorative flourish is the hero's full-width space band:
a static starfield, plus stars, orbits, two moons and a shooting star drawn
inside the logo's own SVG, with a small script (`javascripts/space.js`) for
pointer parallax. The band follows the page's scheme: pale stars and the dark
logo on charcoal, charcoal stars and the light logo on greige. Its colours
come from the `--satyrn-space-*` and `--satyrn-mark-*` tokens, so change them
there, not in the block.
Nothing decorative may sit behind text: the starfield and the scene's left
edge are masked away from the text column, because a dot beside a word
reads as a stray full stop.
Its motion never loops on a clock: it follows scrolling or the pointer,
the shooting star and twinkle are one-shots, browsers without scroll timelines
get one short sweep, and everything stops under `prefers-reduced-motion`.
Anything that moves on its own for more than five seconds needs a pause control (WCAG 2.2.2).
The contributor carousel under "Why Satyrn" is the one thing that does, which is why it has a Pause button.
Its avatars are placeholders until real contributors replace them;
`just check-placeholders` fails the build until they do.
Before adding another ornament, a numbered label or a tinted band,
check it's doing a job a heading or a hairline isn't already doing.
