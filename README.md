# Valobot

A Discord bot for managing Valorant custom games — queue management and team splitting powered by discord.py Components v2.

[日本語版はこちら](README.ja.md)

---

## Features

- `/recruit` — Start a recruitment session with a live-updating embed
- **Join / Leave** — Players join or leave the queue via buttons
- **Split Teams** — Randomly splits queued players into two balanced teams
- **Reset** — Administrators can clear the queue at any time

---

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- A Discord bot token ([Discord Developer Portal](https://discord.com/developers/applications))

---

## Setup

```bash
# 1. Clone the repository
git clone https://github.com/syu-kuri/valobot.git
cd valobot

# 2. Install dependencies
uv sync

# 3. Configure environment variables
cp .env.sample .env
# Edit .env and set your DISCORD_TOKEN

# 4. Run the bot
uv run python main.py
```

---

## Reporting an Issue

1. Search [existing issues](../../issues) to avoid duplicates.
2. Click **New Issue** and choose the appropriate template:
   - **Bug Report** — Something is broken or behaving unexpectedly.
   - **Feature Request** — You have an idea for a new feature or improvement.
3. Fill in all required fields and submit.

> For general questions, please use [GitHub Discussions](../../discussions) instead of opening an issue.

---

## Requesting a Code Change (Pull Request)

### Branch Naming Rules

All branches must be cut from `staging`. **Direct pushes to `main` are prohibited.**

| Type | Pattern | Example |
|---|---|---|
| New feature | `feature/<short-description>` | `feature/rank-based-team-split` |
| Bug fix | `fix/<short-description>` | `fix/join-button-no-response` |
| Documentation | `docs/<short-description>` | `docs/update-readme` |
| Refactoring | `refactor/<short-description>` | `refactor/queue-view-cleanup` |
| Chore | `chore/<short-description>` | `chore/update-dependencies` |

### Workflow

```bash
# 1. Create a branch from staging
git checkout staging
git checkout -b feature/your-feature-name

# 2. Make your changes, then commit
git add <files>
git commit -m "Short description of what and why"

# 3. Push and open a Pull Request targeting staging
git push origin feature/your-feature-name
```

### Code Standards

- All docstrings, comments, and type annotations must be written in **English**
- Every function and class must have a docstring
- All function signatures must include type annotations
- Run lint check before opening a PR:

```bash
uv run ruff check .
uv run ruff format --check .
```

---

## License

MIT
