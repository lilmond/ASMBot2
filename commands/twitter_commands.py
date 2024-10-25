from discord import app_commands
from discord.ext import commands
import discord


class TwitterCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print(f"{__name__} commands synced.")
    

    @app_commands.command(name="link_twitter", description="Link your Twitter account with us and claim amazing prizes!")
    @app_commands.guild_only()
    async def link_twitter(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"**{__name__}.link_twitter** - working")
      

async def setup(client: commands.Bot):
    await client.add_cog(TwitterCommands(client=client))
