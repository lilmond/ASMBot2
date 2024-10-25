from components.database import XamanWallets
from discord import app_commands
from discord.ext import commands
import requests
import discord


class XrplCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print(f"{__name__} commands synced.")
    

    @app_commands.command(name="link_xaman", description="Link your Xaman wallet with us and receive prizes!")
    @app_commands.guild_only()
    async def link_xaman(self, interaction: discord.Interaction):
        payload = {
            "txjson": { "TransactionType": "SignIn" }
        }

        headers = headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "X-API-Key": "7ec3dc0e-8284-4ef7-b2f2-f935b9cca8e4",
            "X-API-Secret": "502b1203-d361-4535-8251-f9cbc944452d"
        }

        http = requests.post("https://xumm.app/api/v1/platform/payload", json=payload, headers=headers).json()

        if not "uuid" in http:
            return await command_respond.respond(interaction, color=0xff0000, title="Error!", description="An error has occured while trying to generate a sign QR code for you. Please try again!")
        
        uuid = http["uuid"]
        qr_code_url = http["refs"]["qr_png"]
        sign_url = http["next"]["always"]

        embed = discord.Embed()
        embed.title = "Link your Xaman!"
        embed.description = f"Open your **Xaman** app to scan the QR code below!\n[Click here]({sign_url}) if you're on mobile."
        embed.color = 0x00ff00
        embed.set_image(url=qr_code_url)

        # Append user into XAMAN_WALLET registration table.
        xaman_wallets_db = XamanWallets()
        xaman_wallets_db.register_uuid(discord_id=interaction.user.id, uuid=uuid)

        await interaction.response.send_message(embed=embed, ephemeral=True)
    

async def setup(client: commands.Bot):
    await client.add_cog(XrplCommands(client=client))
