from os.path import expanduser
from PyQt5.QtWidgets import QFileDialog
import execute

def open_image():
    fname = QFileDialog.getOpenFileName(None, 'Open file', expanduser("~"), "Image files (*.jpg *.png *.gif)")
    execute.root_image_path = fname[0]
    execute.load_image_from_file()

def contrast(value):
    execute.cal_contrast(value)
    return 0

def smoothing(value):
    return 0

def sharpening(value):
    return 0