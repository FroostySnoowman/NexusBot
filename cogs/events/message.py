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
staff_guild_id = data["General"]["STAFF_GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
failed_to_reply_title = msgdata["Global"]["FAILED_TO_REPLY_TITLE"]
failed_to_reply_description = msgdata["Global"]["FAILED_TO_REPLY_DESCRIPTION"]

class OnMessageEventCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener('on_message')
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if not message.reference:
            return
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM commissions WHERE ticket_channel_messaging_message_id=?', (message.reference.message_id, ))
        a = await cursor.fetchone()
        cursor = await db.execute('SELECT * FROM commissions WHERE quote_channel_messaging_message_id=?', (message.reference.message_id, ))
        b = await cursor.fetchone()
        cursor = await db.execute('SELECT * FROM replies WHERE message_id=?', (message.reference.message_id, ))
        c = await cursor.fetchone()
        if a is None:
            if b is None:
                if c is None:
                    pass
                else:
                    cursor = await db.execute('SELECT * FROM commissions WHERE main_server_channel_id=?', (message.channel.id, ))
                    d = await cursor.fetchone()
                    cursor = await db.execute('SELECT * FROM commissions WHERE freelancer_server_channel_id=?', (message.channel.id, ))
                    e = await cursor.fetchone()
                    if d is None:
                        if e is None:
                            embed = discord.Embed(title=failed_to_reply_title, description=failed_to_reply_description, color=discord.Color.red())
                            message.channel.send(embed=embed)
                        else:
                            channel = self.bot.get_channel(e[6])
                            ogmsg = channel.get_partial_message(c[4])
                            if message.content:
                                if message.attachments:
                                    embed = discord.Embed(description=f"Reply to **{c[5]}**: \n\n{message.content}", color=discord.Color.from_str(embed_color))
                                    embed.set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
                                    embed.set_footer(text="To reply to this message, use Discord's built-in reply system!", icon_url=channel.guild.icon.url)
                                    attachments = discord.Embed(title="Attachments", color=discord.Color.from_str(embed_color))
                                    counter = 1
                                    for attachment in message.attachments:
                                        attachments.add_field(name=f"Attachment #{counter}", value=attachment.url)
                                        counter += 1
                                    try:
                                        msg = await ogmsg.reply(embeds=[embed, attachments])
                                    except:
                                        msg = await channel.send(content=f"<@{c[2]}>", embeds=[embed, attachments])
                                else:
                                    embed = discord.Embed(description=f"Reply to **{c[5]}**: \n\n{message.content}", color=discord.Color.from_str(embed_color))
                                    embed.set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
                                    embed.set_footer(text="To reply to this message, use Discord's built-in reply system!", icon_url=channel.guild.icon.url)
                                    try:
                                        msg = await ogmsg.reply(embed=embed)
                                    except:
                                        msg = await channel.send(content=f"<@{c[2]}>", embed=embed)
                            else:
                                if message.attachments:
                                    message.content = "IMAGES ONLY"
                                    attachments = discord.Embed(title="Attachments", description=f"Image reply to **{c[5]}**:", color=discord.Color.from_str(embed_color))
                                    counter = 1
                                    for attachment in message.attachments:
                                        attachments.add_field(name=f"Attachment #{counter}", value=attachment.url)
                                        counter += 1
                                    try:
                                        msg = await ogmsg.reply(embed=attachments)
                                    except:
                                        msg = await channel.send(content=f"<@{c[2]}>", embed=attachments)
                            await db.execute('INSERT INTO replies VALUES (?,?,?,?,?,?);', (e[6], e[7], message.author.id, msg.id, message.content, message.id))
                            await message.add_reaction('✅')
                    else:
                        channel = self.bot.get_channel(d[7])
                        ogmsg = channel.get_partial_message(c[4])
                        if message.content:
                            if message.attachments:
                                embed = discord.Embed(description=f"Reply to **{c[5]}**: \n\n{message.content}", color=discord.Color.from_str(embed_color))
                                embed.set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
                                embed.set_footer(text="To reply to this message, use Discord's built-in reply system!", icon_url=message.guild.icon.url)
                                attachments = discord.Embed(title="Attachments", color=discord.Color.from_str(embed_color))
                                counter = 1
                                for attachment in message.attachments:
                                    attachments.add_field(name=f"Attachment #{counter}", value=attachment.url)
                                    counter += 1
                                try:
                                    msg = await ogmsg.reply(embeds=[embed, attachments])
                                except:
                                    msg = await channel.send(content=f"<@{c[2]}>", embeds=[embed, attachments])
                            else:
                                embed = discord.Embed(description=f"Reply to **{c[5]}**: \n\n{message.content}", color=discord.Color.from_str(embed_color))
                                embed.set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
                                embed.set_footer(text="To reply to this message, use Discord's built-in reply system!", icon_url=message.guild.icon.url)
                                try:
                                    msg = await ogmsg.reply(embed=embed)
                                except:
                                    msg = await channel.send(content=f"<@{c[2]}>", embed=embed)
                        else:
                            if message.attachments:
                                attachments = discord.Embed(title="Attachments", description=f"Image reply to **{c[5]}**:", color=discord.Color.from_str(embed_color))
                                counter = 1
                                for attachment in message.attachments:
                                    attachments.add_field(name=f"Attachment #{counter}", value=attachment.url)
                                    counter += 1
                                try:
                                    msg = await ogmsg.reply(embed=attachments)
                                except:
                                    msg = await channel.send(content=f"<@{c[2]}>", embed=attachments)
                        await db.execute('INSERT INTO replies VALUES (?,?,?,?,?,?);', (d[6], d[7], message.author.id, msg.id, message.id, message.content))
                        await message.add_reaction('✅')
            else:
                channel = self.bot.get_channel(b[6])
                if message.content:
                    if message.attachments:
                        embed = discord.Embed(description=message.content, color=discord.Color.from_str(embed_color))
                        embed.set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
                        embed.set_footer(text="To reply to this message, use Discord's built-in reply system!", icon_url=channel.guild.icon.url)
                        attachments = discord.Embed(title="Attachments", color=discord.Color.from_str(embed_color))
                        counter = 1
                        for attachment in message.attachments:
                            attachments.add_field(name=f"Attachment #{counter}", value=attachment.url)
                            counter += 1
                        msg = await channel.send(embeds=[embed, attachments])
                    else:
                        embed = discord.Embed(description=message.content, color=discord.Color.from_str(embed_color))
                        embed.set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
                        embed.set_footer(text="To reply to this message, use Discord's built-in reply system!", icon_url=channel.guild.icon.url)
                        msg = await channel.send(embed=embed)
                else:
                    if message.attachments:
                        message.content = "IMAGES ONLY"
                        attachments = discord.Embed(title="Attachments", color=discord.Color.from_str(embed_color))
                        counter = 1
                        for attachment in message.attachments:
                            attachments.add_field(name=f"Attachment #{counter}", value=attachment.url)
                            counter += 1
                        msg = await channel.send(embed=attachments)
                await db.execute('INSERT INTO replies VALUES (?,?,?,?,?,?);', (b[6], b[7], message.author.id, msg.id, message.id, message.content))
                await message.add_reaction('✅')
        else:
            channel = self.bot.get_channel(a[7])
            if message.content:
                if message.attachments:
                    embed = discord.Embed(description=message.content, color=discord.Color.from_str(embed_color))
                    embed.set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
                    embed.set_footer(text="To reply to this message, use Discord's built-in reply system!", icon_url=channel.guild.icon.url)
                    attachments = discord.Embed(title="Attachments", color=discord.Color.from_str(embed_color))
                    counter = 1
                    for attachment in message.attachments:
                        attachments.add_field(name=f"Attachment #{counter}", value=attachment.url)
                        counter += 1
                    msg = await channel.send(embeds=[embed, attachments])
                else:
                    embed = discord.Embed(description=message.content, color=discord.Color.from_str(embed_color))
                    embed.set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
                    embed.set_footer(text="To reply to this message, use Discord's built-in reply system!", icon_url=channel.guild.icon.url)
                    msg = await channel.send(embed=embed)
            else:
                if message.attachments:
                    message.content = "IMAGES ONLY"
                    embed = discord.Embed(description=message.content, color=discord.Color.from_str(embed_color))
                    embed.set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
                    embed.set_footer(text="To reply to this message, use Discord's built-in reply system!", icon_url=message.guild.icon.url)
                    attachments = discord.Embed(title="Attachments", color=discord.Color.from_str(embed_color))
                    counter = 1
                    for attachment in message.attachments:
                        attachments.add_field(name=f"Attachment #{counter}", value=attachment.url)
                        counter += 1
                    msg = await channel.send(embeds=[embed, attachments])
            await db.execute('INSERT INTO replies VALUES (?,?,?,?,?,?);', (a[6], a[7], message.author.id, msg.id, message.id, message.content))
            await message.add_reaction('✅')
        await db.commit()
        await db.close()

async def setup(bot):
    await bot.add_cog(OnMessageEventCog(bot))