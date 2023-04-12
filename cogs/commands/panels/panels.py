import discord
import yaml
from discord import app_commands
from discord.ext import commands
from cogs.buttons.tickets.system import CreateTicket
from cogs.buttons.freelancer.freelancer import FreelancerSystem
from cogs.buttons.client.client import ClientSystem, PaySystem

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

main_guild_id = data["General"]["MAIN_GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
report_command = data["Commands"]["REPORT_COMMAND"]
name = data["General"]["NAME"]

class PanelCog(commands.GroupCog, name="panel"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
        self.bot.add_view(CreateTicket(bot))
        self.bot.add_view(FreelancerSystem(bot))
        self.bot.add_view(ClientSystem(bot))
        self.bot.add_view(PaySystem(bot))

    @app_commands.command(name="ticket", description="Sends the ticket panel!")
    @app_commands.default_permissions(administrator=True)
    async def ticket(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)
        view = CreateTicket(self.bot)
        output_string = ""
        for category, roles in data['Roles'].items():
            output_string += f"**{category}** Department\n"
            for role in roles:
                for x, y in role.items():
                    output_string += f"— <@&{y}>\n"
        embed1 = discord.Embed(title=f"What we offer at {name}", description=output_string, color=discord.Color.from_str(embed_color))
        embed2 = discord.Embed(title=f"{name} Ticket Creation", description=f"Please select the relevant button to open a ticket. \n\nIf you wish to report someone then use the {report_command} command.", color=discord.Color.from_str(embed_color))
        await interaction.channel.send(embeds=[embed1, embed2], view=view)
        embed = discord.Embed(description="Sent the ticket panel!", color=discord.Color.from_str(embed_color))
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PanelCog(bot), guilds=[discord.Object(id=main_guild_id)])