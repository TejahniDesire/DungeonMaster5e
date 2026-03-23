from ..objectF import pyHelper
from . import charecterAttributes 

def getGeneralStatDict(input_diction):
    output_diction = {}
    for stat in input_diction.keys():

        name, diction= input_diction[stat].get_save_diction()
        output_diction[name] = diction
        
    return output_diction


# def getMidStatDict(mid_stat_top_diction,mid_stat_mid_diction):
#     output_diction = {}

#     for stat in ['ac','init','speed',]:

#         name, diction= input_diction[stat].get_save_diction()
#         output_diction[name] = diction

#     name, diction=mid_stat_top_diction['ac'].get_save_diction()
#     output_diction[name] = diction

def readMidStatsViewerDict(viewer_dict,input_diction,progress,frac_per_items,processEvents):

    i = 0
    for key in input_diction.keys():
        stat = input_diction[key]
        stat.set_viewer_dict(viewer_dict[i])

        progress.addProgress(frac_per_items)
        processEvents()
        i  += 1

    



def readSkillsViewerDict(viewer_dict,input_diction,progress,frac_per_items,processEvents):
    for i in range(len(viewer_dict.keys())):

        input_diction_key = charecterAttributes.skill_type_to_key[viewer_dict[i].getValue()]

        stat = input_diction[input_diction_key]
        stat.set_viewer_dict(viewer_dict[i])


        progress.addProgress(frac_per_items)
        processEvents()

def readGeneralStatViewerDict(viewer_dict,input_diction,section,progress,frac_per_items,processEvents):
        

        for i in range(len(viewer_dict.keys())):
        
            name = viewer_dict[i].getValue()
            substring = viewer_dict[i][0].getValue()
            props = substring.split('-*^*-')
            print(substring )
            if section == 'RP Top Stats':

                
                if props[0] == 'True':props[1] = int(props[1])

                input_diction_key = {
                    'Name':'name',
                    'Class':'class',
                    'Level': 'level',
                    'Background': 'background',
                    'Race': 'race',
                    'Alignment': 'alignment',
                    'Experience points':'experience'
                }[name]
                stat = input_diction[input_diction_key]
                stat.set(props[1])

            elif section == 'Person Stats':

                input_diction_key = {
                        'Personality Traits':'person',
                        'Ideals':'ideals',
                        'Bonds': 'bonds',
                        'Flaws': 'flaws',
                    }[name]
                stat = input_diction[input_diction_key]
                stat.set_text(props[0])
            
            


            progress.addProgress(frac_per_items)
            processEvents()
       

def readAbilityScoreDict(viewer_dict,input_diction,progress,frac_per_items,processEvents):
        for i in range(len(viewer_dict.keys())):
            input_diction_key = {
                'Strength': 'str',
                'Dexterity': 'dex',
                'Constitution': 'con',
                'Intelligence': 'int',
                'Wisdom': 'wis',
                'Charisma': 'chr',
                'Proficiency Bonus': 'prof'
                }[viewer_dict[i].getValue()]
            stat = input_diction[input_diction_key]
            stat.set_viewer_dict(viewer_dict[i])


            progress.addProgress(frac_per_items)
            processEvents()

    # i = 0
    # for key in input_diction:
        
    #     name = viewer_dict[i].getValue()
    #     substring = viewer_dict[i][0].getValue()
    #     props = substring.split('-*^*-')
    #     if bool(props[0]):props[1] = int(props[1])

    #     input_diction_key = {
    #         'Name':'name',
    #         'Class':'class',
    #         'Level': 'level',
    #         'Background': 'background',
    #         'Race': 'race',
    #         'Alignment': 'alignment',
    #         'Experience points':'experience'
    #     }[name]

    #     stat = input_diction[input_diction_key]
    #     stat.set(props[1])
