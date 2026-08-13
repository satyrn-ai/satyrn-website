# Contributing Guidelines

Almost everything below is a decision someone already made for a reason
that isn't visible in the code.
A few of them fail silently,
so it's worth a skim before your first change.

Run `just ci` before opening a pull request.
CI runs the same recipe:
a strict build, a front-matter check, a navigation check, the blog checks,
an asset-reference check, the linters, and the page weight report.

Strict means `zensical build --strict`,
which turns Zensical's warnings into a non-zero exit.
Link and anchor checking is on by default;
`--strict` is what makes it fail rather than warn.
`[project.validation]` in `zensical.toml` only adds the reference and footnote
checks, which ship off.

`just ci` also runs `check-frontmatter`, which exists because Zensical parses
front matter inside a bare `except`.
A stray colon discards the whole block, `template:` included,
while the build still reports success,
so `--strict` cannot see it and something else has to.

## Where things live

| Path | What it is |
| --- | --- |
| `src/index.md` | The landing page. All of its copy is here as markdown. |
| `src/mission.md`, `src/local-first.md`, `src/get-involved.md` | Top-level pages. Unfinished sections carry a "Still being written" admonition. |
| `src/blog/<year>/` | Posts, one markdown file each. |
| `src/authors/`, `src/tags/` | An index page plus one page per author and per tag. |
| `src/feed.xml` | The Atom feed, rendered as a template rather than a page. |
| `src/stylesheets/satyrn.css` | Brand palette, landing page layout, blog styling. |
| `src/assets/` | Logos, mascot artwork, favicon, and the generated social card. |
| `overrides/main.html` | Head additions, link previews and the listing block, applied to every page. |
| `overrides/home.html` | The landing page shell: its own footer, and the wrapper that keeps its sidebar to the mobile drawer. |
| `overrides/partials/` | The chrome, shadowed from the theme — `tabs.html`, `nav.html`, `footer.html` — plus the blog's own `post-byline.html`, `post-item.html` and `tags.html`. |
| `justfile` | Every command. `just` with no argument lists them. |

`docs/BLOG.md` covers the blog's implementation:
why it is templates rather than a plugin,
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
the blog reads that same tree to build its listings and feed,
so a post the tree doesn't reach is a post they can't see.
A hand-written list would have to name every post to stay correct,
and says nothing when it stops doing so.

## Things that fail quietly

Each of these has already cost someone an afternoon.

### A page title that stops matching

Five settings in `[project.extra]` address pages by their rendered title:
`nav_order`, `nav_collapse`, `nav_recent`, `nav_hide` and `nav_tabs`.
The match is character for character, em dash included.

None of them error on a title that matches nothing.
An unmatched `nav_order` entry drops the page to the end of the sidebar;
an unmatched `nav_tabs` entry removes the tab altogether.
Both build clean.

So renaming a page means grepping `zensical.toml` for its old title.
`just check-nav` covers the tab bar,
by comparing what the built page renders against the configured list.
The other four are on you.

### A bare colon in front matter

```yaml
description: Jupyter for agents: open source   # invalid YAML
```

That second colon makes the block invalid,
so the whole thing is discarded, `template:` along with it.
The page then renders with the wrong layout
while the build still prints "No issues found".
Quote any value containing a colon.

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

A post is a markdown file at `src/blog/<year>/<slug>.md` with the following front matter in `yaml` format:

```yaml
---
title: Your Post Title
date: 2026-08-15
authors:
  - example
tags:
  - engineering
description: One sentence. It carries the listing row, the link preview and the feed.
---
```

Your post's content is written in Markdown.

### Frontmatter notes

Lists go one item per line, not `[example]`.
`unresolved_references` validation reads a flow sequence as a markdown
reference link and fails the build looking for a definition of `[example]`.
The rest of the site writes them this way too.

Four of those five keys have a way of going wrong quietly,
which is what `just check-blog` is for.

`date` has to be exactly `YYYY-MM-DD`.
The feed appends a literal `T00:00:00Z` to it,
so a fuller datetime produces a timestamp no reader will parse.

`authors` are slugs from `[project.extra.authors]` in `zensical.toml`.
Order matters: only the first is credited as the fediverse creator,
because Mastodon attributes one author per page.
An unregistered slug does fail the build,
but the error reads `undefined value` and never names the slug.

`tags` each need a matching `src/tags/<tag>.md`.
Nothing at build time notices a missing one —
the chip still renders as a live link to a dead URL.

`description` is optional to the build and load-bearing everywhere else.
Without it the listing row and the feed entry both come out empty.

An `image:` key overrides the link preview image for that post.
Without one the post falls back to the site-wide card at `extra.og_image`,
which `just og-image` builds.

### Adding a blog author

To add an author, two files must be edited:

- `zensical.toml` needs an entry for the author in the `[project.extra.authors.<slug>]` table
- `src/authors/<slug>.md`

### Blog and author indexes

Neither directory's `index.md` is decorative:
the sidebar collapses each section onto its index,
and a section without one renders expanded instead.

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

Three things carry it, and they are configured separately.

The tab bar is `[[project.extra.nav_tabs]]`,
rendered by `overrides/partials/tabs.html`.
It is an editorial list, not a mirror of the top level:
adding `src/whatever.md` does not earn it a tab.
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
The blog reads the same derived tree for its listings and feed,
so the tree has to reach every post; deriving it guarantees that,
where a hand-written list only promises it.
See "Rules that break things silently" in `docs/BLOG.md` for what that costs.

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
`just og-image` composites the mascot onto brand cream at 1200x630,
so it stays in step with the artwork instead of drifting from it.
JPEG because the page never loads that file — only the crawlers building
link previews do, and their format support is narrower
and harder to verify than a browser's.
It carries no text: the title and description travel as their own meta tags,
and Fredoka is loaded from Google Fonts rather than installed,
so anything typeset here would depend on the machine that ran the recipe.

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

`--satyrn-orange` (`#c8722c`) is the brand orange,
but on cream it only reaches 3.16:1,
under the 4.5:1 that WCAG AA wants for body text.
Link text in light mode uses `--satyrn-orange-text` (`#9f5b23`) instead:
same hue and saturation, lower lightness, 4.67:1.
The brand orange is still used for non-text UI, which only needs 3:1.

Dark mode needs no equivalent.
Gold on ink is already 9.46:1.
