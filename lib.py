import PyQt5
from PyQt5.QtGui import QPixmap
import cv2
import numpy as np
from matplotlib import pyplot as plt
import io


def convert_cvImg_2_qImg(cvImg, c_width = 0, c_height = 0):
    if len(cvImg.shape) < 3:
        height, width = cvImg.shape
    else:
        height, width, channel = cvImg.shape
    bytesPerLine = 3 * width
    qImg = PyQt5.QtGui.QImage(cvImg.data, width, height, bytesPerLine, PyQt5.QtGui.QImage.Format_RGB888).rgbSwapped()
    qPixmap = QPixmap(qImg)
    if c_width < width:
        qPixmap = qPixmap.scaledToWidth(c_width)
    # if c_height < height:
    #     qPixmap = qPixmap.scaledToHeight(c_height)
    return qPixmap

def cal_histogram(img):
    color = ('b','g','r')
    fig, ax = plt.subplots()
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

def gamma_gray(img, gamma, c):
    return float(c) * pow(img, float(gamma))

