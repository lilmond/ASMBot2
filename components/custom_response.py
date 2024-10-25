from discord import app_commands
from discord.ext import commands
import discord

async def command_error(
    interaction: discord.Interaction,
    custom_message: str = None,
    ephemeral: bool = True
):
    embed = discord.Embed()
    embed.color = 0xcf1f25
    embed.title = "Command Error"
    embed.description = "An error has occured while trying to process your command. Please try again!" if not custom_message else custom_message
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1282170749850882189/1297118872306188338/warning.png?ex=6714c396&is=67137216&hm=8999b1a9eb0359fb599889b7d89b72c9d75c341491b70b18807b3fcc755a9969&")

    return await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

async def command_succes(
    interaction: discord.Interaction,
    custom_message: str = None,
    ephemeral: bool = True
):
    embed = discord.Embed()
    embed.color = 0x8dc63f
    embed.title = "Command Success"
    embed.description = "Your command has successfully been executed!" if not custom_message else custom_message
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1282170749850882189/1297119571202932807/check.png?ex=6714c43d&is=671372bd&hm=9597804b47958ba3485eafbdea5195448c098174c419de55245886098c7f5b7c&")

    return await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
