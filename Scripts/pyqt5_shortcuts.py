from Home import *

def create_frame(top_label_str:str, bottom_label_str:str):
    frame = QFrame()
    frame.setFrameShape(QFrame.Panel)
    frame.setMaximumHeight(100)

    layout = QVBoxLayout(frame)

    bottom_label = QLabel()
    bottom_label.setText(bottom_label_str)

    layout.addWidget(create_top_label(top_label_str), alignment=QtCore.Qt.AlignCenter)
    layout.addWidget(bottom_label, alignment=QtCore.Qt.AlignCenter)

    return frame, bottom_label


def create_top_label(string:str):
    top_label = QLabel()
    top_label.setText(string)
    top_label.setFont(style.LabelFont2)
    return top_label