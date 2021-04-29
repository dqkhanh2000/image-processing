import cv2
from gui import ImageProcessing
import numpy as np
from lib import *
GRAY_MODE = True
root_image_path = ''
root_image = []

app_gui = None

def get_gui():
    global app_gui
    if app_gui == None:
        app_gui = ImageProcessing()
    return app_gui

def cal_contrast(value):
    g = 1
    if value < 50:
        g =(60-value)/10
    else:
        g = (100-(value-50)*2)/100

    print(root_image.shape)
    img = gamma_gray(root_image, g, 1)
    new_image = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    app_gui.set_image_processed(new_image)
    app_gui.set_histogram_image(cal_histogram(new_image))
    


def load_image_from_file():
    global root_image
    root_image = cv2.imread(root_image_path)
    width = int(root_image.shape[1]/3)
    height = int(root_image.shape[0] / 3)
    dim = (width, height)
    
    # resize image
    root_image = cv2.resize(root_image, dim, interpolation = cv2.INTER_AREA)
    # img = gamma_gray(root_image, 0.4, 1)
    # new_image = cv2.normalize(img,  None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    # print(root_image[0][0], img[0][0], new_image[0][0])
    # fig = plt.figure(figsize=(16, 9))
    # (ax1, ax2) = fig.subplots(2, 1)
    # ax1.imshow(root_image[..., ::-1])
    # ax2.imshow(new_image[..., ::-1])
    # plt.show()
    app_gui.set_image_root(root_image)
    app_gui.set_image_processed(root_image)
    app_gui.set_histogram_image(cal_histogram(root_image))