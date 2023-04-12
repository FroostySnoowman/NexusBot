import discord
import aiosqlite
import pytz
import yaml
from datetime import datetime

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

with open('configmsg.yml', 'r') as file:
    msgdata = yaml.safe_load(file)

main_guild_id = data["General"]["MAIN_GUILD_ID"]
freelancer_guild_id = data["General"]["FREELANCER_GUILD_ID"]
staff_guild_id = data["General"]["STAFF_GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
name = data["General"]["NAME"]
tz_website = data["General"]["TZ_WEBSITE"]
freelancer_invalid_timezone = msgdata["Global"]["FREELANCER_INVALID_TIMEZONE"]
not_valid_paypal_email_link = msgdata["Freelancer"]["NOT_VALID_PAYPAL_EMAIL_LINK"]
not_valid_paypal_me_link = msgdata["Freelancer"]["NOT_VALID_PAYPAL_ME_LINK"]

class DashboardSystem1(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
    
    @discord.ui.button(emoji='💵', label='Wallet', style=discord.ButtonStyle.gray, custom_id='dashboardsystem:1')
    async def wallet(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (interaction.user.id,))
        a = await cursor.fetchone()
        embed = discord.Embed(color=discord.Color.from_str(embed_color))
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        if a is None:
            await db.execute('INSERT INTO freelancers VALUES (?,?,?,?,?,?,?);', (interaction.user.id, 0, 'NULL', 'NULL', 'NULL', 'NULL', 'NULL'))
            embed.add_field(name="Wallet", value="**$0.00**")
        else:
            embed.add_field(name="Wallet", value=f"**${a[1]:.2f}**")
        await interaction.response.edit_message(embed=embed, view=WalletSystem1(self.bot))

    @discord.ui.button(emoji='🧑‍💻', label='Profile', style=discord.ButtonStyle.gray, custom_id='dashboardsystem:2')
    async def profile(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (interaction.user.id,))
        a = await cursor.fetchone()
        embed = discord.Embed(color=discord.Color.from_str(embed_color))
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        if a is None:
            await db.execute('INSERT INTO freelancers VALUES (?,?,?,?,?,?,?);', (interaction.user.id, 0, 'NULL', 'NULL', 'NULL', 'NULL', 'NULL'))
            embed.add_field(name="Description", value="**N/A**", inline=True)
            embed.add_field(name="Portfolio", value="**N/A**", inline=True)
            embed.add_field(name="Timezone", value="**N/A**", inline=True)
            embed.add_field(name="PayPal", value="**N/A**", inline=True)
            embed.add_field(name="PayPal Me", value="**N/A**", inline=True)
        else:
            if a[2] == 'NULL':
                embed.add_field(name="Description", value="**N/A**", inline=True)
            else:
                embed.add_field(name="Description", value=f"{a[2]}", inline=True)
            if a[3] == 'NULL':
                embed.add_field(name="Portfolio", value="**N/A**", inline=True)
            else:
                embed.add_field(name="Portfolio", value=f"{a[3]}", inline=True)
            if a[4] == 'NULL':
                embed.add_field(name="Timezone", value="**N/A**", inline=True)
            else:
                try:
                    time = pytz.timezone(a[4])
                    settime = datetime.now(time)
                    settime = settime.strftime("%-I:%M:%S %p")
                    embed.add_field(name="Timezone", value=f"{a[4]} (Currrently: {settime})", inline=True)
                except:
                    embed.add_field(name="Timezone", value=freelancer_invalid_timezone, inline=True)
            if a[5] == 'NULL':
                embed.add_field(name="PayPal", value="**N/A**", inline=True)
            else:
                embed.add_field(name="PayPal", value=f"{a[5]}", inline=True)
            if a[6] == 'NULL':
                embed.add_field(name="PayPal Me", value="**N/A**", inline=True)
            else:
                embed.add_field(name="PayPal Me", value=f"{a[6]}", inline=True)
        await interaction.response.edit_message(embed=embed, view=ProfileSystem1(self.bot))

class WalletSystem1(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
    
    @discord.ui.button(emoji='💰', label='Request Payout', style=discord.ButtonStyle.gray, custom_id='walletsystem:1')
    async def payout(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Payout", ephemeral=True)

    @discord.ui.button(emoji='👈', label='Back', style=discord.ButtonStyle.red, custom_id='walletsystem:2', row=2)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(color=discord.Color.from_str(embed_color))
        embed.add_field(name="Wallet", value=f"View and manage your {name} wallet!", inline=False)
        embed.add_field(name="Profile", value=f"View and manage your {name} freelancer profile!", inline=False)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        await interaction.response.edit_message(embed=embed, view=DashboardSystem1(self.bot))

class ProfileSystem1(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
    
    @discord.ui.button(emoji='🦈', label='Set Description', style=discord.ButtonStyle.gray, custom_id='profilesystem:1')
    async def description(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SetDescription(self.bot))

    @discord.ui.button(emoji='✏️', label='Set Portfolio', style=discord.ButtonStyle.gray, custom_id='profilesystem:2')
    async def portfolio(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SetPortfolio(self.bot))

    @discord.ui.button(emoji='🌎', label='Set Timezone', style=discord.ButtonStyle.gray, custom_id='profilesystem:3')
    async def timezone(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SetTimezone(self.bot))

    @discord.ui.button(emoji='💰', label='Set PayPal', style=discord.ButtonStyle.gray, custom_id='profilesystem:4')
    async def paypal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SetPayPal(self.bot))

    @discord.ui.button(emoji='💸', label='Set PayPal Me', style=discord.ButtonStyle.gray, custom_id='profilesystem:5')
    async def paypalme(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SetPayPalMe(self.bot))

    @discord.ui.button(emoji='👈', label='Back', style=discord.ButtonStyle.red, custom_id='walletsystem:2', row=2)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(color=discord.Color.from_str(embed_color))
        embed.add_field(name="Wallet", value=f"View and manage your {name} wallet!", inline=False)
        embed.add_field(name="Profile", value=f"View and manage your {name} freelancer profile!", inline=False)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        await interaction.response.edit_message(embed=embed, view=DashboardSystem1(self.bot))

class SetDescription(discord.ui.Modal, title='Set Your Freelancer Description'):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    description = discord.ui.TextInput(
        label='Description',
        placeholder='Type your freelancer description here...',
        max_length=1000,
        style=discord.TextStyle.paragraph,
    )

    async def on_submit(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (interaction.user.id, ))
        a = await cursor.fetchone()
        if a is None:
            await db.execute('INSERT INTO freelancers VALUES (?,?,?,?,?,?,?);', (interaction.user.id, 0, self.description.value, 'NULL', 'NULL', 'NULL', 'NULL'))
        else:
            await db.execute('UPDATE freelancers SET description=? WHERE freelancer_id=?', (self.description.value, interaction.user.id))
        embed = discord.Embed(color=discord.Color.from_str(embed_color))
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        if self.description.value == 'NULL':
            description = '**N/A**'
        else:
            description = self.description.value
        if a[3] == 'NULL':
            portfolio = '**N/A**'
        else:
            portfolio = a[3]
        if a[4] == 'NULL':
            timezone = '**N/A**'
        else:
            try:
                time = pytz.timezone(a[4])
                settime = datetime.now(time)
                settime = settime.strftime("%-I:%M:%S %p")
                timezone = f"{a[4]} (Currently: {settime})"
            except:
                timezone = freelancer_invalid_timezone
        if a[5] == 'NULL':
            paypal = '**N/A**'
        else:
            paypal = a[5]
        if a[6] == 'NULL':
            paypalme = '**N/A**'
        else:
            paypalme = a[6]
        embed.add_field(name="Description", value=description, inline=True)
        embed.add_field(name="Portfolio", value=portfolio, inline=True)
        embed.add_field(name="Timezone", value=timezone, inline=True)
        embed.add_field(name="PayPal", value=paypal, inline=True)
        embed.add_field(name="PayPal Me", value=paypalme, inline=True)
        await interaction.response.edit_message(embed=embed, view=ProfileSystem1(self.bot))
        await db.commit()
        await db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)
        print(error)

class SetPortfolio(discord.ui.Modal, title='Set Your Freelancer Portfolio'):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    portfolio = discord.ui.TextInput(
        label='Portfolio',
        placeholder='Type your freelancer portfolio here...',
        max_length=200,
        style=discord.TextStyle.paragraph,
    )

    async def on_submit(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (interaction.user.id, ))
        a = await cursor.fetchone()
        if a is None:
            await db.execute('INSERT INTO freelancers VALUES (?,?,?,?,?,?,?);', (interaction.user.id, 0, 'NULL', self.portfolio.value, 'NULL', 'NULL', 'NULL'))
        else:
            await db.execute('UPDATE freelancers SET portfolio=? WHERE freelancer_id=?', (self.portfolio.value, interaction.user.id))
        embed = discord.Embed(color=discord.Color.from_str(embed_color))
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        if a[2] == 'NULL':
            description = '**N/A**'
        else:
            description = a[2]
        if self.portfolio.value == 'NULL':
            portfolio = '**N/A**'
        else:
            portfolio = self.portfolio.value
        if a[4] == 'NULL':
            timezone = '**N/A**'
        else:
            try:
                time = pytz.timezone(a[4])
                settime = datetime.now(time)
                settime = settime.strftime("%-I:%M:%S %p")
                timezone = f"{a[4]} (Currently: {settime})"
            except:
                timezone = freelancer_invalid_timezone
        if a[5] == 'NULL':
            paypal = '**N/A**'
        else:
            paypal = a[5]
        if a[6] == 'NULL':
            paypalme = '**N/A**'
        else:
            paypalme = a[6]
        embed.add_field(name="Description", value=description, inline=True)
        embed.add_field(name="Portfolio", value=portfolio, inline=True)
        embed.add_field(name="Timezone", value=timezone, inline=True)
        embed.add_field(name="PayPal", value=paypal, inline=True)
        embed.add_field(name="PayPal Me", value=paypalme, inline=True)
        await interaction.response.edit_message(embed=embed, view=ProfileSystem1(self.bot))
        await db.commit()
        await db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)
        print(error)

class SetTimezone(discord.ui.Modal, title='Set Your Timezone'):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    timezone = discord.ui.TextInput(
        label=f'Timezone From {tz_website}',
        placeholder='Type your timezone here...',
        max_length=50,
        style=discord.TextStyle.short,
    )

    async def on_submit(self, interaction: discord.Interaction):
        if self.timezone.value in pytz.all_timezones:
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (interaction.user.id, ))
            a = await cursor.fetchone()
            if a is None:
                await db.execute('INSERT INTO freelancers VALUES (?,?,?,?,?,?,?);', (interaction.user.id, 0, 'NULL', 'NULL', self.timezone.value, 'NULL', 'NULL'))
            else:
                await db.execute('UPDATE freelancers SET timezone=? WHERE freelancer_id=?', (self.timezone.value, interaction.user.id))
            embed = discord.Embed(color=discord.Color.from_str(embed_color))
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            if a[2] == 'NULL':
                description = '**N/A**'
            else:
                description = a[2]
            if a[3] == 'NULL':
                portfolio = '**N/A**'
            else:
                portfolio = a[3]
            if self.timezone.value == 'NULL':
                timezone = '**N/A**'
            else:
                try:
                    time = pytz.timezone(self.timezone.value)
                    settime = datetime.now(time)
                    settime = settime.strftime("%-I:%M:%S %p")
                    timezone = f"{self.timezone.value} (Currently: {settime})"
                except:
                    timezone = freelancer_invalid_timezone
            if a[5] == 'NULL':
                paypal = '**N/A**'
            else:
                paypal = a[5]
            if a[6] == 'NULL':
                paypalme = '**N/A**'
            else:
                paypalme = a[6]
            embed.add_field(name="Description", value=description, inline=True)
            embed.add_field(name="Portfolio", value=portfolio, inline=True)
            embed.add_field(name="Timezone", value=timezone, inline=True)
            embed.add_field(name="PayPal", value=paypal, inline=True)
            embed.add_field(name="PayPal Me", value=paypalme, inline=True)
            await interaction.response.edit_message(embed=embed, view=ProfileSystem1(self.bot))
            await db.commit()
            await db.close()
        else:
            embed = discord.Embed(description=f"You must provide a valid timezone from the list displayed at **{tz_website}**!", color=discord.Color.red())
            await interaction.response.edit_message(embed=embed, view=None)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)
        print(error)

