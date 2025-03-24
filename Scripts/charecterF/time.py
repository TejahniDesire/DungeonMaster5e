import numpy as np

from ..objectF import pyHelper

class Time: 

    def __init__(self,name='Grand Time',splinter=False,initial=None,unit=None,covert=False):
        
        # [week, day, hour, minute, second]
        self.unit_to_index = {
            'week':0,
            'day':1,
            'hour':2,
            'minute':3,
            'second':4
        }

        
        self.name = name
        self.time = pyHelper.ReferenceNumber(0) # seconds
        self.show_time = [0,0,0,0,0]
        self.covert = covert

        # Special____________________________________________________________
        self.special_unit_to_index = {
            'year': 0,
            'month': 1,
            'week':2,
            'day':3,
            'hour':4,
            'minute':5,
            'second':6
        }
        self.special_show_time =[0,0,0,0,0,0,0]

        
        self.special_unit_basis = [31536000, 2592000] # seconds in a gegorian [year, month]
        # Special____________________________________________________________

        self.splinters = {}
        self.non_covert_keys = []
        self.isSplinter = False

        self.initial = 0

        if splinter is True:
            self.isSplinter = True
            self.initial = toSecond(initial,unit)        

    def update(self):
        self.updateShowTime()
        for init in self.splinters.keys():
            self.splinters[init].updateShowTime()

    def isCovert(self):
        return self.covert
            
    def updateShowTime(self):
        breakdown = timeBreakdown(int(np.abs(self.time.getValue())),'second')
        i = 0
        for subtime in breakdown:
            self.show_time[i] = subtime
            i += 1

        special_breakdown = specialTimeBreakdown(int(np.abs(self.time.getValue())),self.special_unit_basis)

        i = 0
        for subtime in special_breakdown:
            self.special_show_time[i] = subtime
            i += 1

    def setSpecialTimeBasis(self,units: list[int]):
        self.special_unit_basis = [units]  
        self.updateShowTime()

        for init in self.non_covert_keys:
            self.splinters[init].setSpecialTimeBasis(units)
            self.splinters[init].updateShowTime()

    def splinterTime(self,name=None,covert=False):
        if self.isSplinter:
            raise KeyError("Cannot splinter a splinter")
        if name is None:
            name = "SubTime {}".format(len(self.splinters.values()) + 1)

        initial_time = self.time.getValue()

        if initial_time in self.splinters.keys():
            return initial_time, self.splinters[initial_time]
        

        splinter = Time(name, True,initial=initial_time,unit='second',covert=covert)

        if not covert:
            self.non_covert_keys += [initial_time]
        self.splinters[initial_time ] = splinter
        return initial_time , splinter

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
        for init in self.splinters.keys():
            self.splinters[init].updateShowTime()

    def getSplinter(self,time):
        self.splinters[time]

    def getSplinters(self):
        return self.splinters
    
    def getTime(self,unit=None):
        if unit is None:
            return self.show_time
        elif type(unit) is str:
            unit = self.unit_to_index[unit]
        elif type(unit) is list:
            rlist = []
            for queryUnit in unit:

                if type(queryUnit) is str:
                    
                    queryUnit = self.unit_to_index[queryUnit]
                    rlist += [self.show_time[queryUnit]]
                
            return rlist
                

        return self.show_time[unit]
    
    def getSpecialTime(self,unit=None):
        if unit is None:
            return self.special_show_time
        
        elif type(unit) is str:
        
            return self.special_show_time[self.special_unit_to_index[unit]]
        else:
            return self.special_show_time[unit]

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


def specialTimeBreakdown(amount:int,special_units):
    """_summary_

    Args:
        amount (int): _description_
        unit (str): _description_

    Returns:
        _type_: week, day, hour, minute, second
    """
    if type(amount) is not int:
        raise ValueError("Amount given must be an int")
    
    year_unit = special_units[0]
    month_unit = special_units[1]


    year,amount   = delin(amount, year_unit)
    month,amount  = delin(amount, month_unit)
    week,amount   = delin(amount, 604800)
    day,amount    = delin(amount, 86400)
    hour,amount   = delin(amount, 3600)
    minute,amount = delin(amount, 60)
    second        = amount % 60

    
    return year, month, week, day, hour, minute, second


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
    
