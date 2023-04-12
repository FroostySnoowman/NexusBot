import discord
import aiosqlite
import yaml
from cogs.modals.freelancer import FreelancerQuoteModal
from cogs.dropdowns.freelancer import DenyDropdownView

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

with open('configmsg.yml', 'r') as file:
    msgdata = yaml.safe_load(file)

main_guild_id = data["General"]["MAIN_GUILD_ID"]
freelancer_guild_id = data["General"]["FREELANCER_GUILD_ID"]
staff_guild_id = data["General"]["STAFF_GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
deny_ticket_title = msgdata["Freelancer"]["DENY_TICKET_TITLE"]
deny_ticket_description = msgdata["Freelancer"]["DENY_TICKET_DESCRIPTION"]
not_in_freelancers_table_title = msgdata["Global"]["NOT_IN_FREELANCERS_TABLE_TITLE"]
not_in_freelancers_table_description = msgdata["Global"]["NOT_IN_FREELANCERS_TABLE_DESCRIPTION"]

class FreelancerSystem(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
    
    @discord.ui.button(label='Quote', style=discord.ButtonStyle.green, custom_id='freelancersystem:1')
    async def quote(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (interaction.user.id,))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(title=not_in_freelancers_table_title, description=not_in_freelancers_table_description, color=discord.Coor.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_modal(FreelancerQuoteModal(self.bot))
        await db.close()

    @discord.ui.button(label='Deny', style=discord.ButtonStyle.red, custom_id='freelancersystem:2')
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (interaction.user.id,))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(title=not_in_freelancers_table_title, description=not_in_freelancers_table_description, color=discord.Coor.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title=deny_ticket_title, description=deny_ticket_description, color=discord.Color.from_str(embed_color))
            await interaction.response.send_message(embed=embed, view=DenyDropdownView(self.bot), ephemeral=True)

    @discord.ui.button(label='Reviews', style=discord.ButtonStyle.blurple, custom_id='freelancersystem:3')
    async def reviews(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (interaction.user.id,))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(title=not_in_freelancers_table_title, description=not_in_freelancers_table_description, color=discord.Coor.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("Reviews coming soon...", ephemeral=True)