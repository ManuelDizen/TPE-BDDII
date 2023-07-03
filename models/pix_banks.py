from enum import Enum

class PixBanks(Enum):
    GAL = 0
    STD = 1
    FRA = 2

    def get_id_from_name(self, name):
        if name == "GAL":
            return 0
        elif name == "STD":
            return 1
        elif name == "FRA":
            return 2
        else:
            return -1
        
    def get_name_from_id(self, id):
        if id == 0:
            return "GAL"
        elif id == 1:
            return "STD"
        elif id == 2:
            return "FRA"
        else:
            return -1