import discord
import aiosqlite
import yaml
import pytz
from discord import app_commands
from discord.ext import commands
from datetime import datetime

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

with open('configmsg.yml', 'r') as file:
    msgdata = yaml.safe_load(file)

main_guild_id = data["General"]["MAIN_GUILD_ID"]
freelancer_guild_id = data["General"]["FREELANCER_GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
report_command = data["Commands"]["REPORT_COMMAND"]
main_server_freelancer_role_id = data["Role"]["MAIN_SERVER_FREELANCER_ROLE_ID"]
description_set_title = msgdata["Freelancer"]["DESCRIPTION_SET_TITLE"]
description_set_description = msgdata["Freelancer"]["DESCRIPTION_SET_DESCRIPTION"]
not_freelancer_description_set_title = msgdata["Freelancer"]["NOT_FREELANCER_SET_DESCRIPTION_TITLE"]
not_freelancer_description_set_description = msgdata["Freelancer"]["NOT_FREELANCER_SET_DESCRIPTION_DESCRIPTION"]
portfolio_set_title = msgdata["Freelancer"]["PORTFOLIO_SET_TITLE"]
portfolio_set_description = msgdata["Freelancer"]["PORTFOLIO_SET_DESCRIPTION"]
not_freelancer_portfolio_set_title = msgdata["Freelancer"]["NOT_FREELANCER_SET_PORTFOLIO_TITLE"]
not_freelancer_portfolio_set_description = msgdata["Freelancer"]["NOT_FREELANCER_SET_PORTFOLIO_DESCRIPTION"]
timezone_set_title = msgdata["Freelancer"]["TIMEZONE_SET_TITLE"]
timezone_set_description = msgdata["Freelancer"]["TIMEZONE_SET_DESCRIPTION"]
not_valid_timezone_timezone_set_title = msgdata["Freelancer"]["NOT_VALID_TIMEZONE_TIMEZONE_SET_TITLE"]
not_valid_timezone_timezone_set_description = msgdata["Freelancer"]["NOT_VALID_TIMEZONE_TIMEZONE_SET_DESCRIPTION"]
not_freelancer_timezone_set_title = msgdata["Freelancer"]["NOT_FREELANCER_SET_TIMEZONE_TITLE"]
not_freelancer_timezone_set_description = msgdata["Freelancer"]["NOT_FREELANCER_SET_TIMEZONE_DESCRIPTION"]
paypal_set_title = msgdata["Freelancer"]["PAYPAL_SET_TITLE"]
paypal_set_description = msgdata["Freelancer"]["PAYPAL_SET_DESCRIPTION"]
not_valid_email_paypal_set_title = msgdata["Freelancer"]["NOT_VALID_EMAIL_PAYPAL_SET_TITLE"]
not_valid_email_paypal_set_description = msgdata["Freelancer"]["NOT_VALID_EMAIL_PAYPAL_SET_DESCRIPTION"]
not_freelancer_paypal_set_title = msgdata["Freelancer"]["NOT_FREELANCER_SET_PAYPAL_TITLE"]
not_freelancer_paypal_set_description = msgdata["Freelancer"]["NOT_FREELANCER_SET_PAYPAL_DESCRIPTION"]
paypalme_set_title = msgdata["Freelancer"]["PAYPALME_SET_TITLE"]
paypalme_set_description = msgdata["Freelancer"]["PAYPALME_SET_DESCRIPTION"]
not_valid_link_paypalme_set_title = msgdata["Freelancer"]["NOT_VALID_LINK_PAYPALME_SET_TITLE"]
not_valid_link_paypalme_set_description = msgdata["Freelancer"]["NOT_VALID_LINK_PAYPALME_SET_DESCRIPTION"]
not_freelancer_paypalme_set_title = msgdata["Freelancer"]["NOT_FREELANCER_SET_PAYPALME_TITLE"]
not_freelancer_paypalme_set_description = msgdata["Freelancer"]["NOT_FREELANCER_SET_PAYPALME_DESCRIPTION"]

class SetCog(commands.GroupCog, name="set"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="description", description="Sets your description!")
    @app_commands.describe(description="What is your description?")
    async def description(self, interaction: discord.Interaction, description: str) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)
        db = await aiosqlite.connect('database.db')
        main_guild = self.bot.get_guild(main_guild_id)
        member = main_guild.get_member(interaction.user.id)
        freelancer_role = main_guild.get_role(main_server_freelancer_role_id)
        if freelancer_role in member.roles:
            cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (interaction.user.id,))
            a = await cursor.fetchone()
            if a is None:
                await db.execute('INSERT INTO freelancers VALUES (?,?,?,?,?,?,?);', (interaction.user.id, 0, description, 'NULL', 'NULL', 'NULL', 'NULL'))
            else:
                await db.execute('UPDATE freelancers SET description=? WHERE freelancer_id=?', (description, interaction.user.id))
            embed = discord.Embed(title=description_set_title, description=description_set_description, color=discord.Color.from_str(embed_color))
        else:
            embed = discord.Embed(title=not_freelancer_description_set_title, description=not_freelancer_description_set_description, color=discord.Color.red())
        await interaction.followup.send(embed=embed)
        await db.commit()
        await db.close()

    @app_commands.command(name="portfolio", description="Sets your portfolio!")
    @app_commands.describe(portfolio="What is your portfolio?")
    async def portfolio(self, interaction: discord.Interaction, portfolio: str) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)
        db = await aiosqlite.connect('database.db')
        main_guild = self.bot.get_guild(main_guild_id)
        member = main_guild.get_member(interaction.user.id)
        freelancer_role = main_guild.get_role(main_server_freelancer_role_id)
        if freelancer_role in member.roles:
            cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (interaction.user.id,))
            a = await cursor.fetchone()
            if a is None:
                await db.execute('INSERT INTO freelancers VALUES (?,?,?,?,?,?,?);', (interaction.user.id, 0, 'NULL', portfolio, 'NULL', 'NULL', 'NULL'))
            else:
                await db.execute('UPDATE freelancers SET portfolio=? WHERE freelancer_id=?', (portfolio, interaction.user.id))
            embed = discord.Embed(title=portfolio_set_title, description=portfolio_set_description, color=discord.Color.from_str(embed_color))
        else:
            embed = discord.Embed(title=not_freelancer_portfolio_set_title, description=not_freelancer_portfolio_set_description, color=discord.Color.red())
        await interaction.followup.send(embed=embed)
        await db.commit()
        await db.close()

    @app_commands.command(name="timezone", description="Sets your timezone!")
    @app_commands.describe(timezone="What is your timezone?")
    async def timezone(self, interaction: discord.Interaction, timezone: str) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)
        db = await aiosqlite.connect('database.db')
        main_guild = self.bot.get_guild(main_guild_id)
        member = main_guild.get_member(interaction.user.id)
        freelancer_role = main_guild.get_role(main_server_freelancer_role_id)
        if freelancer_role in member.roles:
            if timezone.lower() in [x.lower() for x in pytz.all_timezones]:
                cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (interaction.user.id,))
                a = await cursor.fetchone()
                if a is None:
                    await db.execute('INSERT INTO freelancers VALUES (?,?,?,?,?,?,?);', (interaction.user.id, 0, 'NULL', 'NULL', timezone, 'NULL', 'NULL'))
                else:
                    await db.execute('UPDATE freelancers SET timezone=? WHERE freelancer_id=?', (timezone, interaction.user.id))
                time = pytz.timezone(timezone)
                settime = datetime.now(time)
                settime = settime.strftime("%-I:%M:%S %p")
                desc = timezone_set_description.replace("%TIME%", f"{settime}")
                embed = discord.Embed(title=timezone_set_title, description=desc, color=discord.Color.from_str(embed_color))
            else:
                desc = not_valid_timezone_timezone_set_description.replace("%TIMEZONE%", f"{timezone}")
                embed = discord.Embed(title=not_valid_timezone_timezone_set_title, description=desc, color=discord.Color.red())
        else:
            embed = discord.Embed(title=not_freelancer_timezone_set_title, description=not_freelancer_timezone_set_description, color=discord.Color.red())
        await interaction.followup.send(embed=embed)
        await db.commit()
        await db.close()

    @timezone.autocomplete("timezone")
    async def role_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        timezones = [x for x in pytz.all_timezones]
        if current != "":
            matches = [times for times in timezones if times.startswith(current)]
        else:
            matches = pytz.all_timezones
        return [app_commands.Choice(name=match, value=match) for match in matches][:25]

    @app_commands.command(name="paypal", description="Sets your PayPal email!")
    @app_commands.describe(email="What is your PayPal email?")
    async def paypal(self, interaction: discord.Interaction, email: str) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)
        db = await aiosqlite.connect('database.db')
        main_guild = self.bot.get_guild(main_guild_id)
        member = main_guild.get_member(interaction.user.id)
        freelancer_role = main_guild.get_role(main_server_freelancer_role_id)
        if freelancer_role in member.roles:
            if "@" in email:
                cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (interaction.user.id,))
                a = await cursor.fetchone()
                if a is None:
                    await db.execute('INSERT INTO freelancers VALUES (?,?,?,?,?,?,?);', (interaction.user.id, 0, 'NULL', 'NULL', 'NULL', email, 'NULL'))
                else:
                    await db.execute('UPDATE freelancers SET paypal=? WHERE freelancer_id=?', (email, interaction.user.id))
                embed = discord.Embed(title=paypal_set_title, description=paypal_set_description, color=discord.Color.from_str(embed_color))
            else:
                desc = not_valid_email_paypal_set_description.replace("%EMAIL%", f"{email}")
                embed = discord.Embed(title=not_valid_email_paypal_set_title, description=desc, color=discord.Color.red())
        else:
            embed = discord.Embed(title=not_freelancer_paypal_set_title, description=not_freelancer_paypal_set_description, color=discord.Color.red())
        await interaction.followup.send(embed=embed)
        await db.commit()
        await db.close()

    @app_commands.command(name="paypalme", description="Sets your PayPalMe link!")
    @app_commands.describe(link="What is your PayPal Me link?")
    async def paypalme(self, interaction: discord.Interaction, link: str) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)
        db = await aiosqlite.connect('database.db')
        main_guild = self.bot.get_guild(main_guild_id)
        member = main_guild.get_member(interaction.user.id)
        freelancer_role = main_guild.get_role(main_server_freelancer_role_id)
        if freelancer_role in member.roles:
            if "paypal.me/" in link:
                cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (interaction.user.id,))
                a = await cursor.fetchone()
                if a is None:
                    await db.execute('INSERT INTO freelancers VALUES (?,?,?,?,?,?,?);', (interaction.user.id, 0, 'NULL', 'NULL', 'NULL', 'NULL', link))
                else:
                    await db.execute('UPDATE freelancers SET paypalme=? WHERE freelancer_id=?', (link, interaction.user.id))
                embed = discord.Embed(title=paypalme_set_title, description=paypalme_set_description, color=discord.Color.from_str(embed_color))
            else:
                desc = not_valid_link_paypalme_set_description.replace("%LINK%", f"{link}")
                embed = discord.Embed(title=not_valid_link_paypalme_set_title, description=desc, color=discord.Color.red())
        else:
            embed = discord.Embed(title=not_freelancer_paypalme_set_title, description=not_freelancer_paypalme_set_description, color=discord.Color.red())
        await interaction.followup.send(embed=embed)
        await db.commit()
        await db.close()

async def setup(bot):
    await bot.add_cog(SetCog(bot), guilds=[discord.Object(id=freelancer_guild_id)])