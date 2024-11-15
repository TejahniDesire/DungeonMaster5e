import math
import numpy as np
import ruleTools
import objectHelperTools as oHT

line = "________________________________________________________________________\n"


class Item:

    def __init__(self, name: str, weight: float, cost: tuple = (0, "gp"), category: str = "Misc"):
        self.name = name
        self.key_name = oHT.name_to_key(self.name)
        self.cost = cost
        self.weight = weight
        self.amount = 0
        self.type = category
        self.is_equipped = False

        # None Objects

        self.weapon_stats = {
            "damage_dice": ruleTools.Dice(1, 4),
            "damage_type": "bludgeoning",
            "properties": None,
            "weapon_class": None
        }

    def __str__(self):
        object_type = "Item Type | " + self.get_type() + "\n"

        name = "Name      | " + self.get_name().replace("_", " ") + '\n'
        cost = "Cost      | " + str(self.get_cost()[0]) + " " + self.get_cost()[1] + '\n'
        weight = "Weight    | " + str(self.get_weight()) + " lbs" + '\n'
        amount = "Amount    | " + str(self.get_amount()) + "x" + '\n'

        return line + object_type + name + cost + weight + amount + line

    def __repr__(self):
        return "DnDItem:" + self.name + "_" + self.type

    def get_name(self):
        """
        :return: str
        """
        return self.name

    def get_key_name(self):
        return self.key_name

    def get_amount(self):
        """
        :return: int
        """
        return self.amount

    def get_weight(self):
        """
        :return: float
        """
        return self.weight

    def get_total_weight(self):
        return self.weight * self.amount

    def get_cost(self):
        """
        :return: tuple
        """
        return self.cost

    def get_normal_cost(self):
        """

        :return: cost of item in copper
        """
        cost = {
            "cp": self.get_cost()[0],
            "sp": self.get_cost()[0] * 10,
            "ep": self.get_cost()[0] * 50,
            "gp": self.get_cost()[0] * 100,
            "pp": self.get_cost()[0] * 1000,
        }
        return cost[self.cost[1]]

    def get_type(self):
        """
        :return: list[str]
        """
        return self.type

    def get_damage_dice(self):
        """
        :return: dice
        """
        return self.weapon_stats["damage_dice"]

    def get_damage_type(self):
        """
        :return: str
        """
        return self.weapon_stats["damage_type"]

    def get_weapon_class(self):
        """
        :return: str
        """
        return self.weapon_stats["weapon_class"]

    def get_properties(self):
        """
        :return: list[str]
        """
        return self.weapon_stats["properties"]

    def getScaling(self):
        return "str"

    # ___________________________________________________________________

    def update_amount(self, new_amount):
        if new_amount < 0:
            raise ValueError("Negative Amount Set")
        self.amount = new_amount

    def add_amount(self, amount_added):
        self.amount += amount_added

    def subtract_amount(self, amount_subtracted: int):

        if self.amount < amount_subtracted:
            raise ValueError("Amount subtracted is less than amount had")
        else:
            self.amount -= amount_subtracted

    def safe_subtract(self, amount_subtracted: int):
        if self.amount < amount_subtracted:
            self.amount = 0
        else:
            self.amount -= amount_subtracted

    # __________________________________________________________________

    def equip(self):
        self.is_equipped = True

    def unequiped(self):
        self.is_equipped = False

    def is_equipped(self):

        return self.is_equipped

    def __getitem__(self, item):
        return self.weapon_stats[item]


scalings = ['str', 'dex', 'con', 'int', 'wis', 'chr']


class Weapon(Item):
    def __init__(self, name: str, weight: float, cost: tuple, damage_dice: tuple,
                 damage_type: str, properties: list[str], weapon_class: str, scaling: str = "str", scaling_fixed:bool=True):
        super().__init__(name, weight, cost)

        self.type = "Weapon"
        self.weapon_stats = {
            "damage_dice": ruleTools.Dice(damage_dice[0], damage_dice[1]),
            "damage_type": damage_type,
            "properties": properties,
            "weapon_class": weapon_class
        }
        self.scaling = scaling
        self.scaling_fixed = scaling_fixed

    def isScalingFixed(self):
        return self.scaling_fixed

    def getScaling(self):
        return self.scaling

    def setScaling(self, scaling: str):
        if not self.scaling_fixed:
            if scaling not in scalings:
                raise ValueError(str(scaling) + "is not a scaling")
            self.scaling = scaling

    def __str__(self):
        object_type = "Item Type  | " + self.get_type() + "\n"
        weapon_class = "Class      | " + self.get_weapon_class() + "\n"
        name = "Name       | " + self.name.replace("_", " ") + '\n'
        cost = "Cost       | " + str(self.cost[0]) + " " + self.cost[1] + '\n'
        damage = "Damage     | " + str(self.get_damage_dice()) + " " + self.get_damage_type() + '\n'
        weight = "Weight     | " + str(self.weight) + " lbs" + '\n'
        properties = "Properties | "
        existing_properties = self.get_properties()
        for i in range(len(existing_properties)):
            properties += existing_properties[i] + ", "
        properties = properties.rstrip(", ")
        properties += "\n"
        return line + object_type + weapon_class + name + cost + damage + weight + properties + line
