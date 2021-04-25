import requests
import discord
import os
from dotenv import load_dotenv
import FFXIV.Worlds
import FFXIV.ClassJobs
from FFXIV.CharacterTools.Character import Character


# Import XIVAPI Key from .env
load_dotenv()
api_key = os.getenv('FFLOGS')


def fetch_logs(forename: str, surname: str, world: str, timeframe: str):
    """
    Returns raw JSON response with all encounter parses in the zone that has yet to be properly edited.

    :param forename: String containing the character's forename
    :param surname: String containing the character's surname
    :param world: String containing the character's home world
    :param timeframe: 'today' shows the percentiles as of today's rankings. 'historical' shows the percentiles as of the log's date
    :return: JSON String containing all parses
    """
    # To fulfill the requirement for the FFLogs API, we need to provide the server region
    if world in FFXIV.Worlds.chaos or world in FFXIV.Worlds.light:
        server_region = 'EU'
    elif world in FFXIV.Worlds.aether or world in FFXIV.Worlds.primal or world in FFXIV.Worlds.crystal:
        server_region = 'NA'
    elif world in FFXIV.Worlds.elemental or world in FFXIV.Worlds.gaia or world in FFXIV.Worlds.mana:
        server_region = 'JP'
    else:
        return None

    char_name = forename + ' ' + surname
    char_server = world

    # Build the API Request URL and get the data
    # https://www.fflogs.com:443/v1/rankings/character/Nekomi%20Niijou/Moogle/EU?metric=rdps&timeframe=historical&api_key=0e3c5487ee7e5f071de77137b9f2c1d7
    # https://www.fflogs.com/v1/zones?api_key=0e3c5487ee7e5f071de77137b9f2c1d7
    url = f'https://fflogs.com/v1/rankings/character/{char_name}/{char_server}/{server_region}?timeframe={timeframe}&metric=rdps&api_key={api_key}'
    response = requests.get(url)
    encounters = response.json()

    return response, encounters


def get_best_logs(forename: str, surname: str, world: str, timeframe: str, embed: discord.Embed):
    response, parses = fetch_logs(forename, surname, world, timeframe)
    if response:
        encounters = []
        jobs = []
        character_name = f'{parses[0]["characterName"]} @ {parses[0]["server"]}'

        for parse in parses:
            # Make a list of all encounters
            if parse['encounterName'] not in encounters and parse['difficulty'] == 101:
                encounters.append(parse['encounterName'])

            # Look with which classes the player ranked
            if parse['spec'] not in jobs:
                jobs.append(parse['spec'])

        # Populate the embed
        for encounter in encounters:
            value = ''
            for job in jobs:
                for parse in parses:
                    if parse['encounterName'] == encounter and parse['spec'] == job and parse['difficulty'] == 101:
                        value += f'{FFXIV.ClassJobs.FULL_JOB[parse["spec"]]} **{int(round(parse["percentile"], 0))}%** *({round(parse["total"], 2)} rDPS)*\n'
            embed.add_field(name=f'<:hed:683101445293080590> {encounter}', value=value, inline=False)

        return embed, character_name
    else:
        return None
