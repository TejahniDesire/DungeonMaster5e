import math
import numpy as np
from ..objectF import pyHelper
from ..metaF import EZPaths
import gc

from PyQt5.QtWidgets import (
    # QApplication,
    # QStackedLayout,
    # QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    # QGridLayout,
    # QLabel,
    # QPushButton,
    # QScrollArea, 
    QFrame, 
    # QCheckBox,
    # QSizePolicy,
    # QTextEdit,
    # QLineEdit,
    QCheckBox,
    # QGraphicsOpacityEffect, 
    # QSpinBox
)

# from PyQt5.QtGui import (
#     QPalette, QColor, QFont, QIcon
# )

from PyQt5 import (
    QtCore, 
    # Qt
)

from PyQt5.QtCore import (
    QSize, QObject, pyqtSignal
)

from PyQt5.sip import delete

import qdarktheme

from . import customWidgets
from functools import partial


from ..customQT import (style, QTHelper)


class MainTab(QWidget):

    def __init__(self, tcharecter, *args, **kwargs):

        super().__init__(*args, **kwargs)
        base_layout = QVBoxLayout()
        self.setLayout(base_layout)

        main_stats_layout = QHBoxLayout()

        # Left_layout_______________________________


        left_stats_layout = QVBoxLayout() 
        
        self.attribute_labels = customWidgets.AllStatWidgets(tcharecter.get_skills_of_attribute,tcharecter.get_all_attributes,tcharecter.get_all_skills,tcharecter.get_all_saving_throws) # Attributes, Skills 

        # top_layout_______________________________
        self.top_widget = customWidgets.RPWidget(tcharecter.get_all_top()) # Top stats (name, class, level, background, Race, Aligment, Experience Points)

        # Mid_layout_______________________________
        mid_layout = QVBoxLayout()
        # Mid top stats (AC, initiative, speed, max hit points, current hit points)
        # Mid mid stats (Hit dice, Death Saving throws)
        self.mid_widget = customWidgets.MiddleWidget(tcharecter.get_all_mid_top(), tcharecter.get_all_mid_mid(),tcharecter.get_time()) 
        mid_layout.addWidget(self.mid_widget.get_widget(),stretch=2)

        # test_button = QPushButton('test')
        # test_button.clicked.connect(partial(self.test))

        # Attack Layout____________________________
        self.weapon_widget = customWidgets.WeaponWidget(
            tcharecter.get_inventory(),
            tcharecter.get_attack_inventory(),
            tcharecter.get_all_attributes()
        )
        mid_layout.addWidget(self.weapon_widget.getWidget(), alignment=QtCore.Qt.AlignTop,stretch=1)

        # Right Layout_____________________________________
        right_layout = QVBoxLayout()

        # RP Trait Layout__________________________________
        self.rp_trait_widget = customWidgets.RPTraitWidget(tcharecter.get_all_rp_traits())

        # adding layouts
        # left_stats_layout.addWidget(test_button)  # Test
        self.attribute_labels.add_widgets_to_layout(left_stats_layout)

        right_layout.addWidget(self.rp_trait_widget.get_widget())

        main_stats_layout.addLayout(left_stats_layout, stretch=2)
        main_stats_layout.addLayout(mid_layout, stretch=2)
        main_stats_layout.addLayout(right_layout, stretch=1)

        # Adding Main Layout
        base_layout.addWidget(self.top_widget.get_widget())
        base_layout.addLayout(main_stats_layout)

    def update(self):
        self.attribute_labels.update()
        self.top_widget.update()
        self.mid_widget.update()
        self.rp_trait_widget.update()
        self.weapon_widget.update()


class FeatNTrait(QWidget):

    def __init__(self, tcharecter, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self):
        pass

class Inventory(QWidget):

    def __init__(self, tcharecter, *args, **kwargs):
        super().__init__(*args, **kwargs)

        inventory_layout = QVBoxLayout()
        self.setLayout(inventory_layout)

        self.inventory_widget = customWidgets.InventoryWidget(tcharecter.get_inventory())
        inventory_layout.addWidget(self.inventory_widget.get_widget())

    def update(self):
        self.inventory_widget.update()


class Options(QWidget):

    def __init__(self,tcharecter_save_func,main_menu_func, *args, main_menu_instance=None,process_events, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.save_func = tcharecter_save_func
        self.main_menu_func = main_menu_func
        self.main_menu_instance = main_menu_instance
        self.process_events = process_events
        # ____________________________________________________________________________________________________________________________________________
        options_layout = QVBoxLayout()
        self.setLayout(options_layout)

        self.save_path = EZPaths.Saves_Path
        saveButton = QTHelper.CreateGenButton("Quick Save", style.LabelFont1, style.SubButtonSheet, self.save, minWidth=400)
        mainMenuButton = QTHelper.CreateGenButton("Main Menu", style.LabelFont1, style.SubButtonSheet, self.launchMainMenu, minWidth=400)

        DarkModeToggle = QCheckBox()
        DarkModeToggle.setText("Dark Mode Toggled: On")
        DarkModeToggle.setFont(style.LabelFont1)
        DarkModeToggle.checked = True
        DarkModeToggle.clicked.connect(partial(self.dark_mode_toggle, DarkModeToggle.setText))
        DarkModeToggle.setStyleSheet(style.SubCheckedSheet)

        frame = QFrame()
        frame.setFrameShape(QFrame.Panel)
        frame.setMinimumWidth(600)
        options_sub_layout = QVBoxLayout(frame)
        options_sub_layout.addWidget(QTHelper.CreateSeperator())
        options_sub_layout.addWidget(mainMenuButton, alignment=QtCore.Qt.AlignCenter)
        options_sub_layout.addWidget(saveButton, alignment=QtCore.Qt.AlignCenter)
        options_sub_layout.addWidget(DarkModeToggle, alignment=QtCore.Qt.AlignCenter)
        options_sub_layout.addWidget(QTHelper.CreateSeperator())

        options_layout.addWidget(frame, alignment=QtCore.Qt.AlignCenter)

    def update(self):
        pass

    def dark_mode_toggle(self, set_text_function, isChecked: bool):
        if isChecked:
            set_text_function("Dark Mode Toggled: OFF PLEASE TURN IT BACK ON OH GOD")
            qdarktheme.setup_theme("light")
        else:
            qdarktheme.setup_theme()
            set_text_function("Dark Mode Toggled: On")

    def save(self):

        progress = pyHelper.ProgressMarker()

        self.progressBar = customWidgets.LoadingBar(progress,'saving_char')
        self.progressBar.show()

        self.save_func(self.save_path,progress,self.process_events)
        self.progressBar.close()

    def launchMainMenu(self):
        if self.main_menu_instance is not None:
            self.main_menu_instance.close()
            gc.collect
            
        self.main_menu_instance = self.main_menu_func()
        self.main_menu_instance.show()
        

