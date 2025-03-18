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
from Scripts.customQT import (customTabs, QTHelper, style)

from Scripts.metaF import (imageURLS, reading, EZPaths)

class DnDWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        qdarktheme.setup_theme()

        self.tcharecter = charecter.CharacterSheet()
        self.setWindowTitle("Charecter Sheet")

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

        self.options_tab = customTabs.Options()
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

        



        dex_base = self.tcharecter.get_attribute('dex').get_total_base()
        self.tcharecter.alter_attribute('dex', 'starter_level',  dex_base + 3,easy=True)

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






app = QApplication(sys.argv)

window = DnDWindow()
window.show()

app.exec()
