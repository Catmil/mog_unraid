from DevTools import DBTools, Dev
from discord.ext import commands
from FFXIV.DutyManager import DutyLister


class DutyManager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None
        Dev.log('[DutyManager] Module initialized.')

    @commands.command(name='duties')
    async def list_duties(self, ctx: commands.Context):
        Dev.log(f'[DutyManager] Command "duties" invoked by {ctx.author} ({ctx.author.id}) on "{ctx.guild.name}" ({ctx.guild.id})')
        Dev.log(f'[DutyManager] Printing supported duties')
        locale = DBTools.get_server_locale(ctx.guild.id)
        await DutyLister.list_duty_list(self.bot, ctx, locale)
        await ctx.message.delete()
