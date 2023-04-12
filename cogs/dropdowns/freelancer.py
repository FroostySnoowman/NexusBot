import discord
import aiosqlite
import yaml
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

with open('configmsg.yml', 'r') as file:
    msgdata = yaml.safe_load(file)

main_guild_id = data["General"]["MAIN_GUILD_ID"]
freelancer_guild_id = data["General"]["FREELANCER_GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
name = data["General"]["NAME"]
ticket_does_not_exist_title = msgdata["Global"]["TICKET_DOES_NOT_EXIST_TITLE"]
ticket_does_not_exist_description = msgdata["Global"]["TICKET_DOES_NOT_EXIST_DESCRIPTION"]
denying_ticket_title = msgdata["Freelancer"]["DENYING_TICKET_TITLE"]
denying_ticket_description = msgdata["Freelancer"]["DENYING_TICKET_DESCRIPTION"]
deny_success_ticket_title = msgdata["Freelancer"]["DENY_SUCCESS_TICKET_TITLE"]
deny_success_ticket_description = msgdata["Freelancer"]["DENY_SUCCESS_TICKET_DESCRIPTION"]
freelancer_busy_title = msgdata["Order"]["FREELANCER_BUSY_TITLE"]
freelancer_busy_footer = msgdata["Order"]["FREELANCER_BUSY_FOOTER"]

class DenyDropdown(discord.ui.Select):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        options = [
            discord.SelectOption(label='Budget'),
            discord.SelectOption(label='Busy'),
            discord.SelectOption(label='Not Interested'),
            discord.SelectOption(label='Not My Niche'),
        ]

        super().__init__(placeholder="Select your reason for denying the ticket!", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM commissions WHERE freelancer_server_channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(title=ticket_does_not_exist_title, description=ticket_does_not_exist_description, color=discord.Color.red())
            await interaction.edit_original_response(embed=embed, view=None)
        else:
            main_guild = self.bot.get_guild(main_guild_id)
            main_server_channel = main_guild.get_channel(a[6])
            deny_partial_message = main_server_channel.get_partial_message(a[9])
            deny_message = await deny_partial_message.fetch()
            if deny_message.embeds[0].description is None:
                embed = discord.Embed(title=freelancer_busy_title, description=f"`{interaction.user.name}` `{self.values[0]}`", color=discord.Color.from_str(embed_color))
            else:
                desc = deny_message.embeds[0].description + f"\n`{interaction.user.name}` `{self.values[0]}`"
                embed = discord.Embed(title=freelancer_busy_title, description=desc, color=discord.Color.from_str(embed_color))
            await deny_partial_message.edit(embed=embed)
            embed = discord.Embed(title=denying_ticket_title, description=denying_ticket_description, color=discord.Color.from_str(embed_color))
            embed.set_footer(text=name, icon_url=main_guild.icon.url)
            await interaction.edit_original_response(embed=embed, view=None)
            await interaction.channel.set_permissions(interaction.user,
                view_channel=False
            )
            embed = discord.Embed(title=deny_success_ticket_title, description=deny_success_ticket_description, color=discord.Color.from_str(embed_color))
            embed.set_footer(text=name, icon_url=main_guild.icon.url)
            await interaction.edit_original_response(embed=embed, view=None)

class DenyDropdownView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

        self.add_item(DenyDropdown(bot))