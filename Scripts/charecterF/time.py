import numpy as np

from ..objectF import pyHelper

class Time:

    def __init__(self,splinter=False,initial=None,unit=None):
        
        # [week, day, hour, minute, second]
        self.unit_to_index = {
            'week':0,
            'day':1,
            'hour':2,
            'minute':3,
            'second':4
        }
        self.time = pyHelper.ReferenceNumber(0) # seconds
        self.show_time = [0,0,0,0,0]
        self.splinters = {}
        self.isSplinter = False

        self.initial = 0

        if splinter is True:
            self.isSplinter = True
            self.initial = toSecond(initial,unit)        
            
    def updateShowTime(self):
        breakdown = timeBreakdown(int(np.abs(self.time.getValue())),'second')
        i = 0
        for subtime in breakdown:
            self.show_time[i] = subtime
            i += 1

    def splinterTime(self):
        if self.isSplinter:
            raise KeyError("Cannot splinter a splinter")
        splinter = Time(True,initial=self.time.getValue(),unit='second')
        self.splinters[splinter.initial] = splinter

    def removeSplinter(self,initial_time):
        del self.splinters[initial_time]

    def add(self,amount:int,unit:str):
        
        if type(amount) is not int:
            raise ValueError("Amount must be an int")
        
        for init in self.splinters.keys():
            self.splinters[init].add(amount,unit)
        
        amount = toSecond(amount,unit)
        self.time.add(amount)


        self.updateShowTime()

    def getSplinters(self):
        return self.splinters

    def __str__(self):
        string = ''
        if np.sign(self.time.getValue()) == -1:
            string += '-'
        for subtime in self.show_time:
            string += str(subtime).zfill(2) + ':'
        
        string = string[:-1]

        return string


def timeBreakdown(amount:int,unit:str):
    """_summary_

    Args:
        amount (int): _description_
        unit (str): _description_

    Returns:
        _type_: week, day, hour, minute, second
    """
    if type(amount) is not int:
        raise ValueError("Amount given must be an int")
    
    if unit == 'week':
        week =   amount
        day =    0
        hour =   0
        minute = 0
        second = 0

    elif unit == 'day':
        week, amount = delin(amount, 7)
        day          = amount % 7
        hour         =   0
        minute       = 0
        second       = 0

    elif unit == 'hour':
        week, amount = delin(amount, 168)
        day, amount  = delin(amount, 24)
        hour         = amount % 24
        minute       = 0
        second       = 0

    elif unit == 'minute':
        week,amount   = delin(amount, 10080)
        day,amount    = delin(amount, 1440)
        hour,amount   = delin(amount, 60)
        minute        = amount % 60
        second        = 0

    elif unit == 'second':
        week,amount   = delin(amount, 604800)
        day,amount    = delin(amount, 86400)
        hour,amount   = delin(amount, 3600)
        minute,amount = delin(amount, 60)
        second        = amount % 60
    else:
        raise ValueError("Time unit not known")
    
    return week, day, hour, minute, second


def delin(amount,denom):
    unitAmount = int(amount / denom)
    return unitAmount, amount - (unitAmount * denom)
    

def toSecond(amount,unit:str):
    if unit == 'week':
        return amount * 604800
    elif unit == 'day':
        return amount * 86400
    elif unit == 'hour':
        return amount * 3600
    elif unit == 'minute':
        return amount * 60
    elif unit == 'second':
        return amount
    
    raise ValueError('Unit "{}" not reconized'.format(unit))
    
