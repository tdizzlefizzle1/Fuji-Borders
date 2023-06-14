import cv2
import os
import numpy as np
import lensfunpy

CAMERA_MAKER = 'FUJIFILM'
CAM_MODEL = 'X-T5'
LENS_MAKER = 'Viltrox'
LENS_MODEL = '23mmF1.4XM'

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
IMAGE_DIR = os.path.join(CURRENT_DIR, "Images")
BORDER_DIR = os.path.join(CURRENT_DIR, "New-Images")
# TEMP_DIR = os.path.join(CURRENT_DIR, "temp")

DB = lensfunpy.Database()
CAM = DB.find_cameras(CAMERA_MAKER, CAM_MODEL)[0]
LENS = DB.find_lenses(CAM, LENS_MAKER, LENS_MODEL)[0]

focal_length = LENS.min_focal
distance = .3
width = 0
height = 0


# LENS_LIST = str(LENS)[5:].split('; ')
# res_dict = {}
# for i in LENS_LIST:
#    stuff = i.split(': ')
#    # print(stuff)
#    key, value = stuff
#    # print(key, value)
#    res_dict[key] = value


# def convert_png():
#    if not os.path.isdir(TEMP_DIR):
#        os.mkdir(TEMP_DIR)
#
#    for i in os.listdir(IMAGE_DIR):
#        file = cv2.imread(os.path.join(IMAGE_DIR, i))
#        new_file_name = i.split('.')
#        print(os.path.join(TEMP_DIR, new_file_name[0] + '.PNG'))
#        cv2.imwrite(os.path.join(TEMP_DIR, new_file_name[0] + '.PNG'), file)

def read_image(image):
    global height, width
    new_image = cv2.imread(os.path.join(IMAGE_DIR, image))
    height, width = new_image.shape[0], new_image.shape[1]
    return new_image


def vignette_correct(image):
    mod = lensfunpy.Modifier(LENS, CAM.crop_factor, width, height)
    mod.initialize(focal_length, 2.4, distance)
    mod.apply_color_modification(image)

    return image


def add_border(image):
    border_image = cv2.copyMakeBorder(image, 250, 250, 250, 250, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    return border_image


def save_image(file_name, image):
    print(file_name, "\n")
    border_path = os.path.join(BORDER_DIR, file_name)
    cv2.imwrite(border_path, image)


if __name__ == '__main__':
    if not os.path.isdir(BORDER_DIR):
        os.mkdir(BORDER_DIR)

    for i in os.listdir(IMAGE_DIR):
        print(i)
        image = read_image(i)
        # write statement to check for whether the exif data is of 1.4 aperture
        new_image = vignette_correct(image)
        new_new_image = add_border(new_image)
        save_image(i, new_new_image)
