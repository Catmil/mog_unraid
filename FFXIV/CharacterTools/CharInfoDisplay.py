import discord

from FFXIV import ClassJobs
from FFXIV.CharacterTools.Character import Character
import FFXIV.ClassJobs
from FFXIV.CharacterTools.Strings import Strings


bot_picture = 'https://cdn.discordapp.com/avatars/676198178621751296/8ad31d8ba300204b4b7940a725ad1bf6.png?size=128'


def get_charinfo_embed(char: Character, lang: Strings) -> discord.Embed:
    """
    Returns an embed with the formatted character data that can be sent into a text channel.

    :param char: A Character object with the data to display
    :param lang: The Strings object with the appropriate language chosen
    :return: An discord.Embed object
    """
    # Let's check if the character data is intact
    if not char.name:
        raise RuntimeError('Character data is corrupted!')

    # Let's decide on a frame color for the embed (depending on the character's active class)
    # Tanks
    if char.active_job in {1, 3, 19, 21, 32, 37}:
        job_color = 0x4e9afd
    # Healers
    elif char.active_job in {6, 24, 28, 33}:
        job_color = 0x34b242
    # DPS
    elif char.active_job in {2, 4, 5, 7, 20, 22, 23, 25, 26, 27, 29, 30, 31, 34, 35, 36, 38}:
        job_color = 0xed0c23
    else:
        job_color = 0x696a6c

    # Let's build the embed
    embed = discord.Embed(title=char.name, url=char.lodestone_url, description=char.title, color=job_color)
    embed.set_author(name=lang.CHAR_EMBED_NAME, icon_url=bot_picture)
    embed.set_thumbnail(url=char.picture_mini)
    embed.set_footer(text=lang.CHAR_EMBED_CREDITS)

    embed.add_field(name=lang.CHAR_EMBED_HOME_WORLD, value=char.world, inline=False)

    # Let's talk about the Grand Company
    if char.gc:
        embed.add_field(name=lang.CHAR_EMBED_GC, value=f'{char.gc}\n{char.gc_rank}', inline=True)
    else:
        embed.add_field(name=lang.CHAR_EMBED_GC, value=lang.CHAR_EMBED_NONE, inline=True)

    # Empty space for looks
    embed.add_field(name="\u200b", value="\u200b", inline=True)

    # Let's talk about the Free Company
    if char.fc:
        embed.add_field(name=lang.CHAR_EMBED_FC,
                        value=f'{char.fc} <<{char.fc_short}>>\n'
                              f'{char.fc_memcount} {lang.CHAR_EMBED_FC_MEMBER_COUNT} / '
                              f'{lang.CHAR_EMBED_FC_RANK} {char.fc_rank}',
                        inline=True)
    else:
        embed.add_field(name=lang.CHAR_EMBED_FC, value=lang.CHAR_EMBED_NONE, inline=True)

    # Let's talk jobs & classes
    # Tanks
    embed.add_field(name=lang.CHAR_EMBED_TANKS,
                    value=f'{ClassJobs.PLD} {char.jobs["PLD"]}\t\t'
                          f'{ClassJobs.WAR} {char.jobs["WAR"]}\t\t'
                          f'{ClassJobs.DRK} {char.jobs["DRK"]}\t\t'
                          f'{ClassJobs.GNB} {char.jobs["GNB"]}'.replace(' 0', ' --'),
                    inline=False)
    # Healers
    embed.add_field(name=lang.CHAR_EMBED_HEALERS,
                    value=f'{ClassJobs.WHM} {char.jobs["WHM"]}\t\t'
                          f'{ClassJobs.SCH} {char.jobs["SCH"]}\t\t'
                          f'{ClassJobs.AST} {char.jobs["AST"]}'.replace(' 0', ' --'),
                    inline=False)
    # DPS
    embed.add_field(name=lang.CHAR_EMBED_DPS,
                    value=f'{ClassJobs.MNK} {char.jobs["MNK"]}\t\t'
                          f'{ClassJobs.DRG} {char.jobs["DRG"]}\t\t'
                          f'{ClassJobs.NIN} {char.jobs["NIN"]}\t\t'
                          f'{ClassJobs.SAM} {char.jobs["SAM"]}\n'
                          f'{ClassJobs.BLM} {char.jobs["BLM"]}\t\t'
                          f'{ClassJobs.SMN} {char.jobs["SMN"]}\t\t'
                          f'{ClassJobs.RDM} {char.jobs["RDM"]}\t\t'
                          f'{ClassJobs.BLU} {char.jobs["BLU"]}\n'
                          f'{ClassJobs.BRD} {char.jobs["BRD"]}\t\t'
                          f'{ClassJobs.MCH} {char.jobs["MCH"]}\t\t'
                          f'{ClassJobs.DNC} {char.jobs["DNC"]}'.replace(' 0', ' --'),
                    inline=False)
    # Crafters
    embed.add_field(name=lang.CHAR_EMBED_CRAFTERS,
                    value=f'{ClassJobs.CRP} {char.jobs["CRP"]}\t\t'
                          f'{ClassJobs.BSM} {char.jobs["BSM"]}\t\t'
                          f'{ClassJobs.ARM} {char.jobs["ARM"]}\t\t'
                          f'{ClassJobs.GSM} {char.jobs["GSM"]}\n'
                          f'{ClassJobs.LTW} {char.jobs["LTW"]}\t\t'
                          f'{ClassJobs.WVR} {char.jobs["WVR"]}\t\t'
                          f'{ClassJobs.ALC} {char.jobs["ALC"]}\t\t'
                          f'{ClassJobs.CUL} {char.jobs["CUL"]}'.replace(' 0', ' -'),
                    inline=False)
    # Gatherers
    embed.add_field(name=lang.CHAR_EMBED_GATHERERS,
                    value=f'{ClassJobs.MIN} {char.jobs["MIN"]}\t\t'
                          f'{ClassJobs.BTN} {char.jobs["BTN"]}\t\t'
                          f'{ClassJobs.FSH} {char.jobs["FSH"]}'.replace(' 0', ' -'),)

    # Return the completely built embed
    return embed
