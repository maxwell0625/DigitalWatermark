from PIL import Image
import cv2


def read_img_by_pillow(path):
    img = Image.open(path)
    return img, (img.size[0], img.size[1])

def read_img_by_cv2(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img, img.shape
