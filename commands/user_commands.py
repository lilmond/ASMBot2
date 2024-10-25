from components import database, custom_logger, custom_response
from discord import app_commands
from discord.ext import commands
import discord


logger = custom_logger.CustomLogger(source_file="USER_COMMANDS")


class UserCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print(f"{__name__} commands synced.")
    

    @app_commands.command(name="claim_daily", description="Claim your daily reward.")
    @app_commands.guild_only()
    async def claim_daily(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"**{__name__}.claim_daily** - working")
    

    @app_commands.command(name="leaderboard", description="Show who's the richest Social user globally.")
    @app_commands.guild_only()
    async def leaderboard(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"**{__name__}.leaderboard** - working")


    @app_commands.command(name="profile", description="Show yours or others Social profile.")
    @app_commands.guild_only()
    async def profile(self, interaction: discord.Interaction, user: discord.User = None):
        if user:
            user = user
        else:
            user = interaction.user

        users_database = database.Users()
        user_profile = users_database.get_user(discord_id=user.id)

        profile_embed = discord.Embed()
        profile_embed.color = 0x5400e6
        profile_embed.title = f"{user.name}'s Profile"
        profile_embed.set_thumbnail(url=user.display_avatar.url)
        profile_embed.add_field(name="Social Credits", value=f"`{user_profile.social_credits}`", inline=True)
        profile_embed.add_field(name="Social Tokens", value=f"`{user_profile.social_tokens}`", inline=True)
        profile_embed.add_field(name="Spent XRP", value=f"`{user_profile.spent_xrp}`", inline=True)
        profile_embed.add_field(name="Twitter", value=f"[Profile](https://twitter.com/intent/user?user_id={user_profile.twitter_id})" if user_profile.twitter_id else "Not linked", inline=True)
        profile_embed.add_field(name="XRP Wallet", value=f"[Explorer](https://xrpscan.com/account/{user_profile.xrp_address})" if user_profile.xrp_address else "Not linked", inline=True)

        await interaction.response.send_message(embed=profile_embed)


async def setup(client: commands.Bot):
    await client.add_cog(UserCommands(client=client))
