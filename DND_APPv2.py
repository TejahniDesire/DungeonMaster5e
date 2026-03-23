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

import qdarktheme



from Scripts.objectF import (
    itemsDnD, objectsDnd, pyHelper
    )
from Scripts.charecterF import (
    inventory, charecter, charecterAttributes, charecterMechanics
    )
from Scripts.customQT import (customTabs, QTHelper, style, customMainMenuTabs)

from Scripts.metaF import (imageURLS, reading, EZPaths)

class MainMenu(QMainWindow):

    def __init__(self,process_events,dnd_app_instance=None,):
        super().__init__()
        qdarktheme.setup_theme()

        main_outer_layout = QVBoxLayout()

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scroll.setWidgetResizable(True)
        self.scroll.setMinimumSize(700, 400)

        widget_scroll = QWidget() # Underlaying tab for all
        widget_scroll.setLayout(main_outer_layout)
        self.scroll.setWidget(widget_scroll)
        self.setCentralWidget(self.scroll)



        self.stacklayout = QStackedLayout()


        main_outer_layout.addLayout(self.stacklayout)


        # tab Widgets_________________________________________________________________________________________________

        self.main_tab = customMainMenuTabs.MainTab(dndWindow_func=partial(DnDWindow,partial(MainMenu,process_events),self,process_events),process_events=process_events,dnd_app=dnd_app_instance)
        self.stacklayout.addWidget(self.main_tab)

    def switch_tab(self, index: int):
        self.stacklayout.setCurrentIndex(index)


