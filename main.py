import asyncio
import logging
import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

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
                logger.info("Loaded extension: %s", extension)
            except Exception as e:
                logger.error("Failed to load extension %s: %s", extension, e)

        await self.tree.sync()

    async def on_ready(self) -> None:
        """Handle the bot ready event."""
        logger.info("Logged in as %s (ID: %s)", self.user, self.user.id)


async def main() -> None:
    """Start the bot."""
    token = os.getenv("DISCORD_TOKEN")

    if not token:
        raise ValueError("DISCORD_TOKEN is not set in the environment")

    async with Valobot() as bot:
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
