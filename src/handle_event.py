    # """
    #     Created by dqkhanh2000
    # """
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

filter_value = {
    "contrast" : 0,
    "brightness" : 0,
    "hue" : 0,
    "saturation" : 0,
    "blur" : 0,
    "blur_method" : "average",
    "is_gray" : False,
    "is_invert" : False,
    "sharpen_method" : None,
    "edge_detection_method" : None,
    "threshsold" : 0}
current_mask = []

segment_value = {
    "option" : "bokeh",
    "mask_threshsold_value" : 0.5,
    "bokeh_blur_value" : 21
}

crop_x_start = -1
crop_y_start = -1

def exec_image(image = []):
    global current_image, cropped_image, background_image
    background_image = []
    if len(image) == 0:
        if len(cropped_image) == 0:
            image = orig_image
        else:
            image = cropped_image
    if len(image) == 0:
        return
    current_image = process_image(image, filter_value)
    if app_gui.bokeh_activated:
        current_image = bokeh_process(current_image)
    app_gui.set_image_processed(current_image)
    app_gui.draw_histogram(current_image)

def set_gui(gui):
    global app_gui
    app_gui = gui

def open_image():
    global orig_image
    fname = QFileDialog.getOpenFileName(None, 'Open file', expanduser("~"), "Image files (*.jpg *.png *.gif)")
    if len(fname[0]) == 0:
        return    
    orig_image = cv2.imread(fname[0])
    app_gui.set_image_root(orig_image)
    # orig_image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
    exec_image()

def change_blur_method(method):
    filter_value["blur_method"]

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
    global orig_image, current_mask
    current_mask = get_mask_from_image(orig_image, threshold_value=value/100.0)
    exec_image()

def edge_detection(state):
    if state == 2:
        filter_value["edge_detection_method"] = app_gui.cbb_edge_detection.currentText()
    else:
        filter_value["edge_detection_method"] = None
    exec_image()

def sharpen(state):
    if state == 2:
        filter_value["sharpen_method"] = app_gui.cbb_sharpen.currentText()
    else:
        filter_value["sharpen_method"] = None
    exec_image()

def combobox_sharpen_change(i):
    if app_gui.ckb_sharpen.isChecked():
        filter_value["sharpen_method"] = app_gui.cbb_sharpen.currentText()
        exec_image()

def combobox_edge_detection_change(i):
    if app_gui.ckb_edge_detection.isChecked():
        filter_value["edge_detection_method"] = app_gui.cbb_edge_detection.currentText()
        exec_image()

def bokeh_process(image):
    global current_mask, background_image
    try:
        if current_mask is None or current_mask == []:
            current_mask = get_mask_from_image(current_image, threshold_value=segment_value["mask_threshsold_value"])
        if segment_value["option"] == "bokeh":
            blur_sigma = segment_value["bokeh_blur_value"]/10.0
            if segment_value["bokeh_blur_value"] % 2 == 0:
                segment_value["bokeh_blur_value"] +=1
            blur_shape = (segment_value["bokeh_blur_value"], segment_value["bokeh_blur_value"])
            image = get_bokeh_image(image, blur_shape, blur_sigma, threshold_value=segment_value["mask_threshsold_value"], mask=current_mask, background_image=background_image)
        elif segment_value["option"] == "object":
            image = get_object_from_image(image, mask=current_mask)
        else:
            image = cv2.normalize(np.array(current_mask), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    except Exception as err:
        
        print(f'error: {err}')
    
    return image

def change_segment_value(title, value):
    segment_value[title] = value
    exec_image()

def save_image():
    fname = QFileDialog.getSaveFileName(None, "Save image as", expanduser("~"), "Image files (*.jpg *.png *.jpeg *.tif)")
    if len(fname[0]) == 0:
        return
    cv2.imwrite(fname[0], current_image)

def crop_image(e):
    global cropped_image
    if app_gui.is_cropping:
        x, y = get_position_cursor_on_label(app_gui.lbl_image_origin, orig_image, e)
        if crop_x_start == -1 or crop_y_start == -1 or x == -1 or y == -1:
            app_gui.set_image_root(orig_image)
        else:
            cropped_image = np.array(orig_image[crop_y_start:y, crop_x_start:x])
            exec_image()

def start_crop(e):
    global crop_x_start, crop_y_start
    if app_gui.is_cropping:
        crop_x_start, crop_y_start = get_position_cursor_on_label(app_gui.lbl_image_origin, orig_image, e)

def crop_move(e):
    if app_gui.is_cropping:
        x, y = get_position_cursor_on_label(app_gui.lbl_image_origin, orig_image, e)
        if crop_x_start == -1 or crop_y_start == -1 or x == -1 or y == -1:
            app_gui.set_image_root(orig_image)
        else:
            img = orig_image.copy()
            image = cv2.rectangle(img, (crop_x_start, crop_y_start),(x, y),(0,255,0),3)
            app_gui.set_image_root(image)

def draw_image(e):
    global current_mask
    x_i, y_i = get_position_cursor_on_label(app_gui.lbl_image_process, current_image, e)
    if x_i >=0 and y_i >= 0:
        if app_gui.is_drawing:
            image = cv2.circle(current_image, (x_i,y_i), app_gui.sld_point_size.value(), (0,0,255), -1)
            exec_image(image)
        elif app_gui.is_editting_mask:
            color = (255, 255, 255)
            if app_gui.rb_sub_mask.isChecked():
                color = (0, 0, 0)
            current_mask = cv2.circle(current_mask, (x_i,y_i), app_gui.sld_point_size.value(), color, -1)
            exec_image()

def change_background():
    global background_image
    fname = QFileDialog.getOpenFileName(None, 'Open file', expanduser("~"), "Image files (*.jpg *.png *.gif)")
    if len(fname[0]) == 0:
        return    
    background_image = cv2.imread(fname[0])
    exec_image()