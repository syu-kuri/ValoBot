"""Cog for the Valorant map roulette feature."""

import random
from enum import Enum
from functools import partial
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands

# Directory that holds map splash images
MAP_IMAGE_DIR = Path(__file__).parent.parent / "assets" / "maps"

# All released standard maps
_STANDARD_MAPS: list[str] = [
    "Ascent",
    "Abyss",
    "Bind",
    "Breeze",
    "Fracture",
    "Haven",
    "Icebox",
    "Lotus",
    "Pearl",
    "Split",
    "Sunset",
]

# Team Deathmatch exclusive maps
_TDM_MAPS: list[str] = [
    "District",
    "Drift",
    "Kasbah",
    "Piazza",
]

# Skirmish exclusive maps
_SKIRMISH_MAPS: list[str] = [
    "Skirmish A",
    "Skirmish B",
    "Skirmish C",
]

# Map name → image filename (place files under assets/maps/)
MAP_IMAGE_FILES: dict[str, str] = {
    # Standard
    "Ascent": "ascent.png",
    "Abyss": "abyss.png",
    "Bind": "bind.png",
    "Breeze": "breeze.png",
    "Fracture": "fracture.png",
    "Haven": "haven.png",
    "Icebox": "icebox.png",
    "Lotus": "lotus.png",
    "Pearl": "pearl.png",
    "Split": "split.png",
    "Sunset": "sunset.png",
    # Team Deathmatch
    "District": "district.png",
    "Drift": "drift.png",
    "Kasbah": "kasbah.png",
    "Piazza": "piazza.png",
    # Skirmish (all three share the same splash image)
    "Skirmish A": "skirmish.png",
    "Skirmish B": "skirmish.png",
    "Skirmish C": "skirmish.png",
}


class GameMode(Enum):
    """Available game modes for the map roulette."""

    STANDARD = "Standard"
    SKIRMISH = "Skirmish"
    TDM = "Team Deathmatch"


MAPS_BY_MODE: dict[GameMode, list[str]] = {
    GameMode.STANDARD: _STANDARD_MAPS,
    GameMode.SKIRMISH: _SKIRMISH_MAPS,
    GameMode.TDM: _TDM_MAPS,
}

MODE_COLORS: dict[GameMode, discord.Color] = {
    GameMode.STANDARD: discord.Color.blurple(),
    GameMode.SKIRMISH: discord.Color.orange(),
    GameMode.TDM: discord.Color.red(),
}


