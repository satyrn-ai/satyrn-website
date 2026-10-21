# Contributing Guidelines

Run `just ci` before opening a pull request.
CI runs the same recipe, and `just` lists what each check does.
The build is strict, so a broken link or anchor fails it.

`docs/BLOG.md` covers how the blog is put together.
Read it before changing anything under `overrides/`.

## Language and spelling

Write in British English: "behaviour", "colour", "organisation".
`just lint` checks it with cspell, so an American spelling fails CI.
New technical words go in `.vscode/cspell.json`.

## Voice

The site should sound like the people building Satyrn, talking to developers.
Aim for the tone of Django's or the kernel's contributor docs.

- Name what the reader deals with.
  "A provider outage is someone else's bad day" beats "resilient and reliable".
  Cut "trust", "innovative", "seamless" and "enterprise scale"
  unless something specific follows.
- A short negative ("Not a hosted service.") lands faster than another claim.
  Only use one you would still stand by in a year.
- Never publish a number without its method: hardware, dataset, what it lost on.
  Never promise a behaviour (telemetry, data, governance) that the code or the
  Team Compass doesn't already back up.
- Buttons say what happens next:
  "Run an experiment" or "Browse open issues", not "Learn more".
- Humour is dry and rare, and never carries a fact.
  If a line needs a shared idiom to land, it can't hold anything important.
  No emoji bullet lists, no "vibrant community", no cosmic mission copy.

## Things that fail quietly

### Renaming a page

`nav_order`, `nav_collapse`, `nav_hide` and `nav_menu` in `zensical.toml`
match pages by rendered title, character for character.
A title that matches nothing is not an error: the page drops to the end of the
sidebar, or out of the menu bar.
After renaming a page, grep `zensical.toml` for its old title.
`just check-nav` covers the menu bar only.

### A bare colon in front matter

```yaml
description: Jupyter for agents: open source   # invalid YAML
```

The whole block is discarded, `template:` with it,
and the build still reports success.
Quote any value containing a colon.
`just check-frontmatter` catches it.

## Accessibility

Treat this as part of done.
`just lint` catches missing alt text and nothing else here.

- Every `<img>` needs an `alt`.
  Describe content images.
  Use `alt=""` for decorative ones, or when adjacent text already says the same thing.
  A missing `alt` makes a screen reader read the filename.
- `width` and `height` must match the file's real pixel dimensions,
  or the layout shifts as the image loads.
- A link inside a sentence needs an underline; colour alone doesn't mark it.
- An icon-only link needs `aria-label`.
  An image inside a link needs `alt` naming the destination, not the picture.
- Use a real element (`<nav>`, `<main>`, `<footer>`) before ARIA.
  Pages already carry several `<nav>` landmarks, so label any you add.
- Interactive targets are at least 24x24px, except links inline in a sentence.
- Focus stays visible.
- Nothing decorative sits behind text.
  Nothing moves on a loop, everything stops under `prefers-reduced-motion`,
  and anything moving for more than five seconds needs a pause control.

Before you call it done, check both colour schemes, widths from 320px up,
tab through it, and measure contrast rather than eyeballing it.

## Marking unfinished work

Use an admonition, not an HTML comment, which the reader can't see:

```markdown
!!! warning "Still being written"

    What is provisional, and what will change.
```

## Writing a blog post

A post is `src/blog/posts/<file>.md`:

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

It builds to `/blog/<year>/<file>/`, so renaming the file moves the post.

- Write lists one item per line, not `[example]`.
  Reference validation reads a flow sequence as a markdown link and fails the build.
- `<!-- more -->` is required; a post without one fails the build.
- `date` is plain `YYYY-MM-DD`.
- `authors` are slugs from `src/blog/.authors.yml`.
  List every author.
- `categories` must come from `categories_allowed` in `zensical.toml`.
- `tags` are free text and need no file.
- `description` is required by `just check-blog`.
- `draft: true` leaves the post out everywhere.
- `image:` overrides the link preview image for that post.

### Adding a blog author

Add an entry to `src/blog/.authors.yml` with `name`, `avatar` and a one-line
`description`, all required.
Leave `url` out: with it set, author names link off-site instead of to the profile.

Write the bio in `src/blog/author/<slug>.md`.
Its front matter needs a quoted `description`, such as `"Posts by Carol Willing."`,
which becomes the profile's link-preview text.

## CSS

The conventions are in the header comment of `src/stylesheets/satyrn.css`.

Most rules don't need a `.md-typeset` prefix to beat the theme:
its typeset rules are single-class specificity and this stylesheet loads after them.
Add specificity only after watching a rule lose.

Style the concept, not the instance.
A rule written for the one element that needed it misses every other place
the same thing shows up.

## Fonts

The Triple Charm faces are licensed with a monthly page-view cap.
Read `docs/fonts.md` before adding a face or changing how they are served.
