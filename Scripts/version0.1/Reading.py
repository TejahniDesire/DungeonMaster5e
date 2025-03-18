from fractions import Fraction
import objectsDnD
import objectHelperTools as oHT
import re


def parseWeaponLine(weaponClass, text):
    text = text.split()
    name = text[0]
    name = name.replace("_", " ")
    cost = text[1].split("_")
    cost = (float(cost[0]), cost[1])
    damage = text[2].split("d")
    damage = (int(damage[0]), int(damage[1]))
    damage_type = text[3]
    weight = float(Fraction(text[4]))
    properties = text[5].split("-")
    weapon = objectsDnD.Weapon(name,weight,cost,damage,damage_type,properties,weaponClass)
    return weapon


def weaponFileReader(file_name:str):
    ST = {}  # symbol table
    file = open(file_name, "r")
    line = "#"
    while line[0] == "#":
        line = file.readline()

    current_weapon_class = file.readline().rstrip("\n")
    current_line = file.readline()
    while current_line[0:3] != "###":  # read untill document end

        while not current_line.isspace():
            current_weapon = parseWeaponLine(current_weapon_class, current_line)
            ST[current_weapon.get_name().casefold().replace(" ", "")] = current_weapon
            current_line = file.readline()

        current_weapon_class = file.readline().rstrip("\n")  # read next weapon class line
        current_line = file.readline()
    file.close()

    return ST


class WeaponReader:

    def __init__(self,file_name:str):
        self.ST = {}  # symbol table
        file = open(file_name, "r")
        line = "#"
        while line[0] == "#":
            line = file.readline()

        current_weapon_class = file.readline().rstrip("\n")
        current_line = file.readline()
        while current_line[0:3] != "###":  # read untill document end

            while not current_line.isspace():
                current_weapon = parseWeaponLine(current_weapon_class, current_line)
                self.ST[current_weapon.get_name().casefold().replace(" ", "")] = current_weapon
                current_line = file.readline()

            current_weapon_class = file.readline().rstrip("\n") # read next weapon class line
            current_line = file.readline()
        file.close()

    def find_weapon_keys(self, query:str):
        """

        :param query:
        :return: Returns list of key names that match the search query
        """
        return oHT.regexSearch(query, list(self.ST))

    def get_weapons(self,weapon_query):
        """

        :param weapon_query:
        :return: Return list of Weapons that match the search query
        """
        key_matches = self.find_weapon_keys(weapon_query)
        weapon_matches = []
        if weapon_query == "":
            key_matches = list(self.ST)
        for key in list(key_matches):
            weapon_matches += [self.ST[key]]

        return sorted(weapon_matches, key=lambda x: x.get_name())

    def get_all_weapons(self):
        return self.get_weapons("")





#
#
# test = WeaponReader("./txtFiles/allWeapons/baseWeapons.txt")
# print(test.find_weapon_keys("sword"))
# print(test.get_weapons("sword")[2])
# #



