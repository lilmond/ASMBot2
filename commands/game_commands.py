from command_views import game_views
from discord import app_commands
from discord.ext import commands
import discord


class GameCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print(f"{__name__} commands synced.")


    @app_commands.command(name="spinwheel", description="A cool spinwheel! Man, what could I get here?")
    @app_commands.guild_only()
    async def spinwheel(self, interaction: discord.Interaction):
        spin_embed = discord.Embed()
        spin_embed.color = 0xe04700
        spin_embed.title = "Spinwheel"
        spin_embed.set_image(url="https://cdn.discordapp.com/attachments/1282170749850882189/1299305760341102643/Untitled.jpg?ex=671cb849&is=671b66c9&hm=ef761591bd81c230ba68c2142c9758b60b2765a6a51b314951e94b75a6265102&")
    
        spin_button = game_views.SpinWheelView(player_id=interaction.user.id)

        await interaction.response.send_message(embed=spin_embed, view=spin_button)

async def setup(client: commands.Bot):
    await client.add_cog(GameCommands(client=client))
