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
    QCheckBox,
    QFrame,
    QSizePolicy,
    QTextEdit,
    QLineEdit,
)
from PyQt5.QtGui import (
    QPalette,
    QColor,
    QFont,
)
from PyQt5.QtCore import (
    QSize
)


from PyQt5 import QtCore, Qt
import qdarktheme
import ruleTools as DT
from functools import partial

from Scripts import style, appHelperTools, charManagers, imageURLS
import numpy as np

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


class AddWindow(QWidget):

    def __init__(self,tinventory:charManagers.Inventory,ATinventory:charManagers.AttackInventory,update_func):
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
        appHelperTools.deleteItemsOfLayout(self.stacked_proper)

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
                    current_page_left_layout.addWidget(appHelperTools.ShopItemLabel(items[j],self.ATinventory,self.update_func), k, 0)
                    j += 1

            for k in range(num_per_column):
                if j < num_of_items:
                    current_page_right_layout.addWidget(appHelperTools.ShopItemLabel(items[j],self.ATinventory,self.update_func), k, 0)
                    j += 1

            if i > 0:
                left_button = appHelperTools.CreateTabButton(self.switch_tab, i - 1, style.LabelFont2, style.TabButtonSheet1, "<-")
                current_page_button_layout.addWidget(left_button,alignment=QtCore.Qt.AlignBottom)

            if i < num_of_pages - 1:
                right_button = appHelperTools.CreateTabButton(self.switch_tab, i + 1, style.LabelFont2, style.TabButtonSheet1, "->")
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

        cancel_search = appHelperTools.CreateGenButton(
            stylesheet=style.ItemEditButton,
            icon_url=imageURLS.XUrl,
            icon_size=QtCore.QSize(20, 20),
            function_list=[partial(self.searchbar.setText,''),self.update]
        )

        filter_button = appHelperTools.CreateGenButton("Filters",style.LabelFont2,style.TabButtonSheet2,
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
        alpha = appHelperTools.CreateGenButton("Alphabetical",style.LabelFont2,sorting_button_style,checkbox=True)
        weight = appHelperTools.CreateGenButton("Weight", style.LabelFont2,sorting_button_style,checkbox=True)
        typet = appHelperTools.CreateGenButton("Category", style.LabelFont2,sorting_button_style,checkbox=True)
        cost = appHelperTools.CreateGenButton("Cost", style.LabelFont2,sorting_button_style,checkbox=True)
        amount = appHelperTools.CreateGenButton("Amount", style.LabelFont2,sorting_button_style,checkbox=True)
        reversal = appHelperTools.CreateGenButton("Reverse", style.LabelFont2,
                                                  sorting_button_style,partial(self.reverse_order),checkbox=True)

        checkboxes = {
            "name":alpha,
            "weight":weight,
            "type":typet,
            "cost":cost,
            "amount":amount,
        }

        for key in checkboxes:
            appHelperTools.ConnectButtonCLicked(checkboxes[key], partial(self.change_order,key,checkboxes))

        filter_layout.addWidget(alpha)
        filter_layout.addWidget(typet)
        filter_layout.addWidget(amount)
        filter_layout.addWidget(cost)
        filter_layout.addWidget(weight)
        filter_layout.addWidget(reversal)

        self.filter_widget.setWindowTitle('Filter')

        self.filter_widget.show()
