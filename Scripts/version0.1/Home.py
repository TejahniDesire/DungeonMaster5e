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

import qdarktheme

# Local_________________________________________________________________ 

import ruleTools,objectHelperTools,imageURLS

import objectsDnD,charManagers,charecter,style,objectsDnD,Reading,EZPaths
import appHelperTools
import pyqt5_Custom_Windows 
import pyqt5_Custom 
import tabs









