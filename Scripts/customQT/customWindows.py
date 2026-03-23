# Global_________________________________________________________________ i
import subprocess
import sys
from functools import partial
import math
import re
import numpy as np
# PyQT_________________________________________________________________ 
from PyQt5.QtWidgets import (
    QApplication,
    QStackedLayout,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QScrollArea, 
    QFrame, 
    QCheckBox,
    QSizePolicy,
    QTextEdit,
    QLineEdit,
    QCheckBox,
    QGraphicsOpacityEffect, 
    QSpinBox,
    QComboBox,
    QFontComboBox
)

from PyQt5.QtGui import (
    QPalette, QColor, QFont, QIcon
)

from PyQt5 import (
    QtCore, Qt
)

from PyQt5.QtCore import (
    QSize, QObject, pyqtSignal
)

from PyQt5.sip import delete


from . import (style, QTHelper)

from ..charecterF import (charecter, charecterMechanics, charecterAttributes, inventory)
from ..objectF import pyHelper, itemsDnD,objectsDnd
from ..metaF import imageURLS



class NameWindow(QWidget):

    def __init__(self, name, update):
        super().__init__()
        mainLayout = QVBoxLayout()
        self.name_function = name
        self.update_function = update
        self.setWindowTitle('Name Your Charecter')
        self.setMinimumSize(300,100)
        self.setLayout(mainLayout)
        self.name_edit = QLineEdit()

        self.name_edit.editingFinished.connect(self.name_change)

        mainLayout.addWidget(self.name_edit)
        #
        # name_edit.textChanged.connect(self.tp['name'].set)

    def name_change(self):
        self.name_function(self.name_edit.text())
        self.update_function()
        self.close()


class AlignmentWindow(QWidget):

    def __init__(self, alignment, update):
        super().__init__()
        mainLayout = QGridLayout()
        self.alignment_function = alignment
        self.update_function = update
        self.setWindowTitle('Choose Your Charecters Alignment')
        self.setMinimumSize(300,300)
        self.setLayout(mainLayout)
        self.alignment_labels = [
            ["Lawful Good","Lawful Neutral","Lawful Evil"],
            ["Neutral Good","True Neutral","Neutral Evil"],
            ["Chaotic Good","Chaotic Neutral","Chaotic Evil"]
        ]
        self.buttons = []
        for i in range(3):
            this_row = []
            for j in range(3):
                this_row += [QPushButton()]
                this_row[j].setText(self.alignment_labels[i][j])
                this_row[j].setStyleSheet(style.TabButtonSheet2)
                mainLayout.addWidget(this_row[j], i, j)
                this_row[j].clicked.connect(partial(self.alignment_change,(i,j)))
            self.buttons += this_row

    def alignment_change(self,label_coords:tuple):
        new_alignment = self.alignment_labels[label_coords[0]][label_coords[1]]
        self.alignment_function(new_alignment)
        self.update_function()
        self.close()

class AttributeWindow(QWidget):
    def __init__(self, attribute:charecterAttributes.Stat,close_function):
        super().__init__()

        self.attribute = attribute
        mainLayout = QVBoxLayout()
        self.setWindowTitle(attribute.type + " Ability Score")
        
        # text_str = str(self.attribute)
        self.setLayout(mainLayout)
        mainLayout.addWidget(self.getTextLayout())
        self.setMinimumWidth(300)
        self.setMaximumWidth(400)
        self.close_function = close_function

    def closeEvent(self,event):
        super().closeEvent(event)
        self.close_function()

    def getTextLayout(self):
        mainWidget = QWidget()
        layout = QGridLayout()

        mainWidget.setLayout(layout)
        mainWidget.setStyleSheet(style.GreyQWidget)
        layout.addWidget(QTHelper.CreateLabel("Score",font=style.LabelFont1,style_sheet=style.GreyLabel),0,0)
        layout.addWidget(QTHelper.CreateLabel("Bonus",font=style.LabelFont1,style_sheet=style.GreyLabel),0,1)

        pure_frame = QFrame()
        pure_frame.setFrameShape(QFrame.Panel)
        pure_layout = QGridLayout()
        pure_frame.setLayout(pure_layout)
        base_names = list(self.attribute.get_all_bases())
        base_values = np.array(list(self.attribute.get_all_bases().values()))
        for i in range(len(base_names)):


            name = pyHelper.key_to_name(base_names[i])
            value = str(base_values[i])

            name_label = QTHelper.CreateLabel(name,font=style.LabelFont2p5,style_sheet=style.DarkGreyLabel)
            value_label = QTHelper.CreateLabel(value,font=style.LabelFont2p5,style_sheet=style.DarkGreyLabel)

            name_label.setMaximumWidth(100)
            name_label.setMaximumHeight(15)
            value_label.setMaximumWidth(30)
            value_label.setMaximumHeight(15)

            pure_layout.addWidget(name_label,i,0)
            pure_layout.addWidget(value_label,i,1)


        name_label = QTHelper.CreateLabel("Total",font=style.LabelFont2p5,style_sheet=style.DarkGreyLabel)
        value_label = QTHelper.CreateLabel(str(self.attribute.get_total_base()),font=style.LabelFont2p5,style_sheet=style.DarkGreyLabel)

        name_label.setMaximumWidth(100)
        name_label.setMaximumHeight(15)
        value_label.setMaximumWidth(30)
        value_label.setMaximumHeight(15)

        pure_layout.addWidget(name_label,len(base_names)+1,0)
        pure_layout.addWidget(value_label,len(base_names)+1,1)


        layout.addWidget(pure_frame,1,0)

        bonus_frame =QFrame()
        bonus_frame.setFrameShape(QFrame.Panel)
        bonus_layout = QGridLayout()
        bonus_frame.setLayout(bonus_layout)
        bonus_names = list(self.attribute.get_all_bonuses())
        bonus_values = np.array(list(self.attribute.get_all_bonuses().values()))
        for i in range(len(bonus_names)):


            name = pyHelper.key_to_name(bonus_names[i])
            value = pyHelper.sign_string(bonus_values[i].getValue(),show_negative=False) + str(bonus_values[i])


            name_label = QTHelper.CreateLabel(name,font=style.LabelFont2p5,style_sheet=style.DarkGreyLabel)
            value_label = QTHelper.CreateLabel(value,font=style.LabelFont2p5,style_sheet=style.DarkGreyLabel)

            name_label.setMaximumWidth(100)
            name_label.setMaximumHeight(15)
            value_label.setMaximumWidth(100)
            value_label.setMaximumHeight(15)

            bonus_layout.addWidget(name_label,i,0)
            bonus_layout.addWidget(value_label,i,1)
            

        name_label = QTHelper.CreateLabel("Total",font=style.LabelFont2p5,style_sheet=style.DarkGreyLabel)
        value_label = QTHelper.CreateLabel(pyHelper.sign_string(self.attribute.get_total_bonus()) + str(self.attribute.get_total_bonus()),font=style.LabelFont2p5,style_sheet=style.DarkGreyLabel)

        name_label.setMaximumWidth(100)
        name_label.setMaximumHeight(15)
        value_label.setMaximumWidth(100)
        value_label.setMaximumHeight(15)

        bonus_layout.addWidget(name_label,len(bonus_names)+1,0)
        bonus_layout.addWidget(value_label,len(bonus_names)+1,1)

        layout.addWidget(bonus_frame,1,1)

        return mainWidget

