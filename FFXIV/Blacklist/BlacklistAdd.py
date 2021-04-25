from discord.ext import commands
from FFXIV.CharacterTools import Character
from DevTools import DBTools


async def add_entry(ctx: commands.Context, character: Character, duty: str, reason: str):
    conn, db = DBTools.db_connect(str(ctx.guild.id))

    # Check if we already have that character on file
    db.execute('SELECT * FROM bl_characters WHERE id = ?', (character.id,))
    result = db.fetchone()
    if result is None:
        # Add the character
        db.execute('INSERT INTO bl_characters (id, name, world) VALUES (?,?,?)', (character.id, character.name, character.world))
        conn.commit()

    # Add the entry
    db.execute('INSERT INTO bl_entries (char_id, duty, reason, author, author_id) VALUES (?,?,?,?,?)', (character.id, duty, reason, ctx.author.name, ctx.author.id))
    conn.commit()

    # Close the connection
    conn.close()
