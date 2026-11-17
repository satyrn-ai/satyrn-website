# AGENTS.md

Read `CONTRIBUTING.md` before changing anything: it holds the project's
conventions and the failures that build green, and it wins over this file.
`docs/BLOG.md` explains the blog, and the `justfile` documents every recipe
(`just` lists them).

- `just ci` is the whole gate; there is no test suite.
- `just lint` covers `src/**/*.md` and the root `*.md` files, this one
  included, so it is spell-checked in British English. Nothing under `docs/`
  is checked.
- `overrides/main.html` must extend `base.html`. Templates resolve
  `overrides/` before the theme, so extending `main.html` from it resolves to
  itself and fails with an inheritance cycle. Other overrides extend
  `main.html`.
- Commit messages use Conventional Commits (`feat(blog): ...`, `fix: ...`,
  `chore(lint): ...`).