class SkillWindow(QWidget):

    def __init__(self, skill:charecterAttributes.Skill,close_function):
        super().__init__()

        self.skill = skill
        mainLayout = QVBoxLayout()
        self.setWindowTitle(skill.name + " Skill")

        self.setLayout(mainLayout)
        mainLayout.addWidget(self.getTextLayout())
        self.setMinimumWidth(300)
        self.setMaximumWidth(400)
        self.close_function = close_function

    def closeEvent(self,event):
        super().closeEvent(event)
        self.close_function()
    
    def getTextLayout(self):
        mainWidget = QWidget()
        layout = QVBoxLayout()

        mainWidget.setLayout(layout)
        mainWidget.setStyleSheet(style.GreyQWidget)
        # layout.addWidget(QTHelper.CreateLabel("Score",font=style.LabelFont1,style_sheet=style.GreyLabel),0,0)
        layout.addWidget(QTHelper.CreateLabel("Bonus",font=style.LabelFont1,style_sheet=style.GreyLabel))


        pure_frame = QFrame()
        pure_frame.setFrameShape(QFrame.Panel)
        pure_layout = QGridLayout()
        pure_frame.setLayout(pure_layout)
        bonus_names = list(self.skill.contrib.keys())
        bonus_values = np.array(list(self.skill.contrib.values()))


        for i in range(len(bonus_names)):

            if bonus_values[i] == 0: continue
            name = pyHelper.key_to_name(bonus_names[i])
            value = pyHelper.sign_string(bonus_values[i],show_negative=False) + str(bonus_values[i])

            

            name_label = QTHelper.CreateLabel(name,font=style.LabelFont2p5,style_sheet=style.DarkGreyLabel)
            value_label = QTHelper.CreateLabel(value,font=style.LabelFont2p5,style_sheet=style.DarkGreyLabel)

            name_label.setMaximumWidth(100)
            name_label.setMaximumHeight(15)
            value_label.setMaximumWidth(100)
            value_label.setMaximumHeight(15)

            pure_layout.addWidget(name_label,i,0)
            pure_layout.addWidget(value_label,i,1)


        name_label = QTHelper.CreateLabel("Total",font=style.LabelFont2p5,style_sheet=style.DarkGreyLabel)
        value_label = QTHelper.CreateLabel(pyHelper.sign_string(self.skill.get_total_bonus(),show_negative=False) + str(self.skill.get_total_bonus()),font=style.LabelFont2p5,style_sheet=style.DarkGreyLabel)

        name_label.setMaximumWidth(100)
        name_label.setMaximumHeight(15)
        value_label.setMaximumWidth(100)
        value_label.setMaximumHeight(15)

        pure_layout.addWidget(name_label,len(bonus_names)+1,0)
        pure_layout.addWidget(value_label,len(bonus_names)+1,1)
        
        layout.addWidget(pure_frame)


        return mainWidget

