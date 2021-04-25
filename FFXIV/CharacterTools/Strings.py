class Strings:
    def __init__(self, locale):
        if locale == 'pl_PL':
            pass
        else:
            self.CHAR_NOT_FOUND = 'Character not found.\n' \
                                  'Make sure you didn\'t make a mistake typing the name or the world.'
            self.CHAR_EMBED_NAME = 'Character information'
            self.CHAR_EMBED_GC = 'Grand Company'
            self.CHAR_EMBED_NONE = 'None'
            self.CHAR_EMBED_FC = 'Free Company'
            self.CHAR_EMBED_FC_MEMBER_COUNT = 'members'
            self.CHAR_EMBED_FC_RANK = 'Rank'
            self.CHAR_EMBED_HOME_WORLD = 'Home World'
            self.CHAR_EMBED_TITLE = 'Title'
            self.CHAR_EMBED_TANKS = 'Tanks'
            self.CHAR_EMBED_HEALERS = 'Healers'
            self.CHAR_EMBED_DPS = 'DPS'
            self.CHAR_EMBED_CRAFTERS = 'Crafters'
            self.CHAR_EMBED_GATHERERS = 'Gatherers'
            self.CHAR_EMBED_CREDITS = 'Powered by XIVAPI & much Moogle Love ❤'
            self.FFLOGS_EMBED_TITLE = 'Ranked logs of {name}'
            self.FFLOGS_NO_DATA = 'No FFLogs data found for **{name}**.'
