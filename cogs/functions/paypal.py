import discord
import aiosqlite
import paypalrestsdk
import yaml
from discord.ext import commands, tasks

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

with open('configmsg.yml', 'r') as file:
    msgdata = yaml.safe_load(file)

embed_color = data["General"]["EMBED_COLOR"]
paypal_client_id = data["PayPal"]["PAYPAL_CLIENT_ID"]
paypal_client_secret = data["PayPal"]["PAYPAL_CLIENT_SECRET"]
paid_paypal_invoice_title = msgdata["Client"]["PAID_PAYPAL_INVOICE_TITLE"]
paid_paypal_invoice_description = msgdata["Client"]["PAID_PAYPAL_INVOICE_DESCRIPTION"]
paypal_payment_received_title = msgdata["Client"]["PAYPAL_PAYMENT_RECEIVED_TITLE"]
paypal_payment_received_description = msgdata["Client"]["PAYPAL_PAYMENT_RECEIVED_DESCRIPTION"]

my_api = paypalrestsdk.Api({
  'mode': 'live',
  'client_id': paypal_client_id,
  'client_secret': paypal_client_secret})

class PayPalPaidCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def cog_load(self):
        self.paypalLoop.start()

    @tasks.loop(seconds = 5)
    async def paypalLoop(self):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM invoices')
        a = await cursor.fetchall()
        for b in a:
            if b[6] == "PAID":
                continue
            else:
                channel = self.bot.get_channel(b[0])
                partialmessage = channel.get_partial_message(b[1])
                message = await channel.fetch_message(partialmessage.id)
                payment = paypalrestsdk.Invoice.find(f"{b[2]}", api=my_api)
                x = payment['status']
                x = "PAID"
                if x == "PAID":
                    cursor = await db.execute('SELECT * FROM commissions WHERE main_server_channel_id=?', (channel.id, ))
                    c = await cursor.fetchone()
                    await db.execute('UPDATE invoices SET status=? WHERE message_id=?', ('PAID', b[1]))
                    embed = discord.Embed(title=paid_paypal_invoice_title, description=paid_paypal_invoice_description, color=discord.Color.from_str(embed_color))
                    embed.set_thumbnail(url=message.embeds[0].thumbnail.url)
                    await message.edit(embed=embed, attachments=[])
                    embed = discord.Embed(title=paypal_payment_received_title, description=paypal_payment_received_description, color=discord.Color.from_str(embed_color))
                    await channel.send(content=f"<@{c[0]}> | <@{c[11]}>", embed=embed)
                else:
                    continue
        await db.commit()
        await db.close()

    @paypalLoop.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(PayPalPaidCog(bot))