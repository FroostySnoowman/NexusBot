import discord
import aiosqlite
import yaml
from discord import app_commands
from discord.ext import commands
from typing import Optional

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

freelancer_guild_id = data["General"]["FREELANCER_GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
busy_command = data["Commands"]["BUSY_COMMAND"]
unbusy_command = data["Commands"]["UNBUSY_COMMAND"]

class BusyCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="busy", description="Mark yourself as busy and no longer receive commission pings!")
    @app_commands.describe(reason="What is the reason for you being busy?")
    async def busy(self, interaction: discord.Interaction, reason: Optional[str]) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM busy WHERE freelancer_id=?', (interaction.user.id, ))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(description=f"Successfully been marked as busy. You will no longer receive commission pings. \n\nUse the {unbusy_command} to remove it!", color=discord.Color.from_str(embed_color))
            if reason is None:
                await db.execute('INSERT INTO busy VALUES (?,?);', (interaction.user.id, 'NULL'))
            else:
                await db.execute('INSERT INTO busy VALUES (?,?);', (interaction.user.id, reason))
        else:
            embed = discord.Embed(description=f"You're already marked as busy. Use the {unbusy_command} to remove it!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

    @app_commands.command(name="unbusy", description="Mark yourself as no longer bosy receive commission pings again!")
    async def unbusy(self, interaction: discord.Interaction) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM busy WHERE freelancer_id=?', (interaction.user.id, ))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(description=f"You're not marked as busy. Use the {busy_command} to add it!", color=discord.Color.from_str(embed_color))
        else:
            await db.execute('DELETE FROM busy WHERE freelancer_id=?', (interaction.user.id, ))
            embed = discord.Embed(description=f"Successfully been marked as unbusy. You will now receive commission pings again. \n\nUse the {busy_command} to add it back!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

async def setup(bot):
    await bot.add_cog(BusyCog(bot), guilds=[discord.Object(id=freelancer_guild_id)])