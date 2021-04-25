from FFXIV.CharacterTools.Strings import Strings
from DevTools import DBTools, Dev
from discord.ext import commands
import FFXIV.DutyManager.Duties
import FFXIV.Worlds
from FFXIV.Blacklist import BlacklistAdd
from FFXIV.CharacterTools import LodestoneSearch
from FFXIV.CharacterTools import Character
import discord


class Blacklist(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None
        Dev.log('[Blacklist] Module initialized.')

    @commands.command(name='bl')
    async def blacklist_add(self, ctx: commands.Context, forename: str, surname: str, world: str, duty: str, *args):
        with ctx.typing():
            Dev.log(f'[Blacklist] Command "bl" invoked by {ctx.author} ({ctx.author.id}) on "{ctx.guild.name}" ({ctx.guild.id})')
            Dev.log(f'[Blacklist] Searching for entered character')

            # Search for the character and request detailed data if found
            attempt = 1
            while attempt <= 3:
                Dev.log(
                    f'[Blacklist] Searching the lodestone for "{forename} {surname} @ {world}" (Attempt: {str(attempt)})')
                search_results = await LodestoneSearch.search_character(forename, surname, world)
                attempt = attempt + 1
                if not len(search_results) == 1:
                    if attempt > 3:
                        Dev.warning(f'[Blacklist] Character "{forename} {surname} @ {world}" not found.')
                        await ctx.send('Character not found.')
                        await ctx.message.delete()
                        return
                    else:
                        Dev.log(
                            f'[Blacklist] Character "{forename} {surname} @ {world}" not found. Retrying...')
                else:
                    attempt = 99
                    Dev.log(f'[Blacklist] Requesting detailed info for character ID {search_results[0]["ID"]}')
                    character: Character = await LodestoneSearch.request_character(int(search_results[0]["ID"]), 'en_US', 'CJ')

            if duty in FFXIV.DutyManager.Duties.duty_list and world in FFXIV.Worlds.worlds:
                reason = ''
                for string in args:
                    reason = reason + string + ' '
                reason = reason[:-1]

                await BlacklistAdd.add_entry(ctx, character, duty, reason)
                await ctx.send(f'**{character.name} @ {character.world}** added to the blacklist.')
                await ctx.message.delete()
            else:
                Dev.warning(f'[Blacklist] Wrong user input! Either duty or world unknown')
                await ctx.send('Check your input - The world or duty you entered is invalid.')
                await ctx.message.delete()