class MidStatWindow(QWidget):

    def __init__(self, name, contrib:list[pyHelper.ReferenceNumber],total:pyHelper.ReferenceNumber ,close_function):
        super().__init__()


        self.contrib = contrib
        self.total = total
        mainLayout = QVBoxLayout()
        self.setWindowTitle(name)
        
        self.setLayout(mainLayout)
        mainLayout.addWidget(self.getTextLayout())
        self.setMinimumWidth(300)
        self.setMaximumWidth(400)
        self.close_function = close_function

    def closeEvent(self,event):
        super().closeEvent(event)
        self.close_function()

    def getTextLayout(self):

        mainWidget = QWidget()
        layout = QVBoxLayout()

        mainWidget.setLayout(layout)
        mainWidget.setStyleSheet(style.GreyQWidget)
        # layout.addWidget(QTHelper.CreateLabel("Score",font=style.LabelFont1,style_sheet=style.GreyLabel),0,0)
        layout.addWidget(QTHelper.CreateLabel("Contributions",font=style.LabelFont1,style_sheet=style.GreyLabel))


        pure_frame = QFrame()
        pure_frame.setFrameShape(QFrame.Panel)
        pure_layout = QGridLayout()
        pure_frame.setLayout(pure_layout)
        bonus_names = list(self.contrib.keys())
        bonus_values = np.array(list(self.contrib.values()))


        for i in range(len(bonus_names)):

            if bonus_values[i] == 0: continue
            name = pyHelper.key_to_name(bonus_names[i])
            value = pyHelper.sign_string(bonus_values[i],show_negative=False) + str(bonus_values[i])

            

            name_label = QTHelper.CreateLabel(name,font=style.LabelFont2p5,style_sheet=style.DarkGreyLabel)
            value_label = QTHelper.CreateLabel(value,font=style.LabelFont2p5,style_sheet=style.DarkGreyLabel)

            name_label.setMaximumWidth(100)
            name_label.setMaximumHeight(15)
            value_label.setMaximumWidth(100)
            value_label.setMaximumHeight(15)

            pure_layout.addWidget(name_label,i,0)
            pure_layout.addWidget(value_label,i,1)


        name_label = QTHelper.CreateLabel("Total",font=style.LabelFont2p5,style_sheet=style.DarkGreyLabel)
        value_label = QTHelper.CreateLabel(str(self.total),font=style.LabelFont2p5,style_sheet=style.DarkGreyLabel)

        name_label.setMaximumWidth(100)
        name_label.setMaximumHeight(15)
        value_label.setMaximumWidth(100)
        value_label.setMaximumHeight(15)

        pure_layout.addWidget(name_label,len(bonus_names)+1,0)
        pure_layout.addWidget(value_label,len(bonus_names)+1,1)
        
        layout.addWidget(pure_frame)


        return mainWidget

class AddWindow(QWidget):
    '''
    window for adding items to inventory
    '''

    def __init__(self,tinventory:inventory.Inventory,ATinventory:inventory.AttackInventory,update_func):
        super().__init__()
        self.setWindowTitle('Select Weapon to Add')
        self.update_func = update_func
        self.tinventory = tinventory
        self.ATinventory = ATinventory
        self.search_items = self.tinventory.get_all_items()

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.stacked_proper = QStackedLayout()
        self.stacked_proper.setAlignment(QtCore.Qt.AlignTop)
        self.search_layout = QHBoxLayout()

        self.mainLayout.addLayout(self.search_layout)
        self.mainLayout.addLayout(self.stacked_proper)
        self.makeStackedLayout()
        self.makeSearchBar()

    def update(self):
        super().update()
        QTHelper.deleteItemsOfLayout(self.stacked_proper)

        self.stacked_proper = QStackedLayout()
        self.stacked_proper.setAlignment(QtCore.Qt.AlignTop)
        self.mainLayout.addLayout(self.stacked_proper)

        self.search_items = self.tinventory.get_items(self.searchbar.text())
        self.makeStackedLayout()

    def makeStackedLayout(self):
        items = self.search_items

        # held_items = self.ATinventory.get_all_items()

        num_of_items = len(items)
        num_per_column = 6
        num_of_pages = int(np.ceil(num_of_items / (num_per_column * 2)))

        j = 0
        for i in range(num_of_pages):
            # Each page list items in range -> [i*16,i*16 + 16)

            current_page_widget = QWidget()
            current_page_outer0_layout = QVBoxLayout()

            book_layout = QHBoxLayout()
            current_page_left_layout = QGridLayout()
            current_page_right_layout = QGridLayout()
            current_page_button_layout = QHBoxLayout()

            current_page_widget.setLayout(current_page_outer0_layout)
            current_page_outer0_layout.addLayout(book_layout)
            current_page_outer0_layout.addLayout(current_page_button_layout)
            book_layout.addLayout(current_page_left_layout)
            book_layout.addLayout(current_page_right_layout)

            for k in range(num_per_column):
                if j < num_of_items:
                    current_page_left_layout.addWidget(QTHelper.ShopItemLabel(items[j],self.ATinventory,self.update_func), k, 0)
                    j += 1

            for k in range(num_per_column):
                if j < num_of_items:
                    current_page_right_layout.addWidget(QTHelper.ShopItemLabel(items[j],self.ATinventory,self.update_func), k, 0)
                    j += 1

            if i > 0:
                left_button = QTHelper.CreateTabButton(self.switch_tab, i - 1, style.LabelFont2, style.TabButtonSheet1, "<-")
                current_page_button_layout.addWidget(left_button,alignment=QtCore.Qt.AlignBottom)

            if i < num_of_pages - 1:
                right_button = QTHelper.CreateTabButton(self.switch_tab, i + 1, style.LabelFont2, style.TabButtonSheet1, "->")
                current_page_button_layout.addWidget(right_button,alignment=QtCore.Qt.AlignBottom)

            # current_page_outer0_layout.setAlignment(QtCore.Qt.AlignTop)
            # current_page_outer1_layout.setAlignment(QtCore.Qt.AlignTop)
            self.stacked_proper.addWidget(current_page_widget)

    def switch_tab(self, index: int):
        self.stacked_proper.setCurrentIndex(index)

    def makeSearchBar(self):
        self.searchbar = QLineEdit()
        self.searchbar.setMaximumWidth(400)
        self.searchbar.textChanged.connect(self.update)

        cancel_search = QTHelper.CreateGenButton(
            stylesheet=style.ItemEditButton,
            icon_url=imageURLS.XUrl,
            icon_size=QtCore.QSize(20, 20),
            function_list=[partial(self.searchbar.setText,''),self.update]
        )

        filter_button = QTHelper.CreateGenButton("Filters",style.LabelFont2,style.TabButtonSheet2,
                                                       partial(self.createFilterWidget))

        self.search_layout.addWidget(self.searchbar)
        self.search_layout.addWidget(cancel_search)
        self.search_layout.addWidget(filter_button)

    def change_order(self,order:str,checkboxes):
        self.tinventory.set_sorting(order)
        for key in checkboxes:
            if key != order:
                checkboxes[key].setChecked(False)
            else:
                print(key)
        self.update()

    def reverse_order(self):
        self.tinventory.reversal()
        self.update()

    def createFilterWidget(self):
        self.filter_widget = QWidget()
        self.filter_widget.setMinimumWidth(150)
        self.filter_widget.setMinimumHeight(250)
        self.filter_widget.setMaximumWidth(150)
        self.filter_widget.setMaximumHeight(250)
        filter_layout = QVBoxLayout(self.filter_widget)

        sorting_button_style = style.TabButtonSheet2
        alpha = QTHelper.CreateGenButton("Alphabetical",style.LabelFont2,sorting_button_style,checkbox=True)
        weight = QTHelper.CreateGenButton("Weight", style.LabelFont2,sorting_button_style,checkbox=True)
        typet = QTHelper.CreateGenButton("Category", style.LabelFont2,sorting_button_style,checkbox=True)
        cost = QTHelper.CreateGenButton("Cost", style.LabelFont2,sorting_button_style,checkbox=True)
        amount = QTHelper.CreateGenButton("Amount", style.LabelFont2,sorting_button_style,checkbox=True)
        reversal = QTHelper.CreateGenButton("Reverse", style.LabelFont2,
                                                  sorting_button_style,partial(self.reverse_order),checkbox=True)

        checkboxes = {
            "name":alpha,
            "weight":weight,
            "type":typet,
            "cost":cost,
            "amount":amount,
        }

        for key in checkboxes:
            QTHelper.ConnectButtonCLicked(checkboxes[key], partial(self.change_order,key,checkboxes))

        filter_layout.addWidget(alpha)
        filter_layout.addWidget(typet)
        filter_layout.addWidget(amount)
        filter_layout.addWidget(cost)
        filter_layout.addWidget(weight)
        filter_layout.addWidget(reversal)

        self.filter_widget.setWindowTitle('Filter')

        self.filter_widget.show()

