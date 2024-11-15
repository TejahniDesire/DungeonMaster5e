import customtkinter
import customtkinter as ctk
import math
import tkinter
import ruleTools
import objectsDnD
import charManagers


class CharacterSheet:

    def __init__(self):
        """"""

        """ Role play-------------------------------------------------------------------------------------"""
        # name, class, level, background, race, alignment, experience points
        self.top_stats = {
            'name': ruleTools.TopStatValue('Name', False),
            'class': ruleTools.TopStatValue('Class', False),
            'level': ruleTools.TopStatValue('Level', True),
            'background': ruleTools.TopStatValue('Background', False),
            'race': ruleTools.TopStatValue('Race', False),
            'alignment': ruleTools.TopStatValue('Alignment', False),
            'experience': ruleTools.TopStatValue('Experience points', True),
        }

        self.person = {
            'person': ruleTools.RPTraits('Personality Traits'),
            'ideals': ruleTools.RPTraits('Ideals'),
            'bonds': ruleTools.RPTraits('Bonds'),
            'flaws': ruleTools.RPTraits('Flaws')
        }

        """ Charecter Statistics-------------------------------------------------------------------------------------"""
        # Ability Score Counter
        self.AbS = {
            'str': ruleTools.Stat('Strength'),
            'dex': ruleTools.Stat('Dexterity'),
            'con': ruleTools.Stat('Constitution'),
            'int': ruleTools.Stat('Intelligence'),
            'wis': ruleTools.Stat('Wisdom'),
            'chr': ruleTools.Stat('Charisma'),
            'prof': ruleTools.Stat('Proficiency Bonus'),
            'insp': 0
        }

        # Skills_________________________________________________________
        self.saving_throws = {
            'str': ruleTools.Skill("Saving Throw", self.AbS['str'], self.AbS['prof']),
            'dex': ruleTools.Skill("Saving Throw", self.AbS['dex'], self.AbS['prof']),
            'con': ruleTools.Skill("Saving Throw", self.AbS['con'], self.AbS['prof']),
            'int': ruleTools.Skill("Saving Throw", self.AbS['int'], self.AbS['prof']),
            'wis': ruleTools.Skill("Saving Throw", self.AbS['wis'], self.AbS['prof']),
            'chr': ruleTools.Skill("Saving Throw", self.AbS['chr'], self.AbS['prof']),
        }

        self.all_skills = {
            'athletics': ruleTools.Skill('Athletics', self.AbS['str'], self.AbS['prof']),
            'acrobatics': ruleTools.Skill("Acrobatics", self.AbS['dex'], self.AbS['prof']),
            'sleight': ruleTools.Skill("Sleight of Hand", self.AbS['dex'], self.AbS['prof']),
            'stealth': ruleTools.Skill("Stealth", self.AbS['dex'], self.AbS['prof']),
            'arcana': ruleTools.Skill("Arcana", self.AbS['int'], self.AbS['prof']),
            'history': ruleTools.Skill("History", self.AbS['int'], self.AbS['prof']),
            'investigation': ruleTools.Skill("Investigation", self.AbS['int'], self.AbS['prof']),
            'nature': ruleTools.Skill("Nature", self.AbS['int'], self.AbS['prof']),
            'religion': ruleTools.Skill("Religion", self.AbS['int'], self.AbS['prof']),
            'animal': ruleTools.Skill("Animal Handling", self.AbS['wis'], self.AbS['prof']),
            'insight': ruleTools.Skill("Insight", self.AbS['wis'], self.AbS['prof']),
            'medicine': ruleTools.Skill("Medicine", self.AbS['wis'], self.AbS['prof']),
            'perception': ruleTools.Skill("Perception", self.AbS['wis'], self.AbS['prof']),
            'survival': ruleTools.Skill("Survival", self.AbS['wis'], self.AbS['prof']),
            'deception': ruleTools.Skill("Deception", self.AbS['chr'], self.AbS['prof']),
            'intimidation': ruleTools.Skill("Intimidation", self.AbS['chr'], self.AbS['prof']),
            'performance': ruleTools.Skill("Performance", self.AbS['chr'], self.AbS['prof']),
            'persuasian': ruleTools.Skill("Persuasian", self.AbS['chr'], self.AbS['prof'])
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
            'ac': ruleTools.Stat('Armor Class'),
            'init': ruleTools.Skill('Initiative', self.AbS['dex'], self.AbS['prof']),
            'speed': ruleTools.Stat('Speed'),
            'mhp': ruleTools.Stat('Hit Point Maximum'),
            'chp': ruleTools.Stat('Current Hit Points')
        }

        # __________________________________
        # Stats for the total middle of the sheet
        self.mid_stat_mid = {
            'hd': ruleTools.HitDice(),
            'death': ruleTools.DeathSavingThrows(),
        }

        """ Beyond Stats____________________________"""
        self.encumberance = ruleTools.Encumbrance(self.AbS['str'])
        self.inventory = charManagers.Inventory(self.encumberance)
        self.attack_inventory = charManagers.AttackInventory(self.inventory)

        # Stats for the right top of the screen

    def update(self):
        self.inventory.update()
        self.attack_inventory.update()

    def get_all_attributes(self):
        return self.AbS

    def get_specific_attribute(self, attribute:str):
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

    def get_specific_skill_of_attribute(self, attribute: str):
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

    def get_specific_skills(self, skill:str):
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

        :return: Top stats (name, class, etc.)
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

    def add_inventory(self,item:objectsDnD.Item,amount):
        self.inventory.add_item(item,amount)

    # Attributes______________________________

    def alter_attribute(self, attribute:str,source,new_base_value):
        self.AbS[attribute].alter_contrib_base(source,new_base_value)

    def alter_attribute_bonus(self, attribute:str,source,new_bonus_value):
        self.AbS[attribute].alter_contrib_bonus(source, new_bonus_value)

    def remove_attribute_contrib(self, attribute:str,source):
        self.AbS[attribute].remove_base(source)

    def remove_attribute_bonus(self, attribute:str,source):
        self.AbS[attribute].remove_bonus(source)

