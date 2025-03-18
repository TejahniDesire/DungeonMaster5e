import math
import numpy as np

from ..objectF import pyHelper

line = "\n____________________________________________________________\n"
half_line = "\n_____________________________\n"
quart_line = "\n_______________\n"
line_left_new = "\n____________________________________________________________"
line_right_new = "____________________________________________________________\n"
line_no_new = "____________________________________________________________"


def calc_bonus(ability_score):
    return math.floor(((ability_score - 10) / 2))


def sign_string(bonus):
    if np.sign(bonus) == -1:
        sign = ''
    else:
        sign = '+'

    return sign


class Stat:

    def __init__(self, attribute: str):
        self.type = attribute

        self.contrib_base = {}  # library for contributions for the base
        self.total_bonus_val = pyHelper.ReferenceNumber(0,is_int=True) # numerical value of bonus summed over all contributions
        self.total_base_val = pyHelper.ReferenceNumber(0,is_int=True) # numerical value of base summed over all contributions
        self.contrib_bonus = {  # library for contributions for the bonus
            'nat_stat': pyHelper.ReferenceNumber(calc_bonus(self.total_base_val.getValue()),True) # bonus resulting only from total base stats
        }


    def update(self):
        # sum over all base contributions
        total_base_val = pyHelper.ReferenceNumber(0,True)
        for number in list(self.contrib_base.values()):
            total_base_val.add(number.getValue())
        self.total_base_val.setValue(total_base_val.getValue())

        self.contrib_bonus['nat_stat'].setValue(calc_bonus(self.total_base_val.getValue())) # set bonus from total base value
        
        # sum over all bonus contributions 
        total_bonus_val = pyHelper.ReferenceNumber(0,True)
        for number in list(self.contrib_bonus.values()):
            total_bonus_val.add(number.getValue())
        self.total_bonus_val.setValue(total_bonus_val.getValue())


    def add_base(self,source: str,amount:pyHelper.ReferenceNumber):
        if type(amount) is not pyHelper.ReferenceNumber:
            raise(KeyError("Given amount is not a reference number"))
        if source in self.contrib_base.keys():
            raise(KeyError("Source is already in stat"))
        self.contrib_base[source] =  amount
        self.update()

    def add_bonus(self,source: str, amount: pyHelper.ReferenceNumber):
        if type(amount) is not pyHelper.ReferenceNumber:
            raise(KeyError("Given amount is not a reference number"))
        self.contrib_bonus[source] = amount
        self.update()


    def alter_contrib_base(self, source: str, amount:int,easy=False):
        """change the amount contributed by a base

        Args:
            source (str): keyname of base
            amount (_type_): new value to be given by base
        """
        if type(amount) is not int:
            raise ValueError("Amount must be an int")
        
        if easy and (not self.contains_base_source(source)):
            self.contrib_base[source] = pyHelper.ReferenceNumber(amount,True)
        else:
            self.contrib_base[source].setValue(amount)
        self.update()

    def alter_contrib_bonus(self, source: str, amount:int, easy=False):
        """change the amount contributed by a bonus

        Args:
            source (str): keyname of bonus 
            amount (_type_): new value to be given by bonus
        """
        if type(amount) is not int:
            raise ValueError("Amount must be an int")
        

        if easy and (not self.contains_bonus_source(source)):
            self.contrib_bonus[source] = pyHelper.ReferenceNumber(amount,True)
        else:
            self.contrib_bonus[source].setValue(amount)
        self.update()

    def remove_base(self, source: str):
        del self.contrib_base[source]
        self.update()

    def remove_bonus(self, source: str):

        if source == 'nat_stat':
            raise KeyError("Attempting to delete nat_stat")
        del self.contrib_bonus[source]
        self.update()

    def contains_base_source(self,source:str):
        return source in self.contrib_base.keys()
    
    def contains_bonus_source(self,source:str):
        return source in self.contrib_bonus.keys()

    def get_total_base_ref(self):
        return self.total_base_val

    def get_total_base(self):
        return self.total_base_val.getValue()

    def get_total_bonus_ref(self):
        return self.total_bonus_val
    
    def get_total_bonus(self):
        return self.total_bonus_val.getValue()

    def get_type(self):
        return self.type

    def get_base_ref(self,source: str):
        return self.contrib_base[source]
    
    def get_bonus_ref(self,source):
        return self.contrib_bonus[source]
    
    def get_base(self,source: str):
        return self.contrib_base[source].getValue()
    
    def get_bonus(self,source):
        return self.contrib_bonus[source].getValue()
    

    def __str__(self):
        base_names = list(self.contrib_base)
        base_values = np.array(list(self.contrib_base.values()))
        string = self.type + ' Stat: ' + line + line_right_new
        string += 'Pure' + half_line
        for i in range(len(base_names)):
            if np.sign(base_values[i].getValue()) == -1:
                sign = ''
            else:
                sign = '+'
            string += ' ' + base_names[i] + ': ' + sign + str(base_values[i].getValue()) + '\n'
        string += '_____\n' + 'Total: ' + str(self.total_base_val)

        string += line + 'Modifier' + half_line
        bonus_names = list(self.contrib_bonus)
        bonus_values = np.array(list(self.contrib_bonus.values()))
        for i in range(len(bonus_names)):
            if np.sign(bonus_values[i].getValue()) == -1:
                sign = ''
            else:
                sign = '+'
            string += ' ' + bonus_names[i] + ': ' + sign + str(bonus_values[i].getValue()) + '\n'

        if np.sign(self.total_bonus_val.getValue()) == -1:
            sign = ''
        else:
            sign = '+'

        string += '_____\n' + 'Total: ' + sign + str(self.total_bonus_val) + line

        return string
        

