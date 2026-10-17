---
title: Design system
search:
  exclude: true
---

# Design system

A living specimen, rendered through the **real** site CSS — every size, colour,
weight and component below is exactly what ships. Hidden from nav and search.
Toggle light/dark with the header switch to check both schemes.

## Typography

The scale is a **golden-derived modular scale**: the ratio between steps is
√φ ≈ **1.272**, so every _two_ steps make a full golden ratio (φ). One variable,
`--type-ratio`, reshapes the whole ladder; `--type-base` sets body size
(1rem = 20px at the theme's default root).

### The scale

<h1>Heading 1 — ~52px, display face</h1>
<h2>Heading 2 — ~41px, display face</h2>
<h3>Heading 3 — ~32px, body face</h3>
<h4>Heading 4 — ~25px, body face</h4>
<h5>Heading 5 — 20px, body face</h5>
<h6>Heading 6 — ~16px, body face</h6>

### Body copy

Running body copy at `--fs-body` (20px) with `--lh-body` (1.55) leading. It
carries **bold emphasis** at the single `--weight-emphasis` (700), _italic
emphasis_, an [inline link](/design/typography/) with its blue underline, and
`inline code`. A second sentence shows the rhythm between lines and the natural
measure of the text face.

<p style="color: var(--md-default-fg-color--light)">Muted secondary text —
<code>--md-default-fg-color--light</code>. Used for dates, meta and captions,
one tier down from body without changing size.</p>

<p><strong>Bold body text</strong> at the emphasis weight, beside regular body
text, so the contrast between 400 and 700 is visible in one line.</p>

- Unordered list item at body size
- Item with an [inline link](/design/typography/)

1. Ordered item one
2. Ordered item two

> A blockquote — one step up from body and italic, so a pull quote reads as its
> own voice rather than indented body copy.

```python
def golden(n: float, ratio: float = 1.272) -> float:
    return n * ratio
```

## Colour

Swatches read the live tokens, so they follow the current scheme.

### Brand hues (light / mid / dark)

<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.5rem;max-width:32rem">
  <div style="height:3rem;border-radius:.4rem;background:var(--satyrn-yellow-dark)"></div>
  <div style="height:3rem;border-radius:.4rem;background:var(--satyrn-yellow-ui)"></div>
  <div style="height:3rem;border-radius:.4rem;background:var(--satyrn-yellow-text)"></div>
  <div style="height:3rem;border-radius:.4rem;background:var(--satyrn-blue-light)"></div>
  <div style="height:3rem;border-radius:.4rem;background:var(--satyrn-blue-mid)"></div>
  <div style="height:3rem;border-radius:.4rem;background:var(--satyrn-blue-dark)"></div>
  <div style="height:3rem;border-radius:.4rem;background:var(--satyrn-pink-light)"></div>
  <div style="height:3rem;border-radius:.4rem;background:var(--satyrn-pink-mid)"></div>
  <div style="height:3rem;border-radius:.4rem;background:var(--satyrn-pink-dark)"></div>
  <div style="height:3rem;border-radius:.4rem;background:var(--satyrn-green-light)"></div>
  <div style="height:3rem;border-radius:.4rem;background:var(--satyrn-green-mid)"></div>
  <div style="height:3rem;border-radius:.4rem;background:var(--satyrn-green-dark)"></div>
</div>

Rows: yellow · blue · pink · green. Only **yellow** (UI) and **blue** (link
underline) are wired to anything today; pink and green are staged for later.

### Text & surfaces

<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.5rem;max-width:32rem">
  <div style="height:3rem;border-radius:.4rem;border:1px solid var(--satyrn-border);background:var(--md-default-bg-color)"></div>
  <div style="height:3rem;border-radius:.4rem;background:var(--satyrn-surface)"></div>
  <div style="height:3rem;border-radius:.4rem;background:var(--md-typeset-color)"></div>
</div>

Page background · surface · body-text colour.

## Components

### Buttons (current)

[Button](/design/typography/){ .md-button }
[Primary button](/design/typography/){ .md-button .md-button--primary }

### CTA button

**Filled blue, white label (4.68:1 — no yellow)**, with an offset outline echo
down-right it presses onto on hover. Styled on `.md-typeset a.satyrn-cta` — one
notch above the theme's `.md-typeset a`, which is what reliably beats its yellow
link colour across browsers.

<a class="satyrn-cta" href="/design/typography/">Get started</a>

### Arrow link ("more →")

[Read the mission](/design/typography/){ .satyrn-arrow-link }

### Pillar cards

<div class="grid cards satyrn-pillars" markdown>

- ### Open Source

    Every line is public. Fork it, audit it, ship it — no black boxes.

- ### Community-Owned

    Built by the people who use it, governed in the open, not owned by a
    single vendor. No paid hosted tier we steer you towards. No token.

- ### Local-First

    Built to run on your machine, on your terms.
    A provider outage is someone else's bad day.

- ### European

    Satyrn is a foundation created in the European Union.

</div>

### Contributor row

<div class="satyrn-crew" role="region" aria-label="Satyrn contributors" tabindex="0" markdown>

- ![Carol Willing](/assets/avatars/contributors/willingc.jpg){ width="64" height="64" loading="lazy" }
- ![Emma Cooke](/assets/avatars/contributors/emmaco.jpg){ width="64" height="64" loading="lazy" }
- ![Laura Summers](/assets/avatars/contributors/summerscope.jpg){ width="64" height="64" loading="lazy" }
- ![Paul Everitt](/assets/avatars/contributors/pauleveritt.jpg){ width="64" height="64" loading="lazy" }
- ![Daria Grudzien](/assets/avatars/contributors/dariagrudzien.jpg){ width="64" height="64" loading="lazy" }
- ![Mike Fiedler](/assets/avatars/contributors/miketheman.jpg){ width="64" height="64" loading="lazy" }
- [![You](/assets/avatars/you.svg){ width="64" height="64" loading="lazy" }You?](/get-involved/){ .satyrn-crew__you }

</div>

### Blog listing row

One row of the blog index, as Zensical's blog plugin emits it,
trimmed to a single post.
Its `article`, `header` and `nav` are `div`s here,
since the lint allows only the elements real pages need;
the styling hangs on the classes alone.
The author name is our hook, `.satyrn-post-author`,
set in the handwritten face.

<div class="md-post md-post--excerpt">
  <div class="md-post__header">
    <div class="md-post__authors md-typeset">
      <span class="md-author"><img src="/assets/avatars/contributors/willingc.jpg" alt="" width="128" height="128"></span>
      <a class="satyrn-post-author" href="/design/typography/">Carol Willing</a>
    </div>
    <div class="md-post__meta md-meta">
      <ul class="md-meta__list">
        <li class="md-meta__item"><time datetime="2026-08-15">August 15, 2026</time></li>
        <li class="md-meta__item">in <a href="/design/typography/" class="md-meta__link">Announcements</a></li>
        <li class="md-meta__item">3 min read</li>
      </ul>
    </div>
  </div>
  <div class="md-post__content md-typeset">
    <h2><a class="toclink" href="/design/typography/">Introducing Satyrn Zen and our Team Compass</a></h2>
    <p>Welcome to Satyrn where we care about sharing knowledge and empowering you on your journey with "trusted and transparent" AI.</p>
    <div class="md-post__action">
      <a href="/design/typography/">Continue reading</a>
    </div>
  </div>
</div>

### Tags

<p class="md-tags"><a href="/design/typography/" class="md-tag">education</a> <a href="/design/typography/" class="md-tag">governance</a> <a href="/design/typography/" class="md-tag">announcements</a> <a href="/design/typography/" class="md-tag">community</a></p>

Hover a tag for its active (yellow) state.

### Admonitions

!!! note
    A note admonition — body-sized text in a titled container.

!!! warning "Still being written"
    A warning admonition, used for work-in-progress notes.

### Table

| Column A | Column B | Column C |
| --- | --- | --- |
| cell | cell | cell |
| cell | cell | cell |
