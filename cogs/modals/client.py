import discord
import aiosqlite
import yaml
from cogs.functions.freelancer import CannotSendFreelancerMessage

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

with open('configmsg.yml', 'r') as file:
    msgdata = yaml.safe_load(file)

main_guild_id = data["General"]["MAIN_GUILD_ID"]
freelancer_guild_id = data["General"]["FREELANCER_GUILD_ID"]
staff_guild_id = data["General"]["STAFF_GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
deny_quote_title = msgdata["Client"]["DENY_QUOTE_TITLE"]
deny_quote_description = msgdata["Client"]["DENY_QUOTE_DESCRIPTION"]
success_deny_quote_title = msgdata["Client"]["SUCCESS_DENY_QUOTE_TITLE"]
success_deny_quote_description = msgdata["Client"]["SUCCESS_DENY_QUOTE_DESCRIPTION"]
deny_quote_freelancer_title = msgdata["Client"]["DENY_QUOTE_FREELANCER_TITLE"]
deny_quote_freelancer_description = msgdata["Client"]["DENY_QUOTE_FREELANCER_DESCRIPTION"]

class ClientDenyQuoteModal(discord.ui.Modal, title='Quote'):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    reason = discord.ui.TextInput(
        label='What is the reason for denying this quote?',
        placeholder='Type the reason here...',
        max_length=2000,
        style=discord.TextStyle.paragraph,
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=deny_quote_title, description=deny_quote_description, color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM quotes WHERE quote_message_id=?', (interaction.message.id,))
        a = await cursor.fetchone()
        await db.execute('DELETE FROM quotes WHERE quote_message_id=?', (interaction.message.id, ))
        await interaction.message.delete()
        freelancer = interaction.guild.get_member(a[0])
        channel = self.bot.get_channel(a[2])
        try:
            description = deny_quote_freelancer_description.replace("%FREELANCER_SERVER_CHANNEL_MENTION%", f"{channel.mention}")
            description = description.replace("%REASON%", f"{self.reason.value}")
            embed = discord.Embed(title=deny_quote_freelancer_title, description=description, color=discord.Color.from_str(embed_color))
            await freelancer.send(embed=embed)
        except:
            reason = "Quote Denied"
            await CannotSendFreelancerMessage(self.bot, freelancer, deny_quote_freelancer_title, description, reason)
        embed = discord.Embed(title=success_deny_quote_title, description=success_deny_quote_description,color=discord.Color.from_str(embed_color))
        await interaction.edit_original_response(embed=embed)
        await db.commit()
        await db.close()