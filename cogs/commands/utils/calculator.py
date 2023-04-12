import discord
from discord import app_commands
from discord.ext import commands
from cogs.buttons.utils.calculator import start_calculator

class CalculatorCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="calculator", description="Calculate something!")
    @app_commands.default_permissions(administrator=True)
    async def calculator(self, interaction: discord.Interaction) -> None:
        return await start_calculator(interaction)

async def setup(bot):
    await bot.add_cog(CalculatorCog(bot))