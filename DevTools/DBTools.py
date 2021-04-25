import sqlite3
import os
from DevTools import Dev

# Get this script's location to allow for relative paths
this_location = os.path.dirname(__file__)


def db_connect(database: str) -> tuple:
    """
    Opens a database connection. The connection must be closed by the handling function.

    :param database: String containing only the database's filename, not the path.
    :return: Tuple containing sqlite3.Connection object and sqlite3.Cursor object.
    :raises sqlite3.Error: See traceback for details
    """
    conn = None
    try:
        conn = sqlite3.connect(os.path.join(this_location, f'../databases/{database}.db'))
        db = conn.cursor()
        return conn, db
    except sqlite3.Error as e:
        Dev.error(f'[ERROR] SQLite3 returned following error: {e}')


def is_server_setup(server_id: int) -> bool:
    """
    Checks if we have a database set up for the server identifiable by the server ID passed to this function.
    If this function returns False, you should call DBTools.setup_server next.

    :param server_id: The server ID obtainable by calling discord.Guild.id
    :return: Boolean indicating if the server has been already set up to use with the bot
    :raises sqlite3.Error: See traceback for details
    """
    conn, db = db_connect(str(server_id))
    try:
        # Check if the table 'server_settings' exists. If not, this database was just created and the server needs to be set up
        db.execute('SELECT count(name) FROM sqlite_master WHERE type=\'table\' AND name=\'server_settings\'')
        if db.fetchone()[0] == 1:
            return True
        else:
            return False

    except sqlite3.Error as e:
        Dev.error(f'[ERROR] SQLite3 raised following error: {e}')
    finally:

        if conn is not None:
            conn.close()


def setup_server(server_id: int) -> bool:
    """
    Sets up the database to be usable with the server identifiable by the server ID passed to this function.
    Creates pre-planned tables (refer to databases/template.db) and populates the server_settings table with default
    values.

    :param server_id: The server ID obtainable by calling discord.Guild.id
    :return: Boolean indicating whether the setup was succesful or not
    """
    conn, db = db_connect(str(server_id))
    try:
        db.execute(f'''CREATE TABLE server_settings (
                        language INT      NOT NULL      DEFAULT (0),
                        prefix   CHAR (1) NOT NULL      DEFAULT (';')
                   )''')
        db.execute(f'''CREATE TABLE characters (
                        id           INTEGER PRIMARY KEY ASC AUTOINCREMENT NOT NULL UNIQUE,
                        name         STRING  NOT NULL,
                        world        STRING  NOT NULL,
                        lodestone_id BIGINT  UNIQUE NOT NULL,
                        owner        INT     UNIQUE NOT NULL REFERENCES users (id) 
                   )''')
        db.execute(f'PRAGMA foreign_keys = 0')
        db.execute(f'''CREATE TABLE users (
                        id          INTEGER PRIMARY KEY ASC AUTOINCREMENT UNIQUE NOT NULL,
                        discord_id  BIGINT  UNIQUE NOT NULL,
                        character_1 INTEGER UNIQUE REFERENCES users (id),
                        msg_count   INTEGER NOT NULL DEFAULT (0) 
                   )''')
        db.execute(f'PRAGMA foreign_keys = 1')
        db.execute(f'INSERT INTO server_settings DEFAULT VALUES')
        db.execute(f'''CREATE TABLE bl_characters (
                        id          INTEGER PRIMARY KEY NOT NULL UNIQUE,
                        name        STRING  NOT NULL,
                        world       STRING  NOT NULL
                    )''')
        db.execute(f'''CREATE TABLE bl_entries (
                        id          INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                        char_id     INTEGER NOT NULL REFERENCES bl_characters (id),
                        duty        STRING  NOT NULL,
                        reason      TEXT    NOT NULL,
                        author      STRING  NOT NULL,
                        author_id   BIGINT  NOT NULL
                    )''')

        # Commit the changes
        conn.commit()
        return True

    except sqlite3.Error as e:
        Dev.error(f'[ERROR] SQLite3 raised following error: {e}')
        return False

    finally:
        conn.close()


def get_server_locale(server_id: int) -> str:
    """
    Returns the locale of the server.

    :param server_id: The server ID obtainable by calling discord.Guild.id
    :return: String containing the server locale
    """
    conn, db = db_connect(str(server_id))
    try:
        # Get the locale from the server_settings table
        db.execute('SELECT language from server_settings')
        locale = db.fetchone()[0]

        if locale == 0:
            return 'en_US'
        elif locale == 1:
            return 'pl_PL'
        else:
            return 'en_US'
    except Exception as e:
        Dev.error(f'[ERROR] System (DBTools) raised following exception: {repr(e)}')
