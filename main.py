import asyncio
import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

COGS_DIR = Path(__file__).parent / "cogs"


class Valobot(commands.Bot):
    """Main bot class for Valobot."""

    def __init__(self) -> None:
        """Initialize the bot with required intents."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self) -> None:
        """Load all cogs from the cogs directory and sync slash commands."""
        for cog_file in COGS_DIR.glob("*.py"):
            if cog_file.stem.startswith("_"):
                continue

            extension = f"cogs.{cog_file.stem}"

            try:
                await self.load_extension(extension)
                print(f"Loaded extension: {extension}")
            except Exception as e:
                print(f"Failed to load extension {extension}: {e}")

        await self.tree.sync()

    async def on_ready(self) -> None:
        """Handle the bot ready event."""
        print(f"Logged in as {self.user} (ID: {self.user.id})")


async def main() -> None:
    """Start the bot."""
    token = os.getenv("DISCORD_TOKEN")

    if not token:
        raise ValueError("DISCORD_TOKEN is not set in the environment")

    async with Valobot() as bot:
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
