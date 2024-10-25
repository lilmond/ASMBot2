from components import custom_response
from command_views import market_views
from discord import app_commands
from discord.ext import commands
import discord


class MarketCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print(f"{__name__} commands synced.")


    @app_commands.command(name="auction_create", description="Create an auction item.")
    @app_commands.guild_only()
    @app_commands.describe(title="Auction's title, this will be displayed in the embed.")
    @app_commands.describe(description="Auction's description.")
    @app_commands.describe(image="Auction item image.")
    @app_commands.describe(expiration="Auction expiration in hours.")
    @app_commands.describe(currency="The currency that users will place bid.")
    @app_commands.describe(starting_bid="Initial bid value.")
    @app_commands.describe(min_overbid="Minimum bid users can add from the current bid.")
    @app_commands.describe(custom_message="Show a custom message above the embed.")
    @app_commands.choices(currency=[
        app_commands.Choice(name="Social Credits", value="social_credits"),
        app_commands.Choice(name="Social Tokens", value="social_tokens")

    ])
    async def auction_create(
        self,
        interaction: discord.Interaction,
        title: str, description: str,
        image: discord.Attachment,
        expiration: int,
        currency: str,
        starting_bid: int,
        min_overbid: int,
        custom_message: str = None
    ):

        await custom_response.command_succes(interaction=interaction)
    

    @app_commands.command(name="market_create_item", description="Create an NFT item everyone can buy using Social Credits/Tokens.")
    @app_commands.guild_only()
    @app_commands.describe(name="NFT item name.")
    @app_commands.describe(description="A brief information about the item.")
    @app_commands.describe(image="Let them see the beauty of this offer.")
    @app_commands.describe(price="Item's price in Social Bot currency.")
    @app_commands.describe(stock="How many stocks to sell?")
    @app_commands.describe(currency="Select which currency users can purchase this item with.")
    @app_commands.choices(currency=[
        app_commands.Choice(name="Social Credits", value="social_credits"),
        app_commands.Choice(name="Social Tokens", value="social_tokens")
    ])
    async def market_create_item(
        self,
        interaction: discord.Interaction,
        name: str,
        description: str,
        image: discord.Attachment,
        price: int,
        stock: int,
        currency: str
    ):
        if currency == "social_credits":
            currency_name = "Social Credits"
        elif currency == "social_tokens":
            currency_name = "Social Tokens"
        else:
            return await custom_response.command_error(interaction=interaction)
        
        image

        item_embed = discord.Embed()
        item_embed.color = 0xffffff
        item_embed.title = name
        item_embed.description = description
        item_embed.set_image(url=image.url)
        item_embed.add_field(name="<:currencies:1297122888440221729> Currency", value=f"`{currency_name}`", inline=True)
        item_embed.add_field(name="<:PriceTag_USD:1297115231281221707> Price", value=f"`{price}`", inline=True)
        item_embed.add_field(name="<:boxes:1297122467684417637> Stock", value=f"`{stock}`", inline=True)

        item_buttons = market_views.MarketItemView()

        await interaction.channel.send(embed=item_embed, view=item_buttons)
        await custom_response.command_succes(interaction=interaction)

async def setup(client: commands.Bot):
    await client.add_cog(MarketCommands(client=client))
