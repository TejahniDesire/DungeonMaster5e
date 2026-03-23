import math
import numpy as np
from ..objectF import pyHelper
import os
from datetime import datetime

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame, 
    QStackedLayout,
    QCheckBox,
    QTextEdit,
    QCheckBox,
    QGridLayout,
    QLineEdit,
    QScrollArea,
    QSlider
)

from PyQt5.QtGui import (
    QFont, 
)

from PyQt5 import (
    QtCore, 

)

from PyQt5.QtCore import (
    QSize, QObject, pyqtSignal
)

from PyQt5.sip import delete
from functools import partial


from . import (style, customWindows, QTHelper,customWidgets)
from ..charecterF import (charecter, charecterMechanics, charecterAttributes, inventory, time)
from ..objectF import pyHelper, itemsDnD
from ..metaF import imageURLS

save_delin = '(138055)'

class loadingWindow():

    def __init__(self,save_path,tcharecter_load_func,launch_app_func,processEvents):
        if save_path[-1] != '/':
            save_path += '/'
        self.tcharecter_load_func = tcharecter_load_func
        self.launch_app_func = launch_app_func
        self.processEvents =processEvents
        


        main_outer_layout = QVBoxLayout()
        
        
        # Scrolling_______________________________
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scroll.setWidgetResizable(True)
        
        self.main_widget = self.scroll
        self.setWindowTitle = self.scroll.setWindowTitle
        self.setWindowTitle("Which Charecter?")

        widget_scroll = QWidget() # Underlaying tab for all
        widget_scroll.setLayout(main_outer_layout)
        self.scroll.setWidget(widget_scroll)
        # self.main_widget.setCentralWidget()

        # Widget_Scroll -> Main_outer -> {buttons, stacked -> {base_widget/layout, others}}


        # button_layout = QHBoxLayout() # Directory to different tabs
        self.stacklayout = QStackedLayout()

        # main_outer_layout.addLayout(button_layout)
        main_outer_layout.addLayout(self.stacklayout)



        self.innerCharSaves = None
        self.num_of_chars=0
        self.stacklayout.addWidget(self.getCharecterTabs(save_path))
        

        # self.charecter_save_tab= getInnerCharSaves(self,inner_save_path)
        # self.stacklayout.addWidget(self.feat_trait_tab)

        # main_layout.addWidget(options_widget)


    def getCharecterTabs(self,save_path):
        
        options_widget = QFrame()
        inner_layout = QVBoxLayout(options_widget)
        options_widget.setFrameShape(QFrame.WinPanel)

        frame = QFrame()
        frame.setFrameShape(QFrame.Panel)
        frame.setMinimumWidth(600)
        
        options_sub_layout = QVBoxLayout(frame)

        inner_layout.addWidget(frame,stretch=0)

        all_items = os.listdir(save_path)
        frame.setMaximumHeight(50 * len(all_items))

        for item in all_items:

            button = QTHelper.CreateGenButton(item, style.LabelFont2, style.SubButtonSheet, partial(self.addInnerCharSaves,save_path + item + '/',item), minWidth=400)
            options_sub_layout.addWidget(button)
        self.num_of_chars = len(all_items)
        self.scroll.setMinimumSize(700, 50 * self.num_of_chars + 30)
        
        return options_widget

        # all_items.reverse()

        
    def addInnerCharSaves(self,inner_save_path,name):
        self.setWindowTitle("Which Save of {}?".format(name))
        if self.innerCharSaves is not None:
            self.innerCharSaves.deleteLater()
            self.innerCharSaves = None
        
        options_widget = QFrame()
        inner_layout = QVBoxLayout(options_widget)
        upper_layout = QHBoxLayout()
        inner_layout.addLayout(upper_layout)
        options_widget.setFrameShape(QFrame.WinPanel)


        upper_layout.addWidget(QTHelper.CreateTabButton(self.resetStacked, 0, style.LabelFont2, style.TabButtonSheet1, "<-"))
        

        all_items = os.listdir(inner_save_path)
        all_items.reverse()

        # To Charecters.

        
        code_dates = []
        names = []
        indices = []
        i = 0
        for item in all_items:
            parts = item.split(save_delin)
            name = parts[0]
            name = name[:len(name) - 5]
            names += [name]
            code_dates += [parts[1]]
            indices += [i]
            i += 1

            # humanTime = pyHelper.timeToHuman(parts[1])

            # proper_strs += [name + ' || ' + humanTime]

        zipped_pairs = zip(code_dates, indices)

        sorted_pairs = sorted(zipped_pairs, key=lambda x: datetime.strptime(x[0], "%m_%d_%y_%H_%M_%S_%f"))

        # Unzip the sorted pairs into two separate tuples
        sorted_code_dates, sorted_indices = zip(*sorted_pairs)
        sorted_code_dates = list(sorted_code_dates)
        sorted_indices = list( sorted_indices)
        
        sorted_code_dates.reverse()
        sorted_indices.reverse()

        for i in range(len(sorted_code_dates)):
            index = sorted_indices[i]
            code_date = sorted_code_dates[i]
            name = names[index]
            item = all_items[index]
            humanTime = pyHelper.timeToHuman(code_date)
            proper_str = name + ' || ' + humanTime

            button = QTHelper.CreateGenButton(proper_str, style.LabelFont2, style.SubButtonSheet, partial(self.loadChar,inner_save_path + item,self.processEvents), minWidth=400)
            inner_layout.addWidget(button)
        self.innerCharSaves = options_widget
        self.stacklayout.addWidget(options_widget)
        min_height  = min( 50 * len(sorted_code_dates) + 30,50 * 7 + 30 )
        self.scroll.setMinimumSize(700, min_height )
        self.stacklayout.setCurrentIndex(1)

    def resetStacked(self,index):
        self.stacklayout.setCurrentIndex(index)
        self.innerCharSaves.deleteLater() 
        self.innerCharSaves = None
        min_height  = min(50 * self.num_of_chars + 30,50 * 7 + 30 )
        self.scroll.setMinimumSize(700,min_height)
        
        self.scroll.resize(700, min_height)


    def loadChar(self,path,processEvents):
        progress = pyHelper.ProgressMarker()

        self.progressBar = customWidgets.LoadingBar(progress,'loading_char')
        self.progressBar.show()
        self.tcharecter_load_func(path,progress,processEvents)
        self.launch_app_func()
        self.main_widget.close()
        self.progressBar.close()

    def getWidget(self):
        return self.main_widget



