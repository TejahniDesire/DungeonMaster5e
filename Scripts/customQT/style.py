# from PyQt5.QtGui import QFont
from PyQt5.QtGui import (
    QPalette, QColor, QFont, QIcon
)


LabelFont1 = QFont('Times', 15, QFont.Decorative)

LabelFont2 = QFont('Times', 12, QFont.Decorative)  # Attributes
LabelFont2p5 = QFont('Times', 11, QFont.Decorative)  # Skills
LabelFont3 = QFont('Times', 10, QFont.Decorative)  # Skills
LabelFontBigBold = QFont('Times', 15, QFont.Bold)  # Skills
LabelFontSmallBold = QFont('Times', 13, QFont.Decorative)  # Skills

ItemLabelFont = QFont('Times', 14, QFont.Decorative)

# Colors
main_highlight = "darkred"
secondary_higlight = "crimson"

main_confirm = "green"
secondary_confirm = "darkgreen"
# StyleSheets_______________________________________________________________________________________
TabButtonSheet = "QPushButton {color: white}"
TabButtonSheet1 = ("QPushButton {background-color: #3e3e42;color: white;  border-radius: 15px}"
                   "QPushButton:hover {color: white; background-color: " + main_highlight + "}"
                   "QPushButton:pressed {color: white; background-color: " + secondary_higlight +"}"
                   )
TabButtonSheet2 = ("QPushButton {color: white}"
                   "QPushButton:hover {color: white; background-color: " + main_highlight + "}"
                   "QPushButton:pressed {color: white; background-color: " + secondary_higlight +"}"
                   )
SubButtonSheet = ("QPushButton {color: white; background-color: grey; border-radius: 9px} "
                  "QPushButton:pressed {color: white; background-color: darkgrey}"
                  "QPushButton:hover {color: white; background-color: " + main_highlight + "}"
                  )

SubCheckedSheet = ("QCheckBox {color: white; background-color: grey; border-radius: 9px} "
                   "QCheckBox:pressed {color: white; background-color: darkgrey}"
                   "QCheckBox:hover {color: white; background-color: darkred}"
                   )

DarkGreyLabel = "QLabel {background-color: black;color: white}"
GreyLabel = ("QLabel {background-color: #3e3e42;color: white;  border-radius: 3"
             "px}")

Attacklabel =  "QLabel {background-color: #3e3e42;color: white}"

ItemFrame = ("QFrame {border-radius: 15px}"
             # "QFrame:hover {color: white; background-color: " + main_highlight + "}"
             )
ItemInnerLabel = ("QLabel {background-color: #3e3e42;color: white;  border-radius: 15px}"
                  "QLabel:pressed {color: white; background-color: darkgrey}"
                  "QLabel:hover {color: white; background-color: " + secondary_higlight + "}"
                  )

ItemEditButton = (
                "QPushButton {border-radius: 15px;background-color: gray}"
                "QPushButton:hover {color: white; background-color: " + main_highlight + "}"
                "QPushButton:pressed {color: white; background-color: " + secondary_higlight +"}"
                  )

ConfirmEditButton = (
                "QPushButton {border-radius: 15px;background-color: gray}"
                "QPushButton:hover {color: white; background-color: " + main_confirm + "}"
                "QPushButton:pressed {color: white; background-color: " + secondary_confirm +"}"
                  )

#  Encumberance Style__________________________________________________________________
