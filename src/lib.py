    # """
    #     Created by dqkhanh2000
    # """

import PyQt5
import math
from PyQt5.QtGui import QPixmap
import cv2
import numpy as np
from matplotlib import pyplot as plt
import io

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
    if c_width > c_height:
        if c_width < width:
            qPixmap = qPixmap.scaledToWidth(c_width)
    else:
        if c_height < height:
            qPixmap = qPixmap.scaledToHeight(c_height)
    # if c_height < height:
    #     qPixmap = qPixmap.scaledToHeight(c_height)
    return qPixmap

def cal_histogram(img):

    width = img.shape[1]
    height = img.shape[0]
    scale_down_ratio = 1
    while height>400 or width >400:
        scale_down_ratio += 1
        width = int(width/scale_down_ratio)
        height = int(height/scale_down_ratio)
    
    new_img = cv2.resize(img, (width, height))
    fig, ax = plt.subplots()
    histr = None
    if len(new_img.shape) == 2:
        histr = cv2.calcHist([new_img], [0], None, [256], [0, 256])
        ax.plot(histr, color = 'b')
    else:
        color = ('b','g','r')
        for i,col in enumerate(color):
            histr = cv2.calcHist([new_img],[i],None,[256],[0,256])
            ax.plot(histr, color = col)
    # plt.axis("off")
    return fig_to_np(fig)

def fig_to_np(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    img = cv2.imdecode(img_arr, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def avg_mask(size):
    avg = 1/(size*size)
    return np.full((size, size), avg)

def gaussian_mask(size, k, o):
    if size == 1:
        return 1
    a = int((size - 1)/2)
    maxtrix = []
    for s in range(-a, a+1):
        maxtrix.append([])
        for t in range(-a, a+1):
            p = - (s*s + t*t)/(2 * o*o)
            value = k*math.exp(p)
            maxtrix[s+a].append(value)
    return (1/4.8976)*np.array(maxtrix)

def gamma(image, gamma, c):
    # return gamma * img + c#float(c) * pow(img, float(gamma))
    new_image = np.zeros(image.shape, image.dtype)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            for c in range(image.shape[2]):
                new_image[y,x,c] = np.clip(gamma*image[y,x,c] + c, 0, 255)
    return new_image

def process_image(image, is_gray = False,
                    is_invert = False, brightness_value = 0,
                    contrast_value = 0, hue_value = 0,
                    saturation_value= 0, blur_value=0, blur_method = "average"):
    if is_gray:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        if (brightness_value != 0 or contrast_value != 0 
            or hue_value != 0 or saturation_value != 0):
            hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            h, s, v = cv2.split(hsv_image)

            # change brightness
            if brightness_value > 0:
                brightness_lim = 255 - brightness_value
                v[v > brightness_lim] = 255
                v[v <= brightness_lim] += brightness_value
            else:
                brightness_value = int(-brightness_value)
                brightness_lim = 0 + brightness_value
                v[v < brightness_lim] = 0
                v[v >= brightness_lim] -= brightness_value

            # change hue
            if hue_value > 0:
                hue_lim = 255 - hue_value
                h[h > hue_lim] = 255
                h[h <= hue_lim] += hue_value
            else:
                hue_value = int(-hue_value)
                hue_lim = 0 + hue_value
                h[h < hue_lim] = 0
                h[h >= hue_lim] -= hue_value

            # change saturation
            if saturation_value > 0:
                saturation_lim = 255 - saturation_value
                s[s > saturation_lim] = 255
                s[s <= saturation_lim] += saturation_value
            else:
                saturation_value = int(-saturation_value)
                saturation_lim = 0 + saturation_value
                s[s < saturation_lim] = 0
                s[s >= saturation_lim] -= saturation_value

            final_hsv = cv2.merge((h, s, v))
            image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2RGB)

    if contrast_value != 0:
        alpha = float(131 * (contrast_value + 127)) / (127 * (131 - contrast_value))
        gamma = 127 * (1 - alpha)

        image = cv2.addWeighted(image, alpha, image, 0, gamma)
        image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    if blur_value != 0:
        x = int(blur_value/5)
        x*=2
        if x%2 == 0:
            x+=1
        mask = avg_mask(x)
        if blur_method == "average":
            image = cv2.filter2D(image, -1, mask)
        if blur_method == "gaussian":
            image = cv2.GaussianBlur(image,(x,x), 1.5)
        image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    if is_invert:
        image = 255 - image

    return image