class CharLoadingBar(QWidget):

    def __init__(self,progress:pyHelper.ProgressMarker):
        super().__init__()
        self.setWindowTitle("Loading Charecter...")
        self.progress = progress
        self.setMinimumWidth(800)
        self.setMaximumHeight(100)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.bar_layout = QHBoxLayout()
        text_layout = QHBoxLayout()
        main_layout.addLayout(self.bar_layout,stretch=2)
        main_layout.addLayout(text_layout,stretch=1)

    
        


        self.progressText = QTHelper.CreateLabel("Loading Charecter...",font=style.LabelFont1,style_sheet=style.DarkGreyLabel)
        text_layout.addWidget(self.progressText)


        self.createProgressBar(0.0)
        self.progress.addFunction(self.createProgressBar)
        

    def createProgressBar(self,fraction):
        # Delete previous bars
        for i in reversed(range(self.bar_layout.count())): 
            self.bar_layout.itemAt(i).widget().setParent(None)
        # ---------------------------------------------------
        num_of_bars = 30
        fill_color = ["gainsboro","palegoldenrod","sandybrown","indianred"]


        num_of_filled_bars = int(fraction * num_of_bars)
        for i in range(num_of_bars):
            if (i + 1) <= num_of_filled_bars:
                color = fill_color[1]
                opacity = .7
            else:
                color = fill_color[0]
                opacity = .4

            currentBar = QTHelper.MakeColorWidget(color,opacity)
            self.bar_layout.addWidget(currentBar,stretch=1)

        section = int(np.floor(fraction * (len(charecter.loadingSectionLabels) -2))) + 1

        self.progressText.setText(str(self.progress) + " Loading " + charecter.loadingSectionLabels[section])
        







    


    