class DiceWindow(QFrame):

    def __init__(self,tchar_all_attributes_func,tchar_all_skills_func,tchar_all_saving_func,suggested_attribute=None,suggested_skill=None,tittle=None,dice_amount=1,dice_type=20):
        super().__init__()

    
        self.setFrameShape(QFrame.WinPanel)
        self.attributes_func = tchar_all_attributes_func
        self.skills_func = tchar_all_skills_func
        self.saving_throws_func = tchar_all_saving_func
        self.selected_attribute = suggested_attribute
        self.selected_skill = suggested_skill
        self.mixed_checks = False
        self.advantage_level = pyHelper.ReferenceNumber(0,True)
        self.diceRoll = DiceRoll(self.advantage_level,dice_amount=dice_amount,dice_type=dice_type)
        self.bonusWidget = self.diceRoll.getBonusWidget()
        

        self.dis_adv_buttons =None
        if tittle is None: tittle = "Roll of the dice..."
        self.setWindowTitle(tittle)
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        
        mainLayout.addWidget(self.getTextLayout())
        self.setMinimumWidth(500)
        self.setMaximumWidth(900)
        
        # self.close_function = close_function

    def getTextLayout(self):
        mainWidget = QFrame()
        mainWidget.setFrameShape(QFrame.Panel)
        mainLayout = QVBoxLayout()

        mainWidget.setLayout(mainLayout)
        # mainWidget.setStyleSheet(style.GreyQWidget)
        # Top: ability/skll and advantage/disadvantage-------------------------------------------------
        top_frame = QFrame()
        top_frame.setFrameShape(QFrame.Panel)
        top_layout = QHBoxLayout()
        top_frame.setLayout(top_layout)

        att_skill_widget=QFrame()
        att_skill_widget.setFrameShape(QFrame.WinPanel)
        att_skill_layout = QGridLayout()
        att_skill_widget.setLayout(att_skill_layout)

        att_skill_layout.addWidget(QTHelper.CreateLabel("Ability:",font=style.LabelFont2p5,style_sheet=style.DarkGreyLabel),0,0,alignment=QtCore.Qt.AlignRight)
        att_skill_layout.addWidget(QTHelper.CreateLabel("Skill:",font=style.LabelFont2p5,style_sheet=style.DarkGreyLabel),1,0,alignment=QtCore.Qt.AlignRight)
        

        
        self.skill_comboBox = QComboBox()
        self.skill_comboBox.setFont(style.LabelFont2)
        self.all_skills = ['None'] + list(charecterAttributes.skill_type_to_key.keys())
        for key in charecterAttributes.AbS_type_to_key.keys():
            self.all_skills += [key + ' ' + 'Saving Throw']
        self.all_skills.pop()
        self.skill_comboBox.addItems(self.all_skills)


        if self.selected_skill is not None:
            if self.selected_skill.get_type() == 'Saving Throw':
                skill_label = self.selected_skill.base.get_type() + ' ' +  self.selected_skill.get_type()
                
                if self.selected_attribute is None:
                    self.selected_attribute = self.selected_skill.base
            else:
                skill_label = self.selected_skill.get_type()
            index = self.all_skills.index(skill_label)
        else:
            index  = 0 

        self.skill_comboBox.setCurrentIndex(index)
        self.skill_comboBox.currentIndexChanged.connect(self.changeSelectedSkill)

        # selected_skill_button = QTHelper.CreateGenButton(skill_label,font=style.LabelFont2,stylesheet=style.SubButtonSheet2)
        att_skill_layout.addWidget(self.skill_comboBox,1,1,alignment=QtCore.Qt.AlignLeft)


        
        self.att_comboBox = QComboBox()
        self.att_comboBox.setFont(style.LabelFont2)
        self.all_atts = ['None'] + list(charecterAttributes.AbS_type_to_key.keys())
        self.all_atts.pop()
        self.att_comboBox.addItems(self.all_atts)
        

        if self.selected_attribute is not None:
            att_label = self.selected_attribute.get_type()
        else:
            att_label = 'None'
        index = self.all_atts.index(att_label)

        
        self.att_comboBox.currentIndexChanged.connect(self.changeSelectedAtt)
        self.att_comboBox.setCurrentIndex(index)

        att_skill_layout.addWidget(self.att_comboBox,0,1,alignment=QtCore.Qt.AlignLeft)

        
        top_layout.addWidget(att_skill_widget,alignment=QtCore.Qt.AlignLeft)
        
        dis_adv_widget = QFrame()
        dis_adv_widget.setFrameShape(QFrame.WinPanel)
        dis_adv_layout = QVBoxLayout()
        dis_adv_widget.setLayout(dis_adv_layout)

        self.dis_adv_buttons = [
            QTHelper.CreateGenButton("Advantage",style.LabelFont2,style.TabButtonSheet2,checkbox=True,function=partial(self.changeAdvantage,True)),
            QTHelper.CreateGenButton("Disadvantage",style.LabelFont2,style.TabButtonSheet2,checkbox=True,function=partial(self.changeAdvantage,False)),
            QTHelper.CreateGenButton("Allow Mixed Checks",style.LabelFont2,style.TabButtonSheet2,checkbox=True,function=self.changeAllowMixed)
            ]
        dis_adv_layout.addWidget(self.dis_adv_buttons[0],alignment=QtCore.Qt.AlignRight)
        dis_adv_layout.addWidget(self.dis_adv_buttons[1],alignment=QtCore.Qt.AlignRight)
        dis_adv_layout.addWidget(self.dis_adv_buttons[2],alignment=QtCore.Qt.AlignRight)
        top_layout.addWidget(dis_adv_widget,alignment=QtCore.Qt.AlignRight)

        mainLayout.addWidget(top_frame)
        
        dice_roll_layout = QHBoxLayout()
        dice_roll_layout.addWidget(self.diceRoll,alignment=QtCore.Qt.AlignCenter)
        dice_roll_layout.addWidget(self.diceRoll.getBonusWidget(),alignment=QtCore.Qt.AlignLeft)
        self.diceRoll.updateBonusLabel()
        mainLayout.addLayout(dice_roll_layout)
        return mainWidget
    
    def changeAdvantage(self,advantage=True):
        if advantage:
            index = 0
            oindex = 1
            sign = 1
        else:
            index = 1
            oindex = 0
            sign = -1
        value = sign * self.dis_adv_buttons[index].checkState()
        ovalue = -1 * sign * self.dis_adv_buttons[oindex].checkState()
        self.advantage_level.setValue(value + ovalue)
        self.diceRoll.updateDisplayDice(0,self.diceRoll.dice_tuple[0])
        

    
    def changeAllowMixed(self):
        self.mixed_checks = (self.dis_adv_buttons[2].checkState() != 0)

        if not self.mixed_checks:
            skill_label = self.selected_skill.get_type()

            if skill_label == 'Saving Throw':
                skill_label = self.selected_skill.base.get_type() + ' ' +  self.selected_skill.get_type()
 
            else:
                skill_label = self.selected_skill.get_type()
            index = self.all_skills.index(skill_label)

            self.changeSelectedSkill(index)
            
    def changeSelectedSkill(self,index):

        new_skill = self.all_skills[index]
        if new_skill == 'None': 
            self.selected_skill = None
            return
        
        if 'Saving Throw' in new_skill:
            skill_key = charecterAttributes.AbS_type_to_key[new_skill.split(' ')[0]]
            self.selected_skill = self.saving_throws_func()[skill_key]
        else:
            skill_key = charecterAttributes.skill_type_to_key[new_skill]
            self.selected_skill = self.skills_func()[skill_key]
        
        
        if ((not self.mixed_checks) and (self.selected_skill.base.get_type() != self.selected_attribute.get_type())):
            index = self.all_atts.index(self.selected_skill.base.get_type())
            self.att_comboBox.setCurrentIndex(index)
            contrib = self.selected_skill.get_contrib().copy()
        elif ((self.mixed_checks) and (self.selected_skill.base.get_type() != self.selected_attribute.get_type())):
            contrib = self.selected_skill.get_contrib().copy()
            contrib['nat_stat'] = self.selected_attribute.get_total_bonus_ref()
        else:
            contrib = self.selected_skill.get_contrib().copy()

        self.diceRoll.setContrib(contrib)
        #     pass
        # else:

    def changeSelectedAtt(self,index):
        new_att = self.all_atts[index]
        if new_att == 'None': 
            self.selected_attribute = None
            self.skill_comboBox.setCurrentIndex(0)
            self.diceRoll.setContrib(None)
            self.diceRoll.update()
            return
        att_key = charecterAttributes.AbS_type_to_key[new_att]

        self.selected_attribute = self.attributes_func()[att_key]

        if (self.selected_skill is not None) and (not self.mixed_checks) and (self.selected_skill.base.get_type() != self.selected_attribute.get_type()):
            # index = self.all_skills.index('None')
            self.skill_comboBox.setCurrentIndex(0)

        
        if self.selected_skill is None:
            contrib = {}
            contrib['nat_stat'] = self.selected_attribute.get_total_bonus_ref()
            self.diceRoll.setContrib(contrib)
        elif self.mixed_checks and (self.selected_skill.base.get_type() != self.selected_attribute.get_type()):
            contrib = self.selected_skill.get_contrib().copy()
            contrib['nat_stat'] = self.selected_attribute.get_total_bonus_ref()
            self.diceRoll.setContrib(contrib)
        elif self.selected_skill.base.get_type() == self.selected_attribute.get_type():
            self.diceRoll.setContrib(self.selected_skill.get_contrib().copy())


            

        #     self.selected_attribute = self.selected_skill.base
