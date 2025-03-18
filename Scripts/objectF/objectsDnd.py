# setting path_____________________
import sys
pathStr = ''
strArr = sys.path[0].split('/')
for string in strArr:
    if string is not strArr[-1]:
        pathStr += string + '/'
sys.path.append(pathStr)
# _________________________________

import numpy as np
import math

def rollDice(amount: int,dicetype:int):
    dice = Dice(amount,dicetype)
    return dice.roll_dice()

class Dice:

    def __init__(self, amount: int, dicetype: int):
        '''
        ndN dice rolling object
        '''
        if amount < 0:
            raise ValueError("Dice amount must be greater than or equal to 0")
        if dicetype <= 0:
            raise ValueError("Dice type must be greater than 1")
        if not isinstance(dicetype, int) or not isinstance(amount, int):
            raise ValueError("Only ints are acceptable arguments")

        self.amount = amount
        self.dice_type = dicetype

    def __str__(self):
        string = str(self.amount) + 'd' + str(self.dice_type)
        return string

    def roll_dice(self, bonus=0):
        total = 0
        for i in range(self.amount):
            total += int(np.random.rand() * self.dice_type + 1)
        total += bonus
        return total

    def get_amount(self):
        return self.amount

    def get_type(self):
        return self.dice_type

    def add_amount(self, amount):
        self.amount += amount

    def remove_amount(self, amount):
        if self.amount == 0:
            raise Exception("No more dice left")
        elif amount > self.amount:
            raise Exception("Dice has less than specified amount")
        else:
            self.amount -= amount

