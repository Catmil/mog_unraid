from FFXIV.CharacterTools.Strings import Strings
from DevTools import DBTools, Dev
from discord.ext import commands
from FFXIV.CharacterTools import LodestoneSearch
from FFXIV.CharacterTools import CharInfoDisplay
from FFXIV.CharacterTools import FFLogs
from FFXIV.Blacklist import BlacklistGet
import discord


class CharacterTools(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None
        Dev.log('[CharacterTools] Module initialized.')

    @commands.command(name='character')
    async def character_info(self, ctx: commands.Context, forename: str, surname: str, world: str):
        Dev.log(
            f'[CharacterTools] Command "character" invoked by {ctx.author} ({ctx.author.id}) on "{ctx.guild.name}" ({ctx.guild.id})')
        locale = DBTools.get_server_locale(ctx.guild.id)
        lang = Strings(locale)

        with ctx.typing():
            try:
                # Search for the character and request detailed data if found
                attempt = 1
                while attempt <= 3:
                    Dev.log(
                        f'[CharacterTools] Searching the lodestone for "{forename} {surname} @ {world}" (Attempt: {str(attempt)})')
                    search_results = await LodestoneSearch.search_character(forename, surname, world)
                    attempt = attempt + 1
                    if not len(search_results) == 1:
                        if attempt > 3:
                            Dev.log(f'[CharacterTools] Character "{forename} {surname} @ {world}" not found.')
                            await ctx.send(lang.CHAR_NOT_FOUND)
                        else:
                            Dev.log(
                                f'[CharacterTools] Character "{forename} {surname} @ {world}" not found. Retrying...')
                    else:
                        attempt = 99
                else:
                    Dev.log(f'[CharacterTools] Requesting detailed info for character ID {search_results[0]["ID"]}')
                    character = await LodestoneSearch.request_character(int(search_results[0]["ID"]), locale, 'CJ,FC')

                    Dev.log(f'[CharacterTools] Responding to request from {ctx.author} ({ctx.author.id}) on "{ctx.guild.name}" ({ctx.guild.id})')
                    await ctx.send(embed=CharInfoDisplay.get_charinfo_embed(character, lang))
            except Exception:
                Dev.error(f'[ERROR] Module (CharacterTools) raised following exception:')
                Dev.error(f'[ERROR] {Dev.print_exception()}')

    @commands.command(name='logs')
    async def character_logs(self, ctx: commands.Context, forename: str, surname: str, world: str):
        Dev.log(
            f'[CharacterTools] Command "logs" invoked by {ctx.author} ({ctx.author.id}) on "{ctx.guild.name}" ({ctx.guild.id})')
        lang = Strings(DBTools.get_server_locale(ctx.guild.id))
        try:
            Dev.log(f'[CharacterTools] Querying FFLogs for data of {forename} {surname} @ {world}')
            embed = discord.Embed(color=0xffff00)
            result = FFLogs.get_best_logs(forename, surname, world, 'historical', embed)

            Dev.log(f'[CharacterTools] Responding to request from {ctx.author} ({ctx.author.id}) on "{ctx.guild.name}" ({ctx.guild.id})')
            if embed:
                embed.set_author(name=lang.FFLOGS_EMBED_TITLE.format(name=result[1]), icon_url='https://cdn.discordapp.com/avatars/676198178621751296/8ad31d8ba300204b4b7940a725ad1bf6.png?size=128')
                embed.set_footer(text=lang.CHAR_EMBED_CREDITS)
                await ctx.send(embed=result[0])
            else:
                await ctx.send(lang.FFLOGS_NO_DATA.format(name=f'{forename} {surname} @ {world}'))
        except Exception:
            Dev.error(f'[ERROR] Module (CharacterTools) raised following exception:')
            Dev.error(f'[ERROR] {Dev.print_exception()}')

    @commands.command(name='check')
    async def check_character(self, ctx: commands.Context, forename: str, surname: str, world: str):
        locale = DBTools.get_server_locale(ctx.guild.id)
        lang = Strings(locale)
        with ctx.typing():
            attempt = 1
            Dev.log(f'[CharacterTools] Command "check" invoked by {ctx.author} ({ctx.author.id}) on "{ctx.guild.name}" ({ctx.guild.id})')
            try:
                while attempt <= 3:
                    Dev.log(
                        f'[CharacterTools] Searching the lodestone for "{forename} {surname} @ {world}" (Attempt: {str(attempt)})')
                    search_results = await LodestoneSearch.search_character(forename, surname, world)
                    attempt = attempt + 1
                    if not len(search_results) == 1:
                        if attempt > 3:
                            Dev.log(f'[CharacterTools] Character "{forename} {surname} @ {world}" not found.')
                            await ctx.send(lang.CHAR_NOT_FOUND)
                        else:
                            Dev.log(f'[CharacterTools] Character "{forename} {surname} @ {world}" not found. Retrying...')
                    else:
                        attempt = 99
                else:
                    Dev.log(f'[CharacterTools] Requesting detailed info for character ID {search_results[0]["ID"]}')
                    character = await LodestoneSearch.request_character(int(search_results[0]["ID"]), locale, 'CJ,FC')

                    # Let's send all we have
                    Dev.log(
                        f'[CharacterTools] Responding character data to request from {ctx.author} ({ctx.author.id}) on "{ctx.guild.name}" ({ctx.guild.id})')
                    await ctx.send(embed=CharInfoDisplay.get_charinfo_embed(character, lang))
                    await ctx.message.delete()

                    # Let's get the logs
                    await self.character_logs(ctx, forename, surname, world)

                    # Let's get the blacklist
                    bl_entries = await BlacklistGet.get_entries_embed(ctx, character)
                    if bl_entries is not None:
                        Dev.log(
                            f'[CharacterTools] Responding character data to request from {ctx.author} ({ctx.author.id}) on "{ctx.guild.name}" ({ctx.guild.id})')
                        await ctx.send(embed=bl_entries)
                        await ctx.message.delete()
            except Exception:
                Dev.error(f'[ERROR] Module (CharacterTools) raised following exception:')
                Dev.error(f'[ERROR] {Dev.print_exception()}')
