    """
        Created by dqkhanh2000
    """

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
    if c_width < width:
        qPixmap = qPixmap.scaledToWidth(c_width)
    # if c_height < height:
    #     qPixmap = qPixmap.scaledToHeight(c_height)
    return qPixmap

def cal_histogram(img):
    fig, ax = plt.subplots()
    histr = None
    if len(img.shape) == 2:
        histr = cv2.calcHist([img], [0], None, [256], [0, 256])
        ax.plot(histr, color = 'g')
    else:
        color = ('b','g','r')
        for i,col in enumerate(color):
            histr = cv2.calcHist([img],[i],None,[256],[0,256])
            ax.plot(histr, color = col)
    plt.axis("off")
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

def gamma(img, gamma, c):
    return float(c) * pow(img, float(gamma))

