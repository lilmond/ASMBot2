from command_views import expiring_views
from components import custom_response
from discord.ext import commands
import discord
import json

CONFIG = json.load(open("config.json", "r"))

class PurgeView(discord.ui.View):
    def __init__(self, client: commands.Bot):
        self.client = client
        super().__init__(timeout=10)
    
    @discord.ui.button(label="AGREE", style=discord.ButtonStyle.red)
    async def agree_button(self, interaction: discord.Interaction, button: discord.Button):
        user_roles = self.client.get_guild(int(CONFIG["DEV_SERVER_ID"])).get_member(interaction.user.id).roles
        if not any(role.id == int(CONFIG["CEO_ROLE_ID"]) for role in user_roles):
            return await custom_response.command_error(interaction, custom_message="You do not have permission to vote on this.", ephemeral=False)
        
        await interaction.response.send_message("You clicked the agree button.")
    
    @discord.ui.button(label="DENY", style=discord.ButtonStyle.green)
    async def deny_button(self, interaction: discord.Interaction, button: discord.Button):
        user_roles = self.client.get_guild(int(CONFIG["DEV_SERVER_ID"])).get_member(interaction.user.id).roles
        if not any(role.id == int(CONFIG["CEO_ROLE_ID"]) for role in user_roles):
            return await custom_response.command_error(interaction, custom_message="You do not have permission to vote on this.", ephemeral=False)

        await interaction.response.send_message("You clicked the deny button.")
