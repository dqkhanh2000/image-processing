    """
        Created by dqkhanh2000
    """
from os.path import expanduser
from PyQt5.QtWidgets import QFileDialog
import src.execute as execute

def open_image():
    fname = QFileDialog.getOpenFileName(None, 'Open file', expanduser("~"), "Image files (*.jpg *.png *.gif)")
    if len(fname[0]) == 0:
        return    
    execute.root_image_path = fname[0]
    execute.load_image_from_file()

def contrast(value):
    execute.cal_contrast(value)

def release():
    execute.release()

def smoothing(value):
    execute.cal_smooth(value)

def edgeDetection(state):
    execute.edge_detection(state)

def sharpening(state):
    execute.sharpen(state)

def invert(state):
    execute.invert_image()

def gray(state):
    execute.gray_image()

def saveImage():
    fname = QFileDialog.getSaveFileName(None, "Save image as", expanduser("~"), "Image files (*.jpg)")
    if len(fname[0]) == 0:
        return
    execute.save_image(fname[0])