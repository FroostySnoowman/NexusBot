import discord
import yaml
from discord import app_commands
from discord.ext import commands
from cogs.buttons.freelancer.dashboard import DashboardSystem1, WalletSystem1, ProfileSystem1

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

with open('configmsg.yml', 'r') as file:
    msgdata = yaml.safe_load(file)

main_guild_id = data["General"]["MAIN_GUILD_ID"]
freelancer_guild_id = data["General"]["FREELANCER_GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
name = data["General"]["NAME"]
main_server_freelancer_role_id = data["Role"]["MAIN_SERVER_FREELANCER_ROLE_ID"]
not_freelancer_dashboard = msgdata["Freelancer"]["NOT_FREELANCER_DASHBOARD"]

class FreelancerCog(commands.GroupCog, name="freelancer"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
        self.bot.add_view(DashboardSystem1(bot))
        self.bot.add_view(WalletSystem1(bot))
        self.bot.add_view(ProfileSystem1(bot))

    @app_commands.command(name="dashboard", description="Manage your freelancer dashboard!")
    async def dashboard(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)
        main_guild = self.bot.get_guild(main_guild_id)
        member = main_guild.get_member(interaction.user.id)
        freelancer_role = main_guild.get_role(main_server_freelancer_role_id)
        if freelancer_role in member.roles:
            embed = discord.Embed(color=discord.Color.from_str(embed_color))
            embed.add_field(name="Wallet", value=f"View and manage your {name} wallet!", inline=False)
            embed.add_field(name="Profile", value=f"View and manage your {name} freelancer profile!", inline=False)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        else:
            embed = discord.Embed(description=not_freelancer_dashboard, color=discord.Color.red())
        await interaction.followup.send(embed=embed, view=DashboardSystem1(self.bot))

async def setup(bot):
    await bot.add_cog(FreelancerCog(bot), guilds=[discord.Object(id=freelancer_guild_id)])