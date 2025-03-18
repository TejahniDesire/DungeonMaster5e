
import sys
import pathlib

from ..objectF import itemsDnD, pyHelper
from . import charecterAttributes, inventory, charecterMechanics, time

class CharacterSheet:

    def __init__(self):
        """"""

        """ Role play-------------------------------------------------------------------------------------"""
        # name, class, level, background, race, alignment, experience points
        self.top_stats = {
            'name': charecterAttributes.TopStatValue('Name', False),
            'class': charecterAttributes.TopStatValue('Class', False),
            'level': charecterAttributes.TopStatValue('Level', True),
            'background': charecterAttributes.TopStatValue('Background', False),
            'race': charecterAttributes.TopStatValue('Race', False),
            'alignment': charecterAttributes.TopStatValue('Alignment', False),
            'experience': charecterAttributes.TopStatValue('Experience points', True),
        }

        self.person = {
            'person': charecterAttributes.RPTraits('Personality Traits'),
            'ideals': charecterAttributes.RPTraits('Ideals'),
            'bonds': charecterAttributes.RPTraits('Bonds'),
            'flaws': charecterAttributes.RPTraits('Flaws')
        }

        """ Charecter Statistics-------------------------------------------------------------------------------------"""
        # Ability Score Counter
        self.AbS = {
            'str': charecterAttributes.Stat('Strength'),
            'dex': charecterAttributes.Stat('Dexterity'),
            'con': charecterAttributes.Stat('Constitution'),
            'int': charecterAttributes.Stat('Intelligence'),
            'wis': charecterAttributes.Stat('Wisdom'),
            'chr': charecterAttributes.Stat('Charisma'),
            'prof': charecterAttributes.Stat('Proficiency Bonus'),
            'insp': 0
        }

        # Skills_________________________________________________________
        self.saving_throws = {
            'str': charecterAttributes.Skill("Saving Throw", self.AbS['str'], self.AbS['prof']),
            'dex': charecterAttributes.Skill("Saving Throw", self.AbS['dex'], self.AbS['prof']),
            'con': charecterAttributes.Skill("Saving Throw", self.AbS['con'], self.AbS['prof']),
            'int': charecterAttributes.Skill("Saving Throw", self.AbS['int'], self.AbS['prof']),
            'wis': charecterAttributes.Skill("Saving Throw", self.AbS['wis'], self.AbS['prof']),
            'chr': charecterAttributes.Skill("Saving Throw", self.AbS['chr'], self.AbS['prof']),
        }

        self.all_skills = {
            'athletics': charecterAttributes.Skill('Athletics', self.AbS['str'], self.AbS['prof']),
            'acrobatics': charecterAttributes.Skill("Acrobatics", self.AbS['dex'], self.AbS['prof']),
            'sleight': charecterAttributes.Skill("Sleight of Hand", self.AbS['dex'], self.AbS['prof']),
            'stealth': charecterAttributes.Skill("Stealth", self.AbS['dex'], self.AbS['prof']),
            'arcana': charecterAttributes.Skill("Arcana", self.AbS['int'], self.AbS['prof']),
            'history': charecterAttributes.Skill("History", self.AbS['int'], self.AbS['prof']),
            'investigation': charecterAttributes.Skill("Investigation", self.AbS['int'], self.AbS['prof']),
            'nature': charecterAttributes.Skill("Nature", self.AbS['int'], self.AbS['prof']),
            'religion': charecterAttributes.Skill("Religion", self.AbS['int'], self.AbS['prof']),
            'animal': charecterAttributes.Skill("Animal Handling", self.AbS['wis'], self.AbS['prof']),
            'insight': charecterAttributes.Skill("Insight", self.AbS['wis'], self.AbS['prof']),
            'medicine': charecterAttributes.Skill("Medicine", self.AbS['wis'], self.AbS['prof']),
            'perception': charecterAttributes.Skill("Perception", self.AbS['wis'], self.AbS['prof']),
            'survival': charecterAttributes.Skill("Survival", self.AbS['wis'], self.AbS['prof']),
            'deception': charecterAttributes.Skill("Deception", self.AbS['chr'], self.AbS['prof']),
            'intimidation': charecterAttributes.Skill("Intimidation", self.AbS['chr'], self.AbS['prof']),
            'performance': charecterAttributes.Skill("Performance", self.AbS['chr'], self.AbS['prof']),
            'persuasian': charecterAttributes.Skill("Persuasian", self.AbS['chr'], self.AbS['prof'])
        }

        # Specific skills__________
        con_skills = {
            'saving': self.saving_throws['con'],
        }

        str_skils = {
            'saving': self.saving_throws['str'],
            'athletics': self.all_skills['athletics']
        }

        dex_skills = {
            'saving': self.saving_throws['dex'],
            'acrobactics': self.all_skills['acrobatics'],
            'sleight': self.all_skills['sleight'],
            'stealth': self.all_skills['stealth']
        }

        int_skills = {
            'int': self.saving_throws['int'],
            'arcana': self.all_skills['arcana'],
            'history': self.all_skills['history'],
            'investigation': self.all_skills['investigation'],
            'nature': self.all_skills['nature'],
            'religion': self.all_skills['religion'],
        }

        wis_skills = {
            'wis': self.saving_throws['wis'],
            'animal': self.all_skills['animal'],
            'insight': self.all_skills['insight'],
            'medicine': self.all_skills['medicine'],
            'perception': self.all_skills['perception'],
            'survival': self.all_skills['survival'],
        }

        chr_skills = {
            'chr': self.saving_throws['chr'],
            'deception': self.all_skills['deception'],
            'intimidation': self.all_skills['intimidation'],
            'performance': self.all_skills['performance'],
            'persuasian': self.all_skills['persuasian'],
        }

        self.specific_skills = {
            'str': str_skils,
            'dex': dex_skills,
            'con': con_skills,
            'int': int_skills,
            'wis': wis_skills,
            'chr': chr_skills
        }

        """Stats for the middle top of the sheet___________________________"""
        self.mid_stat_top = {
            'ac': charecterAttributes.Stat('Armor Class'),
            'init': charecterAttributes.Skill('Initiative', self.AbS['dex'], self.AbS['prof']),
            'speed': charecterAttributes.Stat('Speed'),
            'mhp': charecterAttributes.Stat('Hit Point Maximum'),
            'chp': charecterAttributes.Stat('Current Hit Points')
        }

        # __________________________________
        # Stats for the total middle of the sheet
        self.mid_stat_mid = {
            'hd': charecterMechanics.HitDice(),
            'death': charecterMechanics.DeathSavingThrows(),
        }

        """ Beyond Stats____________________________"""
        self.encumberance = charecterMechanics.Encumbrance(self.AbS['str'])
        self.inventory = inventory.Inventory(self.encumberance)
        self.attack_inventory = inventory.AttackInventory(self.inventory)
        self.time = time.Time()

        # Stats for the right top of the screen

    def update(self):
        for key in list(self.AbS.keys()):
            if key == 'insp':
                continue
            self.AbS[key].update()

        for key in list(self.all_skills.keys()):
            self.all_skills[key].update()

        for key in list(self.saving_throws.keys()):
            self.saving_throws[key].update()

        self.inventory.update()
        self.attack_inventory.update()

        

    def get_all_attributes(self):
        return self.AbS

    def get_attribute(self, attribute:str):
        """
            'str': DT.Stat('Strength'),
            'dex': DT.Stat('Dexterity'),
            'con': DT.Stat('Constitution'),
            'int': DT.Stat('Intelligence'),
            'wis': DT.Stat('Wisdom'),
            'chr': DT.Stat('Charisma'),
            'prof': DT.Stat('Proficiency Bonus'),
            'insp': 0
        :param attribute:
        :return:
        """
        return self.AbS[attribute]

    def get_all_skills(self):
        return self.all_skills

    def get_skills_of_attribute(self, attribute: str):
        """
            'str': str_skils,
            'dex': dex_skills,
            'con': con_skills,
            'int': int_skills,
            'wis': wis_skills,
            'chr': chr_skills
        :param attribute:
        :return:
        """
        return self.specific_skills[attribute]

    def get_skill(self, skill:str):
        """
            'athletics': DT.Skill('Athletics', self.AbS['str'], self.AbS['prof']),
            'acrobatics': DT.Skill("Acrobatics",  self.AbS['dex'], self.AbS['prof']),
            'sleight': DT.Skill("Sleight of Hand",  self.AbS['dex'], self.AbS['prof']),
            'stealth': DT.Skill("Stealth",  self.AbS['dex'], self.AbS['prof']),
            'arcana': DT.Skill("Arcana",  self.AbS['int'], self.AbS['prof']),
            'history': DT.Skill("History",  self.AbS['int'], self.AbS['prof']),
            'investigation': DT.Skill("Investigation",  self.AbS['int'], self.AbS['prof']),
            'nature': DT.Skill("Nature",  self.AbS['int'], self.AbS['prof']),
            'religion': DT.Skill("Religion",  self.AbS['int'], self.AbS['prof']),
            'animal': DT.Skill("Animal Handling",  self.AbS['wis'], self.AbS['prof']),
            'insight': DT.Skill("Insight",  self.AbS['wis'], self.AbS['prof']),
            'medicine': DT.Skill("Medicine",  self.AbS['wis'], self.AbS['prof']),
            'perception': DT.Skill("Perception",  self.AbS['wis'], self.AbS['prof']),
            'survival': DT.Skill("Survival",  self.AbS['wis'], self.AbS['prof']),
            'deception': DT.Skill("Deception",  self.AbS['chr'], self.AbS['prof']),
            'intimidation': DT.Skill("Intimidation",  self.AbS['chr'], self.AbS['prof']),
            'performance': DT.Skill("Performance",  self.AbS['chr'], self.AbS['prof']),
            'persuasian': DT.Skill("Persuasian", self.AbS['chr'], self.AbS['prof'])
        :param skill:
        :return: one of above
        """
        return self.all_skills[skill]

    def get_all_top(self):
        '''

        :return: Top stats (name, class, level, background, Race, Aligment, Experience Points)
        '''
        return self.top_stats

    def get_specific_top(self, label:str):
        """
            'name': DT.RPValue('Name', False),
            'class': DT.RPValue('Class',False),
            'level': DT.RPValue('Level',True),
            'background': DT.RPValue('Background',False),
            'race': DT.RPValue('Race',False),
            'alignment': DT.RPValue('Alignment',False),
            'experience': DT.RPValue('Experience points',True),
        :param label:
        :return:
        """
        return self.top_stats[label]

    def get_all_mid_top(self):
        """
        Returns:
            _type_: Mid top stats (AC, initiative, speed, max hit points, current hit points)
        """
        return self.mid_stat_top 

    def get_specific_mid_top(self,label:str):
        """
        :return:
            'ac': DT.Stat('Armor Class'),
            'init': DT.Skill('Initiative', self.AbS['dex'], self.AbS['prof']),
            'speed': DT.Stat('Speed'),
            'mhp': DT.Stat('Hit Point Maximum'),
            'chp': DT.Stat('Current Hit Points')
        :param label: Query
        """
        return self.mid_stat_top[label]

    def get_all_mid_mid(self):
        """

        Returns:
            Hit dice, Death Saving throws
        """
        return self.mid_stat_mid

    def get_specific_mid_mid(self,label:str):
        """
            'hd': DT.HitDice(),
            'death': DT.DeathSavingThrows(),
        :param label: query
        :return: one of above
        """
        return self.mid_stat_mid[label]

    def get_all_rp_traits(self):
        return self.person

    def get_specific_rp_traits(self, query:str):
        return self.person[query]

    # Top Stats_____________________________________

    def get_name(self):
        return self.top_stats['name'].get_value()

    def get_class(self):
        return self.top_stats['class'].get_value()

    def get_level(self):
        return self.top_stats['level'].get_value()

    def get_background(self):
        return self.top_stats['background'].get_value()

    def get_race(self):
        return self.top_stats['race'].get_value()

    def get_alignment(self):
        return self.top_stats['alignment'].get_value()

    def get_experience(self):
        return self.top_stats['experience'].get_value()

    #  Inventory Function

    def get_inventory(self):
        return self.inventory

    def get_attack_inventory(self):
        return self.attack_inventory

    def add_inventory(self,item:itemsDnD.Item,amount):
        self.inventory.add_item(item,amount)

    # Attributes______________________________



    def get_attribute(self, attribute:str):
        return self.AbS[attribute]
    
    def alter_attribute(self, attribute:str,source,new_base_value:int,easy=False):
        self.AbS[attribute].alter_contrib_base(source,new_base_value,easy)

    def add_attribute_source(self,attribute:str,source,new_base_value:pyHelper.ReferenceNumber):
        self.AbS[attribute].add_base(source,new_base_value)

    def alter_attribute_bonus(self, attribute:str,source,new_bonus_value:int):
        self.AbS[attribute].alter_contrib_bonus(source, new_bonus_value)

    def add_attribute_bonus_source(self, attribute:str,source,new_bonus_value:pyHelper.ReferenceNumber,easy=False):
        self.AbS[attribute].add_bonus(source, new_bonus_value,easy)

    def remove_attribute_contrib(self, attribute:str,source):
        self.AbS[attribute].remove_base(source)

    def remove_attribute_bonus(self, attribute:str,source):
        self.AbS[attribute].remove_bonus(source)

    # Time

    def get_time(self):
        return self.time