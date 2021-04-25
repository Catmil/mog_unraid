import os
import discord
from DevTools import DBTools, Dev
from dotenv import load_dotenv
from discord.ext import commands

# Module imports
from FFXIV.CharacterTools.Core import CharacterTools
from FFXIV.DutyManager.Core import DutyManager
from FFXIV.Blacklist.Core import Blacklist

# Import user token from .env
load_dotenv()
user_token = os.getenv('DISCORD_TOKEN')

# Setup bot variables
bot = commands.Bot(command_prefix=';')
first_connection = True


# on_ready runs when the bot has (re)connected.
@bot.event
async def on_ready():
    global first_connection
    if first_connection:
        first_connection = False

        for guild in bot.guilds:
            Dev.log(f'[SYSTEM] {bot.user.name} has succesfully connected to {guild.name} (ID: {guild.id} / {len(guild.members)} members)')

            # Check if we need to setup a database for this server
            if not DBTools.is_server_setup(guild.id):
                Dev.log(f'[SETUP] Setting up server {guild.name} (ID: {guild.id})')
                setup_success = DBTools.setup_server(guild.id)
                if setup_success:
                    Dev.log(f'[SETUP] Server {guild.name} (ID: {guild.id}) is ready to go.')
                else:
                    Dev.log(f'[ERROR] Failed setting up server {guild.name} (ID: {guild.id})! Attention needed!')

    else:
        Dev.log(f'[SYSTEM] {bot.user.name} has succesfully reconnected to all servers')

    await bot.change_presence(activity=discord.Game('with my pom pom'))


# For ze lols
@bot.event
async def on_message(message: discord.Message):
    try:
        if message.author.id != bot.user.id:
            pass
    except Exception:
        pass

    ctx: commands.Context = await bot.get_context(message)
    if message.content == 'good bot' or message.content == 'Good Bot' or message.content == 'Good bot':
        await message.add_reaction('❤')
        await ctx.send('aww thank you UwU')
        await ctx.send('<:UwU:785201374911660112>')

    await bot.invoke(ctx)


# Obligatory hello world
@bot.command(name='hello')
async def hello_world(ctx: commands.Context):
    response = await ctx.send(f'oi blyat, {ctx.message.author.name}!')
    await response.add_reaction('😊')


# Clear
@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def channel_purge(ctx: commands.Context, amount):
    try:
        Dev.warning(f'[SYSTEM] Command "clear" triggered by user {ctx.author} (ID: {ctx.author.id}) on server \'{ctx.guild.name}\' (ID: {ctx.guild.id})')
    except Exception:
        pass
    await Dev.channel_purge(ctx, amount)


# Initialize modules
bot.add_cog(CharacterTools(bot))
bot.add_cog(DutyManager(bot))
bot.add_cog(Blacklist(bot))

# Connect the bot
bot.run(user_token)
