from functools import partial

import numpy as np


class ReferenceNumber:
    def __init__(self, number, is_int=False):
        self.value = number
        self.is_int = is_int

    def getValue(self):
        return self.value

    def subtract(self,amount):
        if self.is_int:
            amount = int(amount)
        self.value -= amount

    def add(self,amount):
        if self.is_int:
            amount = int(amount)
        self.value += amount

    def setValue(self,new_value):
        if self.is_int:
            new_value = int(new_value)
        self.value = new_value

    def __str__(self):
        return str(self.value)


def preform(function:list,args:list):
    for i in range(len(function)):
        if len(args) > i:
            if type(args[i]) is list:
                evaluated_args = []
                for j in range(len(args[i])):
                    if callable(args[i][j]):
                        evaluated_args += [args[i][j]()]
                    else:
                        evaluated_args += [args[i][j]]

                function[i](*evaluated_args)
            else:
                if callable(args[i]):
                    function[i](args[i]())
                else:
                    function[i](args[i])
        else:
            function[i]()