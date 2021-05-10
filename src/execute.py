import cv2
from numpy import lib
from src.handle_event import contrast, smoothing
from src.gui import ImageProcessing
import numpy as np
from src.lib import *
GRAY_MODE = True
root_image_path = ''
root_image = []
backup_image = []
contrast_image = []
smoothing_image = []

app_gui = None

def get_gui():
    global app_gui
    if app_gui == None:
        app_gui = ImageProcessing()
    return app_gui

def cal_contrast(value):
    global contrast_image
    g = 1
    if value < 50:
        g =(60-value)/10
    else:
        g = (100-(value-50)*2)/100

    img = gamma(root_image, g, 1.5)
    new_image = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    app_gui.set_image_processed(new_image)
    app_gui.set_histogram_image(cal_histogram(new_image))
    app_gui.sldSmoothing.setValue(0)
    contrast_image = new_image

def cal_smooth(value):
    global contrast_image, smoothing_image

    x = int(value/5)
    x*=2
    if x%2 == 0:
        x+=1
    mask = avg_mask(x)

    img = []
    if app_gui.rbSmoothing1.isChecked:
        img = cv2.filter2D(contrast_image, -1, mask)
    else:
        img = cv2.GaussianBlur(img,(x,x),0)
    new_image = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    app_gui.set_image_processed(new_image)
    app_gui.set_histogram_image(cal_histogram(new_image))
    smoothing_image = new_image

def invert_image():
    global contrast_image
    img = np.subtract(255, contrast_image)
    new_image = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    app_gui.set_image_processed(new_image)
    app_gui.set_histogram_image(cal_histogram(new_image))
    contrast_image = new_image

def sharpen(state):
    global contrast_image

    mask = np.array([[0, 1, 0],
                    [1, -4, 1],
                    [0, 1, 0],
                ])
    img = []
    if state == 2:
        img = cv2.filter2D(contrast_image, -1, mask)
        img = np.subtract(contrast_image, img)
    else:
        img = root_image
    new_image = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    app_gui.set_image_processed(new_image)
    app_gui.set_histogram_image(cal_histogram(new_image))
    contrast_image = new_image

def edge_detection(state):
    global contrast_image

    mask = np.array([[-1, -2, -1],
                    [0, 0, 0],
                    [1, 2, 1],
                ])
    img = []
    if state == 2:
        if len(smoothing_image.shape) == 3:
            app_gui.ckbGray.setChecked(True)
        img = cv2.filter2D(smoothing_image, -1, mask)
    else:
        img = root_image
    new_image = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    app_gui.set_image_processed(new_image)
    app_gui.set_histogram_image(cal_histogram(new_image))
    contrast_image = new_image

def release():
    # global list_step, current_image
    # list_step.append(current_image)
    pass

def gray_image():
    global root_image, backup_image, smoothing_image, contrast_image
    root_image, backup_image = [backup_image, root_image]
    contrast_image = root_image
    smoothing_image = root_image

    app_gui.set_image_processed(root_image)
    app_gui.set_histogram_image(cal_histogram(root_image))
    app_gui.sldGamma.setValue(50)
    app_gui.sldSmoothing.setValue(0)

def load_image_from_file():
    global root_image, contrast_image, smoothing_image, backup_image
    root_image = cv2.imread(root_image_path)
    # if root_image.shape[1] > 1000 or root_image.shape[0] > 1000:
    #     width = int(root_image.shape[1]/3)
    #     height = int(root_image.shape[0]/3)
    #     dim = (width, height)
    #     root_image = cv2.resize(root_image, dim, interpolation = cv2.INTER_AREA)
    backup_image = cv2.cvtColor(root_image, cv2.COLOR_BGR2GRAY)
    contrast_image = root_image
    smoothing_image = root_image
    app_gui.set_image_root(root_image)
    app_gui.set_image_processed(root_image)
    app_gui.set_histogram_image(cal_histogram(root_image))
    app_gui.sldGamma.setValue(50)
    app_gui.sldSmoothing.setValue(0)

def save_image(fname):
    cv2.imwrite(fname, contrast_image)