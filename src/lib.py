    # """
    #     Created by dqkhanh2000
    # """

import PyQt5
from PyQt5.QtGui import QPixmap
import cv2
import numpy as np
from matplotlib import pyplot as plt
import io

from numpy.core import machar


def convert_cvImg_2_qImg(cvImg, c_width = 0, c_height = 0):
    height = cvImg.shape[0]
    width = cvImg.shape[1]
    bytesPerLine = 3 * width
    qImg = []
    if len(cvImg.shape) == 2:
        qImg = PyQt5.QtGui.QImage(cvImg.data, width, height, width, PyQt5.QtGui.QImage.Format_Grayscale8)
    else:
        qImg = PyQt5.QtGui.QImage(cvImg.data, width, height, bytesPerLine, PyQt5.QtGui.QImage.Format_RGB888).rgbSwapped()
    
    qPixmap = QPixmap.fromImage(qImg)
    if width > height:
        if c_width < width:
            qPixmap = qPixmap.scaledToWidth(c_width)
    else:
        if c_height < height:
            qPixmap = qPixmap.scaledToHeight(c_height)
    # if c_height < height:
    #     qPixmap = qPixmap.scaledToHeight(c_height)
    return qPixmap

def cal_histogram(img, fig):

    width = img.shape[1]
    height = img.shape[0]
    scale_down_ratio = 1
    while height>400 or width >400:
        scale_down_ratio += 1
        width = int(width/scale_down_ratio)
        height = int(height/scale_down_ratio)
    
    new_img = cv2.resize(img, (width, height))
    histr = None
    fig.clear()
    ax = fig.add_subplot(111, position=[-10,10,0,0])
    # ax.axis("off")
    if len(new_img.shape) == 2:
        histr = cv2.calcHist([new_img], [0], None, [256], [0, 256])
        ax.plot(histr, color = 'b')
    else:
        color = ('b','g','r')
        for i,col in enumerate(color):
            histr = cv2.calcHist([new_img],[i],None,[256],[0,256])
            ax.plot(histr, color = col)

def fig_to_np(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="jpg")
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    img = cv2.imdecode(img_arr, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def avg_mask(size):
    avg = 1/(size*size)
    return np.full((size, size), avg)

def process_image(image, filter_value):
    if filter_value["is_gray"]:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        if (filter_value["brightness"] != 0 or filter_value["contrast"] != 0 
            or filter_value["hue"] != 0 or filter_value["saturation"] != 0):
            hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            h, s, v = cv2.split(hsv_image)
            h = np.uint16(h)
            s = np.uint16(s)
            v = np.uint16(v)

            # change brightness
            if filter_value["brightness"] != 0:
                v = v + filter_value["brightness"]
                v = np.clip(v, 0, 255)
                
            # change hue
            if filter_value["hue"] != 0:
                h = h + filter_value["hue"]
                h = np.clip(h, 0, 255)

            # change saturation
            if filter_value["saturation"] != 0:
                s = s + filter_value["saturation"]
                s = np.clip(s, 0, 255)

            h = np.uint8(h)
            s = np.uint8(s)
            v = np.uint8(v)
            final_hsv = cv2.merge((h, s, v))
            image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2RGB)

    if filter_value["contrast"] != 0:
        contrast_value = filter_value["contrast"]
        alpha = contrast_value/127 + 1
        beta = - contrast_value
        image = image * alpha + beta
        image = np.clip(image, 0, 255)
        image = np.uint8(image)

    if filter_value["blur"] != 0:
        x = int(filter_value["blur"]/5)
        x*=2
        if x%2 == 0:
            x+=1
        mask = avg_mask(x)
        if filter_value["blur_method"] == "average":
            image = cv2.filter2D(image, -1, mask)
        if filter_value["blur_method"] == "gaussian":
            image = cv2.GaussianBlur(image,(x,x), 1.5)
        image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    if filter_value["is_invert"]:
        image = 255 - image

    if filter_value["sharpen_method"]:
        img = []
        if filter_value["sharpen_method"] == "Laplacian":
            mask = np.array([[0, 1, 0],
                            [1, -4, 1],
                            [0, 1, 0],])
            img = cv2.filter2D(image, -1, mask)
        elif filter_value["sharpen_method"] == "Sobel":
            mask_x = np.array([ [-1, -2, -1],
                            [0, 0, 0],
                            [1, 2, 1],])
            mask_y = np.array([ [-1, 0, 1],
                            [-2, 0, 2],
                            [-1, 0, 1],])
            img1 = cv2.filter2D(image, -1, mask_x)
            img2 = cv2.filter2D(image, -1, mask_y)
            img = np.add(img1, img2)
        elif filter_value["sharpen_method"] == "Robert":
            mask_x = np.array([[-1,0], [0,1]])
            mask_y = np.array([[0, -1], [1, 0]])
            img1 = cv2.filter2D(image, -1, mask_x)
            img2 = cv2.filter2D(image, -1, mask_y)
            img = np.add(img1, img2)
        img = np.subtract(image, img)
        image = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    if filter_value["edge_detection_method"]:
        img = []
        if filter_value["edge_detection_method"] == "Laplacian":
            mask = np.array([[0, 1, 0],
                            [1, -4, 1],
                            [0, 1, 0],])
            img = cv2.filter2D(image, -1, mask)
        elif filter_value["edge_detection_method"] == "Sobel":
            mask_x = np.array([ [-1, -2, -1],
                            [0, 0, 0],
                            [1, 2, 1],])
            mask_y = np.array([ [-1, 0, 1],
                            [-2, 0, 2],
                            [-1, 0, 1],])
            img1 = cv2.filter2D(image, -1, mask_x)
            img2 = cv2.filter2D(image, -1, mask_y)
            img = np.add(img1, img2)
        elif filter_value["edge_detection_method"] == "Robert":
            mask_x = np.array([[-1,0], [0,1]])
            mask_y = np.array([[0, -1], [1, 0]])
            img1 = cv2.filter2D(image, -1, mask_x)
            img2 = cv2.filter2D(image, -1, mask_y)
            img = np.add(img1, img2)
        
        image = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    if filter_value["threshsold"] != 0:
        _ , img = cv2.threshold(image, filter_value["threshsold"], 255, cv2.THRESH_BINARY)
        image = img

    return image

def get_position_cursor_on_label(label, image, e):
    q_width = label.pixmap().width()
    q_height = label.pixmap().height()
    l_width = label.width()
    l_height = label.height()
    if q_width == l_width:
        c = int((l_height - q_height)/2)
    else:
        c = int((l_width - q_width)/2)
    x_i = -1
    y_i = -1
    ratio = image.shape[1]/q_width
    if e.x() in range(0, l_width+1) and e.y() in range(c, q_height+c+1):
            if q_width == l_width:
                x_i = int(e.x() * ratio)
                y_i = int((e.y()-c) * ratio)
            elif q_height == l_height:
                x_i = int((e.x()-c) * ratio)
                y_i = int(e.y() * ratio)
            else:
                x_i = int((e.x()-c) * ratio)
                y_i = int((e.y()-c) * ratio)
    return (x_i, y_i)
