import discord
import asyncio
import datetime as DT
import aiosqlite
import yaml
import re
from datetime import datetime, timedelta
from cogs.buttons.freelancer.freelancer import FreelancerSystem

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

with open('configmsg.yml', 'r') as file:
    msgdata = yaml.safe_load(file)

main_guild_id = data["General"]["MAIN_GUILD_ID"]
freelancer_guild_id = data["General"]["FREELANCER_GUILD_ID"]
staff_guild_id = data["General"]["STAFF_GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
commission1_ticket_category_id = data["Channels"]["COMMISSION1_TICKET_CATEGORY_ID"]
commission2_ticket_category_id = data["Channels"]["COMMISSION2_TICKET_CATEGORY_ID"]
commission3_ticket_category_id = data["Channels"]["COMMISSION3_TICKET_CATEGORY_ID"]
commission4_ticket_category_id = data["Channels"]["COMMISSION4_TICKET_CATEGORY_ID"]
claim_ticket_channel_id = data["Channels"]["CLAIM_TICKET_CHANNEL_ID"]
tos_agreement_title = msgdata["Order"]["TOS_AGREEMENT_TITLE"]
tos_agreement_description = msgdata["Order"]["TOS_AGREEMENT_DESCRIPTION"]
decline_tos_agreement_title = msgdata["Order"]["DECLINE_TOS_AGREEMENT_TITLE"]
decline_tos_agreement_description = msgdata["Order"]["DECLINE_TOS_AGREEMENT_DESCRIPTION"]
invalid_budget_title = msgdata["Order"]["INVALID_BUDGET_TITLE"]
invalid_budget_description = msgdata["Order"]["INVALID_BUDGET_DESCRIPTION"]
invalid_deadline_not_enough_args_title = msgdata["Order"]["INVALID_DEADLINE_NOT_ENOUGH_ARGS_TITLE"]
invalid_deadline_not_enough_args_description = msgdata["Order"]["INVALID_DEADLINE_NOT_ENOUGH_ARGS_DESCRIPTION"]
invalid_deadline_args_invalid_title = msgdata["Order"]["INVALID_DEADLINE_ARGS_INVALID_TITLE"]
invalid_deadline_args_invalid_description = msgdata["Order"]["INVALID_DEADLINE_ARGS_INVALID_DESCRIPTION"]
max_tickets_open_title = msgdata["Order"]["MAX_TICKETS_OPEN_TITLE"]
max_tickets_open_description = msgdata["Order"]["MAX_TICKETS_OPEN_DESCRIPTION"]
new_order_category_ticket_title = msgdata["Order"]["NEW_ORDER_CATEGORY_TICKET_TITLE"]
new_order_category_ticket_description = msgdata["Order"]["NEW_ORDER_CATEGORY_TICKET_DESCRIPTION"]
new_order_role_ticket_title = msgdata["Order"]["NEW_ORDER_ROLE_TICKET_TITLE"]
new_order_role_ticket_description = msgdata["Order"]["NEW_ORDER_ROLE_TICKET_DESCRIPTION"]
new_order_creating_title = msgdata["Order"]["NEW_ORDER_CREATING_TITLE"]
new_order_creating_description = msgdata["Order"]["NEW_ORDER_CREATING_DESCRIPTION"]
success_new_order_creating_title = msgdata["Order"]["SUCCESS_NEW_ORDER_CREATING_TITLE"]
success_new_order_creating_description = msgdata["Order"]["SUCCESS_NEW_ORDER_CREATING_DESCRIPTION"]
client_messaging_title = msgdata["Order"]["CLIENT_MESSAGING_TITLE"]
client_messaging_description = msgdata["Order"]["CLIENT_MESSAGING_DESCRIPTION"]
freelancer_messaging_title = msgdata["Order"]["FREELANCER_MESSAGING_TITLE"]
freelancer_messaging_description = msgdata["Order"]["FREELANCER_MESSAGING_DESCRIPTION"]
freelancer_busy_title = msgdata["Order"]["FREELANCER_BUSY_TITLE"]
freelancer_busy_footer = msgdata["Order"]["FREELANCER_BUSY_FOOTER"]

class CreateTicket(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
    
    @discord.ui.button(label='Order', style=discord.ButtonStyle.green, custom_id='create:1')
    async def order(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title=tos_agreement_title, description=tos_agreement_description, color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, view=TOSAgreement(self.bot), ephemeral=True)

    @discord.ui.button(label='Support', style=discord.ButtonStyle.red, custom_id='create:2')
    async def support(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('test')

class TOSAgreement(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
    
    @discord.ui.button(label='Accept', style=discord.ButtonStyle.green, custom_id='tos:1')
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title=new_order_category_ticket_title, description=new_order_category_ticket_description, color=discord.Color.from_str(embed_color))
        await interaction.response.edit_message(embed=embed, view=OrderCategoryDropdownView(self.bot))

    @discord.ui.button(label='Decline', style=discord.ButtonStyle.red, custom_id='tos:2')
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title=decline_tos_agreement_title, description=decline_tos_agreement_description, color=discord.Color.red())
        await interaction.response.edit_message(embed=embed, view=None)

class OrderCategoryDropdown(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot

        options = []
        for category in data["Roles"].items():
            emoji = data["Roles"][category[0]][0]
            cat = category[0].replace("_", " ")
            options.append(discord.SelectOption(label=cat, emoji=emoji, description=cat))
        

        super().__init__(placeholder="Select a department related to your ticket!", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title=new_order_role_ticket_title, description=new_order_role_ticket_description, color=discord.Color.from_str(embed_color))
        category = self.values[0].replace(" ", "_")
        await interaction.response.edit_message(embed=embed, view=OrderRoleDropdownView(self.bot, category))

class OrderCategoryDropdownView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

        self.add_item(OrderCategoryDropdown(bot))

class OrderRoleDropdown(discord.ui.Select):
    def __init__(self, bot, category):
        self.bot = bot
        self.category = category

        options = []
        num = 0
        for roles in data["Roles"][category]:
            if num == 0:
                num += 1
                continue
            else:
                role = next(iter(roles.keys())).title()
                roles[list(roles.keys())[0]][0]
                emoji = roles[list(roles.keys())[0]][4]
                role = role.replace("_", " ")
                role = role.replace("Gfx", "GFX")
                options.append(discord.SelectOption(label=role, emoji=emoji, description=role))
        

        super().__init__(placeholder="Select a role related to your ticket!", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        value = self.values[0].upper()
        value = value.replace(" ", "_")
        role = data["Roles"][self.category]
        for item in role:
            if value in item:
                main_server_freelancer_role_id = item[value][0]
                freelancer_server_freelancer_role_id = item[value][1]
                freelancer_category_id = item[value][2]
                main_category_id = item[value][3]
                break
        await interaction.response.send_modal(OrderModal(self.bot, main_server_freelancer_role_id, freelancer_server_freelancer_role_id, freelancer_category_id, main_category_id, self.category, value))

class OrderRoleDropdownView(discord.ui.View):
    def __init__(self, bot, category):
        super().__init__()
        self.bot = bot
        self.category = category

        self.add_item(OrderRoleDropdown(bot, category))

class OrderModal(discord.ui.Modal, title='Order Services'):
    def __init__(self, bot, main_server_freelancer_role_id, freelancer_server_freelancer_role_id, freelancer_category_id, main_category_id, category, value):
        super().__init__(timeout=None)
        self.bot = bot
        self.main_server_freelancer_role_id = main_server_freelancer_role_id
        self.freelancer_server_freelancer_role_id = freelancer_server_freelancer_role_id
        self.freelancer_category_id = freelancer_category_id
        self.main_category_id = main_category_id
        self.category = category
        self.value = value

    budget = discord.ui.TextInput(
        label='Budget',
        placeholder='What is your budget in USD?',
        max_length=5,
    )

    deadline = discord.ui.TextInput(
        label='Deadline',
        placeholder='What is your deadline? Ex: 7d, 1w, 1m',
        max_length=25,
    )

    description = discord.ui.TextInput(
        label='Project Description',
        style=discord.TextStyle.long,
        placeholder='What is your project description?',
        max_length=2000,
        min_length=100,
    )

    async def on_submit(self, interaction: discord.Interaction):
        budget = self.budget.value

        # CHECK FOR INVALID BUDGETS
        if "$" in budget:
            budget = budget.replace("$", "")
        try:
            int(budget)
        except:
            embed = discord.Embed(title=invalid_budget_title, description=invalid_budget_description, color=discord.Color.red())
            await interaction.response.edit_message(embed=embed, view=None)
            return
        
        # CHECK FOR INVALID DEADLINES
        try:
            time_list = re.split('(\d+)', self.deadline.value)
            if time_list[2] == "d":
                time_in_s = int(time_list[1]) * 60 * 60 * 24
            if time_list[2] == "w":
                time_in_s = int(time_list[1]) * 60 * 60 * 24 * 7
            if time_list[2] == "m":
                time_in_s = int(time_list[1]) * 60 * 60 * 24 * 30
            timestamp = DT.datetime.now().timestamp()
            x = datetime.now() + timedelta(seconds=time_in_s)
            timestamp = int(x.timestamp())
        except IndexError:
            embed = discord.Embed(title=invalid_deadline_not_enough_args_title, description=invalid_deadline_not_enough_args_description, color=discord.Color.red())
            await interaction.response.edit_message(embed=embed, view=None)
            return
        except UnboundLocalError:
            embed = discord.Embed(title=invalid_deadline_args_invalid_title, description=invalid_deadline_args_invalid_description, color=discord.Color.red())
            await interaction.response.edit_message(embed=embed, view=None)
            return
        
        embed = discord.Embed(title=new_order_creating_title, description=new_order_creating_description, color=discord.Color.from_str(embed_color))
        await interaction.response.edit_message(embed=embed, view=None)
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM busy')
        a = await cursor.fetchall()

        # GUILDS
        staff_server = self.bot.get_guild(staff_guild_id)
        freelancer_server = self.bot.get_guild(freelancer_guild_id)

        # ROLES
        main_server_freelancer_role = interaction.guild.get_role(self.main_server_freelancer_role_id)
        freelancer_server_freelancer_role = freelancer_server.get_role(self.freelancer_server_freelancer_role_id)

        # CATEGORIES
        freelancer_category = freelancer_server.get_channel(self.freelancer_category_id)
        main_category1 = interaction.guild.get_channel(commission1_ticket_category_id)
        main_category2 = interaction.guild.get_channel(commission2_ticket_category_id)
        main_category3 = interaction.guild.get_channel(commission3_ticket_category_id)
        main_category4 = interaction.guild.get_channel(commission4_ticket_category_id)

        if len(main_category1.channels) >= 25:
            if len(main_category2.channels) >= 25:
                if len(main_category3.channels) >= 25:
                    if len(main_category4.channels) >= 25:
                        embed = discord.Embed(title=max_tickets_open_title, description=max_tickets_open_description, color=discord.Color.red())
                        await interaction.edit_original_response(content=None, embed=embed, view=None)
                        await db.close()
                        return
                    else:
                        main_category = main_category4
                else:
                    main_category = main_category3
            else:
                main_category = main_category2
        else:
            main_category = main_category1
        
        ticket_channel = await main_category.create_text_channel(f"order-{interaction.user.name}")
        await ticket_channel.set_permissions(interaction.guild.get_role(interaction.guild.id),
            send_messages=False,
            read_messages=False
        )
        
        await ticket_channel.set_permissions(interaction.user,
            send_messages=True,
            read_messages=True,
            add_reactions=True,
            embed_links=True,
            attach_files=True,
            read_message_history=True,
            external_emojis=True,
            use_application_commands=True
        )

        quote_channel = await freelancer_category.create_text_channel(f"quote-{interaction.user.name}")
        await quote_channel.set_permissions(freelancer_server.get_role(freelancer_guild_id),
            send_messages=False,
            read_messages=False
        )
        try:
            await quote_channel.set_permissions(interaction.user,
                send_messages=False,
                read_messages=False,
                add_reactions=False,
                embed_links=False,
                attach_files=False,
                read_message_history=False,
                external_emojis=False,
                use_application_commands=False
            )
        except:
            pass

        await quote_channel.set_permissions(freelancer_server_freelancer_role,
            send_messages=True,
            read_messages=True,
            add_reactions=True,
            embed_links=True,
            attach_files=True,
            read_message_history=True,
            external_emojis=True,
            use_application_commands=True
        )

        # QUOTE CHANNEL MESSAGE
        for users in a:
            try:
                user = freelancer_server.get_member(users[0])
                await quote_channel.set_permissions(user,
                    send_messages=False,
                    read_messages=False,
                    add_reactions=False,
                    embed_links=False,
                    attach_files=False,
                    read_message_history=False,
                    external_emojis=False,
                    use_application_commands=False
                )
            except:
                continue

        embed = discord.Embed(title="Ticket Information", description=f"""
**Description**
{self.description.value}

**Budget**
${budget}

**Deadline**
<t:{timestamp}:F>
""",
        color=discord.Color.from_str(embed_color))
        embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url)
        embed.timestamp = DT.datetime.now()

        b = await quote_channel.send(content=f"New ticket for {freelancer_server_freelancer_role.mention}!", embed=embed, view=FreelancerSystem(self.bot))
        try:
            c = asyncio.create_task(self.bot.wait_for("message", check=lambda message: message.type is discord.MessageType.pins_add and message.reference.message_id == b.id, timeout=5))
            await b.pin()
            found_message = await c
            await found_message.delete()
        except:
            pass

        embed = discord.Embed(title=client_messaging_title, description=client_messaging_description, color=discord.Color.from_str(embed_color))
        embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url)
        embed.timestamp = DT.datetime.now()
        quote_channel_messaging_message = await quote_channel.send(embed=embed)

        d = f'{interaction.user.mention}'

        # MAIN SERVER MESSAGE
        embed = discord.Embed(title="Ticket Information",
                            description=f"""
**Budget**
${budget}

**Description**
{self.description.value}

**Deadline**
<t:{timestamp}:F>

**Seeking For**
{main_server_freelancer_role.mention}

**Client**
{interaction.user}
""", color=discord.Color.from_str(embed_color))
        embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url)
        embed.timestamp = DT.datetime.now()

        e = await ticket_channel.send(content=d, embed=embed)
        try:
            f = asyncio.create_task(self.bot.wait_for("message", check=lambda message: message.type is discord.MessageType.pins_add and message.reference.message_id == e.id, timeout=5))
            await e.pin()
            found_message = await f
            await found_message.delete()
        except:
            pass

        embed = discord.Embed(title=freelancer_messaging_title, description=freelancer_messaging_description, color=discord.Color.from_str(embed_color))
        embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url)
        embed.timestamp = DT.datetime.now()
        ticket_channel_messaging_message = await ticket_channel.send(embed=embed)
        str = ""
        cursor = await db.execute('SELECT * FROM busy')
        z = await cursor.fetchall()
        for zz in z:
            try:
                busy_freelancer = interaction.guild.get_member(zz[0])
                if main_server_freelancer_role in busy_freelancer.roles:
                    str = str + f"\n`{busy_freelancer.name}` `Busy`"
            except:
                continue
        embed = discord.Embed(title=freelancer_busy_title, description=str, color=discord.Color.from_str(embed_color))
        embed.set_footer(text=freelancer_busy_footer)
        ticket_channel_busy_message = await ticket_channel.send(embed=embed)

        embed = discord.Embed()

        await db.execute('INSERT INTO commissions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);', (interaction.user.id, budget, self.deadline.value, self.description.value, self.category, self.value, ticket_channel.id, quote_channel.id, ticket_channel_messaging_message.id, ticket_channel_busy_message.id, quote_channel_messaging_message.id, 'NULL', 0))

        desc = success_new_order_creating_description.replace("%CHANNEL%", f"{ticket_channel.mention}")
        embed = discord.Embed(title=success_new_order_creating_title, description=desc, color=discord.Color.from_str(embed_color))
        await interaction.edit_original_response(embed=embed)

        await db.commit()
        await db.close()
    
    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        raise error