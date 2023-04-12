import discord
import yaml

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

main_guild_id = data["General"]["MAIN_GUILD_ID"]
freelancer_guild_id = data["General"]["FREELANCER_GUILD_ID"]
staff_guild_id = data["General"]["STAFF_GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
support_ticket_category_id = data["Support_Tickets"]["SUPPORT_TICKET_CATEGORY_ID"]
support_ticket_added_roles = data["Support_Tickets"]["SUPPORT_TICKET_ADDED_ROLES"]

async def CannotSendFreelancerMessage(bot, freelancer, embed_title, embed_description, reason):
    main_guild = bot.get_guild(main_guild_id)
    category_channel = main_guild.get_channel(support_ticket_category_id)
    ticket_channel = await category_channel.create_text_channel(f"support-{freelancer.name}")
    await ticket_channel.set_permissions(main_guild.get_role(main_guild.id),
        send_messages=False,
        read_messages=False)

    mentions = f"{freelancer.mention}"
    for role_id in support_ticket_added_roles:

        role = main_guild.get_role(role_id)
        mentions = mentions + f" |{role.mention}"

        await ticket_channel.set_permissions(role,
            send_messages=True,
            read_messages=True,
            add_reactions=True,
            embed_links=True,
            read_message_history=True,
            external_emojis=True)

    await ticket_channel.set_permissions(freelancer,
        send_messages=True,
        read_messages=True,
        add_reactions=True,
        embed_links=True,
        attach_files=True,
        read_message_history=True,
        external_emojis=True)

    embed = discord.Embed(title="Freelancer Error", description=f"I was unable to send you a PM. You must allow PMs, failure to do so will result in removal of the team. \n\nYou have 48 hours to enable them.", color=discord.Color.from_str(embed_color))
    embed2 = discord.Embed(title=embed_title, description=embed_description, color=discord.Color.from_str(embed_color))
    embed2.set_footer(text=f"Reason for PM Check: {reason}")

    await ticket_channel.send(content=mentions, embeds=[embed, embed2])