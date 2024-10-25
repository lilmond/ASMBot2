from components import custom_response
import discord

class SpinWheelView(discord.ui.View):
    def __init__(self, player_id: int):
        self.player_id = player_id
        super().__init__(timeout=60)
    
    @discord.ui.button(label="SPIN", style=discord.ButtonStyle.green)
    async def spin_button(self, interaction: discord.Interaction, button: discord.Button):
        if not interaction.user.id == self.player_id:
            return await custom_response.command_error(interaction, custom_message="Sorry, this button does not belong to you.")
        
        await interaction.response.send_message("You clicked the button.")
    
    
