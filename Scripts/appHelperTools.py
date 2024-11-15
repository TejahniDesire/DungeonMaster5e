import sys

import numpy as np
from PyQt5.QtWidgets import (
    QApplication,
    QStackedLayout,
    QMainWindow,
    QWidget,
    QCheckBox,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame, QGraphicsOpacityEffect, QLineEdit, QSpinBox
)
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon
from PyQt5 import QtCore, Qt
import qdarktheme
from functools import partial

from PyQt5.sip import delete

from Scripts import objectsDnD, style, charManagers, ruleTools, imageURLS, pyObjects


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def CreateTabButton(switch_tab_function, tab_value: int, label_font, style_sheet: str, label: str):
    tab_button = QPushButton()
    tab_button.setText(label)
    tab_button.clicked.connect(partial(switch_tab_function, tab_value))
    tab_button.setFont(label_font)
    tab_button.setStyleSheet(style_sheet)
    return tab_button


def CreateGenButton(text=None, font=None, stylesheet=None, function=None, function_list=None, minWidth=None,
                    minHeight=None, icon_url=None, icon_size: QIcon = None,checkbox=False,):
    if checkbox:
        button = QCheckBox()

    else:
        button = QPushButton()
    if text is not None:
        button.setText(text)

    if font is not None:
        button.setFont(font)

    if stylesheet is not None:
        button.setStyleSheet(stylesheet)

    if minHeight is not None:
        button.setMinimumHeight(minHeight)

    if minWidth is not None:
        button.setMinimumWidth(minWidth)

    if function is not None:
        button.clicked.connect(function)

    if icon_url is not None:
        button.setIcon(QIcon(icon_url))
        if icon_size is not None:
            button.setIconSize(icon_size)

    if function_list is not None:
        for i in range(len(function_list)):
            button.clicked.connect(function_list[i])

    return button


def ConnectButtonCLicked(button,function=None,function_list=None):
    if function is not None:
        button.clicked.connect(function)
    elif function_list is not None:
        for i in range(len(function_list)):
            button.clicked.connect(function_list[i])
    else:
        raise ValueError("No Function given")


def CreateSeperator():
    separator = QFrame()
    separator.setFrameShape(QFrame.HLine)
    return separator


def CreateVSeperator():
    separator = QFrame()
    separator.setFrameShape(QFrame.VLine)
    return separator


def CreateLabel(text: str, font: QFont, style_sheet=None):
    label = QLabel()
    label.setText(text)
    label.setFont(font)

    if style_sheet is not None:
        label.setStyleSheet(style_sheet)
    return label


def deleteItemsOfLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                deleteItemsOfLayout(item.layout())


class CustomQSpinBox(QSpinBox):
    def __init__(self, function, operation: str):
        super().__init__()
        self.function = function
        self.operation = operation

        if operation == "add":
            self.widget_for_info = {"addAmount": self}
        elif operation == "subtract":
            self.widget_for_info = {"subtractAmount": self}

    def focusOutEvent(self, QFocusEvent):
        super(CustomQSpinBox, self).focusOutEvent(QFocusEvent)
        self.function(self.operation, self.widget_for_info)

    def mousePressEvent(self, QMouseEvent):
        super(CustomQSpinBox, self).mousePressEvent(QMouseEvent)
        self.function(self.operation, self.widget_for_info)


