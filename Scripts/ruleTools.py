import math
import numpy as np


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


class Dice:

    def __init__(self, amount: int, dicetype: int):
        if amount < 0:
            raise ValueError("Dice amount must be greater than or equal to 0")
        if dicetype <= 0:
            raise ValueError("Dice type must be greater than 0")
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


class Stat:

    def __init__(self, attribute: str):
        self.type = attribute

        self.contrib_base = {}
        self.total_base_val = 0
        self.contrib_bonus = {
            'nat_stat': self.total_base_val
        }
        self.total_bonus_val = 0

    def update(self):
        self.total_base_val = int(np.sum(list(self.contrib_base.values())))
        self.contrib_bonus['nat_stat'] = calc_bonus(self.total_base_val)
        self.total_bonus_val = int(np.sum(list(self.contrib_bonus.values())))

    def alter_contrib_base(self, source: str, amount):
        self.contrib_base[source] = amount
        self.update()

    def alter_contrib_bonus(self, source: str, amount):
        self.contrib_bonus[source] = amount
        self.update()

    def remove_base(self, source: str):
        del self.contrib_base[source]
        self.update()

    def remove_bonus(self, source: str):
        del self.contrib_bonus[source]
        self.update()

    def get_total_base(self):
        return self.total_base_val

    def get_total_bonus(self):
        return self.total_bonus_val

    def get_type(self):
        return self.type

    def __str__(self):
        base_names = list(self.contrib_base)
        base_values = np.array(list(self.contrib_base.values()))
        string = self.type + ' Stat: ' + line + line_right_new
        string += 'Straight' + half_line
        for i in range(len(base_names)):
            if np.sign(base_values[i]) == -1:
                sign = ''
            else:
                sign = '+'
            string += ' ' + base_names[i] + ': ' + sign + str(base_values[i]) + '\n'
        string += '_____\n' + 'Total: ' + str(self.total_base_val)

        string += line + 'Modifier' + half_line
        bonus_names = list(self.contrib_bonus)
        bonus_values = np.array(list(self.contrib_bonus.values()))
        for i in range(len(bonus_names)):
            if np.sign(bonus_values[i]) == -1:
                sign = ''
            else:
                sign = '+'
            string += ' ' + bonus_names[i] + ': ' + sign + str(bonus_values[i]) + '\n'

        if np.sign(self.total_bonus_val) == -1:
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
            'nat_stat': self.base.get_total_bonus(),
            'prof': 0
        }
        self.bonus = self.contrib['nat_stat']

        self.have = False  # is this skill had by this charecter
        self.expertise = False
        self.prof = prof  #

    def update(self):
        self.contrib['nat_stat'] = self.base.get_total_bonus()

        if self.has_skill():
            if self.is_expert():  # if expertise, double profeciency
                self.contrib['prof'] = 2 * self.prof.get_total_base()
            else:
                self.contrib['prof'] = self.prof.get_total_base()
        else:
            self.contrib['prof'] = 0

        bonus = 0

        for name in list(self.contrib):
            bonus += self.contrib[name]

        self.bonus = bonus

    def alter_contrib(self, source, amount):
        self.contrib[source] = amount
        self.update()

    def remove(self, source):
        del self.contrib[source]
        self.update()

    def has_skill(self):
        '''
        :return: Does this charecter have this skill
        '''
        return self.have

    def is_expert(self):
        return self.expertise

    def give(self):
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
        return self.bonus

    def get_total_bonus_string(self):
        sign = sign_string(self.get_total_bonus())
        string = sign + str(self.get_total_bonus())
        return string


class TopStatValue:

    def __init__(self, label: str, is_number: bool):
        self.type = label
        self.is_number = is_number

        if is_number:
            self.value = 0
        else:
            self.value = ''

    def get_type(self):
        return self.type

    def get_value(self):
        return self.value

    def add(self, amount):
        if self.is_number:
            self.value += amount
        else:
            raise ValueError('This RPValue is not a number type')

    def subtract(self, amount):
        if self.is_number:
            self.value -= amount
        else:
            raise ValueError('This RPValue is not a number type')

    def set(self, new_value):
        self.value = new_value

    def __str__(self):
        return self.type + ': ' + str(self.value)


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

    def get_labels(self):
        return self.labels

    def get_type(self):
        return self.type

    def get_success_label(self):
        return self.labels[0]

    def get_failure_label(self):
        return self.labels[1]


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


class Encumbrance:

    def __init__(self,str_score:Stat):
        self.weight = 0
        self.enc_status = -1  # -1: unencumbered| 0: lvl0 encumbered| 1: lvl1 encumvered| 2: at/past max encumbered
        self.str_score = str_score
        self.enc_levels_multipliers = {
            'lvl0': 5,
            'lvl1': 10,
            'lvl2': 15  # max
        }
        self.enc_levels = self.calculate_encumberence_levels()

        self.encum_word_status_array = ["Unencumbered", "Encumbered","Heavily Encumbered", "Max Load"]
        self.encum_word_status = self.encum_word_status_array[self.enc_status + 1]

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
        return status, self.encum_word_status_array[status + 1]

    def set_weight(self,amount):
        if amount < 0:
            raise ValueError("Negative weight inputed")
        self.weight = amount
        self.update()

    def zeroWeight(self):
        self.weight = 0

    def add_weight(self,amount):
        self.weight += amount
        self.update()

    def subtract_weight(self,amount):
        if self.weight >= amount:
            self.weight -= amount
        else:
            raise ValueError("Subtracting more weight than currently present")
        self.update()

    def get_weight(self):
        return self.weight

    def get_encumberance_status(self):
        return self.enc_status

    def get_encumberance_word_status(self):
        return self.encum_word_status

    def get_encumberance_levels(self):
        return self.enc_levels


