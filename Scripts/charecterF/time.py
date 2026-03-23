import numpy as np

from ..objectF import pyHelper

class Time: 

    def __init__(self,name='Grand Time',splinter=False,initial=None,unit=None,covert=False,protected_count=0,player_name=None):
        
        # [week, day, hour, minute, second]
        self.unit_to_index = {
            'week':   0,
            'day':    1,
            'hour':   2,
            'minute': 3,
            'second': 4
        }
        self.index_to_unit = {
            0: 'week',
            1: 'day',
            2: 'hour',
            3: 'minute',
            4: 'second'
        }

        
        self.name = name
        self.time = pyHelper.ReferenceNumber(0) # seconds
        self.initial = 0
        self.show_time = [0,0,0,0,0] # [Year, Month, Week, Day, Second]
        self.covert = covert
        self.protected_count = protected_count
        self.player_name = player_name


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
        self.covert_splinters = {}
        

        
        self.isSplinter = False
        if splinter is True:
            self.isSplinter = True
            self.initial = toSecond(initial,unit)        

    def setName(self,string:str):
        self.name =  string

    def update(self):
        self.updateShowTime()
        for init in self.splinters.keys():
            self.splinters[init].updateShowTime()

        for init in self.covert_splinters.keys():
            self.covert_splinters[init].updateShowTime()

    def isCovert(self):
        return self.covert
    
    def isProtected(self):
        return self.protected_count > 0 
            
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

        for init in self.splinters.keys():
            self.splinters[init].setSpecialTimeBasis(units)
            self.splinters[init].updateShowTime()

    def splinterTime(self,name=None,covert=False,protect=False,protection_count=None,initial_time=None,player_name=None):
        if self.isSplinter: raise ValueError("Cannot splinter a splinter")
        if (type(name) is not str) and (name is not None): raise ValueError("Name must be a string or None, not '{}'".format(type(name)))
        if name is None:
            name = "SubTime {}".format(len(self.splinters.values()) + 1)

        if initial_time is None: initial_time = self.time.getValue()
        elif not isinstance(initial_time, int):  raise ValueError("initial_time must be an integer or None, not '{}'".format(type(initial_time)))

        if initial_time in self.splinters.keys():
            if protect:
                self.splinters[initial_time].protectByOne()
            return initial_time, self.splinters[initial_time]
        
        if protect is False:
            new_protected_count = 0
        else:
            new_protected_count = 1

        if protection_count is not None:
            if type(protection_count) is not int: raise ValueError("protection_count must be an integer or None")
            new_protected_count = protection_count

        splinter = Time(name, splinter=True,initial=initial_time,unit='second',covert=covert,protected_count=new_protected_count,player_name=player_name)

        if not covert:
            self.splinters[initial_time ] = splinter
        else:
            self.covert_splinters[initial_time ] = splinter
        
        return initial_time , splinter

    def removeSplinter(self,initial_time=None,covert=False, splinter=None):
        if splinter is not None:
            # 
            if not splinter.isSplinter: raise ValueError("Attempting to remove a none splinter")

            initial_time = splinter.getInit()
            covert = splinter.isCovert
        else:
            if initial_time is None: raise ValueError("splinter and initial_time cannot both be None")
    

        if covert:
            query_splinter = self.covert_splinters[initial_time]
            query_dictionary = self.covert_splinters
        else: 
            query_splinter = self.splinters[initial_time]
            query_dictionary = self.splinters

        if query_splinter.isProtected():
            print("WARNING: Attempting to delete protected splinter. First unprotect the splinter.")
            return
    
        del query_dictionary[initial_time]

    def getInit(self):
        return self.initial

    def add(self,amount:int,unit:str):
        
        if not isinstance(amount, int):raise ValueError("Amount must be an int")
        
        for init in self.splinters.keys():
            self.splinters[init].add(amount,unit)
        
        amount = toSecond(amount,unit)
        self.time.add(amount)


        self.updateShowTime()
        for init in self.splinters.keys():
            self.splinters[init].updateShowTime()

    def setTime(self,amount:int,unit:str):
        if not isinstance(amount, int):raise ValueError("Amount must be an int")
        amount = toSecond(amount,unit)

        self.time.setValue(amount)

        for init in self.splinters.keys():

            splinter_amount = amount - init
            self.splinters[init].setTime(splinter_amount,unit)

        self.update()

    def setPlayerName(self,name):
        self.player_name = name

    def getSplinter(self,time):
        self.splinters[time]

    def getSplinters(self,covert=False):
        if covert: return self.covert_splinters
        else: return self.splinters

    def getTime(self,unit=None,absolute=False):
        """_summary_

        Args:
            unit (str | list, optional): [year, month, week, day, second]. Defaults to None.

        Returns:
            _type_: Returns member of array [Year, Month, Week, Day, Second]
        """
        if unit is None:

            if absolute:
                return self.time.getValue() # seconds
            else:
                return self.show_time
            
        if type(unit) is str:

            if absolute:
                return toUnitFromSecond(self.time.getValue(),unit)
            else:
                unit = self.unit_to_index[unit]
                return self.show_time[unit]

        elif type(unit) is list:
            rlist = []
            for queryUnit in unit:

                if type(queryUnit) is str:
                    
                    queryUnit = self.unit_to_index[queryUnit]
                rlist += [self.show_time[queryUnit]]
                
            return rlist

        raise ValueError("Unit of type '{}' unknown".format(type(unit)))
        
        
    def get_save_diction(self):

        name = "Time"

        diction = {
            'time': {str(self.time.getValue()):0}
        }
        
        diction["splinters"] = {}


        for init in self.splinters.keys():
            splinter = self.splinters[init]
            splinter_diction = {
                'name': {splinter.getName():0},
                'init': {str(init):0},
                'protected':{str(splinter.getProtectedStatus()):0},
                'covert': {str(splinter.isCovert()):0},
                'player_name': {str(splinter.player_name):0}
            }

            diction["splinters"][splinter.getName() + str(init)] = splinter_diction

        diction["covert_splinters"] = {}
        for init in self.covert_splinters.keys():
            splinter = self.covert_splinters[init]
            splinter_diction = {
                'name': {splinter.getName():0},
                'init': {str(init):0},
                'protected':{str(splinter.getProtectedStatus()):0},
                'covert': {str(splinter.isCovert()):0},
                'player_name': {str(splinter.player_name):0}
            }

            diction["covert_splinters"][splinter.getName() + str(init)] = splinter_diction

        return diction


    def set_viewer_dict(self,viewerDict):

        time = int(viewerDict[0][0].getValue())
        
        for key in viewerDict[1].keys():

            diction = viewerDict[1][key]
            name = diction[0][0].getValue()
            init = int(diction[1][0].getValue())
            protected = int(diction[2][0].getValue())
            covert = diction[3][0].getValue() == "True"
            player_name = diction[4][0].getValue()
            if player_name == 'None':
                player_name = None

            self.splinterTime(name=name,covert=covert,protection_count=protected ,initial_time=init,player_name=player_name)
            time_difference = init 

        self.setTime(time,'second')

            




        
    
    def getSpecialTime(self,unit=None):
        """_summary_

        Args:
            unit (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: year, month, week, day, hour, minute, second
        """
        if unit is None:
            return self.special_show_time
        
        elif type(unit) is str:
        
            return self.special_show_time[self.special_unit_to_index[unit]]
        else:
            return self.special_show_time[unit]
        
    def getSignString(self):
        string = pyHelper.sign_string(self.time.getValue(),show_positive=True)


        return string
    
    def getSign(self):
        return np.sign(self.time.getValue())

    def __str__(self):

        
        # string = ''
        # if np.sign(self.time.getValue()) == -1:
        #     string += '-'
        # for subtime in self.show_time:
        #     string += str(subtime).zfill(2) + ':'
        
        string = "("+ self.getSignString() + ") "
        string += str(self.getTime("week")) + ' Weeks '
        string += str(self.getTime("day")) + ' Days '
        string += str(self.getTime("hour")) + ' Hours '
        string += str(self.getTime("minute")) + ' Minutes '
        string += str(self.getTime("second")) + ' Seconds '
        # string = string[:-1]

        return string
    
    def getName(self):
        return self.name
    
    def getProtectedStatus(self):
        return self.protected_count
    
    def unprotectByOne(self):
        self.protected_count -= 1

    def unprotect(self):
        self.protected_count = 0

    def protectByOne(self):
        self.protected_count += 1




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
        _type_: year, month, week, day, hour, minute, second

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

def toUnitFromSecond(amount, unit):
    if unit == 'year':
        return amount / 3.154e+7
    elif unit == 'week':
        return amount / 604800
    elif unit == 'day':
        return amount / 86400
    elif unit == 'hour':
        return amount / 3600
    elif unit == 'minute':
        return amount / 60
    elif unit == 'second':
        return amount
    
