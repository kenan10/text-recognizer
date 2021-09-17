import json
import os

from PIL import Image
from detect import Detect

with open("config.json", "r") as read_file:
    data = json.load(read_file)

rotation = data["rotation"]
crop_points = data["crop_points"]

image_folder = data["image_folder"]
finnaly_folder = data["finnaly_folder"]

tesseract_config = r'--oem 3 --psm 13'

def check_out_value(value, last_value):
    if type(value) == int:
        return value
    else:
        return last_value

for image_name in os.listdir(image_folder):
    if image_name.find("checked") == -1:
        print("1")
        image_path = image_folder + image_name

        folder_name = image_name[slice(image_name.find("volt_") + 5, image_name.find("."))]
        os.mkdir(finnaly_folder + folder_name)

        with Image.open(image_path) as image:
            image = Detect(image)
            out_data = image.to_text(rotation, crop_points)

            out_data.image_cropped.save(finnaly_folder + folder_name + "/cropped.jpeg")
            out_data.image.save(finnaly_folder + folder_name + "/input.jpeg")
            with open(finnaly_folder + folder_name + "/text.txt", "w") as file:
                file.write(out_data.text)

            try:
                with open("data/last.json", "r") as file:
                    last_json = json.load(file)

                with open("data/last.json", "w") as file:
                    json.dump({
                        "in_voltage": check_out_value(out_data.in_voltage, last_json["in_voltage"]),
                        "amper": check_out_value(out_data.amper, last_json["amper"]),
                        "gear": check_out_value(out_data.gear, last_json["gear"]),
                        "out_voltage": check_out_value(out_data.out_voltage, last_json["out_voltage"])
                    }, file)
                print("done!")
            except BaseException:
                with open("data/last.json", "w") as file:
                    json.dump({
                        "in_voltage": 0,
                        "amper": 0,
                        "gear": 0,
                        "out_voltage": 0
                    }, file)

        # Mark as checked
        # os.rename(image_path, image_folder + image_name[slice(image_name.find("."))] + "_checked" + ".jpeg")
        print(image_folder + image_name[slice(image_name.find("."))] + "_checked" + ".jpeg")