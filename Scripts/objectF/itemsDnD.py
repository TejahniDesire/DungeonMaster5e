import sys
import pathlib

from . import pyHelper, objectsDnd
# print(Scripts)
# from Scripts.objectF import pyHelper
# from Scripts.objectF import objectsDnD

line = "________________________________________________________________________\n"
Delineator = '-*^*-'
Weapon_Property_Delineator = ';]},'
class Item:

    def __init__(self, name: str, weight: float, cost: tuple = (0, "gp"), category: str = "Misc",bonus: int = 0):
        """_summary_

        Args:
            name (str): Name of Item
            weight (float): Pounds
            cost (tuple, optional): (Amount, delimination).
            category (str, optional): Category of item (Misc, Weapon)
            bonus (int, optional): _description_. Defaults to 0.
        """
        self.name = name
        self.key_name = pyHelper.name_to_key(self.name)
        self.cost = cost
        self.weight = float(weight)
        self.amount = 1
        self.type = category
        self.is_equipped = False

        # None Objects

        self.weapon_stats = {
            "damage_dice": objectsDnd.Dice(1, 4),
            "damage_type": "bludgeoning",
            "properties": None,
            "weapon_class": None,
            "bonus": None
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
    
    def get_bonus(self):
        return self.weapon_stats["bonus"]

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
    
    # __________________________________________________________________

    def set_name(self,name):
        self.name = name
        self.key_name = pyHelper.name_to_key(self.name)

    def set_bonus(self,bonus):
        self.weapon_stats['bonus'] =  bonus

    def copy(self):
        return Item(self.get_name(), self.get_weight(), self.get_cost(), self.get_type(), self.get_bonus())
    
    # __________________________________________________________________

    def save_text(self):
        name = self.name
        string = ''
        
        for prop in [self.cost,self.weight,self.amount,self.is_equipped,self.type]:
            string += str(prop) + Delineator

        return name, string


scalings = ['str', 'dex', 'con', 'int', 'wis', 'chr']

# Specific stats: damage_dice, damage_type,  properties, weapon_class, scaling
class Weapon(Item):
    def __init__(self, name: str, weight: float, cost: tuple, damage_dice: tuple,
                 damage_type: str, properties: list[str], weapon_class: str, scaling: str = "str", scaling_fixed:bool=True,bonus:int = 0):
        super().__init__(name, weight, cost)

        self.type = "Weapon"
        self.weapon_stats = {
            "damage_dice": objectsDnd.Dice(damage_dice[0], damage_dice[1]),
            "damage_type": damage_type,
            "properties": properties,
            "weapon_class": weapon_class,
            "bonus": bonus # TODO: make this a reference number
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
    
    def copy(self):
        return Weapon(self.get_name(), self.get_weight(), self.get_cost(), (self.get_damage_dice().get_amount(),self.get_damage_dice().get_type()),
                 self.get_damage_type(), self.get_properties(), self.get_weapon_class, self.getScaling(), self.isScalingFixed(),self.get_bonus())
    
    def save_text(self):
        name, string = super().save_text()
        string += str((self.weapon_stats['damage_dice'].get_amount(), self.weapon_stats['damage_dice'].get_type())) + Delineator
        string += str(self.weapon_stats['damage_type']) + Delineator
        
        for prop in self.weapon_stats['properties']:
            string += prop + Weapon_Property_Delineator
        string = string[:-4]
        string += Delineator

        string +=str(self.weapon_stats["weapon_class"]) + Delineator
        string +=str(self.weapon_stats["bonus"]) + Delineator
        string +=str(self.scaling)+ Delineator
        string +=str(self.scaling_fixed)+ Delineator
        return self.name, string


def generalItemTextParser(item_string):
    props = item_string.split('-*^*-')
    
    cost = pyHelper.readTuple(props[0],pos1_type=int,pos2_type=str)
    weight = float(props[1])
    amount= int(props[2])
    
    is_equipped = bool(props[3])
    category = props[4]

    return cost, weight, amount, is_equipped, category, props

def loadItem(name,item_string):
    cost, weight, amount, is_equipped, category, _ = generalItemTextParser(item_string)
    item = Item(name=name,weight=weight,cost=cost,category=category)
    item.update_amount(amount)
    {True:item.equip, False:item.unequiped}[is_equipped]
    return item

def loadWeapon(name, item_string):
    cost, weight, amount, is_equipped, category, props = generalItemTextParser(item_string)
    damage_dice = pyHelper.readTuple(props[5],pos1_type=int,pos2_type=int)
    print("DDD",damage_dice)
    damage_type = props[6]
    properties =[]
    for weapon_prop in props[7].split(Weapon_Property_Delineator):
        properties += [weapon_prop]

    weapon_class = props[8]
    bonus = int(props[9])
    scaling = props[10]
    scaling_fixed = bool(props[11])
    return Weapon(name=name,weight=weight,cost=cost,damage_dice=damage_dice, damage_type=damage_type, properties=properties,
                  weapon_class=weapon_class,scaling=scaling,scaling_fixed=scaling_fixed,bonus=bonus)

def loadGenItem(name, item_string):

    item_type = item_string.split('-*^*-')[4]
    if item_type == "Weapon":
        return loadWeapon(name,item_string)
    else:
        return loadItem(name,item_string)