class Skill:

    def __init__(self, name: str, base: Stat, prof: Stat):
        '''
        :param name: name of skill
        :param base: Base attribute for skill
        :param prof: proficiency attribure, total value is the bonus
        '''
        self.name = name
        self.base = base

        self.contrib = {
            'nat_stat': self.base.get_total_bonus_ref(),
            'prof': prof.get_total_base_ref(),
            'expert': pyHelper.ReferenceNumber(0,True)
        }

        self.bonus = pyHelper.ReferenceNumber(0,True)

        self.have = False  # is this skill had by this charecter
        self.expertise = False
        self.prof = prof

    def update(self):
        self.contrib['nat_stat'] = self.base.get_total_bonus_ref()

        if self.has_skill():
            self.contrib['prof'].setValue(self.prof.get_total_base())
            if self.is_expert():  # if expertise, double profeciency
                self.contrib['expert'].setValue(self.prof.get_total_base())
            else:
                self.contrib['expert'].setValue(0)
  
        else:
            self.contrib['prof'].setValue(0) # if skill is not had, no proffeciency bonus
            self.contrib['expert'].setValue(0)

        bonus = 0

        # exceptions = ['prof','expert']
        for name in list(self.contrib):
            bonus += self.contrib[name].getValue()



        self.bonus.setValue(bonus)


    def add_bonus(self,source: str, amount: pyHelper.ReferenceNumber):
        if type(amount) is not pyHelper.ReferenceNumber:
            raise(KeyError("Given amount is not a reference number"))
        self.contrib[source] = amount
        self.update()

    def alter_bonus(self, source, amount:int,easy=False):
        if type(amount) is not int:
            raise ValueError("Amount must be an int")
        
        if easy and (not self.contains_source(source)):
            self.contrib[source] = pyHelper.ReferenceNumber(amount,True)
        else:
            self.contrib[source].setValue(amount)

        self.update()

    def remove_bonus(self, source):
        del self.contrib[source]
        self.update()

    def has_skill(self):
        '''
        :return: Does this charecter have this skill
        '''
        return self.have

    def is_expert(self):
        return self.expertise

    def learn(self):
        '''
        give the charecter this skill
        '''
        self.have = True
        self.update()

    def give_expertise(self):
        self.expertise = True
        self.update()

    def unlearn(self):
        '''
        take away this skill from this charecter
        :return:
        '''
        self.have = False
        self.update()

    def unlearn_expertise(self):
        self.expertise = False
        self.update()

    def get_type(self):
        return self.name

    def get_total_bonus(self):
        return self.bonus.getValue()
    
    def get_total_bonus_ref(self):
        return self.bonus

    def get_total_bonus_string(self):
        sign = sign_string(self.get_total_bonus())
        string = sign + str(self.get_total_bonus())
        return string
    
    def get_source_ref(self,source:str):
        return self.contrib[source]
    
    def get_source(self,source:str):
        return self.contrib[source].getValue()
    
    def contains_source(self,source:str):
        return source in self.contrib.keys()
    
    def __str__(self):
        base_names = list(self.contrib)
    
        base_values = np.array(list(self.contrib.values()))
        string = self.name + ' Skill ({}): '.format(self.base.type) + line + line_right_new

        for i in range(len(base_names)):
            if np.sign(base_values[i].getValue()) == -1:
                sign = ''
            else:
                sign = '+'
            string += ' ' + base_names[i] + ': ' + sign + str(base_values[i].getValue()) + '\n'

        string += ' Has Skill: '
        if self.has_skill():
            profVal = self.contrib['prof'].getValue()
            if np.sign(profVal) == -1:
                sign = ''
            else:
                sign = '+'
            string += 'Yes ({}{})\n'.format(sign,profVal)
        else: 
            string += 'No\n'

        string += ' Is Expert: '
        if self.is_expert():
            expertVal = self.contrib['expert'].getValue()
            if np.sign(expertVal) == -1:
                sign = ''
            else:
                sign = '+'
            string += 'Yes ({}{})\n'.format(sign,expertVal)
        else: 
            string += 'No\n'

        if np.sign(self.bonus.getValue()) == -1:
            sign = ''
        else:
            sign = '+'

        string += '_____\n' + 'Total: ' + sign + str(self.bonus) + line

        return string


class TopStatValue:

    def __init__(self, label: str, is_number: bool):
        self.type = label
        self.is_number = is_number

        if is_number:
            self.value = pyHelper.ReferenceNumber(0)
        else:
            self.value = ''

    def get_type(self):
        return self.type

    def get_value(self):
        return self.value

    def add(self, amount):
        if self.is_number:
            self.value.add(amount)
        else:
            raise ValueError('This RPValue is not a number type')

    def subtract(self, amount):
        if self.is_number:
            self.value.subtract(amount)
        else:
            raise ValueError('This RPValue is not a number type')

    def set(self, new_value):
        if self.is_number:
            self.value.setValue(new_value)
        self.value = new_value

    def __str__(self):
        return self.type + ': ' + str(self.value)


class RPTraits:

    def __init__(self, type):
        self.type = type
        self.text = ''

    def get_type(self):
        return self.type

    def get_text(self):
        return self.text

    def set_text(self, text: str):
        self.text = text


