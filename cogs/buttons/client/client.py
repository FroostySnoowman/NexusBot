import discord
import aiosqlite
import qrcode
import yaml
import io
from cogs.modals.client import ClientDenyQuoteModal
from cogs.functions.client import createinvoice
from discord.ext import tasks

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

with open('configmsg.yml', 'r') as file:
    msgdata = yaml.safe_load(file)

main_guild_id = data["General"]["MAIN_GUILD_ID"]
freelancer_guild_id = data["General"]["FREELANCER_GUILD_ID"]
staff_guild_id = data["General"]["STAFF_GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
name = data["General"]["NAME"]
accept_quote_title = msgdata["Client"]["ACCEPT_QUOTE_TITLE"]
accept_quote_description = msgdata["Client"]["ACCEPT_QUOTE_DESCRIPTION"]
not_client_accept_quote_title = msgdata["Client"]["NOT_CLIENT_ACCEPT_QUOTE_TITLE"]
not_client_accept_quote_description = msgdata["Client"]["NOT_CLIENT_ACCEPT_QUOTE_DESCRIPTION"]
success_accept_quote_title = msgdata["Client"]["SUCCESS_ACCEPT_QUOTE_TITLE"]
success_accept_quote_description = msgdata["Client"]["SUCCESS_ACCEPT_QUOTE_DESCRIPTION"]
success_accept_quote_title2 = msgdata["Client"]["SUCCESS_ACCEPT_QUOTE_TITLE2"]
success_accept_quote_description2 = msgdata["Client"]["SUCCESS_ACCEPT_QUOTE_DESCRIPTION2"]
not_client_paypal_invoice_title = msgdata["Client"]["NOT_CLIENT_PAYPAL_INVOICE_TITLE"]
not_client_paypal_invoice_description = msgdata["Client"]["NOT_CLIENT_PAYPAL_INVOICE_DESCRIPTION"]
paypal_invoice_title = msgdata["Client"]["PAYPAL_INVOICE_TITLE"]
paypal_invoice_description = msgdata["Client"]["PAYPAL_INVOICE_DESCRIPTION"]
success_paypal_invoice_title = msgdata["Client"]["SUCCESS_PAYPAL_INVOICE_TITLE"]
success_paypal_invoice_description = msgdata["Client"]["SUCCESS_PAYPAL_INVOICE_DESCRIPTION"]
not_client_balance_invoice_title = msgdata["Client"]["NOT_CLIENT_BALANCE_INVOICE_TITLE"]
not_client_balance_invoice_description = msgdata["Client"]["NOT_CLIENT_BALANCE_INVOICE_DESCRIPTION"]
not_client_deny_quote_title = msgdata["Client"]["NOT_CLIENT_DENY_QUOTE_TITLE"]
not_client_deny_quote_description = msgdata["Client"]["NOT_CLIENT_DENY_QUOTE_DESCRIPTION"]

class ClientSystem(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
    
    @discord.ui.button(label='Accept', style=discord.ButtonStyle.green, custom_id='clientsystem:1')
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM commissions WHERE main_server_channel_id=?', (interaction.channel.id,))
        a = await cursor.fetchone()
        if a[0] == interaction.user.id:
            embed = discord.Embed(title=accept_quote_title, description=accept_quote_description, color=discord.Color.from_str(embed_color))
            await interaction.response.send_message(embed=embed, ephemeral=True)
            cursor = await db.execute('SELECT * FROM quotes WHERE quote_message_id=?', (interaction.message.id,))
            b = await cursor.fetchone()
            cursor = await db.execute('SELECT * FROM quotes WHERE main_server_channel_id=?', (interaction.channel.id,))
            c = await cursor.fetchall()
            cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (interaction.user.id,))
            d = await cursor.fetchone()
            for x in c:
                quote = interaction.channel.get_partial_message(x[4])
                await quote.delete()
            questionmsg = interaction.channel.get_partial_message(a[8])
            await questionmsg.delete()
            replymsg = interaction.channel.get_partial_message(a[9])
            await replymsg.delete()
            freelancer_server_channel = self.bot.get_channel(a[7])
            await freelancer_server_channel.delete()
            await db.execute('UPDATE commissions SET freelancer_id=?, freelancer_server_channel_id=?, ticket_channel_messaging_message_id=?, quote_channel_messaging_message_id=? WHERE main_server_channel_id=?', (b[0], 'NULL', 'NULL', 'NULL', interaction.channel.id))
            await db.execute('DELETE FROM quotes WHERE main_server_channel_id=?', (interaction.channel.id, ))
            description = success_accept_quote_description.replace("%FREELANCERNAME%", f"{interaction.user.name}")
            description = description.replace("%FREELANCER%", f"{interaction.user}")
            embed = discord.Embed(title=success_accept_quote_title, description=description, color=discord.Color.from_str(embed_color))
            await interaction.edit_original_response(embed=embed)
            main_server_role_id = None
            for item in data['Roles'][a[4]]:
                if isinstance(item, dict) and a[5] in item:
                    main_server_role_id = item[a[5]][0]
                    main_server_role_category_id = item[a[5]][3]
                    break
            main_server_role_category = self.bot.get_channel(main_server_role_category_id)
            await interaction.channel.edit(category=main_server_role_category)
            description = success_accept_quote_description2.replace("%QUOTE%", f"{b[3]:.2f}")
            description = description.replace("%SERVICE%", f"<@&{main_server_role_id}>")
            description = description.replace("%FREELANCERNAME%", f"{interaction.user.name}")
            description = description.replace("%FREELANCER%", f"{interaction.user}")
            f = discord.File("imgs/invoice.png", filename="invoice.png")
            embed = discord.Embed(title=success_accept_quote_title2, description=description, color=discord.Color.from_str(embed_color))
            embed.set_thumbnail(url="attachment://invoice.png")
            view = PaySystem(self.bot)
            if d is None:
                view.balance.disabled = True
            if d[1] == 0:
                view.balance.disabled = True
            await interaction.channel.send(embed=embed, view=view, file=f)
        else:
            embed = discord.Embed(title=not_client_accept_quote_title, description=not_client_accept_quote_description, color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

    @discord.ui.button(label='Deny', style=discord.ButtonStyle.red, custom_id='clientsystem:2')
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM commissions WHERE main_server_channel_id=?', (interaction.channel.id,))
        a = await cursor.fetchone()
        if a[0] == interaction.user.id:
            await interaction.response.send_modal(ClientDenyQuoteModal(self.bot))
        else:
            embed = discord.Embed(title=not_client_deny_quote_title, description=not_client_deny_quote_description, color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.close()

class PaySystem(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label='PayPal', style=discord.ButtonStyle.blurple, custom_id='paysystem:1')
    async def paypal(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM commissions WHERE main_server_channel_id=?', (interaction.channel.id,))
        a = await cursor.fetchone()
        if a[0] == interaction.user.id:
            embed = discord.Embed(title=paypal_invoice_title, description=paypal_invoice_description, color=discord.Color.from_str(embed_color))
            await interaction.response.edit_message(embed=embed, view=None, attachments=[])
            id = await createinvoice(a[1])
            img = qrcode.make(f'https://www.paypal.com/invoice/s/pay/{id}')
            fp = io.BytesIO()
            img.save(fp)
            fp.seek(0)
            f = discord.File(fp, filename="paypal.png")
            embed = discord.Embed(title=success_paypal_invoice_title, description=success_paypal_invoice_description, color=discord.Color.from_str(embed_color))
            embed.set_thumbnail(url="attachment://paypal.png")
            msg = await interaction.edit_original_response(embed=embed, view=PayPalLink(id), attachments=[f])
            total = a[1] + (a[1] * 0.05 + 0.4)
            fees = a[1] * 0.05 + 0.4
            await db.execute('INSERT INTO invoices VALUES (?,?,?,?,?,?,?);', (interaction.channel.id, msg.id, id, a[1], fees, total, "UNPAID"))
        else:
            embed = discord.Embed(title=not_client_paypal_invoice_title, description=not_client_paypal_invoice_description, color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

    @discord.ui.button(label='Balance', style=discord.ButtonStyle.blurple, custom_id='paysystem:2')
    async def balance(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM commissions WHERE main_server_channel_id=?', (interaction.channel.id,))
        a = await cursor.fetchone()
        if a[0] == interaction.user.id:
            await interaction.response.send_message("Balance stuff here...", ephemeral=True)
        else:
            embed = discord.Embed(title=not_client_balance_invoice_title, description=not_client_balance_invoice_description, color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

class PayPalLink(discord.ui.View):
    def __init__(self, id):
        super().__init__()
        id = id
        url = f'https://www.paypal.com/invoice/s/pay/{id}'
        self.add_item(discord.ui.Button(emoji='<:PayPal:1092994298972213269>', label='Pay', url=url))