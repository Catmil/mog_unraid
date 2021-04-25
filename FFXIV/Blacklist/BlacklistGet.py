from discord.ext import commands
from FFXIV.CharacterTools import Character
from DevTools import Dev
from DevTools import DBTools
import discord


async def get_entries(ctx: commands.Context, character: Character):
    Dev.log(f'[Blacklist] Checking database for info on character ID {character.id}')
    conn, db = DBTools.db_connect(ctx.guild.id)

    # Check blacklist entries
    db.execute('SELECT * FROM bl_entries WHERE char_id = ?', (int(character.id),))
    result = db.fetchall()

    if result is not None:
        char_entries = result

        # Check if name is still up to date
        db.execute('SELECT * FROM bl_characters WHERE id = ?', (int(character.id),))
        result = db.fetchone()
        if result is not None:
            if character.name != result[1] or character.world != result[2]:
                Dev.log(f'[Blacklist] Lodestone and internal data mismatch, updating character data for {character.id}')
                update_character(ctx, character)

        # Return the entries
        conn.close()
        return char_entries
    else:
        conn.close()
        return None


async def get_entries_embed(ctx: commands.Context, character: Character):
    entries = await get_entries(ctx, character)
    if entries:
        embed = discord.Embed(color=0xff00f7)
        embed.set_author(name=f'Blacklist entries - {character.name} @ {character.world}', icon_url='https://cdn.discordapp.com/avatars/676198178621751296/8ad31d8ba300204b4b7940a725ad1bf6.png?size=128')

        # Populate the embed
        id_string = ''
        duty_string = ''
        reason_string = ''
        author_string = ''
        for entry in entries:
            duty = await get_duty_name(entry[2])
            duty_string = duty_string + duty[4] + ' ' + duty[2] + '  -  *' + entry[3] + f'* ~ <@{entry[5]}>\n'

        embed.add_field(name='Blacklist', value=duty_string, inline=True)

        embed.set_footer(text='Powered by XIVAPI & much Moogle Love ❤')

        return embed
    else:
        return None


def update_character(ctx: commands.Context, character: Character):
    conn, db = DBTools.db_connect(ctx.guild.id)
    db.execute('UPDATE bl_characters SET name = ?, world = ? WHERE id = ?', (character.name, character.world, character.id))
    Dev.log(f'[Blacklist] Character {character.id} ({character.name} @ {character.world}) is now updated.')
    conn.commit()
    conn.close()


async def get_duty_name(duty: str):
    conn, db = DBTools.db_connect('duties')
    db.execute('SELECT name FROM sqlite_master WHERE type = ? ORDER BY name', ('table',))
    tables = db.fetchall()

    if tables is not None:
        for table in tables:
            db.execute(f'SELECT * FROM {(table[0])} WHERE shortcut = ? ORDER BY prio', (duty,))
            result = db.fetchone()
            if result is not None:
                conn.close()
                return result

        conn.close()
        return None
    else:
        raise Exception
