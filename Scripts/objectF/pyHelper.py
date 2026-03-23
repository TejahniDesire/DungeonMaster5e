# setting path_____________________
# import sys
# pathStr = ''
# strArr = sys.path[0].split('/')
# for string in strArr:
#     if string is not strArr[-1]:
#         pathStr += string + '/'
# sys.path.append(pathStr)
# _________________________________
import numpy as np

import re

def sign_string(bonus,show_positive =True,show_negative = True):
    if np.sign(bonus) == -1:
        if show_negative:
            sign = '-'
        else:
            sign = ''
    else:
        if show_positive:
            sign = '+'
        else:
            sign = ''

    return sign

def string_to_list(string:str, delineator:str = ','):
    return list(map(str, string.split(delineator)))

def keep_only_char(string,charz):
    return ''.join([char for char in string if char == charz])

def readTuple(tupleStr,delineator=',',pos1_type=int,pos2_type=int):
    pos1 = ''.join(filter(str.isalnum, tupleStr.split(delineator)[0]))
    pos2 = ''.join(filter(str.isalnum, tupleStr.split(delineator)[1]))
    return (pos1_type(pos1),pos2_type(pos2))

def name_to_key(name:str):
    return name.casefold().replace(" ", "_")

def key_to_name(key:str):
    return key.replace("_"," ").title()

def regexSearch(query:str, searchList):
    query = name_to_key(query)
    regex = ".*" + query + ".*"
    item_list = "\n".join(searchList)
    return re.findall(regex, item_list)

def preform(function:list,args:list):
    '''
    preforms a list of functions, matching the ith argument with the ith function.
    members of args can be partial functions themselves, in which case they will be called before being fed into their respective function
    '''
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


class ReferenceNumber:
    '''
    A number that is pass by reference
    '''
    def __init__(self, number, is_int=False):
        self.value = number
        self.is_int = is_int

    def getValue(self):
        return self.value

    def subtract(self,amount):
        if type(amount) == ReferenceNumber:
            amount = amount.getValue()
        if self.is_int:
            amount = int(amount)
        self.value -= amount

    def minus(self,amount):
        self.subtract(amount)

    def add(self,amount):

        if type(amount) == ReferenceNumber:
            amount = amount.getValue()
        if self.is_int:
            amount = int(amount)
        self.value += amount

    def setValue(self,new_value):

        if type(new_value) == ReferenceNumber:
            new_value = new_value.getValue()
        if self.is_int:
            new_value = int(new_value)
        self.value = new_value

    def copy(self):
        return ReferenceNumber(self.getValue(), self.is_int)

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self,number):
        if type(number) == ReferenceNumber:
            number = number.getValue()

        return self.getValue() == number
    
    def __lt__(self,number):
        if type(number) == ReferenceNumber:
            number = number.getValue()
            
        return self.getValue() < number

    def __le__(self,number):
        if type(number) == ReferenceNumber:
            number = number.getValue()

        return self.getValue() <= number
    
    def __gt__(self,number):
        if type(number) == ReferenceNumber:
            number = number.getValue()

        return self.getValue() > number
    
    def __ge__(self,number):
        if type(number) == ReferenceNumber:
            number = number.getValue()

        return self.getValue() >= number


    
class ReferenceString:

    def __init__(self,string):
        self.string = str(string)

    def setString(self,string):
        self.string = str(string)

    def getString(self):
        return self.string
    
    def __str__(self):
        return self.string
    
class ProgressMarker:

    def __init__(self,functions=[]):
        

        self.fraction = ReferenceNumber(0.0,is_int=False)
        self.functions = []
        if type(functions) is list:
            for function in functions:
                self.functions += [function]
        else:
            self.functions += [functions]

    def addFunction(self,function):
        """_summary_

        Args:
            function (_type_): a function that takes a fraction as an argument
        """
        self.functions += [function]
    
    def propagateFunctions(self):
        for function in self.functions:
            function(self.getProgressValue())

    def getProgessRef(self):
        return self.fraction
    
    def getProgressValue(self):
        return self.fraction.getValue()
    
    def setProgress(self,value):
        if (value > 1) or (value < 0): raise ValueError("Value must be between 0 and 1 inclusively")
        self.fraction.setValue(value)
        self.propagateFunctions()

    def resetProgress(self):
        self.fraction.setValue(0.0)
        self.propagateFunctions()
        
    def completeProgress(self):
        self.fraction.setValue(1.0)
        self.propagateFunctions()

    def addProgress(self,value):
        if (value > 1) or (value < 0): raise ValueError("Value must be between 0 and 1 inclusively")
        self.fraction.add(float(value))
        self.propagateFunctions()


    def __str__(self):
        return "{:.2f}%".format(self.fraction.getValue() * 100) 

# TIME______________________________________________________________________________________________________________________________
Month = {
    '01':  'January',
    '02':  'February',
    '03':  'March',
    '04':  'April',
    '05':  'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September',
    '1':  'January',
    '2':  'February',
    '3':  'March',
    '4':  'April',
    '5':  'May',
    '6': 'June',
    '7': 'July',
    '8': 'August',
    '9': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December',
}

def hourTime(hour,minute,second):
    hour = int(hour)

    if hour > 12:
        string = str(hour % 12) + ':' + minute + ':' + second + 'PM'
    else:
        string = str(hour) + ':' + minute + ':' + second + 'PM'

    return string



def timeToHuman(string):
    parts = string.split('_')

    hstring = Month[parts[0]] + '-' + parts[1] + '-' + '20' + parts[2] + '-' + hourTime(parts[3],parts[4],parts[5]) 

    return hstring