def getSeperators():
    separator1 = QFrame()
    separator1.setFrameShape(QFrame.HLine)
    return separator1

class DiceRoll(QFrame):
    



    def __init__(self,advantage_level,contrib=None,dice_amount=1,dice_type=20,):
        super().__init__()
        self.setFrameShape(QFrame.Panel)


        self.advantage_level = advantage_level
        self.layoutOuter = QHBoxLayout()
        self.setLayout(self.layoutOuter)
        self.layout = QHBoxLayout()
        


        self.layoutOuter.addWidget(getSeperators())
        self.layoutOuter.addWidget(getSeperators())

        InnerFrame = QFrame()
        InnerFrame.setFrameShape(QFrame.WinPanel)
        InnerFrame.setLayout(self.layout)
        self.layoutOuter.addWidget(InnerFrame)

        self.layoutOuter.addWidget(getSeperators())
        self.layoutOuter.addWidget(getSeperators())
        
        if contrib is None: self.contrib = {}
        else: self.contrib = contrib.copy()
        self.state = 0 # 0 = rolling, 1 = post roll
        self.dice_tuple = [dice_amount,dice_type] # ([0]d[1])
       
        self.amount_label = None
        self.type_label = None


        self.bonusWidget = BonusWidget(self.contrib,set_higher_contrib_func = self.setContrib)
        self.update()

    def setContrib(self,contrib):
        if contrib is None: self.contrib = {}
        else: self.contrib = contrib

        self.bonusWidget.setContrib(contrib=self.contrib)
        self.updateBonusLabel()

    
    def update(self):
        # QTHelper.deleteItemsOfLayout(self.layout)
        QTHelper.clear_layout2(self.layout)
        if self.amount_label is not None:
            QTHelper.deleteItemsOfLayout(self.amount_label.layout)
            QTHelper.deleteItemsOfLayout(self.type_label.layout)
            self.amount_label.deleteLater() 
            self.type_label.deleteLater() 
            self.amount_label = None
        if self.getState() == 0:
            self.buildState0()
        else:
            self.buildState1()

        
    def getBonusWidget(self):
        return self.bonusWidget

    def getState(self):
        return self.state
    
    def setState(self,state):
        self.state = state
        self.update()
    
    def getBonusWidget(self):
        return self.bonusWidget
    
    def buildState0(self):
        state_0_layout = QVBoxLayout()
        
        self.layout.addLayout(state_0_layout)

        # Dice Type Selection---------------------------------------
        dice_type_layout = QHBoxLayout()

        self.amount_label = QTHelper.ButtonSpinBox(style.TabButtonSheet3,None,value=self.dice_tuple[0],font=style.LabelFont1,update_func=partial(self.updateDisplayDice,0))
        
        d_label = QLabel()
        d_label.setText('D')
        d_label.setAlignment(QtCore.Qt.AlignCenter)
        d_label.setFont(style.LabelFont1)
        

        self.type_label = QTHelper.ButtonSpinBox(style.TabButtonSheet3,None,value=self.dice_tuple[1],font=style.LabelFont1,update_func=partial(self.updateDisplayDice,1))
        self.bonus_label = QLabel()
        self.bonus_label.setText('')
        self.bonus_label.setAlignment(QtCore.Qt.AlignCenter)
        self.bonus_label.setFont(style.LabelFont1)
        self.bonusWidget.setBonusLabelFunc(self.updateBonusLabel)
        self.updateBonusLabel()
        # self.type_label.editingFinished
        
        dice_type_layout.addWidget(QLabel(),stretch=1)
        dice_type_layout.addWidget(self.amount_label,alignment=QtCore.Qt.AlignRight)
        dice_type_layout.addWidget(d_label,alignment=QtCore.Qt.AlignCenter)
        dice_type_layout.addWidget(self.type_label,alignment=QtCore.Qt.AlignLeft)
        dice_type_layout.addWidget(self.bonus_label,alignment=QtCore.Qt.AlignLeft)
        # dice_type_layout.setSpacing(0) 
        dice_type_layout.addWidget(QLabel(),stretch=1)
        
        state_0_layout.addLayout(dice_type_layout)
        # Dice Button---------------------------------------
        diceFrame = QFrame()
        diceFrame.setFrameShape(QFrame.Panel)
        diceFrame_layout = QHBoxLayout(self)
      
        diceFrame.setStyleSheet(style.highlighted_Qframe)

        self.roll_dice = QPushButton()
        self.roll_dice.pressed.connect(partial(self.setState,1))
        self.roll_dice.setStyleSheet(style.ItemEditButton2) 
        self.updateDisplayDice(1,self.dice_tuple[1])
        # self.roll_dice.setIcon(QIcon(self.dice_url_paths[self.dice_tuple[1]]))
        
        # roll_dice.setMinimumWidth(size)
        # roll_dice.setMinimumHeight(size)
        # roll_dice.setMaximumWidth(size)
        # roll_dice.setMaximumHeight(size)
        # roll_dice.setIconSize(QtCore.QSize(size -5,size -5))

        
        diceFrame_layout.addWidget(self.roll_dice,alignment=QtCore.Qt.AlignCenter)
        # diceFrame_layout.addWidget(self.bonusWidget,alignment=QtCore.Qt.AlignLeft)
        state_0_layout.addLayout(diceFrame_layout)

    def buildState1(self):
        rolls = 0
        if self.advantage_level == 0:
            num_of_rolls =1
        else:
            num_of_rolls = 2

        rolls,totals = objectsDnd.complexRollDice(num_of_rolls=num_of_rolls,dice_per_roll=self.dice_tuple[0],dicetype=self.dice_tuple[1])
        
        state_1_layout = QVBoxLayout()
        self.layout.addLayout(state_1_layout)
        

        # Refresh Button______________________________________________________________________
        refresh_layout = QHBoxLayout()
        refresh_button = QTHelper.CreateGenButton(
            stylesheet=style.TabButtonSheet1,
            icon_url=imageURLS.RefreshUrl,
            icon_size=QtCore.QSize(20, 20),
            function_list= [partial(self.removeRefreshButton)]
        )
        # ,partial(self.setState,0)
        refresh_layout.addWidget(QLabel(),stretch=1)
        refresh_layout.addWidget(refresh_button,stretch=0,alignment=QtCore.Qt.AlignRight)
        state_1_layout.addLayout(refresh_layout)
        # ____________________________________________________________________________________
        gridLayout = QGridLayout()
        

        if self.advantage_level == 0: selected_run = -1
        else:
            selected_run = {
                -2:totals.argmin(),
                2:totals.argmax()
            }[self.advantage_level.getValue()]
        total_bonus = self.getTotalBonus()
        for i in range(num_of_rolls):
            scroll = QScrollArea()
            scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
            scroll.setWidgetResizable(True)
            scroll.setMaximumHeight(60)
            # scroll.setMinimumSize(600, 50)

            

            inner_scroll_layout = QHBoxLayout()
            widget_scroll = QFrame() # Underlaying tab for all
            widget_scroll.setFrameShape(QFrame.Panel)
            widget_scroll.setLayout(inner_scroll_layout)
            widget_scroll.setStyle
            scroll.setWidget(widget_scroll)


            label = QLabel()
            label.setText(" + ".join(str(rolls[i,:])[1:][:-1].strip().split()))
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setFont(style.LabelFontBigBold)
            if (selected_run == -1) or (i != selected_run):
                stylesheet = style.GreyLabel2
            elif i == selected_run:
                if self.advantage_level > 0:
                    stylesheet = style.GreenFontGreyLabel2
                else:
                    stylesheet = style.RedFontGreyLabel2
            label.setStyleSheet(stylesheet)
            inner_scroll_layout.addWidget(label)

            if total_bonus != 0:
                label = QLabel()
                label.setText(' ' + pyHelper.sign_string(total_bonus) + ' ')
                label.setAlignment(QtCore.Qt.AlignCenter)
                label.setFont(style.LabelFontBigBold)
                label.setStyleSheet(stylesheet)
                label.setStyleSheet("border-radius: 5")
                inner_scroll_layout.addWidget(label)

            bonus_label = QLabel()
            bonus_string = '= ' + str(total_bonus + totals[i])
            if total_bonus != 0:
                bonus_string = '('+str(np.abs(total_bonus)) + ')'+ ' ' + bonus_string
            bonus_label.setText(bonus_string)
            bonus_label.setAlignment(QtCore.Qt.AlignCenter)
            bonus_label.setFont(style.LabelFontBigBold)
            bonus_label.setStyleSheet(stylesheet)
            # gridLayout.addWidget(bonus_label,i,1)
            if (total_bonus != 0) or (self.advantage_level != 0):
                if total_bonus != 0:
                    inner_scroll_layout.addWidget(bonus_label)
                    inner_scroll_layout.addWidget(QLabel(),stretch=1)
                gridLayout.addWidget(scroll,i,0)
        if total_bonus != 0: gridLayout.setColumnStretch(2, 1) 
        state_1_layout.addLayout(gridLayout)
        

        final = QFrame()


        final_layout = QVBoxLayout()
        final.setLayout(final_layout)
        final_roll = totals[selected_run]
        final_label = QLabel()
        final_label.setText(" "+ str(final_roll + total_bonus) + " ")
        final_label.setAlignment(QtCore.Qt.AlignCenter)
        final_label.setFont(style.LargeLabelFontBold)
        final_label.setStyleSheet(style.GreyLabel2)
        final_layout.addWidget(final_label,alignment=QtCore.Qt.AlignCenter)
        state_1_layout.addWidget(final,alignment=QtCore.Qt.AlignCenter)
        pass

    def removeRefreshButton(self):
        # QTHelper.clear_layout2(self.layout)
        # if self.refresh_layout is not None:
            
        #     self.refresh_layout.removeWidget(self.refresh_button)
        #     self.refresh_layout.deleteLater() 
        #     self.refresh_layout = None
        # if self.refresh_button is not None:
        #     self.refresh_button.deleteLater()
        self.setState(0)

    def updateDisplayDice(self,index,new_value):
        size = 200
        self.dice_tuple[index] = new_value
        icon = QTHelper.createDiceIcon(self.dice_tuple[0],self.dice_tuple[1])
        # self.roll_dice.setIcon(QIcon(dice_url_paths[self.dice_tuple[1]]))
        self.roll_dice.setIcon(icon)
        self.roll_dice.setMinimumWidth(size)
        self.roll_dice.setMinimumHeight(size)
        self.roll_dice.setMaximumWidth(size)
        self.roll_dice.setMaximumHeight(size)
        self.roll_dice.setIconSize(QtCore.QSize(size -5,size -5))

        styleSheet = {
            -2: style.RedItemEditButton,
            0: style.ItemEditButton2,
            2: style.GreenItemEditButton
        }[self.advantage_level.getValue()]

        self.roll_dice.setStyleSheet(styleSheet) 

    def updateBonusLabel(self):
        total_bonus = self.getTotalBonus()

        if total_bonus == 0:
            text = ''
        else:
            text = pyHelper.sign_string(total_bonus,show_negative=False) + str(total_bonus)
        if self.bonus_label is not None: self.bonus_label.setText(text)

    def getTotalBonus(self):
        total_bonus = 0
        for key in self.contrib:
            total_bonus += self.contrib[key].getValue()
        return total_bonus

    # def changeDiceType(self,new_value):
    #     self.dice_tuple[1] = new_value
    #     self.update()

    # def changeDiceAmount(self,new_value):
    #     self.dice_tuple[0] = new_value
    #     self.update()




