import os
import discord
from discord.ext import commands
import pyxivapi as xivapi
from dotenv import load_dotenv
from FFXIV.CharacterTools.Character import Character


# Import XIVAPI Key from .env
load_dotenv()
api_key = os.getenv('XIVAPI')


async def search_character(forename: str, surname: str, world: str) -> dict:
    """
    Returns a dictionary containing the results of the lodestone character search.
    Ideally, the length of dict['Results'] should be 1.

    :param forename: String representing the character's forename
    :param surname: String representing the character's surname
    :param world: String representing the character's home world
    :return: Dictionary containing the search results
    """
    xiv_client = xivapi.XIVAPIClient(api_key=api_key)
    results = await xiv_client.character_search(forename=forename, surname=surname, world=world)
    return results['Results']


async def request_character(char_id: int, locale: str, data: str) -> Character:
    """
    Returns a Character object containing detailed information about a character on the Lodestone.\n
    Additional information for the 'data' parameter:\n
    The options are separated by a comma and following options are available:\n
    'AC' for Achievements,\n
    'MIMO' for Minions & Mounts,\n
    'CJ' for Class/Jobs data,\n
    'FR' for the Friends List,\n
    'FC' for the Free Company,\n
    'FCM' for the Free Company Members,\n
    'PVP' for info on the PVP Team.

    :param char_id: The Lodestone ID of the character to be fetched. Can be obtained by calling search_character() first
    :param locale: The locale of the server.
    :param data: String containing data options to be fetched. For example 'CJ,FC'
    :return: Character object containing the most important information fetched from the lodestone
    """
    # Set the language for the query
    if locale == 'fr_FR':
        language = 'fr'
    elif locale == 'jp_JP':
        language = 'jp'
    elif locale == 'de_DE':
        language = 'de'
    else:
        language = 'en'

    # Run the query
    xiv_client = xivapi.XIVAPIClient(api_key=api_key)
    char_data = await xiv_client.character_by_id(lodestone_id=char_id, extended=True, include_freecompany=True)
    return Character(char_data)
