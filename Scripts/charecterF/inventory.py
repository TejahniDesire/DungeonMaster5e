import sys
import pathlib

from ..objectF import (pyHelper, itemsDnD) 
from ..charecterF import(charecterMechanics)

import numpy as np

class ItemHolder:
    def __init__(self):
        self.inventory = {}
        self.order = "name"
        self.reverse = False
        
    def update(self):
        mark_for_deletion = []
        for key in self.inventory:
            if self.inventory[key].get_amount() == 0:
                mark_for_deletion += [key]
        for i in range(len(mark_for_deletion)):
            print(self.inventory[mark_for_deletion[i]])
            del self.inventory[mark_for_deletion[i]]
            
    def add_item(self, item: itemsDnD.Item, amount=1):
        key = item.get_key_name()
        if key in self.inventory.keys():  # if item already present, add to amount
            self.inventory[key].add_amount(amount)
        else:
            self.inventory[key] = item
            self.inventory[key].add_amount(amount)
        self.update()
    
    def subtract_item(self, key, amount):
        self.inventory[key].subtract_amount(amount)
        if self.inventory[key].get_amount() == 0:
            del self.inventory[key]
        self.update()

    def remove_item(self,key):
        del self.inventory[key]

    def find_keys_of_item(self, query_item:str):
        return pyHelper.regexSearch(query_item, list(self.inventory))
    
    def set_sorting(self,order:str):
        self.order = order

    def set_reversal(self,reverse:bool):
        self.reverse = reverse

    def reversal(self):
        self.reverse = not self.reverse

    def get_all_items(self):
        """
        :return: symbol list of all items
        """
        functions = {
            "name": lambda x: x.get_name(),
            "cost": lambda x: x.get_normal_cost(),
            "weight": lambda x: x.get_total_weight(),
            "amount": lambda x: x.get_amount(),
            "type": lambda x: x.get_type(),
        }
        items = list(self.inventory.values())
        key_values = [functions[self.order](item) for item in items]

        new_list = list(zip(items, key_values))

        new_list = sorted(new_list, key=lambda x: x[1], reverse=self.reverse)
        return [i[0] for i in new_list]

    def get_items(self, query_item:str):
        """
        :param query_item:
        :return:
        """
        if query_item == '':
            return self.get_all_items()
        functions = {
            "name": lambda x: x.get_name(),
            "cost": lambda x: x.get_normal_cost(),
            "weight": lambda x: x.get_total_weight(),
            "amount": lambda x: x.get_amount(),
            "type": lambda x: x.get_type(),
        }

        key_matches = self.find_keys_of_item(query_item)

        item_matches = []  # list[items]
        for key in list(key_matches):
            item_matches += [self.inventory[key]]

        key_values = [functions[self.order](item) for item in item_matches]

        new_list = list(zip(item_matches, key_values))

        new_list = sorted(new_list, key=lambda x: x[1], reverse=self.reverse)

        return [i[0] for i in new_list]
    
    def get_total_weight(self):
        items = self.get_all_items
        weight = 0
        for item in items():
            weight += item.get_weight()
        return weight

    def __getitem__(self, item: str):
        item = pyHelper.name_to_key(item)
        return self.inventory[item]

    def __str__(self):
        return str(self.get_all_items())


class Inventory(ItemHolder):

    def __init__(self, encumberance:charecterMechanics.Encumbrance):
        super().__init__()
        self.money = {
            "cp": pyHelper.ReferenceNumber(0,is_int=True),
            "sp": pyHelper.ReferenceNumber(0,is_int=True),
            "ep": pyHelper.ReferenceNumber(0,is_int=True),
            "gp": pyHelper.ReferenceNumber(0,is_int=True),
            "pp": pyHelper.ReferenceNumber(0,is_int=True)
        }
        self.encumberance = encumberance
        self.encumberance_weight = self.encumberance.get_weight()

    def update(self):
        super().update()
        self.encumberance_weight.setValue(0)
        for key in self.inventory.keys():
            self.encumberance_weight.add(self.inventory[key].get_total_weight())
        self.encumberance.update()

    def add_money(self, amount, denominations):
        """
        :param amount: amount to be added. To subtract, set negative
        :param denominations:
        """
        denominations.casefold()
        if np.sign(amount) == -1:
            if self.money[denominations].value < amount:
                raise ValueError("Amount subtracted is less than amount had")
        self.money[denominations].add(amount)

    def add_item(self, item: itemsDnD.Item, amount=1):
        key = item.get_key_name()
        if key in self.inventory.keys():  # if item already present, add to amount
            print("ALREADY IN")
            self.inventory[key].add_amount(amount)
        else:
            self.inventory[key] = item
            # self.inventory[key].add_amount(amount)
        self.update()

        # add to list by type

    def subtract_item(self, key, amount):
        super().subtract_item(key,amount)
        self.update()

    def remove_item(self,key):
        super().remove_item()

    def get_weight(self):
        return self.encumberance_weight.getValue()

    def get_encumberance_status(self):
        return self.encumberance.get_encumberance_status()

    def get_money_ref(self, denominations=None):
        """
        :param denominations:
        :return: list[cp, sp, ep, gp] of type Reference number
        """
        if denominations is None:
            return [self.money["cp"], self.money["sp"], self.money["ep"], self.money["gp"], self.money["pp"]]
        else:
            return [self.money[denominations]]

    def get_money(self, denominations=None):
        """
        :param denominations:
        :return: list[cp, sp, ep, gp] of type Reference number
        """
        if denominations is None:
            return [self.money["cp"].getValue(), self.money["sp"].getValue(), self.money["ep"].getValue(), self.money["gp"].getValue(), self.money["pp"].getValue()]
        else:
            return [self.money[denominations].getValue()]


class AttackInventory(ItemHolder):

    def __init__(self,inventory:Inventory):
        super().__init__()
        self.item_inventory_object = inventory  # higher inventory of charecter

    def update(self):
        super().update()
        for key in self.inventory:
            if key not in self.item_inventory_object.inventory:
                self.remove_item(key)

    def add_attack_item(self,item):
        if type(item) is str:
            item = pyHelper.name_to_key(item)
        else:
            item = item.get_key_name()

        if item in self.item_inventory_object.inventory:
            self.add_item(self.item_inventory_object.inventory[item],amount=0)
        else:
            print(item + " not in inventory")



