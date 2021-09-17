import sys
import pytesseract
from PIL import Image

class Detect(object):
    def __init__(self, image):
        super(Detect, self).__init__()

        self.image = image
        self.tesseract_config = r'--oem 3 --psm 13'

    def to_text(self, rotate_deg, crop_coords):

        # Rotate and crop
        self.image_rot = self.image.rotate(rotate_deg)
        self.image_cropped = self.image_rot.crop(crop_coords)
        
        # To text
        self.text = pytesseract.image_to_string(self.image_cropped, config=self.tesseract_config)

        try:
            self.in_voltage = int(self.text[slice(0, 3)])
        except ValueError:
            self.in_voltage = False

        try:
            self.amper = int(self.text[5])
        except ValueError:
            self.amper = False

        try:
            self.gear = int(self.text[slice(self.text.find("/") + 1, self.text.find("/") + 3)].strip(" "))
        except ValueError:
            self.gear = False

        try:
            self.out_voltage = int(self.text[slice(len(self.text) - 6, len(self.text) - 3)])
        except ValueError:
            self.amper = False
 
        return self

if __name__ == "__main__":
    image_path = sys.argv[1]
    print(image_path)

    data = { 
        "rotation": -89,
        "crop_points": [71, 121, 307, 153]
    }

    with Image.open(image_path) as image:
        image = image

        indicators = Detect(image, data)
        indicators.to_text()
        indicators.image_cropped.show()
        print(indicators.text)