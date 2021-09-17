import json
import os
from shlex import join
from shutil import copyfile
import time

import pytesseract
from PIL import Image

with open("config.json", "r") as read_file:
    data = json.load(read_file)

rotation = data["rotation"]
crop_points = data["crop_points"]

image_folder = data["image_folder"]
finnaly_folder = data["finnaly_folder"]

tesseract_config = r'--oem 3 --psm 13'

images_pathes = []
for image_name in os.listdir(image_folder):
    images_pathes.append(image_folder + image_name)

with open("data/last.json", "w") as file:
    json.dump({
        "in_voltage": 0,
        "amper": 0,
        "gear": 0,
        "out_voltage": 0
    }, file)

def to_text(rot, crop_coords, image_path, finnaly_directory):
    showed = False

    with Image.open(image_path) as image:
        # Rotate and crop
        image_rot = image.rotate(rot)
        image_cropped = image_rot.crop(crop_coords)
        image_cropped.save(f"data/finnaly/{finnaly_directory}/cropped.jpeg")

        if not showed:
            # image_cropped.show()
            time.sleep(0.5)
            showed = True
        
        # To text
        text = pytesseract.image_to_string(image_cropped, config=tesseract_config)

        with open("data/last.json", "r") as file:
            last_json = json.load(file)

        try:
            in_voltage = int(text[slice(0, 3)])

            if in_voltage > 230 or in_voltage < 180:
                in_voltage = last_json["in_voltage"]
        except ValueError:
            in_voltage = last_json["in_voltage"]

        try:
            amper = int(text[5])

            if amper > 70 or amper < 1:
                amper = last_json["amper"]
        except ValueError:
            amper = last_json["amper"]
        
        try:
            gear = int(text[slice(text.find("/") + 1, text.find("/") + 3)].strip(" "))

            if gear < 1 or gear > 16:
                gear = last_json["gear"]
        except ValueError:
            gear = last_json["gear"]
        
        try:
            out_voltage = int(text[slice(len(text) - 6, len(text) - 3)])

            if out_voltage < 210 or out_voltage > 230:
                out_voltage = last_json["out_voltage"]
        except ValueError:
            out_voltage = last_json["out_voltage"]

        with open("data/last.json", "w") as file:
            json.dump({
                "in_voltage": in_voltage,
                "amper": amper,
                "gear": gear,
                "out_voltage": out_voltage
            }, file)

        with open(f"data/finnaly/{finnaly_directory}/volt.txt", "w") as file:
            file.write(text)

def manage_files(images_pathes):
    if images_pathes:
        for image_path in images_pathes:
            if image_path[image_path.find(".") - 1] != "c":
                # Make directory
                name_of_file_slice = slice(image_path.find("volt"), len(image_path))
                name_of_file = image_path[name_of_file_slice]

                format_slice = slice(name_of_file.find("."))

                name_of_dir_slice = slice(name_of_file.find("volt")+5, len(name_of_file)-5)
                name_of_dir = name_of_file[name_of_dir_slice]

                os.mkdir(f"data/finnaly/{name_of_dir}")
                copyfile(image_path, f"data/finnaly/{name_of_dir}/{name_of_file}")
                #########################################################################

                to_text(rotation, crop_points, image_path, name_of_dir)

                # Mark checked files
                # os.rename(image_path, image_path[format_slice]+"c"+".jpeg")
                print(image_path[format_slice]+"c"+".jpeg")
manage_files(images_pathes)