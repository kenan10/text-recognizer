from PIL import Image
import PyQt5.QtGui as QtGui
from numpy.lib.npyio import save

class Rocr(object):
    def __init__(self, image_path):
        super().__init__()
        self.image_pil = Image.open(image_path)
        self.angel = 0

        self.crop_points = []

    def get_pixmap(self):
        image_pil = self.image_pil

        if image_pil.mode == "RGB":
            r, g, b = image_pil.split()
            image_pil = Image.merge("RGB", (b, g, r))
        elif  image_pil.mode == "RGBA":
            r, g, b, a = image_pil.split()
            image_pil = Image.merge("RGBA", (b, g, r, a))
        elif image_pil.mode == "L":
            image_pil = image_pil.convert("RGBA")

        image_pil2 = image_pil.convert("RGBA")
        data = image_pil2.tobytes("raw", "RGBA")

        qim = QtGui.QImage(data, image_pil.size[0], image_pil.size[1], QtGui.QImage.Format_ARGB32)
        pixmap = QtGui.QPixmap.fromImage(qim)

        self.pixmap = pixmap
        return pixmap

    def rotate (self, angel):
        self.image_pil = self.image_pil.rotate(angel)
        self.angel += -angel
        
        if self.angel >= 360:
            self.angel = 0
        
        print(f"Rotated on {-angel} degrees")

    def save(self, path):
        self.image_pil.save(path)

    def add_crop_point(self, point_coords):
        if len(self.crop_points) < 4:
            self.crop_points.append(point_coords)

        print("added")
        