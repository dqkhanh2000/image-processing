    # """
    #     Created by dqkhanh2000
    # """
from os.path import expanduser
from PyQt5.QtWidgets import QFileDialog
import cv2
from src.lib import process_image, cal_histogram
import numpy as np
app_gui = None
orig_image = None
filter_value = {
    "contrast" : 0,
    "brightness" : 0,
    "hue" : 0,
    "saturation" : 0,
    "blur" : 0,
    "blur_method" : "average",
    "is_gray" : False,
    "is_invert" : False
}

def exec_image():
    current_image = process_image(orig_image, contrast_value=filter_value["contrast"],
                                    brightness_value=filter_value["brightness"],
                                    hue_value=filter_value["hue"],
                                    saturation_value=filter_value["saturation"],
                                    blur_value=filter_value["blur"],
                                    blur_method=filter_value["blur_method"], 
                                    is_gray=filter_value["is_gray"],
                                    is_invert=filter_value["is_invert"])
    app_gui.set_image_root(orig_image)
    app_gui.set_image_processed(current_image)
    # app_gui.set_histogram_image(cal_histogram(current_image))

def set_gui(gui):
    global app_gui
    app_gui = gui

def open_image():
    global orig_image
    fname = QFileDialog.getOpenFileName(None, 'Open file', expanduser("~"), "Image files (*.jpg *.png *.gif)")
    if len(fname[0]) == 0:
        return    
    orig_image = cv2.imread(fname[0])
    # orig_image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
    exec_image()

def release(filter, value = 0):
    pass

def change_filter(filter, value):
    filter_value[filter] = value
    exec_image()

def invert(state):
    filter_value["is_invert"] = (state == 2)
    exec_image()

def gray(state):
    filter_value["is_gray"] = (state == 2)
    exec_image()

def mask_threshsold(value):
    pass

def repaint_mask():
    pass

def threshsold(value):
    pass

def edge_detection(state):
    mask = np.array([[-1, -2, -1],
                    [0, 0, 0],
                    [1, 2, 1],
                ])
    img = []
    if state == 2:
        if len(orig_image.shape) == 3:
            app_gui.ckb_gray.setChecked(True)
        img = cv2.filter2D(orig_image, -1, mask)
        # img = cv2.Canny(orig_image, 30, 100)
    else:
        img = orig_image
    
    img = np.absolute(img)
    img = np.uint8(img)
    new_image = np.uint8(img)
    app_gui.set_image_processed(new_image)

def sharpen(state):
    mask = np.array([[0, 1, 0],
                    [1, -4, 1],
                    [0, 1, 0],
                ])
    img = []
    if state == 2:
        img = cv2.filter2D(orig_image, -1, mask)
        img = np.subtract(orig_image, img)
        new_image = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        app_gui.set_image_processed(new_image)

def undo():
    pass

def change_bokeh_option(radio_button):
    pass

def save_image():
    fname = QFileDialog.getSaveFileName(None, "Save image as", expanduser("~"), "Image files (*.jpg)")
    if len(fname[0]) == 0:
        return
    execute.save_image(fname[0])

def crop_image():
    pass

def draw_image():
    pass