# Valobot

A Discord bot for managing Valorant custom games — queue management and team splitting powered by discord.py Components v2.

[日本語版はこちら](README.ja.md)

---

## Features

- `/recruit` — Start a recruitment session with a live-updating embed
- **Join / Leave** — Players join or leave the queue via buttons
- **Split Teams** — Randomly splits queued players into two balanced teams
- **Reset** — Administrators can clear the queue at any time
- `/map-roulette` — Randomly selects a Valorant map with splash image (Standard / Skirmish / TDM modes)

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

# 4. Download map images (required for /map-roulette)
uv run python scripts/download_maps.py

# 5. Run the bot
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

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide — fork workflow, branch naming, code standards, and PR instructions.

---

## Map Images

Map splash images are **not** included in this repository (Riot Games copyright).
Run `scripts/download_maps.py` after cloning to download them from [valorant-api.com](https://valorant-api.com).
The images are used solely for in-Discord display and are not redistributed.

> All game assets belong to Riot Games. This project is not affiliated with or endorsed by Riot Games.

---

## Map Images

Map splash images are **not** included in this repository (Riot Games copyright).
Run `scripts/download_maps.py` after cloning to download them from [valorant-api.com](https://valorant-api.com).
The images are used solely for in-Discord display and are not redistributed.

> All game assets belong to Riot Games. This project is not affiliated with or endorsed by Riot Games.

---

## License

[MIT](LICENSE)
