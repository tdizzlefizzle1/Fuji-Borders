import cv2
import os

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
IMAGE_DIR = os.path.join(CURRENT_DIR, "Images")
BORDER_DIR = os.path.join(CURRENT_DIR, "New-Images")


def add_border(i):
    image = cv2.imread(os.path.join(IMAGE_DIR, i))
    border_image = cv2.copyMakeBorder(image, 150, 150, 150, 150, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    return border_image


def save_image(file_name, image):
    print(file_name)
    border_path = os.path.join(BORDER_DIR, file_name)
    cv2.imwrite(border_path, image)


if __name__ == '__main__':
    if not os.path.isdir(BORDER_DIR):
        os.mkdir(BORDER_DIR)

    for i in os.listdir(IMAGE_DIR):
        image = add_border(i)
        save_image(i, image)
