# Dev-only image: runs the Zensical live-reload server (`just serve-at`).
# Not used for production -- Cloudflare Pages builds `main` itself (see README).
FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim

# The project directory gets bind-mounted over at `docker run`, which would
# otherwise hide a venv installed under /app. Keep it outside the mount instead.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv

WORKDIR /app

# Install dependencies in their own layer so editing source doesn't invalidate
# this and force a re-download of zensical.
COPY pyproject.toml uv.lock ./
RUN uv sync --locked

COPY . .

EXPOSE 8000

# Binds 0.0.0.0 so the container accepts the forwarded connection; site_url
# ends up http://0.0.0.0:8000/, browse via http://localhost:8000.
#
# `uv run` rather than a bare `just`: rust-just is a dev dependency so it lives in the uv-managed venv at
# UV_PROJECT_ENVIRONMENT, not on PATH.
CMD ["uv", "run", "just", "serve-at", "0.0.0.0:8000"]