class DnDWindow(QMainWindow):

    def __init__(self,main_menu_func,main_menu_instance,process_events,tcharecter:charecter.CharacterSheet):
        super().__init__()
        qdarktheme.setup_theme()

        self.tcharecter = tcharecter
        self.setWindowTitle("Charecter Sheet")
        self.process_events = process_events
        main_outer_layout = QVBoxLayout()

        # Scrolling_______________________________
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scroll.setWidgetResizable(True)
        self.scroll.setMinimumSize(900, 500)

        widget_scroll = QWidget() # Underlaying tab for all
        widget_scroll.setLayout(main_outer_layout)
        self.scroll.setWidget(widget_scroll)
        self.setCentralWidget(self.scroll)

        # Widget_Scroll -> Main_outer -> {buttons, stacked -> {base_widget/layout, others}}


        button_layout = QHBoxLayout() # Directory to different tabs
        self.stacklayout = QStackedLayout()

        main_outer_layout.addLayout(button_layout)
        main_outer_layout.addLayout(self.stacklayout)



        # tab Widgets_________________________________________________________________________________________________
        self.main_tab = customTabs.MainTab(self.tcharecter)
        self.stacklayout.addWidget(self.main_tab)


        self.feat_trait_tab = customTabs.FeatNTrait(self.tcharecter)
        self.stacklayout.addWidget(self.feat_trait_tab)


        self.inventory_tab = customTabs.Inventory(self.tcharecter)
        self.stacklayout.addWidget(self.inventory_tab)

        self.options_tab = customTabs.Options(tcharecter_save_func=self.tcharecter.save,main_menu_func=partial(main_menu_func,self),main_menu_instance=main_menu_instance,process_events=self.process_events)
        self.stacklayout.addWidget(self.options_tab)



        # Tab Buttons_________________________________________________________________________________________________
        refresh_button = QTHelper.CreateGenButton(
            stylesheet=style.TabButtonSheet1,
            icon_url=imageURLS.RefreshUrl,
            icon_size=QtCore.QSize(20, 20),
            function_list=[partial(self.update)]
        )
        refresh_button.setMaximumWidth(30)
        button_layout.addWidget(refresh_button)

        button_layout.addWidget(QTHelper.CreateTabButton(self.switch_tab, 0, style.LabelFont2,
                                                    style.TabButtonSheet2, "Main Window"))
        button_layout.addWidget(QTHelper.CreateTabButton(self.switch_tab, 1, style.LabelFont2,
                                                    style.TabButtonSheet2, "Features && Traits"))
        
        button_layout.addWidget(QTHelper.CreateTabButton(self.switch_tab, 2, style.LabelFont2,
                                                    style.TabButtonSheet2, "Inventory"))
        button_layout.addWidget(QTHelper.CreateTabButton(self.switch_tab, 3, style.LabelFont2,
                                                    style.TabButtonSheet2, "Options"))

        test_button = QPushButton('test')
        test_button.clicked.connect(partial(self.test))
        button_layout.addWidget(test_button)


    def test(self):
        # self.tcharecter.alter_attribute('prof','starter_level',
        #                                 self.tcharecter.get_specific_attribute('prof').get_total_base() + 3)
        self.tcharecter.alter_attribute('str', 'starter_level', 800,easy=True)
        self.tcharecter.alter_attribute('chr', 'starter_level', 8,easy=True)

        self.tcharecter.get_time().add(12,'hour')
        self.tcharecter.get_time().add(22,'minute')


        dex_base = self.tcharecter.get_attribute('dex').get_total_base()
        self.tcharecter.alter_attribute('dex', 'starter_level',  dex_base + 3,easy=True)
        self.tcharecter.alter_attribute('dex', 'cool_factor',  20,easy=True)
        self.tcharecter.alter_attribute('dex', 'rage',  12,easy=True)
        self.tcharecter.alter_attribute_bonus('dex', 'love_sword',  12,easy=True)


        self.tcharecter.alter_attribute('prof', 'starter_level',  23,easy=True)
        mid_top_stats = self.tcharecter.get_all_mid_top()
        mid_top_stats['hp'].alter_contrib_base('Monk level', 100,easy=True)
        mid_top_stats['hp'].replenish(int(mid_top_stats['hp'].get_amount_missing() * .1))

        mid_top_stats['speed'].alter_contrib_base('human race', 30,easy=True)

        mid_top_stats['speed'].replenish(int(mid_top_stats['speed'].get_amount_missing() * .5))

        mid_top_stats['ac'].alter_contrib_base('Splint Armor', 18,easy=True)
        mid_top_stats['ac'].alter_contrib_base('Shield', 2,easy=True)

        print()
        print("new Prof: ", self.tcharecter.AbS['prof'].get_all_bases())
        print("new Prof: ", self.tcharecter.AbS['prof'].get_total_base())
        print("new prof:",self.tcharecter.all_skills['stealth'].get_total_bonus())
        print()
        # self.tcharecter.get_specific_skills('sleight').give_expertise()
        # self.tcharecter.get_specific_top('name').set('Lucas Cyr')
        # self.tcharecter.get_specific_top('class').set('Killer')
        # self.tcharecter.get_specific_top('alignment').set('Neutral Evil')
        # self.tcharecter.get_specific_top('race').set('Other Kin')
        # self.tcharecter.get_specific_top('background').set('France')
        # self.tcharecter.get_specific_top('level').add(1000)
        # self.tcharecter.get_specific_top('experience').add(1000)
        # self.tcharecter.get_specific_mid_top('ac').alter_contrib_base("foo", 18)
        # self.tcharecter.get_specific_mid_mid('death').mark_failure()
        # self.tcharecter.get_specific_mid_mid('hd').set_total_hd(10)
        # self.tcharecter.get_specific_mid_mid('hd').set_d_type(10)
        # self.tcharecter.get_specific_mid_top('mhp').alter_contrib_base("god",1000000)
        # self.tcharecter.get_specific_mid_top('chp').alter_contrib_base("god", 1000000)
        # self.tcharecter.get_specific_rp_traits('ideals').set_text("Man, you don't wanna know")

        inventory = self.tcharecter.get_inventory()
        apple = itemsDnD.Item("Apple", 100, category="Food")
        pear = itemsDnD.Item("Pear", 1)
        ear = itemsDnD.Item("Ear", 10, cost=(100, "gp"))
        sword = itemsDnD.Weapon("Sword", 10, (10000, "gp"), (1, 4),
                                  "piercing", ["Throw"], "Simple")

        inventory.add_item(sword, 1)
        inventory.add_item(apple, 1)
        inventory.add_item(pear, 1)
        inventory.add_item(ear, 1)
        inventory.add_money(inventory.get_money("gp")[0] + 1, "gp")

        testWeapons = reading.WeaponReader(EZPaths.Weapon_Path)
        list_weapons = testWeapons.get_all_weapons()
        for i in range(len(list_weapons)):
            inventory.add_item(list_weapons[i], i + 1)

        self.tcharecter.get_attack_inventory().add_attack_item("Battleaxe")
        # self.update()


        

        self.tcharecter.alter_attribute('prof', 'starter_level',
                                        self.tcharecter.get_attribute('prof').get_total_base() + 3,easy=True)

        self.tcharecter.alter_attribute('chr', 'starter_level', 8,easy=True)
        self.tcharecter.alter_attribute('dex', 'starter_level',
                                        self.tcharecter.get_attribute('dex').get_total_base() + 3,easy=True)
        self.tcharecter.get_skill('sleight').give_expertise()
        self.tcharecter.get_specific_top('name').set('Christopher "Terror" Clark')
        self.tcharecter.get_specific_top('class').set('Killer')
        self.tcharecter.get_specific_top('alignment').set('True Evil')
        self.tcharecter.get_specific_top('race').set('Beyond Comprehension')
        self.tcharecter.get_specific_top('background').set('Cracker Barrel')
        self.tcharecter.get_specific_top('level').add(1000)
        self.tcharecter.get_specific_top('experience').add(1000)


        self.tcharecter.get_specific_mid_mid('death').mark_failure()
        self.tcharecter.get_specific_mid_mid('hd').set_total_hd(10)
        self.tcharecter.get_specific_mid_mid('hd').set_d_type(10)

        # self.tcharecter.get_specific_mid_top('ac').add_base("foo", pyHelper.ReferenceNumber(20))
        # self.tcharecter.get_specific_mid_top('mhp').add_base("god", pyHelper.ReferenceNumber(1000000))
        # self.tcharecter.get_specific_mid_top('chp').add_base("god", pyHelper.ReferenceNumber(1000000))
        self.tcharecter.get_specific_rp_traits('ideals').set_text("Man, you don't wanna know")
        self.update()



    def update(self):
        self.tcharecter.update()
        self.main_tab.update()
        self.inventory_tab.update()

    def switch_tab(self, index: int):
        self.stacklayout.setCurrentIndex(index)

    # def loadCharecter(self,path):







app = QApplication(sys.argv)

window = MainMenu(process_events=app.processEvents)
window.show()

# window = DnDWindow()
# window.show()

app.exec()
