from discord import app_commands
from discord.ext import commands
import discord
import asyncio
import json
import os

CONFIG = json.load(open("./config.json", "r"))

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@client.event
async def on_ready():
    await client.tree.sync()
    print(f"Logged In: {client.user.name}")

@client.event
async def setup_hook():
    print("Setting up hook...")

async def load_commands():
    for script in os.listdir("./commands"):
        if script.endswith(".py"):
            await client.load_extension(f"commands.{script[:-3]}")

async def main():
    async with client:
        await load_commands()
        await client.start(token=CONFIG["TOKEN"])

if __name__ == "__main__":
    asyncio.run(main())
