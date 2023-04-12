import discord
import aiosqlite
import yaml
from discord import app_commands
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

with open('configmsg.yml', 'r') as file:
    msgdata = yaml.safe_load(file)

main_guild_id = data["General"]["MAIN_GUILD_ID"]
freelancer_guild_id = data["General"]["FREELANCER_GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
report_command = data["Commands"]["REPORT_COMMAND"]
main_server_freelancer_role_id = data["Role"]["MAIN_SERVER_FREELANCER_ROLE_ID"]
description_remove_title = msgdata["Freelancer"]["DESCRIPTION_REMOVE_TITLE"]
description_remove_description = msgdata["Freelancer"]["DESCRIPTION_REMOVE_DESCRIPTION"]
no_description_remove_title = msgdata["Freelancer"]["NO_DESCRIPTION_REMOVE_TITLE"]
no_description_remove_description = msgdata["Freelancer"]["NO_DESCRIPTION_REMOVE_DESCRIPTION"]
not_freelancer_remove_description_title = msgdata["Freelancer"]["NOT_FREELANCER_REMOVE_DESCRIPTION_TITLE"]
not_freelancer_remove_description_description = msgdata["Freelancer"]["NOT_FREELANCER_REMOVE_DESCRIPTION_DESCRIPTION"]
portfolio_remove_title = msgdata["Freelancer"]["PORTFOLIO_REMOVE_TITLE"]
portfolio_remove_description = msgdata["Freelancer"]["PORTFOLIO_REMOVE_DESCRIPTION"]
no_portfolio_remove_title = msgdata["Freelancer"]["NO_PORTFOLIO_REMOVE_TITLE"]
no_portfolio_remove_description = msgdata["Freelancer"]["NO_PORTFOLIO_REMOVE_DESCRIPTION"]
not_freelancer_remove_portfolio_title = msgdata["Freelancer"]["NOT_FREELANCER_REMOVE_PORTFOLIO_TITLE"]
not_freelancer_remove_portfolio_description = msgdata["Freelancer"]["NOT_FREELANCER_REMOVE_PORTFOLIO_DESCRIPTION"]
timezone_remove_title = msgdata["Freelancer"]["TIMEZONE_REMOVE_TITLE"]
timezone_remove_description = msgdata["Freelancer"]["TIMEZONE_REMOVE_DESCRIPTION"]
no_timezone_remove_title = msgdata["Freelancer"]["NO_TIMEZONE_REMOVE_TITLE"]
no_timezone_remove_description = msgdata["Freelancer"]["NO_TIMEZONE_REMOVE_DESCRIPTION"]
not_freelancer_remove_timezone_title = msgdata["Freelancer"]["NOT_FREELANCER_REMOVE_TIMEZONE_TITLE"]
not_freelancer_remove_timezone_description = msgdata["Freelancer"]["NOT_FREELANCER_REMOVE_TIMEZONE_DESCRIPTION"]
paypal_remove_title = msgdata["Freelancer"]["PAYPAL_REMOVE_TITLE"]
paypal_remove_description = msgdata["Freelancer"]["PAYPAL_REMOVE_DESCRIPTION"]
no_paypal_remove_title = msgdata["Freelancer"]["NO_PAYPAL_REMOVE_TITLE"]
no_paypal_remove_description = msgdata["Freelancer"]["NO_PAYPAL_REMOVE_DESCRIPTION"]
not_freelancer_remove_paypal_title = msgdata["Freelancer"]["NOT_FREELANCER_REMOVE_PAYPAL_TITLE"]
not_freelancer_remove_paypal_description = msgdata["Freelancer"]["NOT_FREELANCER_REMOVE_PAYPAL_DESCRIPTION"]
paypalme_remove_title = msgdata["Freelancer"]["PAYPALME_REMOVE_TITLE"]
paypalme_remove_description = msgdata["Freelancer"]["PAYPALME_REMOVE_DESCRIPTION"]
no_paypalme_remove_title = msgdata["Freelancer"]["NO_PAYPALME_REMOVE_TITLE"]
no_paypalme_remove_description = msgdata["Freelancer"]["NO_PAYPALME_REMOVE_DESCRIPTION"]
not_freelancer_remove_paypalme_title = msgdata["Freelancer"]["NOT_FREELANCER_REMOVE_PAYPALME_TITLE"]
not_freelancer_remove_paypalme_description = msgdata["Freelancer"]["NOT_FREELANCER_REMOVE_PAYPALME_DESCRIPTION"]

class RemoveCog(commands.GroupCog, name="remove"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="description", description="Removes your description!")
    async def description(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)
        db = await aiosqlite.connect('database.db')
        main_guild = self.bot.get_guild(main_guild_id)
        member = main_guild.get_member(interaction.user.id)
        freelancer_role = main_guild.get_role(main_server_freelancer_role_id)
        if freelancer_role in member.roles:
            cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (interaction.user.id,))
            a = await cursor.fetchone()
            if a is None:
                embed = discord.Embed(title=no_description_remove_title, description=no_description_remove_description, color=discord.Color.red())
            else:
                await db.execute('UPDATE freelancers SET description=? WHERE freelancer_id=?', ('NULL', interaction.user.id))
                embed = discord.Embed(title=description_remove_title, description=description_remove_description, color=discord.Color.from_str(embed_color))
        else:
            embed = discord.Embed(title=not_freelancer_remove_description_title, description=not_freelancer_remove_description_title, color=discord.Color.red())
        await interaction.followup.send(embed=embed)
        await db.commit()
        await db.close()

    @app_commands.command(name="portfolio", description="Removes your portfolio!")
    async def portfolio(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)
        db = await aiosqlite.connect('database.db')
        main_guild = self.bot.get_guild(main_guild_id)
        member = main_guild.get_member(interaction.user.id)
        freelancer_role = main_guild.get_role(main_server_freelancer_role_id)
        if freelancer_role in member.roles:
            cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (interaction.user.id,))
            a = await cursor.fetchone()
            if a is None:
                embed = discord.Embed(title=no_portfolio_remove_title, description=no_portfolio_remove_description, color=discord.Color.red())
            else:
                await db.execute('UPDATE freelancers SET portfolio=? WHERE freelancer_id=?', ('NULL', interaction.user.id))
                embed = discord.Embed(title=portfolio_remove_title, description=portfolio_remove_description, color=discord.Color.from_str(embed_color))
        else:
            embed = discord.Embed(title=not_freelancer_remove_portfolio_title, description=not_freelancer_remove_portfolio_title, color=discord.Color.red())
        await interaction.followup.send(embed=embed)
        await db.commit()
        await db.close()

    @app_commands.command(name="timezone", description="Removes your timezone!")
    async def timezone(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)
        db = await aiosqlite.connect('database.db')
        main_guild = self.bot.get_guild(main_guild_id)
        member = main_guild.get_member(interaction.user.id)
        freelancer_role = main_guild.get_role(main_server_freelancer_role_id)
        if freelancer_role in member.roles:
            cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (interaction.user.id,))
            a = await cursor.fetchone()
            if a is None:
                embed = discord.Embed(title=no_timezone_remove_title, description=no_timezone_remove_description, color=discord.Color.red())
            else:
                await db.execute('UPDATE freelancers SET timezone=? WHERE freelancer_id=?', ('NULL', interaction.user.id))
                embed = discord.Embed(title=timezone_remove_title, description=timezone_remove_description, color=discord.Color.from_str(embed_color))
        else:
            embed = discord.Embed(title=not_freelancer_remove_timezone_title, description=not_freelancer_remove_timezone_title, color=discord.Color.red())
        await interaction.followup.send(embed=embed)
        await db.commit()
        await db.close()

    @app_commands.command(name="paypal", description="Removes your PayPal email!")
    async def paypal(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)
        db = await aiosqlite.connect('database.db')
        main_guild = self.bot.get_guild(main_guild_id)
        member = main_guild.get_member(interaction.user.id)
        freelancer_role = main_guild.get_role(main_server_freelancer_role_id)
        if freelancer_role in member.roles:
            cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (interaction.user.id,))
            a = await cursor.fetchone()
            if a is None:
                embed = discord.Embed(title=no_paypal_remove_title, description=no_paypal_remove_description, color=discord.Color.red())
            else:
                await db.execute('UPDATE freelancers SET paypal=? WHERE freelancer_id=?', ('NULL', interaction.user.id))
                embed = discord.Embed(title=paypal_remove_title, description=paypal_remove_description, color=discord.Color.from_str(embed_color))
        else:
            embed = discord.Embed(title=not_freelancer_remove_paypal_title, description=not_freelancer_remove_paypal_title, color=discord.Color.red())
        await interaction.followup.send(embed=embed)
        await db.commit()
        await db.close()

    @app_commands.command(name="paypalme", description="Removes your PayPalMe link!")
    async def paypalme(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)
        db = await aiosqlite.connect('database.db')
        main_guild = self.bot.get_guild(main_guild_id)
        member = main_guild.get_member(interaction.user.id)
        freelancer_role = main_guild.get_role(main_server_freelancer_role_id)
        if freelancer_role in member.roles:
            cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (interaction.user.id,))
            a = await cursor.fetchone()
            if a is None:
                embed = discord.Embed(title=no_paypalme_remove_title, description=no_paypalme_remove_description, color=discord.Color.red())
            else:
                await db.execute('UPDATE freelancers SET paypal=? WHERE freelancer_id=?', ('NULL', interaction.user.id))
                embed = discord.Embed(title=paypalme_remove_title, description=paypalme_remove_description, color=discord.Color.from_str(embed_color))
        else:
            embed = discord.Embed(title=not_freelancer_remove_paypalme_title, description=not_freelancer_remove_paypalme_title, color=discord.Color.red())
        await interaction.followup.send(embed=embed)
        await db.commit()
        await db.close()

async def setup(bot):
    await bot.add_cog(RemoveCog(bot), guilds=[discord.Object(id=freelancer_guild_id)])