from discord import app_commands
from discord.ext import commands
import discord


class MarketItemView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    

    @discord.ui.button(label="Purchase", custom_id="market_item:purchase", style=discord.ButtonStyle.green)
    async def purchase(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message(f"{interaction.user.mention} button click detected.")
