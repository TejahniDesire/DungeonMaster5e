
import sys
import pathlib
from functools import partial
from datetime import datetime

from ..objectF import itemsDnD, pyHelper, dataBase
from ..metaF import directoryCrawler
from . import charecterAttributes, inventory, charecterMechanics, time, characterHelper



loadingSectionLabels = [
    None, 
    "Inventory", "Attack Inventory", "RP Stats", 
    "Person Stats", "Ability Score", "Skills", 
    "Mid Stats", "Hit Dice & Death Saves", "Time",
    "Complete"]
# savingSectionLabels = [None, "Inventory", "Attack Inventory", "RP Stats", "Person Stats", "Ability Score" , "Complete"]
num_of_sections = len(loadingSectionLabels ) - 2
frac_per_section = 1/num_of_sections
inventories = 'inventories/'
stats = 'stats/'
mechanics = 'mechanics/'

save_dirs_keys = [
    'main_inventory',
    'attack_inventory',
    'rp_top_stats',
    'person_stats',
    'ability_score_stats',
    'skill_stats',
    'mid_stats_top',
    'mid_stats_mid',
    'time'
    ]
save_dirs_titles = [
    'Main Inventory',
    'Attack Inventory',
    'RP Top Stats',
    'Person Stats',
    'Ability Score Stats',
    'Skills',
    "Mid Stats",
    "Mid Stats Mid",
    "Time"
    ]
save_dirs = [
    inventories + 'main_inventory.txt',
    inventories + 'attack_inventory.txt',
    stats + 'rp_top_stats.txt',
    stats + 'person_stats.txt',
    stats + 'ability_score_stats.txt',
    stats + 'skill_stats.txt',
    stats + 'mid_stats_top.txt',
    stats + 'mid_stats_mid.txt',
    mechanics + 'time.txt'
    ]


save_dirs_dict = {}
save_dirs_titles_dict = {}

for i in range(len(save_dirs_keys)):
    key = save_dirs_keys[i]
    save_dirs_dict[key] = save_dirs[i]
    save_dirs_titles_dict[key] = save_dirs_titles[i]


# save_dictionary = {
#     'main_inventory': inventories + 'main_inventory.txt',
#     'attack_inventory': inventories + 'attack_inventory.txt',
#     'rp_top_stats': stats + 'rp_top_stats.txt',
#     'person_stats': stats + 'person_stats.txt',
#     'ability_score_stats': stats + 'ability_score_stats.txt'
# }
# save_dictionary_titles = {
#     'main_inventory':     'Main Inventory',
#     'attack_inventory':   'Attack Inventory',
#     'rp_top_stats':       'RP Top Stats',
#     'person_stats':       'Person Stats',
#     'ability_score_stats':'Ability Score Stats'
# }
# Saving Notices

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
        # self.AbS = {
        #     'str': charecterAttributes.Stat(charecterAttributes.AbS_key_to_type['str']),
        #     'dex': charecterAttributes.Stat(charecterAttributes.AbS_key_to_type['dex']),
        #     'con': charecterAttributes.Stat(charecterAttributes.AbS_key_to_type['con']),
        #     'int': charecterAttributes.Stat(charecterAttributes.AbS_key_to_type['int']),
        #     'wis': charecterAttributes.Stat(charecterAttributes.AbS_key_to_type['wis']),
        #     'chr': charecterAttributes.Stat(charecterAttributes.AbS_key_to_type['chr']),
        #     'prof': charecterAttributes.Stat(charecterAttributes.AbS_key_to_type['prof']), # Use bases contrib only
        #     # 'insp': 0
        # }
        self.AbS = {}
        for key in charecterAttributes.AbS_key_to_type.keys():
            AbS_type = charecterAttributes.AbS_key_to_type[key]
            self.AbS[key] = charecterAttributes.Stat(AbS_type)

        self.insperation = pyHelper.ReferenceNumber(0,True)

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
            'persuasian': charecterAttributes.Skill("Persuasian", self.AbS['chr'], self.AbS['prof']),
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
            'speed': charecterAttributes.ConsumableStat('Speed'),
            'hp': charecterAttributes.ConsumableStat('Hit Points'),
            # 'chp': charecterAttributes.Stat('Current Hit Points')
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

        # Meta
        self.data_base = dataBase.DataBasePage()
        

    def update(self):
        for key in list(self.AbS.keys()):
            # if key == 'insp':
            #     continue
            self.AbS[key].update()

        for key in list(self.all_skills.keys()):
            self.all_skills[key].update()

        for key in list(self.saving_throws.keys()):
            self.saving_throws[key].update()

        self.inventory.update()
        self.attack_inventory.update()

    def save(self,path:str,progress,processEvents,save_name=None):
        save_delin = '(138055)'
        if path[-1] != '/':
            path += '/'

        path_to_dir = path + self.get_name() + '/'
        directoryCrawler.createSubDirectory(path_to_dir,kill_policy=False)
        

        save_file_name = "{}_save".format(self.get_name()) + save_delin +  datetime.now().strftime("%m_%d_%y_%H_%M_%S_%f") + '/'
        save_dir =path_to_dir  + save_file_name 
        directoryCrawler.createSubDirectory(save_dir,kill_policy=True)
