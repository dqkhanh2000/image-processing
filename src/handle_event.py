from os.path import expanduser
from PyQt5.QtWidgets import QFileDialog
import cv2
from src.lib import get_position_cursor_on_label, process_image
from src.segment_image import *
import numpy as np

app_gui = None
orig_image = []
current_image = []
cropped_image = []
background_image = None

def set_gui(gui):
    global app_gui
    app_gui = gui

def open_image():
    global orig_image, current_image
    fname = QFileDialog.getOpenFileName(None, 'Open file', expanduser("~"), "Image files (*.jpg *.png *.gif)")
    if len(fname[0]) == 0:
        return    
    orig_image = cv2.imread(fname[0])
    app_gui.set_image_root(orig_image)
    current_image, mask = bokeh_process(orig_image)
    app_gui.set_image_processed(current_image)
    app_gui.set_image_bg_separation(mask)


def bokeh_process(image):
    mask = get_mask_from_image(image)
    display_mask = get_mask_predict_from_image(image)
    image = get_object_from_image(image, mask=mask)
    return (image, display_mask)


def save_image():
    fname = QFileDialog.getSaveFileName(None, "Save image as", expanduser("~"), "Image files (*.jpg *.png *.jpeg *.tif)")
    if len(fname[0]) == 0:
        return
    cv2.imwrite(fname[0], current_image)



