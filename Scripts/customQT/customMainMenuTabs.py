import math
import numpy as np
import sys
from ..objectF import pyHelper
from ..metaF import EZPaths
from ..customQT import style,QTHelper
import gc
from functools import partial
from PyQt5.QtWidgets import (
    QApplication,
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

from Scripts.charecterF import (
    inventory, charecter, charecterAttributes, charecterMechanics
    )

from ..customQT import customMainMenuWidgets

class MainTab(QWidget):

    def __init__(self, dndWindow_func,process_events, *args, dnd_app=None, **kwargs):
        """_summary_

        Args:
            dndWindow_func (_type_): Function that creates a DND app
            dnd_app (_type_, optional): Insitantiation of DND window function. Defaults to None.
        """

        super().__init__(*args, **kwargs)
        base_layout = QVBoxLayout()
        self.setLayout(base_layout)
        self.dndWindow_func = dndWindow_func
        self.app = dnd_app
        self.loadingWindow = None
        self.process_events = process_events
        self.savePath = EZPaths.Saves_Path
        # Buttons

        new_charecter_button = QTHelper.CreateGenButton("New Charecter", style.LabelFontBigBold , style.SubButtonSheet, self.newChar, minWidth=400)
        load_charecter_button = QTHelper.CreateGenButton("Load Charecter", style.LabelFontBigBold , style.SubButtonSheet, self.loadChar, minWidth=400)



        frame = QFrame()
        frame.setFrameShape(QFrame.Panel)
        frame.setMinimumWidth(600)
        options_sub_layout = QVBoxLayout(frame)
        options_sub_layout.addWidget(QTHelper.CreateSeperator())
        options_sub_layout.addWidget(QTHelper.CreateSeperator())
        options_sub_layout.addWidget(new_charecter_button, alignment=QtCore.Qt.AlignCenter)
        options_sub_layout.addWidget(load_charecter_button, alignment=QtCore.Qt.AlignCenter)
        options_sub_layout.addWidget(QTHelper.CreateSeperator())
        options_sub_layout.addWidget(QTHelper.CreateSeperator())


        base_layout.addWidget(frame, alignment=QtCore.Qt.AlignCenter)


    def newChar(self):
        tcharecter = charecter.CharacterSheet()

        self.launchApp(tcharecter)

        # if self.app is not None:
        #     self.app.close()

        # self.app = self.dndWindow_func(tcharecter)
        # self.app.show()

    def loadChar(self):
        gc.collect()
        tcharecter = charecter.CharacterSheet()

        self.loadingWindow = customMainMenuWidgets.loadingWindow(EZPaths.Saves_Path,tcharecter_load_func=tcharecter.load,launch_app_func = partial(self.launchApp,tcharecter),processEvents=self.process_events)
        windowWidget = self.loadingWindow.getWidget()
        windowWidget.show()

    def launchApp(self,tcharecter):

        if self.app is not None: # an app is already open, close it first
                self.app.close()

        self.app = self.dndWindow_func(tcharecter)
        self.app.update()
        self.app.show()
        


            