class SetPayPal(discord.ui.Modal, title='Set Your PayPal'):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    paypal = discord.ui.TextInput(
        label=f'PayPal',
        placeholder='Type your paypal email here...',
        max_length=50,
        style=discord.TextStyle.short,
    )

    async def on_submit(self, interaction: discord.Interaction):
        if "@" in self.paypal.value or "NULL" in self.paypal.value:
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (interaction.user.id, ))
            a = await cursor.fetchone()
            if a is None:
                await db.execute('INSERT INTO freelancers VALUES (?,?,?,?,?,?,?);', (interaction.user.id, 0, 'NULL' 'NULL', 'NULL', self.paypal.value, 'NULL'))
            else:
                await db.execute('UPDATE freelancers SET paypal=? WHERE freelancer_id=?', (self.paypal.value, interaction.user.id))
            embed = discord.Embed(color=discord.Color.from_str(embed_color))
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            if a[2] == 'NULL':
                description = '**N/A**'
            else:
                description = a[2]
            if a[3] == 'NULL':
                portfolio = '**N/A**'
            else:
                portfolio = a[3]
            if a[4] == 'NULL':
                timezone = '**N/A**'
            else:
                try:
                    time = pytz.timezone(a[4])
                    settime = datetime.now(time)
                    settime = settime.strftime("%-I:%M:%S %p")
                    timezone = f"{a[4]} (Currently: {settime})"
                except:
                    timezone = freelancer_invalid_timezone
            if self.paypal.value == 'NULL':
                paypal = '**N/A**'
            else:
                paypal = self.paypal.value
            if a[6] == 'NULL':
                paypalme = '**N/A**'
            else:
                paypalme = a[6]
            embed.add_field(name="Description", value=description, inline=True)
            embed.add_field(name="Portfolio", value=portfolio, inline=True)
            embed.add_field(name="Timezone", value=timezone, inline=True)
            embed.add_field(name="PayPal", value=paypal, inline=True)
            embed.add_field(name="PayPal Me", value=paypalme, inline=True)
            await interaction.response.edit_message(embed=embed, view=ProfileSystem1(self.bot))
            await db.commit()
            await db.close()
        else:
            embed = discord.Embed(description=not_valid_paypal_email_link, color=discord.Color.red())
            await interaction.response.edit_message(embed=embed, view=None)

