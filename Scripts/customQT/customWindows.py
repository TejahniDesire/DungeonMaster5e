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
    QSpinBox
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
from ..objectF import pyHelper, itemsDnD
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
        
        text_str = str(self.attribute)
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
            value = pyHelper.sign_string(bonus_values[i].getValue()) + str(bonus_values[i])


            name_label = QTHelper.CreateLabel(name,font=style.LabelFont2p5,style_sheet=style.DarkGreyLabel)
            value_label = QTHelper.CreateLabel(value,font=style.LabelFont2p5,style_sheet=style.DarkGreyLabel)

            name_label.setMaximumWidth(100)
            name_label.setMaximumHeight(15)
            value_label.setMaximumWidth(30)
            value_label.setMaximumHeight(15)

            bonus_layout.addWidget(name_label,i,0)
            bonus_layout.addWidget(value_label,i,1)
            

        name_label = QTHelper.CreateLabel("Total",font=style.LabelFont2p5,style_sheet=style.DarkGreyLabel)
        value_label = QTHelper.CreateLabel(pyHelper.sign_string(self.attribute.get_total_bonus()) + str(self.attribute.get_total_bonus()),font=style.LabelFont2p5,style_sheet=style.DarkGreyLabel)

        name_label.setMaximumWidth(100)
        name_label.setMaximumHeight(15)
        value_label.setMaximumWidth(30)
        value_label.setMaximumHeight(15)

        bonus_layout.addWidget(name_label,len(bonus_names)+1,0)
        bonus_layout.addWidget(value_label,len(bonus_names)+1,1)

        layout.addWidget(bonus_frame,1,1)

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