class ItemLabel(QFrame):

    def __init__(self, item: objectsDnD.Item, ATinventory: charManagers.AttackInventory = None, update_func=None):
        super().__init__()
        self.ATinventory = ATinventory
        self.update_func = update_func
        self.layout = QHBoxLayout(self)
        self.setFrameShape(QFrame.Panel)
        # self.setMaximumSize(100,50)
        self.item = item
        self.text_label = QLabel()
        self.button_layout = QHBoxLayout()

        # Default
        self.text_label.setFont(style.ItemLabelFont)
        self.text_label.setText(self.create_text())
        self.text_label.setStyleSheet(style.GreyLabel)
        self.layout.addWidget(self.text_label, stretch=3)
        self.layout.addLayout(self.button_layout)
        if self.ATinventory is None:
            self.create_button_layout()

        # self.setMaximumWidth(300)
        self.setFixedHeight(80)
        self.setStyleSheet(style.ItemFrame)
        self.edit_button_layout = None

    def default_state_creation(self):
        self.text_label.setFont(style.ItemLabelFont)
        self.text_label.setText(self.create_text())
        self.text_label.setStyleSheet(style.GreyLabel)
        self.layout.addWidget(self.text_label, stretch=3)
        self.layout.addLayout(self.button_layout)
        self.create_button_layout()

    def change_amount(self, operation: str):
        self.clear_button_layout()
        self.layout.addLayout(self.button_layout)
        # spinbox = CustomQSpinBox(self.refresh_edit_layout,operation)

        spinbox = QSpinBox()
        spinbox.setMaximum(1000000)
        amount = pyObjects.ReferenceNumber(0, is_int=True)

        spinbox.valueChanged.connect(partial(amount.setValue))

        self.button_layout.addWidget(spinbox)

        self.edit_button_layout = QHBoxLayout()
        self.button_layout.addLayout(self.edit_button_layout)

        # self.refresh_edit_layout(operation,widget_for_info)
        # self.create_cancel_button()
        # self.refresh_edit_layout('add',widget_for_info)
        function2 = partial(self.refresh_button_layout)
        if operation == 'add':
            # amount = int(widget_for_info['addAmount'].value())
            if self.ATinventory is None:
                function1 = partial(pyObjects.preform, [self.item.add_amount], [amount.getValue])
            else:
                print("RIGHT")
                function1 = partial(pyObjects.preform, [self.ATinventory.add_attack_item, self.update_func],
                                    [self.item])

            confirm_button = CreateGenButton(
                stylesheet=style.ConfirmEditButton,
                icon_url=imageURLS.CheckUrl,
                icon_size=QtCore.QSize(20, 20),
                function_list=[function1, function2]
            )
            self.edit_button_layout.addWidget(confirm_button)

        elif operation == 'subtract':
            function1 = partial(pyObjects.preform, [self.item.safe_subtract], [amount.getValue])
            confirm_button = CreateGenButton(
                stylesheet=style.ConfirmEditButton,
                icon_url=imageURLS.CheckUrl,
                icon_size=QtCore.QSize(20, 20),
                function_list=[function1, function2]
            )
            self.edit_button_layout.addWidget(confirm_button)
        #
        cancel_button = CreateGenButton(
            stylesheet=style.ItemEditButton,
            icon_url=imageURLS.XUrl,
            icon_size=QtCore.QSize(20, 20),
            function_list=[partial(self.refresh_button_layout)]
        )
        self.edit_button_layout.addWidget(cancel_button)

        oldfunc = spinbox.keyPressEvent
        spinbox.keyPressEvent = partial(self.LinekeyPressEvent, oldfunc, function1)

    def LinekeyPressEvent(self, func, operation_function, QKeyEvent):
        func(QKeyEvent)
        if QKeyEvent.key() == QtCore.Qt.Key_Return:
            operation_function()
            self.refresh_button_layout()

    def create_cancel_button(self):
        button = CreateGenButton(
            stylesheet=style.ItemEditButton,
            icon_url=imageURLS.XUrl,
            icon_size=QtCore.QSize(20, 20),
            function_list=[partial(self.refresh_button_layout)]
        )
        self.edit_button_layout.addWidget(button)

    def create_text(self):
        text = ''
        text += self.item.get_name() + " " + str(self.item.get_amount()) + "x"
        text += "\n     "
        text += self.item.get_type() + "| "
        if self.item.get_amount() > 1:
            text += "(" + '{:,}'.format(self.item.get_amount() * self.item.get_weight()) + ")"
        text += str(self.item.get_weight()) + " lbs" + " | "
        text += str(self.item.get_cost()[0]) + " " + self.item.get_cost()[1]
        return text

    def clear_button_layout(self):
        self.text_label.deleteLater()
        self.text_label = QLabel()
        deleteItemsOfLayout(self.button_layout)
        self.button_layout = QHBoxLayout()

    def refresh_button_layout(self):
        self.text_label.deleteLater()
        self.text_label = QLabel()
        deleteItemsOfLayout(self.button_layout)
        self.button_layout = QHBoxLayout()
        self.default_state_creation()

    def create_button_layout(self):
        edit_button = CreateGenButton(stylesheet=style.ItemEditButton,
                                      icon_url=imageURLS.IconUrl, icon_size=QtCore.QSize(20, 20))

        add_button = CreateGenButton(stylesheet=style.ItemEditButton,
                                     icon_url=imageURLS.AddUrl, icon_size=QtCore.QSize(20, 20),
                                     function=partial(self.change_amount, "add"))

        minus_button = CreateGenButton(stylesheet=style.ItemEditButton,
                                       icon_url=imageURLS.MinusUrl, icon_size=QtCore.QSize(20, 20),
                                       function=partial(self.change_amount, "subtract"))

        self.button_layout.addWidget(add_button, stretch=0)
        self.button_layout.addWidget(minus_button, stretch=0)
        self.button_layout.addWidget(edit_button, stretch=0)
        self.layout.addLayout(self.button_layout)

    def update(self):
        self.text_label.setText(self.create_text())


class ShopItemLabel(ItemLabel):
    def __init__(self, item: objectsDnD.Item, ATinventory: charManagers.AttackInventory, update_func):
        super().__init__(item, ATinventory, update_func)
        self.ATinventory = ATinventory
        self.update_func = update_func
        self.create_button_layout()

    def create_button_layout(self):
        add_button = CreateGenButton(stylesheet=style.ItemEditButton,
                                     icon_url=imageURLS.AddUrl, icon_size=QtCore.QSize(20, 20),
                                     function=partial(self.addItem,self.item))

        self.button_layout.addWidget(add_button, stretch=0)
        self.layout.addLayout(self.button_layout)

    def addItem(self,item):
        self.ATinventory.add_attack_item(item)
        self.update_func()

def MakeColorWidget(color, opacity):
    widget = QFrame()

    stylesheet = ("QFrame {border-radius: 5px; background-color: " + color + "}"
                  )
    widget.setStyleSheet(stylesheet)
    # creating a opacity effect
    widget.opacity_effect = QGraphicsOpacityEffect()

    # setting opacity level
    widget.opacity_effect.setOpacity(opacity)

    # adding opacity effect to the label
    widget.setGraphicsEffect(widget.opacity_effect)

    widget.setMinimumHeight(10)
    return widget

#
#
