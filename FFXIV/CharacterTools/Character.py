class Character:
    def __init__(self, char_data: dict):
        try:
            self.name = char_data["Character"]["Name"]
            self.world = char_data["Character"]["Server"]
            self.title = char_data["Character"]["Title"]["Name"]
            self.active_job = char_data["Character"]["ActiveClassJob"]["Class"]["ID"]

            self.id = char_data["Character"]["ID"]
            self.lodestone_url = f'https://eu.finalfantasyxiv.com/lodestone/character/{self.id}/'
            self.picture_mini = char_data["Character"]["Avatar"]

            try:
                self.gc = char_data["Character"]["GrandCompany"]["Company"]["Name"].replace('[p]', '')
                self.gc_rank = char_data["Character"]["GrandCompany"]["Rank"]["Name"]
            except Exception:
                self.gc = None
                self.gc_rank = None

            try:
                self.fc = char_data["FreeCompany"]["Name"]
                self.fc_short = char_data["FreeCompany"]["Tag"]
                self.fc_rank = char_data["FreeCompany"]["Rank"]
                self.fc_memcount = char_data["FreeCompany"]["ActiveMemberCount"]
            except Exception:
                self.fc = None
                self.fc_short = None
                self.fc_rank = None
                self.fc_memcount = None

            self.jobs = {
                'PLD': char_data["Character"]["ClassJobs"][0]["Level"],
                'WAR': char_data["Character"]["ClassJobs"][1]["Level"],
                'DRK': char_data["Character"]["ClassJobs"][2]["Level"],
                'GNB': char_data["Character"]["ClassJobs"][3]["Level"],

                'WHM': char_data["Character"]["ClassJobs"][8]["Level"],
                'SCH': char_data["Character"]["ClassJobs"][9]["Level"],
                'AST': char_data["Character"]["ClassJobs"][10]["Level"],

                'MNK': char_data["Character"]["ClassJobs"][4]["Level"],
                'DRG': char_data["Character"]["ClassJobs"][5]["Level"],
                'NIN': char_data["Character"]["ClassJobs"][6]["Level"],
                'SAM': char_data["Character"]["ClassJobs"][7]["Level"],
                'BLM': char_data["Character"]["ClassJobs"][14]["Level"],
                'SMN': char_data["Character"]["ClassJobs"][15]["Level"],
                'RDM': char_data["Character"]["ClassJobs"][16]["Level"],
                'BLU': char_data["Character"]["ClassJobs"][17]["Level"],
                'BRD': char_data["Character"]["ClassJobs"][11]["Level"],
                'MCH': char_data["Character"]["ClassJobs"][12]["Level"],
                'DNC': char_data["Character"]["ClassJobs"][13]["Level"],

                'CRP': char_data["Character"]["ClassJobs"][18]["Level"],
                'BSM': char_data["Character"]["ClassJobs"][19]["Level"],
                'ARM': char_data["Character"]["ClassJobs"][20]["Level"],
                'GSM': char_data["Character"]["ClassJobs"][21]["Level"],
                'LTW': char_data["Character"]["ClassJobs"][22]["Level"],
                'WVR': char_data["Character"]["ClassJobs"][23]["Level"],
                'ALC': char_data["Character"]["ClassJobs"][24]["Level"],
                'CUL': char_data["Character"]["ClassJobs"][25]["Level"],

                'MIN': char_data["Character"]["ClassJobs"][26]["Level"],
                'BTN': char_data["Character"]["ClassJobs"][27]["Level"],
                'FSH': char_data["Character"]["ClassJobs"][28]["Level"],
            }
        except Exception:
           raise RuntimeError('Character data is corrupted!')
