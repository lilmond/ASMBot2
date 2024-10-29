from components import database, custom_logger, custom_response
from discord import app_commands
from discord.ext import commands
import discord
import time

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
        users_db = database.Users()
        user_data = users_db.get_user(discord_id=interaction.user.id)

        last_daily = user_data.last_daily

        if not user_data.last_daily:
            last_daily = 0
        
        print(f"Last Daily: {last_daily}")

        if (time.time() - last_daily) < 76800:
            print("Already claimed")
            return await custom_response.command_error(interaction, custom_message=f"You have recently claimed your daily reward. Please come back at <t:{int(last_daily + 76800)}:F>", ephemeral=False)
        
        print(f"Claiming")
        user_data.user_points(action="add", currency="social_credits", value=100)
        print(f"Added points")
        user_data.set_last_daily(epoch=time.time())
        print("Set last daily")

        return await custom_response.command_succes(interaction, custom_message=f"You have successfully claimed your daily reward of 100 Social Credits!", ephemeral=False)


    @app_commands.command(name="leaderboard", description="Show who's the richest Social user globally.")
    @app_commands.guild_only()
    @app_commands.choices(stats=[
        app_commands.Choice(name="Social Credits", value="social_credits"),
        app_commands.Choice(name="Social Tokens", value="social_tokens"),
        app_commands.Choice(name="Spent XRP", value="spent_xrp"),

    ])
    async def leaderboard(self, interaction: discord.Interaction, stats: str):
        users_db = database.Users()
        leaderboard = users_db.get_leaderboard(stats=stats)
        leaderboard_name = ' '.join(x.capitalize() for x in stats.split('_'))

        leaderboard_embed = discord.Embed()
        leaderboard_embed.color = 0x5400e6
        leaderboard_embed.title = f"{leaderboard_name} Leaderboard"
        leaderboard_embed.description = ""

        if not leaderboard:
            leaderboard_embed.description = f"Wow! Current no one has enough {leaderboard_name} to be shown on the leaderboard."
        else:
            for user in leaderboard:
                leaderboard_embed.description += f"<@{user.discord_id}> - {user.__getattribute__(stats)}\n"

        await interaction.response.send_message(embed=leaderboard_embed)


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
