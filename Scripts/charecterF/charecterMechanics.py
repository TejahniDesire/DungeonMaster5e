from ..objectF import pyHelper
from .charecterAttributes import Stat

class HitDice:

    def __init__(self):
        self.labels = ['Total Hit Dice', 'Current Hit Dice']
        self.total_hd = 0
        self.current_hd = 0
        self.hd_type = 0

    def update(self):
        pass

    def set_d_type(self, type: int):
        self.hd_type = type

    def set_total_hd(self, amount: int):
        self.total_hd = amount

    def add_hd(self, amount: type):
        if self.current_hd >= self.total_hd:
            self.current_hd = self.total_hd
        else:
            self.current_hd += amount

    def subtract_hd(self):
        if self.current_hd <= 0:
            raise ValueError('Current Hit dice is at 0')
        else:
            self.current_hd -= 1

    def get_total_hd_label(self):
        return self.labels[0]

    def get_total_hd(self):
        return self.total_hd

    def get_total_hd_string(self):
        string = ''
        string += str(self.get_total_hd()) + 'D' + str(self.get_hd_type())
        return string

    def get_current_hd_label(self):
        return self.labels[1]

    def get_current_hd(self):
        return self.current_hd

    def get_current_hd_string(self):
        string = ''
        string += str(self.get_current_hd()) + 'D' + str(self.get_hd_type())
        return string

    def get_hd_type(self):
        return self.hd_type


class DeathSavingThrows:

    def __init__(self):
        self.type = 'Death Saving Throws'
        self.labels = ['Successes', 'Failures']
        self.successes = 0
        self.failures = 0
        self.isDead = False
        self.isStable = False

    def update(self):
        if self.successes == 3:
            self.isStable = True
        elif self.failures == 3:
            self.isDead = True

    def mark_success(self):
        if self.successes < 3:
            self.successes += 1

    def reduce_success(self):
        if self.successes > 0:
            self.successes -= 1

    def mark_failure(self):
        if self.failures < 3:
            self.failures += 1

    def reduce_failure(self):
        if self.failures > 0:
            self.failures -= 1

    def reset(self):
        self.successes = 0
        self.failures = 0
        self.isDead = False
        self.isStable = False

    def get_num_success(self):
        return self.successes

    def get_num_failure(self):
        return self.failures
    
    def isAlive(self):
        return self.get_num_failure() < 3
    
    def isStable(self):
        return self.get_num_success() == 3

    def get_labels(self):
        return self.labels

    def get_type(self):
        return self.type

    def get_success_label(self):
        return self.labels[0]

    def get_failure_label(self):
        return self.labels[1]


class Encumbrance:

    def __init__(self,str_score:Stat):
        self.weight = pyHelper.ReferenceNumber(0)
        self.enc_status = pyHelper.ReferenceNumber(-1,is_int=True)  # -1: unencumbered| 0: lvl0 encumbered| 1: lvl1 encumvered| 2: at/past max encumbered
        self.str_score = str_score
        self.enc_levels_multipliers = {
            'lvl0': 5,
            'lvl1': 10,
            'lvl2': 15  # max
        }
        self.enc_levels = self.calculate_encumberence_levels()

        self.encum_word_status_array = ["Unencumbered", "Encumbered","Heavily Encumbered", "Max Load"]
        self.encum_word_status = self.encum_word_status_array[self.enc_status.getValue() + 1]

    def set_encumberance_level_multiplier(self,lvl:int, multiplier:float):
        """

        :param lvl: encumberence level multiplier to set (lvl0,lvl1,lv2)
        :param multiplier: Multiplier to be set as
        :return:
        """
        self.enc_levels_multipliers["lvl" + str(lvl)] = multiplier
        self.update()

    def update(self):
        self.enc_levels = self.calculate_encumberence_levels()
        self.enc_status, self.encum_word_status = self.calculate_encumberence_status()

    def calculate_encumberence_levels(self):
        """
        :return: Encumberence levels in list [lvl0,lvl1,lvl2]
        """
        str_score = self.str_score.get_total_base()
        return [self.enc_levels_multipliers['lvl0'] * str_score,
                self.enc_levels_multipliers['lvl1'] * str_score,
                self.enc_levels_multipliers['lvl2'] * str_score]

    def calculate_encumberence_status(self):
        """
        :return: calculate if current weight is > lvl0,lv1,or lvl2
        """
        weight = self.get_weight()
        status = -1

        if weight > self.enc_levels[0]:
            status += 1

        if weight > self.enc_levels[1]:
            status += 1

        if weight >= self.enc_levels[2]:
            status += 1
        return pyHelper.ReferenceNumber(status), self.encum_word_status_array[status + 1]

    def set_weight(self,amount):
        if amount < 0:
            raise ValueError("Negative weight inputed")
        self.weight.setValue(amount)
        self.update()

    def zeroWeight(self):
        self.weight.setValue(0)

    def add_weight(self,amount):
        self.weight.add(amount)
        self.update()

    def subtract_weight(self,amount):
        if self.weight.getValue() >= amount:
            self.weight.subtract(amount)
        else:
            raise ValueError("Subtracting more weight than currently present")
        self.update()

    def get_weight(self):
        return self.weight
    
    def get_weight_value(self):
        return self.weight.getValue()

    def get_encumberance_status(self):
        return self.enc_status

    def get_encumberance_word_status(self):
        return self.encum_word_status

    def get_encumberance_levels(self):
        return self.enc_levels