class BonusWidget(QFrame):
    



    def __init__(self,contrib=None,bonus_total_label_func=None,set_higher_contrib_func=None):
        super().__init__()
        self.setFrameShape(QFrame.Panel)

        self.contrib = contrib
        self.bonus_total_label_func = bonus_total_label_func
        self.set_higher_contrib_func = set_higher_contrib_func
        
        self.layoutOuter = QHBoxLayout()
        self.setLayout(self.layoutOuter)
        self.layout = QVBoxLayout()
        

        
        self.layoutOuter.addWidget(getSeperators())
        self.layoutOuter.addWidget(getSeperators())

        InnerFrame = QFrame()
        InnerFrame.setFrameShape(QFrame.WinPanel)
        InnerFrame.setLayout(self.layout)
        self.layoutOuter.addWidget(InnerFrame)

        self.layoutOuter.addWidget(getSeperators())
        self.layoutOuter.addWidget(getSeperators())

        # scroll || add bar
        self.scroll_layout = QVBoxLayout()
        self.layout.addLayout(self.scroll_layout)
        # Add Button--------------------------------
        add_widget = QFrame()
        add_widget.setFrameShape(QFrame.WinPanel)
        add_layout = QHBoxLayout()
        add_widget.setLayout(add_layout)


        self.add_amount = pyHelper.ReferenceNumber(0, is_int=True)


        self.add_bar = [
            QLineEdit(),
            QSpinBox(),
            QTHelper.CreateGenButton(
                stylesheet=style.ConfirmEditButton,
                icon_url=imageURLS.CheckUrl,
                icon_size=QtCore.QSize(20, 20),
                function=self.addContrib
            )
        ]
        self.add_bar[0].setFont(style.LabelFont2)
        self.add_bar[1].setFont(style.LabelFont2)
        self.add_bar[1].setMaximum(1001)
        self.add_bar[1].setMinimum(-1001)
        self.add_bar[1].valueChanged.connect(partial(self.add_amount.setValue))
        self.add_bar[0].setPlaceholderText("Name of Bonus...")

        add_layout.addWidget(self.add_bar[0],alignment=QtCore.Qt.AlignLeft)
        add_layout.addWidget(self.add_bar[1],alignment=QtCore.Qt.AlignLeft)
        add_layout.addWidget(QLabel(),stretch=1)
        add_layout.addWidget(self.add_bar[2],alignment=QtCore.Qt.AlignRight)
        self.layout.addWidget(add_widget)
        self.update()
        

    def update(self):
        QTHelper.deleteItemsOfLayout(self.scroll_layout)
        if self.bonus_total_label_func is not None: self.bonus_total_label_func()
        self.makeScrollWidget()
    
    def setBonusLabelFunc(self,bonus_total_label_func):
        self.bonus_total_label_func = bonus_total_label_func

    def setContrib(self,contrib):
        self.contrib = contrib
        self.update()

    def addContrib(self):
        key = pyHelper.name_to_key(self.add_bar[0].text())
        value = pyHelper.ReferenceNumber(self.add_amount.getValue())

        if key.isspace() or (value == 0): return
        self.add_bar[1].setValue(0)
        self.add_bar[0].setPlaceholderText("Name of Bonus...")
        self.contrib[key] = value
        self.set_higher_contrib_func(self.contrib)
    

    def makeScrollWidget(self):
        
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scroll.setWidgetResizable(True)
        scroll.setMaximumSize(500, 600)

        

        inner_scroll_layout = QVBoxLayout()
        widget_scroll = QWidget() # Underlaying tab for all
        widget_scroll.setLayout(inner_scroll_layout)
        scroll.setWidget(widget_scroll)

        self.scroll_layout.addWidget(scroll)


        for contrib_i in self.contrib.keys():

            contrib_name = pyHelper.key_to_name(contrib_i)
            contrib_value = self.contrib[contrib_i].getValue()

            if contrib_name == 'Nat Stat':
                contrib_name = 'Attribute Bonus'

            if contrib_value == 0:
                continue

            contrib_widget = QFrame()
            contrib_widget.setFrameShape(QFrame.StyledPanel)
            contrib_widget.setMaximumHeight(40)
            contrib_layout = QHBoxLayout()
            contrib_widget.setLayout(contrib_layout)
            


            label = QLabel()
            label.setText(contrib_name + ':')
            label.setAlignment(QtCore.Qt.AlignLeft)
            label.setFont(style.LabelFont2)

            value_label  = QLabel()
            value_label.setText(pyHelper.sign_string(contrib_value,show_negative=False) + str(contrib_value))
            value_label.setAlignment(QtCore.Qt.AlignRight)
            value_label.setFont(style.LabelFont2)

            # print(contrib_name + ':', pyHelper.sign_string(contrib_value) + str(contrib_value))
            contrib_layout.addWidget(label,alignment=QtCore.Qt.AlignLeft)

            contrib_layout.addWidget(QLabel(),stretch=1)

            contrib_layout.addWidget(value_label,alignment=QtCore.Qt.AlignRight)
            
            minus_button = QTHelper.CreateGenButton(stylesheet=style.ItemEditButton2,
                                                    icon_url=imageURLS.XUrl,
                                                    icon_size=QtCore.QSize(20, 20),
                                                    function=partial(self.removeContrib, contrib_i))
            minus_button.setMaximumSize(20,20)
            minus_button.setMinimumSize(20,20)
            
            contrib_layout.addWidget(minus_button,alignment=QtCore.Qt.AlignRight)
            

            inner_scroll_layout.addWidget(contrib_widget,alignment=QtCore.Qt.AlignTop)
            

        inner_scroll_layout.addWidget(QLabel(),stretch=1)

    def removeContrib(self,key):
        del self.contrib[key]
        self.update()




