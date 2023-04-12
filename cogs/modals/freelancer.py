import discord
import aiosqlite
import datetime as DT
import yaml
import pytz
import re
from datetime import datetime, timedelta
from cogs.buttons.client.client import ClientSystem

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

with open('configmsg.yml', 'r') as file:
    msgdata = yaml.safe_load(file)

main_guild_id = data["General"]["MAIN_GUILD_ID"]
freelancer_guild_id = data["General"]["FREELANCER_GUILD_ID"]
staff_guild_id = data["General"]["STAFF_GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
client_invalid_timezone = msgdata["Global"]["CLIENT_INVALID_TIMEZONE"]
quote_not_integer_title = msgdata["Freelancer"]["QUOTE_NOT_INTEGER_TITLE"]
quote_not_integer_description = msgdata["Freelancer"]["QUOTE_NOT_INTEGER_DESCRIPTION"]
quote_deadline_not_enough_args_title = msgdata["Freelancer"]["QUOTE_DEADLINE_NOT_ENOUGH_ARGS_TITLE"]
quote_deadline_not_enough_args_description = msgdata["Freelancer"]["QUOTE_DEADLINE_NOT_ENOUGH_ARGS_DESCRIPTION"]
quote_deadline_arg_not_valid_title = msgdata["Freelancer"]["QUOTE_DEADLINE_ARG_NOT_VALID_TITLE"]
quote_deadline_arg_not_valid_description = msgdata["Freelancer"]["QUOTE_DEADLINE_ARG_NOT_VALID_DESCRIPTION"]
quote_sent_title = msgdata["Freelancer"]["QUOTE_SENT_TITLE"]
quote_sent_description = msgdata["Freelancer"]["QUOTE_SENT_DESCRIPTION"]
new_quote_title = msgdata["Client"]["NEW_QUOTE_TITLE"]
new_quote_description = msgdata["Client"]["NEW_QUOTE_DESCRIPTION"]

class FreelancerQuoteModal(discord.ui.Modal, title='Quote'):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    amount = discord.ui.TextInput(
        label='Amount',
        placeholder='The amount, in USD, you would like to quote.',
        max_length=10,
    )

    finishtime = discord.ui.TextInput(
        label='Estimated Finish Time',
        placeholder='Ex: 7d, 1w, 1m',
        max_length=10,
    )

    comment = discord.ui.TextInput(
        label='Comment',
        style=discord.TextStyle.long,
        placeholder='Anything else you would like to add?',
        max_length=2000,
        required=False,
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            float(self.amount.value)
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * FROM commissions WHERE freelancer_server_channel_id=?', (interaction.channel.id,))
            a = await cursor.fetchone()
            try:
                time_list = re.split('(\d+)', self.finishtime.value)
                if time_list[2] == "d":
                    time_in_s = int(time_list[1]) * 60 * 60 * 24
                if time_list[2] == "w":
                    time_in_s = int(time_list[1]) * 60 * 60 * 24 * 7
                if time_list[2] == "m":
                    time_in_s = int(time_list[1]) * 60 * 60 * 24 * 30
                timestamp = DT.datetime.now().timestamp()
                x = datetime.now() + timedelta(seconds=time_in_s)
                timestamp = int(x.timestamp())
                try:
                    main_guild = self.bot.get_guild(main_guild_id)
                    creator = main_guild.get_member(a[0])
                    channel = main_guild.get_channel(a[6])
                    cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (interaction.user.id,))
                    b = await cursor.fetchone()
                    title = new_quote_title.replace("%FREELANCERNAME%", f"{interaction.user.name}")
                    title = title.replace("%FREELANCER%", f"{interaction.user}")
                    desc = new_quote_description.replace("%FREELANCERNAME%", f"{interaction.user.name}")
                    desc = desc.replace("%QUOTE%", self.amount.value)
                    desc = desc.replace("%RATING%", "RATING HERE")
                    if b[3] == 'NULL':
                        portfolio = "N/A"
                    else:
                        portfolio = b[3]
                    desc = desc.replace("%PORTFOLIO%", portfolio)
                    if b[4] == 'NULL':
                        timezone = "N/A"
                    else:
                        try:
                            time = pytz.timezone(b[4])
                            settime = datetime.now(time)
                            settime = settime.strftime("%-I:%M:%S %p")
                            timezone = f"{b[4]} (Currently: {settime})"
                        except:
                            timezone = client_invalid_timezone
                    desc = desc.replace("%TIMEZONE%", timezone)
                    desc = desc.replace("%FINISHTIME%", f"<t:{timestamp}:F>")
                    if self.comment.value is None:
                        desc = desc.replace("%COMMENT%", "N/A")
                    else:
                        if self.comment.value == "":
                            desc = desc.replace("%COMMENT%", "N/A")
                        else:
                            desc = desc.replace("%COMMENT%", f"{self.comment.value}")
                    embed = discord.Embed(title=title, description=desc, color=discord.Color.from_str(embed_color))
                    msg = await channel.send(content=creator.mention, embed=embed, view=ClientSystem(self.bot))
                    await db.execute('INSERT INTO quotes VALUES (?,?,?,?,?);', (interaction.user.id, channel.id, interaction.channel.id, self.amount.value, msg.id))
                    embed = discord.Embed(title=quote_sent_title, description=quote_sent_description, color=discord.Color.from_str(embed_color))
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                except:
                    raise
            except IndexError:
                embed = discord.Embed(title=quote_deadline_not_enough_args_title, description=quote_deadline_not_enough_args_description, color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            except UnboundLocalError:
                embed = discord.Embed(title=quote_deadline_arg_not_valid_title, description=quote_deadline_arg_not_valid_description, color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            await db.commit()
            await db.close()
        except ValueError:
            embed = discord.Embed(title=quote_not_integer_title, description=quote_not_integer_description, color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)