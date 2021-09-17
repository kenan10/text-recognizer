from PyQt5 import QtCore
from PyQt5.Qt import *
from PyQt5.QtWidgets import QLabel
import design

class Gui(QMainWindow, design.Ui_Settings):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.image = MyImage(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(50, 60, 521, 451))
        self.image.setText("")
        self.image.setScaledContents(True)
        self.image.setObjectName("image")

        self.setWindowTitle("Settings")

    def load_image(self, pixmap):
        self.image.setPixmap(pixmap)

    def show_amount_of_left_points(self, amount):
        self.left_points.setText(f"Left {amount} points")

class MyImage(QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        self.click_coords = (event.x(), event.y())
        print(self.click_coords)