class SetPayPalMe(discord.ui.Modal, title='Set Your PayPal Me'):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    paypalme = discord.ui.TextInput(
        label=f'PayPal Me',
        placeholder='Type your paypal me link here...',
        max_length=200,
        style=discord.TextStyle.short,
    )

    async def on_submit(self, interaction: discord.Interaction):
        if "paypal.me/" in self.paypalme.value or "NULL" in self.paypalme.value:
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (interaction.user.id, ))
            a = await cursor.fetchone()
            if a is None:
                await db.execute('INSERT INTO freelancers VALUES (?,?,?,?,?,?,?);', (interaction.user.id, 0, 'NULL', 'NULL', 'NULL', 'NULL', self.paypalme.value))
            else:
                await db.execute('UPDATE freelancers SET paypalme=? WHERE freelancer_id=?', (self.paypalme.value, interaction.user.id))
            embed = discord.Embed(color=discord.Color.from_str(embed_color))
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            if a[2] == 'NULL':
                description = '**N/A**'
            else:
                description = a[2]
            if a[3] == 'NULL':
                portfolio = '**N/A**'
            else:
                portfolio = a[3]
            if a[4] == 'NULL':
                timezone = '**N/A**'
            else:
                try:
                    time = pytz.timezone(a[4])
                    settime = datetime.now(time)
                    settime = settime.strftime("%-I:%M:%S %p")
                    timezone = f"{a[4]} (Currently: {settime})"
                except:
                    timezone = freelancer_invalid_timezone
            if a[5] == 'NULL':
                paypal = '**N/A**'
            else:
                paypal = a[5]
            if self.paypalme.value == 'NULL':
                paypalme = '**N/A**'
            else:
                paypalme = self.paypalme.value
            embed.add_field(name="Description", value=description, inline=True)
            embed.add_field(name="Portfolio", value=portfolio, inline=True)
            embed.add_field(name="Timezone", value=timezone, inline=True)
            embed.add_field(name="PayPal", value=paypal, inline=True)
            embed.add_field(name="PayPal Me", value=paypalme, inline=True)
            await interaction.response.edit_message(embed=embed, view=ProfileSystem1(self.bot))
            await db.commit()
            await db.close()
        else:
            embed = discord.Embed(description=not_valid_paypal_me_link, color=discord.Color.red())
            await interaction.response.edit_message(embed=embed, view=None)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)
        print(error)