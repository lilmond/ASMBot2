from components import custom_response, custom_logger, database
from command_views import admin_views
from discord import app_commands
from discord.ext import commands
import discord
import json

CONFIG = json.load(open("config.json", "r"))
logger = custom_logger.CustomLogger(source_file="ADMIN_COMMANDS")


class AdminCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print(f"{__name__} commands synced.")


    @app_commands.command(name="user_points", description="Configure a user's points data.")
    @app_commands.guild_only()
    @app_commands.describe(action="Action to be performed on the user's points.")
    @app_commands.describe(user="The user to which the action will be performed.")
    @app_commands.describe(currency="The currency that will be modified.")
    @app_commands.describe(value="The value of currency that will either be set to, added or deducted.")
    @app_commands.choices(action=[
        app_commands.Choice(name="Add", value="add"),
        app_commands.Choice(name="Deduct", value="deduct"),
        app_commands.Choice(name="Set", value="set")
    ])
    @app_commands.choices(currency=[
        app_commands.Choice(name="Social Credits", value="social_credits"),
        app_commands.Choice(name="Social Tokens", value="social_tokens")
    ])
    async def user_points(self, interaction: discord.Interaction, user: discord.User, action: str, currency: str, value: int):
        logger.log_security(f"Discord ID: {interaction.user.id} executed user_points command, Locals: {locals()}")

        if not action in ["add", "deduct", "set"]:
            logger.log_security(f"{interaction.user.id} tried to execute user_points command with an action that does not exist. Locals: {locals()}")
            return await custom_response.command_error(custom_message="Invalid command action.")
        
        users_database = database.Users()
        user = users_database.get_user(discord_id=user.id)
        user.user_points(action=action, currency=currency, value=value)

        await custom_response.command_succes(interaction, ephemeral=False)


    @app_commands.command(name="purge", description="Purge the entire user points database.")
    @app_commands.guild_only()
    async def purge(self, interaction: discord.Interaction):
        user_roles = self.client.get_guild(int(CONFIG["DEV_SERVER_ID"])).get_member(interaction.user.id).roles
        if not any(role.id == int(CONFIG["CEO_ROLE_ID"]) for role in user_roles):
            return await custom_response.command_error(interaction, custom_message="You do not have permission to use this command.", ephemeral=False)

        purge_embed = discord.Embed()
        purge_embed.color = 0xffff00
        purge_embed.title = "Purge"
        purge_embed.description = "Delete all user data? This requires at least 2 votes from the CEO's. This action is irreversible. The buttons will timeout in 10 seconds."

        purge_view = admin_views.PurgeView(client=self.client)

        await interaction.response.send_message(embed=purge_embed, view=purge_view)

async def setup(client: commands.Bot):
    await client.add_cog(AdminCommands(client=client))
