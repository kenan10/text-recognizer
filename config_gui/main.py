from PyQt5.Qt import *
import sys

from rocr import Rocr
from gui import Gui

class Main(object):
    def __init__(self):
        super(Main, self).__init__()
        self.image = Rocr("data/img/volt_2021_08_20_12_48_56.jpeg")
        self.step = 90
        
    def setupGui(self):
        self.app = QApplication(sys.argv)
        self.gui = Gui()
        self.gui.show()

        self.gui.left_btn.clicked.connect(lambda: self.rotate(+self.step))
        self.gui.right_btn.clicked.connect(lambda: self.rotate(-self.step))
        self.gui.load_image(self.image.get_pixmap())

        self.gui.done_btn.clicked.connect(lambda: self.image.save("data/temp/result.jpeg"))

        self.gui.crop_btn.clicked.connect(self.click_crop_btn)

        sys.exit(self.app.exec_())

    def rotate(self, angel):
        self.image.rotate(angel)
        pixmap = self.image.get_pixmap()
        self.gui.load_image(pixmap)

    def click_crop_btn(self):
        self.gui.image.clicked.connect(self.add_crop_point)
        self.gui.show_amount_of_left_points(4)

    def add_crop_point(self):
        self.image.add_crop_point(self.gui.image.click_coords)
        print(self.image.crop_points)

        print(len(self.image.crop_points))
        amount_of_left_points = 4 - len(self.image.crop_points)
        self.gui.show_amount_of_left_points(amount_of_left_points)

main = Main()
main.setupGui()