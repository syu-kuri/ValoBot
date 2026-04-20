# Contributing to Valobot

Thank you for your interest in contributing!
This guide covers everything you need to get started as an external contributor.

---

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/<your-username>/valobot.git
cd valobot
```

### 2. Set Up the Development Environment

```bash
# Install dependencies
uv sync

# Configure environment variables
cp .env.sample .env
# Edit .env and set your DISCORD_TOKEN

# Download map images (required for /map-roulette)
uv run python scripts/download_maps.py
```

### 3. Create a Branch

All branches must be cut from `staging`.
Open a PR targeting **this repository's `staging` branch** — not `main`.

```bash
git remote add upstream https://github.com/syu-kuri/valobot.git
git fetch upstream
git checkout -b feature/your-feature-name upstream/staging
```

Branch naming conventions:

| Type | Pattern | Example |
|---|---|---|
| New feature | `feature/<short-description>` | `feature/rank-based-team-split` |
| Bug fix | `fix/<short-description>` | `fix/join-button-no-response` |
| Documentation | `docs/<short-description>` | `docs/update-readme` |
| Refactoring | `refactor/<short-description>` | `refactor/queue-view-cleanup` |
| Chore | `chore/<short-description>` | `chore/update-dependencies` |

---

## Code Standards

- All docstrings, comments, and type annotations must be written in **English**
- Every function and class must have a docstring
- All function signatures must include type annotations
- No tests are required — this project has no test suite
- No type checker (mypy) — ruff lint only

### Running the Linter

Run this before opening a PR:

```bash
uv run ruff check .
uv run ruff format --check .
```

---

## Opening a Pull Request

1. Push your branch to your fork
2. Open a PR from your fork's branch targeting **`staging`** on this repository
3. Fill in the PR template — all fields are required

```bash
git push origin feature/your-feature-name
# Then open a PR on GitHub targeting syu-kuri/valobot:staging
```

---

## Architecture Notes

- One Cog per feature domain in `cogs/` — file name reflects the domain (e.g. `team.py`)
- Place shared logic in `utils/` only when it is used across multiple Cogs
- All UI must use Components v2 (`discord.ui.LayoutView`)
- Each feature exposes **exactly one slash command** as its entry point
- All subsequent operations are handled by **buttons on the embed**
- Slash commands only — no prefix commands

---

## Questions

For general questions, please use [GitHub Discussions](https://github.com/syu-kuri/valobot/discussions) rather than opening an issue.