class MapRouletteView(discord.ui.LayoutView):
    """Components v2 view for the map roulette.

    Manages three display states:
    1. Mode selection — user picks Standard / Skirmish / Team Deathmatch.
    2. Map pool     — shows available maps with a Spin button.
    3. Result       — shows the selected map with its local splash image.
    """

    def __init__(self) -> None:
        """Initialize the view in mode-selection state."""
        super().__init__(timeout=None)
        self._mode: GameMode | None = None
        self._selected: str | None = None
        self._build()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _maps(self) -> list[str]:
        """Return the map list for the current mode."""
        return [] if self._mode is None else MAPS_BY_MODE[self._mode]

    def _color(self) -> discord.Color:
        """Return the accent color for the current mode."""
        return discord.Color.blurple() if self._mode is None else MODE_COLORS[self._mode]

    def _image_file(self) -> discord.File | None:
        """Return a discord.File for the selected map image, or None if unavailable.

        Returns:
            A File ready to attach, or None when no image exists locally.
        """
        if self._selected is None:
            return None
        filename = MAP_IMAGE_FILES.get(self._selected)
        if filename is None:
            return None
        path = MAP_IMAGE_DIR / filename
        return discord.File(path, filename=filename) if path.exists() else None

    def _change_mode_button(self) -> discord.ui.Button["MapRouletteView"]:
        """Build the shared Change Mode button."""
        btn: discord.ui.Button[MapRouletteView] = discord.ui.Button(
            label="Change Mode",
            style=discord.ButtonStyle.secondary,
            custom_id="mr:change_mode",
        )
        btn.callback = self._on_change_mode
        return btn

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def _build(self) -> None:
        """Rebuild the component tree based on the current state."""
        self.clear_items()
        if self._mode is None:
            self._build_mode_selection()
        elif self._selected is None:
            self._build_map_pool()
        else:
            self._build_result()

    def _build_mode_selection(self) -> None:
        """Build the mode selection state."""
        standard_btn: discord.ui.Button[MapRouletteView] = discord.ui.Button(
            label="Standard",
            style=discord.ButtonStyle.primary,
            custom_id="mr:mode:standard",
        )
        skirmish_btn: discord.ui.Button[MapRouletteView] = discord.ui.Button(
            label="Skirmish",
            style=discord.ButtonStyle.secondary,
            custom_id="mr:mode:skirmish",
        )
        tdm_btn: discord.ui.Button[MapRouletteView] = discord.ui.Button(
            label="Team Deathmatch",
            style=discord.ButtonStyle.secondary,
            custom_id="mr:mode:tdm",
        )

        standard_btn.callback = partial(self._on_mode_select, mode=GameMode.STANDARD)
        skirmish_btn.callback = partial(self._on_mode_select, mode=GameMode.SKIRMISH)
        tdm_btn.callback = partial(self._on_mode_select, mode=GameMode.TDM)

        self.add_item(
            discord.ui.Container(
                discord.ui.TextDisplay("## 🗺️ Map Roulette\nSelect a game mode to get started."),
                discord.ui.Separator(visible=True),
                discord.ui.ActionRow(standard_btn, skirmish_btn, tdm_btn),
                accent_color=discord.Color.blurple(),
            )
        )

    def _build_map_pool(self) -> None:
        """Build the map pool state for the selected mode."""
        assert self._mode is not None

        maps = self._maps()
        map_text = (
            "\n".join(f"• {m}" for m in maps) if maps else "*No maps available for this mode.*"
        )

        spin_btn: discord.ui.Button[MapRouletteView] = discord.ui.Button(
            label="Spin",
            style=discord.ButtonStyle.success,
            emoji="🎰",
            custom_id="mr:spin",
            disabled=not maps,
        )
        spin_btn.callback = self._on_spin

        self.add_item(
            discord.ui.Container(
                discord.ui.TextDisplay(
                    f"## 🗺️ Map Roulette — {self._mode.value}\n**Map Pool**\n{map_text}"
                ),
                discord.ui.Separator(visible=True),
                discord.ui.ActionRow(spin_btn, self._change_mode_button()),
                accent_color=self._color(),
            )
        )

    def _build_result(self) -> None:
        """Build the result state showing the selected map and its image."""
        assert self._mode is not None
        assert self._selected is not None

        spin_again_btn: discord.ui.Button[MapRouletteView] = discord.ui.Button(
            label="Spin Again",
            style=discord.ButtonStyle.success,
            emoji="🎰",
            custom_id="mr:spin",
        )
        spin_again_btn.callback = self._on_spin

        header = f"## 🗺️ Map Roulette — {self._mode.value}\n### 🎯 Selected Map\n# {self._selected}"

        filename = MAP_IMAGE_FILES.get(self._selected)
        has_image = filename is not None and (MAP_IMAGE_DIR / filename).exists()

        if has_image:
            self.add_item(
                discord.ui.Container(
                    discord.ui.Section(
                        discord.ui.TextDisplay(header),
                        accessory=discord.ui.Thumbnail(media=f"attachment://{filename}"),
                    ),
                    discord.ui.Separator(visible=True),
                    discord.ui.ActionRow(spin_again_btn, self._change_mode_button()),
                    accent_color=self._color(),
                )
            )
        else:
            self.add_item(
                discord.ui.Container(
                    discord.ui.TextDisplay(header),
                    discord.ui.Separator(visible=True),
                    discord.ui.ActionRow(spin_again_btn, self._change_mode_button()),
                    accent_color=self._color(),
                )
            )

    # ------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------

    async def _on_mode_select(self, interaction: discord.Interaction, *, mode: GameMode) -> None:
        """Handle mode selection buttons.

        Args:
            interaction: The button interaction.
            mode: The game mode that was selected.
        """
        self._mode = mode
        self._selected = None
        self._build()
        await interaction.response.edit_message(view=self, attachments=[])

    async def _on_spin(self, interaction: discord.Interaction) -> None:
        """Handle the Spin / Spin Again button press.

        Args:
            interaction: The button interaction.
        """
        maps = self._maps()
        if not maps:
            await interaction.response.send_message(
                "No maps available for this mode.", ephemeral=True
            )
            return

        self._selected = random.choice(maps)
        self._build()

        file = self._image_file()
        await interaction.response.edit_message(
            view=self,
            attachments=[file] if file else [],
        )

    async def _on_change_mode(self, interaction: discord.Interaction) -> None:
        """Handle the Change Mode button; return to mode selection.

        Args:
            interaction: The button interaction.
        """
        self._mode = None
        self._selected = None
        self._build()
        await interaction.response.edit_message(view=self, attachments=[])


class MapRoulette(commands.Cog):
    """Provides the Valorant map roulette slash command."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the MapRoulette cog.

        Args:
            bot: The running Bot instance.
        """
        self.bot = bot

    @app_commands.command(name="map-roulette", description="Spin to pick a random Valorant map.")
    async def map_roulette(self, interaction: discord.Interaction) -> None:
        """Start the map roulette.

        Args:
            interaction: The interaction triggered by the slash command.
        """
        await interaction.response.send_message(view=MapRouletteView())


async def setup(bot: commands.Bot) -> None:
    """Load the MapRoulette cog into the bot.

    Args:
        bot: The running Bot instance.
    """
    await bot.add_cog(MapRoulette(bot))
