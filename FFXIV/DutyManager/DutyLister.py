import discord
from discord.ext import commands
from DevTools import Dev
from DevTools import DBTools


async def list_duty_list(bot, ctx, locale):
    if locale == 'de_de':
        index = 3
    else:
        index = 2

    conn, db = DBTools.db_connect('duties')

    async with ctx.typing():
        sent = await ctx.send('Choose the reaction corresponding to the duty category you wish to see.')

    embed = discord.Embed(color=0x00aaff)
    embed.set_author(name='Supported duties',
                     icon_url='https://cdn.discordapp.com/avatars/676198178621751296/8ad31d8ba300204b4b7940a725ad1bf6.png?size=128')

    class ReactionListener(commands.Cog):
        def __init__(self):
            self.bot = bot
            self.db = db
            self.index = index

        @commands.Cog.listener()
        async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
            if reaction.message.id == sent.id:
                if user.id == ctx.message.author.id:
                    if str(reaction.emoji) == '<:hed:683101445293080590>':
                        # High-End Duties
                        hed_trials_l = ''
                        hed_trials_s = ''
                        hed_raids_l = ''
                        hed_raids_s = ''
                        ultimate_l = ''
                        ultimate_s = ''

                        # High-End Trials
                        self.db.execute('SELECT * FROM hedTrial ORDER BY prio ASC')
                        result = self.db.fetchall()
                        for row in result:
                            hed_trials_l = hed_trials_l + f'{row[4]} {row[self.index]}\n'
                            hed_trials_s = hed_trials_s + f'{row[1]}\n'

                        # High-End Raids
                        self.db.execute('SELECT * FROM hedRaid ORDER BY prio ASC')
                        result = self.db.fetchall()
                        for row in result:
                            hed_raids_l = hed_raids_l + f'{row[4]} {row[self.index]}\n'
                            hed_raids_s = hed_raids_s + f'{row[1]}\n'

                        # Ultimates
                        self.db.execute('SELECT * FROM Ultimate ORDER BY prio ASC')
                        result = self.db.fetchall()
                        for row in result:
                            ultimate_l = ultimate_l + f'{row[4]} {row[self.index]}\n'
                            ultimate_s = ultimate_s + f'{row[1]}\n'

                        embed.add_field(name='High-end Duties (Trials)', value=hed_trials_l, inline=True)
                        embed.add_field(name='\u200b', value='\u200b', inline=True)
                        embed.add_field(name='\u200b', value=hed_trials_s, inline=True)

                        embed.add_field(name='High-end Duties (Raids)', value=hed_raids_l, inline=True)
                        embed.add_field(name='\u200b', value='\u200b', inline=True)
                        embed.add_field(name='\u200b', value=hed_raids_s, inline=True)

                        embed.add_field(name='Ultimate Raids', value=ultimate_l, inline=True)
                        embed.add_field(name='\u200b', value='\u200b', inline=True)
                        embed.add_field(name='\u200b', value=ultimate_s, inline=True)

                        embed.set_footer(text='Powered by XIVAPI & much Moogle Love ❤')
                        await ctx.send(embed=embed)
                        bot.remove_cog('ReactionListener')

                    elif str(reaction.emoji) == '<:raid:683119786414047313>':
                        # Raids
                        raids80_l = ''
                        raids70_l = ''
                        raids60_l = ''
                        raids50_l = ''
                        ex_raids80_l = ''
                        alli80_l = ''
                        alli_old_l = ''
                        raids80_s = ''
                        raids70_s = ''
                        raids60_s = ''
                        raids50_s = ''
                        ex_raids80_s = ''
                        alli80_s = ''
                        alli_old_s = ''

                        self.db.execute('SELECT * FROM Raid80 ORDER BY prio ASC')
                        result = self.db.fetchall()
                        for row in result:
                            raids80_l = raids80_l + f'{row[4]} {row[self.index]}\n'
                            raids80_s = raids80_s + f'{row[1]}\n'

                        self.db.execute('SELECT * FROM ExRaid80 ORDER BY prio ASC')
                        result = self.db.fetchall()
                        for row in result:
                            ex_raids80_l = ex_raids80_l + f'{row[4]} {row[self.index]}\n'
                            ex_raids80_s = ex_raids80_s + f'{row[1]}\n'

                        self.db.execute('SELECT * FROM Raid70 ORDER BY prio ASC')
                        result = self.db.fetchall()
                        for row in result:
                            raids70_l = raids70_l + f'{row[4]} {row[self.index]}\n'
                            raids70_s = raids70_s + f'{row[1]}\n'

                        self.db.execute('SELECT * FROM Raid60 ORDER BY prio ASC')
                        result = self.db.fetchall()
                        for row in result:
                            raids60_l = raids60_l + f'{row[4]} {row[self.index]}\n'
                            raids60_s = raids60_s + f'{row[1]}\n'

                        self.db.execute('SELECT * FROM Raid50 ORDER BY prio ASC')
                        result = self.db.fetchall()
                        for row in result:
                            raids50_l = raids50_l + f'{row[4]} {row[self.index]}\n'
                            raids50_s = raids50_s + f'{row[1]}\n'

                        self.db.execute('SELECT * FROM Alli80 ORDER BY prio ASC')
                        result = self.db.fetchall()
                        for row in result:
                            alli80_l = alli80_l + f'{row[4]} {row[self.index]}\n'
                            alli80_s = alli80_s + f'{row[1]}\n'

                        self.db.execute('SELECT * FROM AlliOld ORDER BY prio ASC')
                        result = self.db.fetchall()
                        for row in result:
                            alli_old_l = alli_old_l + f'{row[4]} {row[self.index]}\n'
                            alli_old_s = alli_old_s + f'{row[1]}\n'

                        embed.add_field(name='Raids (Shadowbringers)', value=raids80_l, inline=True)
                        embed.add_field(name='\u200b', value='\u200b', inline=True)
                        embed.add_field(name='\u200b', value=raids80_s, inline=True)

                        embed.add_field(name='High-end Raids (Shadowbringers)', value=ex_raids80_l, inline=True)
                        embed.add_field(name='\u200b', value='\u200b', inline=True)
                        embed.add_field(name='\u200b', value=ex_raids80_s, inline=True)

                        embed.add_field(name='Raids (Stormblood)', value=raids70_l, inline=True)
                        embed.add_field(name='\u200b', value='\u200b', inline=True)
                        embed.add_field(name='\u200b', value=raids70_s, inline=True)

                        embed.add_field(name='Raids (Heavensward)', value=raids60_l, inline=True)
                        embed.add_field(name='\u200b', value='\u200b', inline=True)
                        embed.add_field(name='\u200b', value=raids60_s, inline=True)

                        embed.add_field(name='Raids (A Realm Reborn)', value=raids50_l, inline=True)
                        embed.add_field(name='\u200b', value='\u200b', inline=True)
                        embed.add_field(name='\u200b', value=raids50_s, inline=True)

                        embed.add_field(name='Alliance Raids (Shadowbringers)', value=alli80_l, inline=True)
                        embed.add_field(name='\u200b', value='\u200b', inline=True)
                        embed.add_field(name='\u200b', value=alli80_s, inline=True)

                        embed.add_field(name='Alliance Raids (previous expansions)', value=alli_old_l, inline=True)
                        embed.add_field(name='\u200b', value='\u200b', inline=True)
                        embed.add_field(name='\u200b', value=alli_old_s, inline=True)

                        embed.set_footer(text='Powered by XIVAPI & much Moogle Love ❤')
                        await ctx.send(embed=embed)
                        bot.remove_cog('ReactionListener')

                    elif str(reaction.emoji) == '<:trial:683119829976350759>':
                        # Trials
                        trials80_l = ''
                        trials70_l = ''
                        trials60_l = ''
                        trials50_l = ''
                        ex_trials80_l = ''
                        ex_trials70_l = ''
                        ex_trials60_l = ''
                        ex_trials50_l = ''
                        trials80_s = ''
                        trials70_s = ''
                        trials60_s = ''
                        trials50_s = ''
                        ex_trials80_s = ''
                        ex_trials70_s = ''
                        ex_trials60_s = ''
                        ex_trials50_s = ''

                        self.db.execute('SELECT * FROM Trial80 ORDER BY prio ASC')
                        result = self.db.fetchall()
                        for row in result:
                            trials80_l = trials80_l + f'{row[4]} {row[self.index]}\n'
                            trials80_s = trials80_s + f'{row[1]}\n'

                        self.db.execute('SELECT * FROM ExTrial80 ORDER BY prio ASC')
                        result = self.db.fetchall()
                        for row in result:
                            ex_trials80_l = ex_trials80_l + f'{row[4]} {row[self.index]}\n'
                            ex_trials80_s = ex_trials80_s + f'{row[1]}\n'

                        self.db.execute('SELECT * FROM Trial70 ORDER BY prio ASC')
                        result = self.db.fetchall()
                        for row in result:
                            trials70_l = trials70_l + f'{row[4]} {row[self.index]}\n'
                            trials70_s = trials70_s + f'{row[1]}\n'

                        self.db.execute('SELECT * FROM ExTrial70 ORDER BY prio ASC')
                        result = self.db.fetchall()
                        for row in result:
                            ex_trials70_l = ex_trials70_l + f'{row[4]} {row[self.index]}\n'
                            ex_trials70_s = ex_trials70_s + f'{row[1]}\n'

                        self.db.execute('SELECT * FROM Trial60 ORDER BY prio ASC')
                        result = self.db.fetchall()
                        for row in result:
                            trials60_l = trials60_l + f'{row[4]} {row[self.index]}\n'
                            trials60_s = trials60_s + f'{row[1]}\n'

                        self.db.execute('SELECT * FROM ExTrial60 ORDER BY prio ASC')
                        result = self.db.fetchall()
                        for row in result:
                            ex_trials60_l = ex_trials60_l + f'{row[4]} {row[self.index]}\n'
                            ex_trials60_s = ex_trials60_s + f'{row[1]}\n'

                        self.db.execute('SELECT * FROM Trial50 ORDER BY prio ASC')
                        result = self.db.fetchall()
                        for row in result:
                            trials50_l = trials50_l + f'{row[4]} {row[self.index]}\n'
                            trials50_s = trials50_s + f'{row[1]}\n'

                        self.db.execute('SELECT * FROM ExTrial50 ORDER BY prio ASC')
                        result = self.db.fetchall()
                        for row in result:
                            ex_trials50_l = ex_trials50_l + f'{row[4]} {row[self.index]}\n'
                            ex_trials50_s = ex_trials50_s + f'{row[1]}\n'

                        embed.add_field(name='Trials (Shadowbringers)', value=trials80_l, inline=True)
                        embed.add_field(name='\u200b', value='\u200b', inline=True)
                        embed.add_field(name='\u200b', value=trials80_s, inline=True)

                        embed.add_field(name='High-end Trials (Shadowbringers)', value=ex_trials80_l, inline=True)
                        embed.add_field(name='\u200b', value='\u200b', inline=True)
                        embed.add_field(name='\u200b', value=ex_trials80_s, inline=True)

                        embed.add_field(name='Trials (Stormblood)', value=trials70_l, inline=True)
                        embed.add_field(name='\u200b', value='\u200b', inline=True)
                        embed.add_field(name='\u200b', value=trials70_s, inline=True)

                        embed.add_field(name='High-end Trials (Stormblood)', value=ex_trials70_l, inline=True)
                        embed.add_field(name='\u200b', value='\u200b', inline=True)
                        embed.add_field(name='\u200b', value=ex_trials70_s, inline=True)

                        embed.add_field(name='Trials (Heavensward)', value=trials60_l, inline=True)
                        embed.add_field(name='\u200b', value='\u200b', inline=True)
                        embed.add_field(name='\u200b', value=trials60_s, inline=True)

                        embed.add_field(name='High-end Trials (Heavensward)', value=ex_trials60_l, inline=True)
                        embed.add_field(name='\u200b', value='\u200b', inline=True)
                        embed.add_field(name='\u200b', value=ex_trials60_s, inline=True)

                        embed.add_field(name='Trials (A Realm Reborn)', value=trials50_l, inline=True)
                        embed.add_field(name='\u200b', value='\u200b', inline=True)
                        embed.add_field(name='\u200b', value=trials50_s, inline=True)

                        embed.add_field(name='High-end Trials (A Realm Reborn)', value=ex_trials50_l, inline=True)
                        embed.add_field(name='\u200b', value='\u200b', inline=True)
                        embed.add_field(name='\u200b', value=ex_trials50_s, inline=True)

                        embed.set_footer(text='Powered by XIVAPI & much Moogle Love ❤')
                        await ctx.send(embed=embed)
                        bot.remove_cog('ReactionListener')

                    elif str(reaction.emoji) == '<:dungeon:683345719385653298>':
                        # Dungeons
                        dungeons_l = ''
                        dungeons_s = ''

                        self.db.execute('SELECT * FROM Dungeon ORDER BY prio ASC')
                        result = self.db.fetchall()
                        for row in result:
                            dungeons_l = dungeons_l + f'{row[4]} {row[self.index]}\n'
                            dungeons_s = dungeons_s + f'{row[1]}\n'

                        embed.add_field(name='Dungeons', value=dungeons_l, inline=True)
                        embed.add_field(name='\u200b', value='\u200b', inline=True)
                        embed.add_field(name='\u200b', value=dungeons_s, inline=True)

                        embed.set_footer(text='Powered by XIVAPI & much Moogle Love ❤')
                        await ctx.send(embed=embed)

                    elif str(reaction.emoji) == '<:roulette:684562882519629844>':
                        # Others
                        other_l = ''
                        other_s = ''

                        self.db.execute('SELECT * FROM Other ORDER BY prio ASC')
                        result = self.db.fetchall()
                        for row in result:
                            other_l = other_l + f'{row[4]} {row[self.index]}\n'
                            other_s = other_s + f'{row[1]}\n'

                        embed.add_field(name='Others', value=other_l, inline=True)
                        embed.add_field(name='\u200b', value='\u200b', inline=True)
                        embed.add_field(name='\u200b', value=other_s, inline=True)

                        embed.set_footer(text='Powered by XIVAPI & much Moogle Love ❤')
                        await ctx.send(embed=embed)
                        bot.remove_cog('ReactionListener')

                    elif str(reaction.emoji) == '<:SchwabbelKappa:765476661662842901>':
                        await ctx.send('<:SchwabbelKappa:765476661662842901>')
                        bot.remove_cog('ReactionListener')

                    conn.close()



    await sent.add_reaction('<:hed:683101445293080590>')
    await sent.add_reaction('<:raid:683119786414047313>')
    await sent.add_reaction('<:trial:683119829976350759>')
    await sent.add_reaction('<:dungeon:683345719385653298>')
    await sent.add_reaction('<:roulette:684562882519629844>')
    await sent.add_reaction('<:SchwabbelKappa:765476661662842901>')
    bot.add_cog(ReactionListener())
