import cv2
import os
from PIL import Image
import lensfunpy
import piexif

CONVERT_PNG = False

CAMERA_MAKER = 'FUJIFILM'
CAM_MODEL = 'X-T4'
LENS_MAKER = 'Viltrox'
LENS_MODEL = '23mmF1.4XM'

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
IMAGE_DIR = os.path.join(CURRENT_DIR, "Images")
BORDER_DIR = os.path.join(CURRENT_DIR, "New_Images")
PNG_DIR = os.path.join(CURRENT_DIR, "PNG_Converted")

DB = lensfunpy.Database()
CAM = DB.find_cameras(CAMERA_MAKER, CAM_MODEL)[0]
LENS = DB.find_lenses(CAM, LENS_MAKER, LENS_MODEL)[0]

focal_length = LENS.min_focal
distance = .3
width = 0
height = 0
aperture = ''
EXIF = ''


# LENS_LIST = str(LENS)[5:].split('; ')
# res_dict = {}
# for i in LENS_LIST:
#    stuff = i.split(': ')
#    # print(stuff)
#    key, value = stuff
#    # print(key, value)
#    res_dict[key] = value


def convert_png():
    if not os.path.isdir(PNG_DIR):
        os.mkdir(PNG_DIR)

    for i in os.listdir(IMAGE_DIR):
        file = cv2.imread(os.path.join(IMAGE_DIR, i))
        new_file_name = i.split('.')
        print(os.path.join(PNG_DIR, new_file_name[0] + '.PNG'))
        cv2.imwrite(os.path.join(PNG_DIR, new_file_name[0] + '.PNG'), file)


def read_exif(i):
    global EXIF, aperture
    image_path = os.path.join(IMAGE_DIR, i)
    EXIF = piexif.load(image_path)
    aperture = EXIF['Exif'][33437]
    aperture = aperture[0] / aperture[1]
    print(aperture)
    # pillow_image = Image.open(os.path.join(IMAGE_DIR, image))
    # EXIF = pillow_image.info['exif']


def transplant_exif(i):
    image_path = os.path.join(IMAGE_DIR, i)
    border_path = os.path.join(BORDER_DIR, i)
    piexif.transplant(image_path, border_path)

def check_orientation(image):
    orientation = EXIF["0th"].pop(piexif.ImageIFD.Orientation)
    if orientation == 8:
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    return image

def read_image(image):
    global height, width
    new_image = cv2.imread(os.path.join(IMAGE_DIR, image))
    height, width = new_image.shape[0], new_image.shape[1]
    return new_image


def vignette_correct(image):
    mod = lensfunpy.Modifier(LENS, CAM.crop_factor, width, height)
    mod.initialize(focal_length, 2.8, distance)
    mod.apply_color_modification(image)
    return image


def add_border(image):
    border_image = cv2.copyMakeBorder(image, 250, 250, 250, 250, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    return border_image


def save_image(file_name, image):
    border_path = os.path.join(BORDER_DIR, file_name)
    cv2.imwrite(border_path, image)
    # pil_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # pil_image = Image.fromarray(pil_image)
    # pil_image.save(border_path, 'JPEG', exif=EXIF, quality=100)


if __name__ == '__main__':
    if not os.path.isdir(BORDER_DIR):
        os.mkdir(BORDER_DIR)

    if CONVERT_PNG:
        convert_png()

    for i in os.listdir(IMAGE_DIR):
        print(i)
        image = read_image(i)
        read_exif(i)
        if aperture == 1.4:
            new_image = vignette_correct(image)
            print("vignette corrected")
        else:
            new_image = image
        new_new_image = add_border(new_image)
        new_new_new_image = check_orientation(new_new_image)
        save_image(i, new_new_new_image)
        transplant_exif(i)
