import sys
import linecache
import datetime
import discord
from DevTools.Colors import *
from discord.ext import commands


def time():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')


def log(text: str):
    print(f'[{time()}]' + text)


def error(text: str):
    print(f'{Colors.FAIL}[{time()}]' + text + Colors.ENDC)


def warning(text: str):
    print(f'{Colors.WARNING}[{time()}]' + text + Colors.ENDC)


def print_exception():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)

    return f'File: {filename}, Line {lineno} "{line.strip()}" [{exc_type}: {exc_obj}]'


async def channel_purge(ctx: commands.Context, amount):
    async with ctx.typing():
        counter = 0
        if amount == 'all':
            limit = None
        else:
            limit = int(amount)

        async for message in ctx.history(limit=limit):
            counter = counter + 1
            await message.delete()
        sent = await ctx.send(f'Cleared **{counter}** messages.')
        await sent.add_reaction('✅')