# save_dictionary = {
#     'main_inventory': inventories + 'main_inventory.txt',
#     'attack_inventory': inventories + 'attack_inventory.txt',
#     'rp_top_stats': stats + 'rp_top_stats.txt',
#     'person_stats': stats + 'person_stats.txt',
#     'ability_score_stats': stats + 'ability_score_stats.txt'
# }


        save_dirs_funct_dict = {
            'main_inventory': partial(self.inventory.getItemDictionary),
            'attack_inventory': partial(self.attack_inventory.getItemDictionary),
            'rp_top_stats': partial(characterHelper.getGeneralStatDict,self.top_stats),
            'person_stats': partial(characterHelper.getGeneralStatDict,self.person),
            'ability_score_stats': partial(characterHelper.getGeneralStatDict,self.AbS),
            'skill_stats': partial(characterHelper.getGeneralStatDict,self.all_skills),
            'mid_stats_top': partial(characterHelper.getGeneralStatDict,self.mid_stat_top),
            'mid_stats_mid': partial(characterHelper.getGeneralStatDict,self.mid_stat_mid),
            'time':partial(self.time.get_save_diction)
        }

        for key in save_dirs_keys:
            directory = save_dir + save_dirs_dict[key]
            funct = save_dirs_funct_dict[key]
            title = save_dirs_titles_dict[key] 
            # print(funct())
            self.data_base.AddPage(funct(),title,directory,replace_old=True)
            self.data_base.writePage(title=title)    
            progress.addProgress(frac_per_section)
            processEvents()
               
               
               
        progress.completeProgress()
        processEvents()


        # Inventory Protocal____________________________________________________________________________________________________
        # inventory_file_dir = save_dir + save_dictionary['main_inventory']
        # self.data_base.AddPage(self.inventory.getItemDictionary(),'Main Inventory',inventory_file_dir,replace_old=True)
        # self.data_base.writePage(title='Main Inventory')        
        # # Attack Inventory Protocal_____________________________________________________________________________________________
        # inventory_file_dir = save_dir + save_dictionary['attack_inventory']
        # self.data_base.AddPage(self.attack_inventory.getItemDictionary(),'Attack Inventory',inventory_file_dir,replace_old=True)
        # self.data_base.writePage(title='Attack Inventory')     
        # # Top RP Stats Protocal_________________________________________________________________________________________________
        # rp_top_stats_dir = save_dir + save_dictionary['rp_top_stats']
        # self.data_base.AddPage(characterHelper.getGeneralStatDict(self.top_stats), 'RP Top Stats',rp_top_stats_dir,replace_old=True)
        # self.data_base.writePage(title='RP Top Stats')   

        # # Person Stats Protocal_________________________________________________________________________________________________
        # person_stats_dir = save_dir + save_dictionary['person_stats']
        # self.data_base.AddPage(characterHelper.getGeneralStatDict(self.person), 'Person Stats',person_stats_dir,replace_old=True)
        # self.data_base.writePage(title='Person Stats')   

        # Ability Score Stats 


    def load(self,save_dir,progress:pyHelper.ProgressMarker,processEvents):
        if save_dir[-1] != '/':
            save_dir += '/'

        
        # Inventory____________________________________________________________
        inventory_file_dir = save_dir + save_dirs_dict['main_inventory']

        self.data_base.readPage(inventory_file_dir)        
        items = itemsDnD.loadItemViewerDicts(self.data_base.getPage(save_dirs_titles_dict['main_inventory']))
        frac_per_items = (1 / len(items)) * frac_per_section
        for item in items:
            self.inventory.add_item(item=item)
            progress.addProgress(frac_per_items)
            processEvents()

        # Attack Inventory____________________________________________________________
        inventory_file_dir = save_dir + save_dirs_dict['attack_inventory']
        self.data_base.readPage(inventory_file_dir)   
        items = itemsDnD.loadItemViewerDicts(self.data_base.getPage(save_dirs_titles_dict['attack_inventory']))
        frac_per_items = (1 / len(items)) * frac_per_section
        for item in items:
            self.attack_inventory.add_attack_item(item=item)
            progress.addProgress(frac_per_items)
            processEvents()

        # Top RP Stats Protocal_________________________________________________________________________________________________
        rp_top_stats_dir = save_dir + save_dirs_dict['rp_top_stats']
        self.data_base.readPage(rp_top_stats_dir)  
        viewer_dict = self.data_base.getPage(save_dirs_titles_dict['rp_top_stats'])

        frac_per_items = (1 / len(viewer_dict.keys())) * frac_per_section
        
        characterHelper.readGeneralStatViewerDict(viewer_dict,self.top_stats,save_dirs_titles_dict['rp_top_stats'],progress,frac_per_items,processEvents)

        # Person Stats Protocal_________________________________________________________________________________________________
        key = 'person_stats'
        person_stats_dir = save_dir + save_dirs_dict[key ]
        self.data_base.readPage(person_stats_dir)  
        viewer_dict = self.data_base.getPage(save_dirs_titles_dict[key ])

        frac_per_items = (1 / len(viewer_dict.keys())) * frac_per_section
        characterHelper.readGeneralStatViewerDict(viewer_dict,self.person,save_dirs_titles_dict[key ],progress,frac_per_items,processEvents)

        # Ability Score Protocal_________________________________________________________________________________________________
        key = 'ability_score_stats'
        ability_score_stats_dir = save_dir + save_dirs_dict[key]
        self.data_base.readPage(ability_score_stats_dir) 
        viewer_dict = self.data_base.getPage(save_dirs_titles_dict[key])

        frac_per_items = (1 / len(viewer_dict.keys())) * frac_per_section
        characterHelper.readAbilityScoreDict(viewer_dict,self.AbS,progress,frac_per_items,processEvents)

        # skill Protocal_________________________________________________________________________________________________
        key = 'skill_stats'
        ability_score_stats_dir = save_dir + save_dirs_dict[key]
        self.data_base.readPage(ability_score_stats_dir) 
        viewer_dict = self.data_base.getPage(save_dirs_titles_dict[key])

        frac_per_items = (1 / len(viewer_dict.keys())) * frac_per_section
        characterHelper.readSkillsViewerDict(viewer_dict,self.all_skills,progress,frac_per_items,processEvents)

        # Mid Stats Top Protocal_________________________________________________________________________________________________
        key = 'mid_stats_top'
        ability_score_stats_dir = save_dir + save_dirs_dict[key]
        self.data_base.readPage(ability_score_stats_dir) 
        viewer_dict = self.data_base.getPage(save_dirs_titles_dict[key])

        frac_per_items = (1 / len(viewer_dict.keys())) * frac_per_section
        characterHelper.readMidStatsViewerDict(viewer_dict,self.mid_stat_top,progress,frac_per_items,processEvents)

        # Mid Stats Mid Protocal_________________________________________________________________________________________________
        key = 'mid_stats_mid'
        ability_score_stats_dir = save_dir + save_dirs_dict[key]
        self.data_base.readPage(ability_score_stats_dir) 
        viewer_dict = self.data_base.getPage(save_dirs_titles_dict[key])

        frac_per_items = (1 / len(viewer_dict.keys())) * frac_per_section
        characterHelper.readMidStatsViewerDict(viewer_dict,self.mid_stat_mid,progress,frac_per_items,processEvents)

        # Time Protocal_________________________________________________________________________________________________
        key = 'time'
        ability_score_stats_dir = save_dir + save_dirs_dict[key]
        self.data_base.readPage(ability_score_stats_dir) 
        viewer_dict = self.data_base.getPage(save_dirs_titles_dict[key])

        self.time.set_viewer_dict(viewer_dict)
        progress.addProgress(frac_per_section)
        processEvents()
        

        # for i in range(len(viewer_dict.keys())):
            
        #     name = viewer_dict[i].getValue()
        #     substring = viewer_dict[i][0].getValue()
        #     props = substring.split('-*^*-')
        #     print(substring )
        #     if props[0] == 'True':props[1] = int(props[1])

            

        #     input_diction_key = {
        #         'Name':'name',
        #         'Class':'class',
        #         'Level': 'level',
        #         'Background': 'background',
        #         'Race': 'race',
        #         'Alignment': 'alignment',
        #         'Experience points':'experience'
        #     }[name]

        #     stat = self.top_stats[input_diction_key]

        #     if props[0] == 'True':
        #         print("SETTING A NUMBER")
        #     stat.set(props[1])

        #     progress.addProgress(frac_per_items)
        #     processEvents()



        print("PROGRESS: ", progress)
        progress.completeProgress()
        processEvents()
        
        

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
    
    def get_skills_of_attribute_keys(self, attribute: str):
        return self.specific_skills[attribute].keys()

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
    
    def get_all_saving_throws(self):
        return self.saving_throws

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

    def alter_attribute_bonus(self, attribute:str,source,new_bonus_value:int,easy=False):
        self.AbS[attribute].alter_contrib_bonus(source, new_bonus_value,easy)

    def add_attribute_bonus_source(self, attribute:str,source,new_bonus_value:pyHelper.ReferenceNumber):
        self.AbS[attribute].add_bonus(source, new_bonus_value)

    def remove_attribute_contrib(self, attribute:str,source):
        self.AbS[attribute].remove_base(source)

    def remove_attribute_bonus(self, attribute:str,source):
        self.AbS[attribute].remove_bonus(source)

    # Time

    def get_time(self):
        return self.time
    


    # ACTIONS
    def walk(self,amount:int):
        speed = self.get_specific_mid_top('speed')


    