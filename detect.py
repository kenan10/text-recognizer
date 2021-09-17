import sys
import pytesseract
from PIL import Image

class Detect(object):
    def __init__(self, image, data):
        super(Detect, self).__init__()

        self.image = image
        self.rotation = data["rotation"]
        self.crop_coords = data["crop_points"]
        self.tesseract_config = r'--oem 3 --psm 13'

    def to_text(self):
        # Rotate and crop
        self.image_rot = self.image.rotate(self.rotation)
        self.image_cropped = self.image_rot.crop(self.crop_coords)
        
        # To text
        self.text = pytesseract.image_to_string(self.image_cropped, config=self.tesseract_config)

        self.in_voltage = int(self.text[slice(0, 3)])
        self.amper = int(self.text[5])
        self.gear = int(self.text[slice(self.text.find("/") + 1, self.text.find("/") + 3)].strip(" "))
        self.out_voltage = int(self.text[slice(len(self.text) - 6, len(self.text) - 3)])

        return self

if __name__ == "__main__":
    image_path = sys.argv[1]
    print(image_path)

    with Image.open(image_path) as image:
        image = image
    data = { 
        "rotation": -89,
        "crop_points": [71, 121, 307, 153]
    }

    indicators = Detect(image, data)
    indicators.to_text()
    print(indicators.in_voltage)