from discord.ext import commands
import discord
import time

class ExpiringView(discord.ui.View):
    _interaction: discord.Interaction = None
    _expires_epoch: float = None

    def __init__(self, timeout=None, client=None):
        self.client: commands.Bot = client
        super().__init__(timeout=timeout)

    async def on_timeout(self) -> None:
        await self.disable_buttons()

        return await super().on_timeout()

    async def interaction_check(self, interaction: discord.Interaction[discord.Client]) -> bool:
        if self._expires_epoch:
            self.timeout = self._expires_epoch - time.time()

        return await super().interaction_check(interaction)

    async def disable_buttons(self):
        for child in self.children:
            if type(child) == discord.ui.Button:
                child.disabled = True

        if type(self._interaction) == discord.Interaction:
            await self._interaction.edit_original_response(view=self)
        elif type(self._interaction == discord.Message):
            await self._interaction.edit(view=self)
