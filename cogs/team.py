import random
import uuid

import discord
from discord import app_commands
from discord.ext import commands

MIN_PLAYERS = 2
QUEUE_CAPACITY = 10


class QueueView(discord.ui.LayoutView):
    """Interactive Components v2 view for the custom game queue."""

    def __init__(self) -> None:
        """Initialize the queue view with an empty queue and a unique session ID."""
        super().__init__(timeout=None)
        self._session_id: str = uuid.uuid4().hex
        self._queue: list[discord.Member] = []
        self._rebuild()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _in_queue(self, member: discord.Member) -> bool:
        """Return True if the member is already in the queue.

        Args:
            member: The Discord member to check.
        """
        return any(m.id == member.id for m in self._queue)

    def _rebuild(self) -> None:
        """Rebuild the Components v2 component tree to reflect current queue state."""
        self.clear_items()

        sid = self._session_id
        join_btn: discord.ui.Button[QueueView] = discord.ui.Button(
            label="Join",
            style=discord.ButtonStyle.primary,
            emoji="✅",
            custom_id=f"queue:join:{sid}",
        )
        leave_btn: discord.ui.Button[QueueView] = discord.ui.Button(
            label="Leave",
            style=discord.ButtonStyle.secondary,
            emoji="🚪",
            custom_id=f"queue:leave:{sid}",
        )
        start_btn: discord.ui.Button[QueueView] = discord.ui.Button(
            label="Split Teams",
            style=discord.ButtonStyle.success,
            emoji="⚔️",
            custom_id=f"queue:start:{sid}",
        )
        reset_btn: discord.ui.Button[QueueView] = discord.ui.Button(
            label="Reset",
            style=discord.ButtonStyle.danger,
            emoji="🔄",
            custom_id=f"queue:reset:{sid}",
        )

        join_btn.callback = self._on_join
        leave_btn.callback = self._on_leave
        start_btn.callback = self._on_start
        reset_btn.callback = self._on_reset

        player_lines = (
            "\n".join(f"`{i + 1}.` {m.display_name}" for i, m in enumerate(self._queue))
            if self._queue
            else "*No players yet. Press **Join** to enter the queue!*"
        )

        self.add_item(
            discord.ui.Container(
                discord.ui.TextDisplay(
                    f"## 🎮 Custom Game — Recruiting\n`{len(self._queue)} / {QUEUE_CAPACITY}` players"
                ),
                discord.ui.Separator(visible=True),
                discord.ui.TextDisplay(player_lines),
                discord.ui.Separator(visible=True),
                discord.ui.ActionRow(join_btn, leave_btn, start_btn, reset_btn),
                accent_color=discord.Color.blurple(),
            )
        )

    # ------------------------------------------------------------------
    # Button callbacks
    # ------------------------------------------------------------------

    async def _on_join(self, interaction: discord.Interaction) -> None:
        """Handle the Join button press.

        Args:
            interaction: The button interaction.
        """
        if not isinstance(interaction.user, discord.Member):
            return

        member: discord.Member = interaction.user
        if self._in_queue(member):
            await interaction.response.send_message("You are already in the queue.", ephemeral=True)
            return
        if len(self._queue) >= QUEUE_CAPACITY:
            await interaction.response.send_message("The queue is full.", ephemeral=True)
            return

        self._queue.append(member)
        self._rebuild()
        await interaction.response.edit_message(view=self)

    async def _on_leave(self, interaction: discord.Interaction) -> None:
        """Handle the Leave button press.

        Args:
            interaction: The button interaction.
        """
        if not isinstance(interaction.user, discord.Member):
            return

        member: discord.Member = interaction.user
        if not self._in_queue(member):
            await interaction.response.send_message("You are not in the queue.", ephemeral=True)
            return

        self._queue = [m for m in self._queue if m.id != member.id]
        self._rebuild()
        await interaction.response.edit_message(view=self)

    async def _on_start(self, interaction: discord.Interaction) -> None:
        """Handle the Start button press; split players into two random teams.

        Args:
            interaction: The button interaction.
        """
        if len(self._queue) < MIN_PLAYERS:
            await interaction.response.send_message(
                f"At least **{MIN_PLAYERS}** players are required to split teams.",
                ephemeral=True,
            )
            return

        shuffled = self._queue[:]
        random.shuffle(shuffled)
        mid = len(shuffled) // 2
        team_a, team_b = shuffled[:mid], shuffled[mid:]

        await interaction.response.edit_message(view=TeamsView(team_a, team_b))

    async def _on_reset(self, interaction: discord.Interaction) -> None:
        """Handle the Reset button press. Restricted to administrators.

        Args:
            interaction: The button interaction.
        """
        if not isinstance(interaction.user, discord.Member):
            return

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "Only administrators can reset the queue.", ephemeral=True
            )
            return

        self._queue.clear()
        self._rebuild()
        await interaction.response.edit_message(view=self)


class TeamsView(discord.ui.LayoutView):
    """Components v2 view that displays the two generated teams."""

    def __init__(
        self,
        team_a: list[discord.Member],
        team_b: list[discord.Member],
    ) -> None:
        """Initialize the teams view.

        Args:
            team_a: Members assigned to Team A.
            team_b: Members assigned to Team B.
        """
        super().__init__(timeout=None)
        self._session_id: str = uuid.uuid4().hex
        self._team_a = team_a
        self._team_b = team_b
        self._build()

    def _build(self) -> None:
        """Build the Components v2 layout for the teams display."""
        new_queue_btn: discord.ui.Button[TeamsView] = discord.ui.Button(
            label="New Queue",
            style=discord.ButtonStyle.primary,
            emoji="🔄",
            custom_id=f"teams:new_queue:{self._session_id}",
        )
        new_queue_btn.callback = self._on_new_queue

        team_a_lines = "\n".join(f"• {m.display_name}" for m in self._team_a)
        team_b_lines = "\n".join(f"• {m.display_name}" for m in self._team_b)

        self.add_item(
            discord.ui.Container(
                discord.ui.TextDisplay("## ⚔️ Teams are set! Good luck!"),
                discord.ui.Separator(visible=True),
                discord.ui.TextDisplay(f"### 🔴 Team A\n{team_a_lines}"),
                discord.ui.Separator(visible=False),
                discord.ui.TextDisplay(f"### 🔵 Team B\n{team_b_lines}"),
                discord.ui.Separator(visible=True),
                discord.ui.ActionRow(new_queue_btn),
                accent_color=discord.Color.green(),
            )
        )

    async def _on_new_queue(self, interaction: discord.Interaction) -> None:
        """Handle the New Queue button; transition back to a fresh QueueView.

        Args:
            interaction: The button interaction.
        """
        await interaction.response.edit_message(view=QueueView())


class Team(commands.Cog):
    """Manages the custom game queue and team splitting."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the Team cog.

        Args:
            bot: The running Bot instance.
        """
        self.bot = bot

    @app_commands.command(name="recruit", description="Start a custom game recruitment.")
    async def recruit(self, interaction: discord.Interaction) -> None:
        """Start a custom game recruitment session.

        Args:
            interaction: The interaction triggered by the slash command.
        """
        await interaction.response.send_message(view=QueueView())


async def setup(bot: commands.Bot) -> None:
    """Load the Team cog into the bot.

    Args:
        bot: The running Bot instance.
    """
    await bot.add_cog(Team(bot))
