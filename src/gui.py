from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.lib import *
import src.handle_event as handle_event

class ImageProcessing(QWidget):

    def __init__(self):
        super().__init__()
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height() - 150
        self.width = self.screenRect.width() - 50

        sshFile="src/style.qss"
        with open(sshFile,"r") as fh:
            self.setStyleSheet(fh.read())

        self.title = 'Image processing'
        self.left = 20
        self.top = 40
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        ################################ set GUI ##########################################
        ################################ Top Tool ######################################
        # button open img
        btnOpenImg = QPushButton(self)
        btnOpenImg.setToolTip("Open Image")
        btnOpenImg.clicked.connect(handle_event.open_image)
        btnOpenImg.setIcon(QIcon("src/img/icon_OpenImg.png"))
        btnOpenImg.setIconSize(QSize(25,25))

        btnSave = QPushButton(self)
        btnSave.setToolTip("Save Image")
        btnSave.setToolTip("Save Image")
        btnSave.clicked.connect(handle_event.saveImage)
        btnSave.setIcon(QIcon("src/img/icon_SaveImg.png"))
        btnSave.setIconSize(QSize(25, 25))

        # img before
        self.lblImgBefore = QLabel("Open image to start",self)
        self.lblImgBefore.setToolTip("Image Before")
        self.lblImgBefore.resize(self.width / 3, self.height)
        self.lblImgBefore.setAlignment(QtCore.Qt.AlignCenter)

        #img after
        self.lblImgAfter = QLabel("Open image to start", self)
        self.lblImgAfter.setToolTip("Image After")
        self.lblImgAfter.resize(self.width / 3, self.height)
        self.lblImgAfter.setAlignment(QtCore.Qt.AlignCenter)

        #line vertical
        lineVertical = QLabel(self)
        lineHorizone = QLabel(self)

        #img histogram
        self.lblHistogram = QLabel(self)
        self.lblHistogram.resize(200,100)
        self.lblHistogram.setAlignment(QtCore.Qt.AlignCenter)

        self.ckbGray = QCheckBox("Ảnh xám")
        self.ckbGray.stateChanged.connect(handle_event.gray)
        hboxDaoAnh = QHBoxLayout()
        hboxDaoAnh.addWidget(self.ckbGray,5)
        hboxDaoAnh.addStretch(4)

        ################################ Slider #####################################

        #slider tăng chỉnh Gamma #####################
        vboxGamma = QVBoxLayout()
        hboxGamma = QHBoxLayout()

        self.sldGamma = QSlider(Qt.Horizontal, self)
        self.sldGamma.setRange(0, 100)
        self.sldGamma.setFocusPolicy(Qt.NoFocus)
        self.sldGamma.setValue(50)
        self.sldGamma.valueChanged.connect(handle_event.contrast)
        self.sldGamma.sliderReleased.connect(handle_event.release)

        self.lblTextGamma = QLabel('Tăng chỉnh độ sáng', self)
        self.lblTextGamma.setToolTip("DÙng hàm gamma")
        self.lblTextGamma.setObjectName("lblSliderName")

        hboxGamma.addWidget(self.lblTextGamma)
        vboxGamma.addLayout(hboxGamma)
        vboxGamma.addWidget(self.sldGamma)

        # slider làm mịn ###############################
        vboxSmoothing = QVBoxLayout()
        hboxSmoothing = QHBoxLayout()

        self.sldSmoothing = QSlider(Qt.Horizontal, self)
        self.sldSmoothing.setRange(0, 100)

        self.sldSmoothing.setFocusPolicy(Qt.NoFocus)
        self.sldSmoothing.setPageStep(5)

        self.sldSmoothing.valueChanged.connect(handle_event.smoothing)
        self.sldSmoothing.sliderReleased.connect(handle_event.release)

        lblTextSmoothing = QLabel('Làm mịn', self)
        lblTextSmoothing.setObjectName("lblSliderName")

        self.rbSmoothing1 = QRadioButton("Hàm lọc TB", self)
        self.rbSmoothing1.setChecked(True)

        rbSmoothing2 = QRadioButton("Hàm Gaussian", self)

        hboxSmoothing.addWidget(lblTextSmoothing)
        hboxSmoothing.addWidget(self.rbSmoothing1)
        hboxSmoothing.addWidget(rbSmoothing2)
        vboxSmoothing.addLayout(hboxSmoothing)
        vboxSmoothing.addWidget(self.sldSmoothing)

        # slider làm sắc nét #########################
        vboxSharpen = QVBoxLayout()
        hboxSharpen = QHBoxLayout()

        self.ckbInvert = QCheckBox("Đảo ảnh")
        self.ckbInvert.stateChanged.connect(handle_event.invert)
        self.ckbSharpen = QCheckBox("Làm sắc nét")
        self.ckbSharpen.stateChanged.connect(handle_event.sharpening)
        self.ckbEdgeDetection = QCheckBox("Tách biên")
        self.ckbEdgeDetection.stateChanged.connect(handle_event.edgeDetection)
        
        hboxSharpen.addWidget(self.ckbInvert)
        hboxSharpen.addWidget(self.ckbSharpen)
        hboxSharpen.addWidget(self.ckbEdgeDetection)
        vboxSharpen.addLayout(hboxSharpen)
        ################################## set style ###########################################
        self.lblImgBefore.setStyleSheet("background-color: #282828;  ")
        self.lblImgAfter.setStyleSheet("background-color: #282828; ")

        lineVertical.setStyleSheet("border-right : 1px solid black;")
        lineVertical.setGeometry(self.lblImgAfter.width() + self.lblImgBefore.width() + 20, 0, 1, self.height)

        lineHorizone.setStyleSheet("border-top : 1px solid black;")
        lineHorizone.setGeometry(self.lblImgAfter.width() + self.lblImgBefore.width() + 20, self.height / 4, self.width / 5, 1)

        self.lblHistogram.setStyleSheet("background-color: #282828; ")

        #################################### setup layout #####################################

        hboxImg = QHBoxLayout()
        hboxImg.addWidget(self.lblImgBefore)
        hboxImg.addWidget(self.lblImgAfter)
        # hbox.addStretch(1)

        hboxImg.setContentsMargins(50, 0, 0, 10)

        hboxTopTool = QHBoxLayout()
        hboxTopTool.addWidget(btnOpenImg, 2)
        hboxTopTool.addWidget(btnSave, 2)
        hboxTopTool.addStretch(20)
        # hboxTopTool.addWidget(cbb, 2)
        hboxTopTool.setContentsMargins(50, 10, 0, 10)

        hboxAi = QHBoxLayout()
        hboxAi.addStretch(35)
        hboxAi.setContentsMargins(50, 0, 0, 10)

        vboxLeft = QVBoxLayout()
        vboxLeft.addLayout(hboxTopTool,1)
        vboxLeft.addLayout(hboxImg,9)
        vboxLeft.addLayout(hboxAi,1)

        vboxRight = QVBoxLayout()
        vboxRight.addWidget(self.lblHistogram)
        vboxRight.addWidget(lineHorizone)
        vboxRight.addLayout(hboxDaoAnh)
        vboxRight.addStretch(1)
        vboxRight.addLayout(vboxGamma)
        vboxRight.addStretch(1)
        vboxRight.addLayout(vboxSmoothing)
        vboxRight.addStretch(1)
        vboxRight.addLayout(vboxSharpen)
        vboxRight.addStretch(1)
        vboxRight.addStretch(6)

        hboxMain = QHBoxLayout()
        hboxMain.addLayout(vboxLeft,8)
        hboxMain.addWidget(lineVertical)
        hboxMain.addLayout(vboxRight,2)

        #################################################################################
        self.setLayout(hboxMain)
        self.show()

    def set_image_processed(self, image):
        pixmap_image = convert_cvImg_2_qImg(image, self.lblImgAfter.width(), self.lblImgAfter.height())
        self.lblImgAfter.setPixmap(pixmap_image)

    def set_image_root(self, image):
        pixmap_image = convert_cvImg_2_qImg(image, self.lblImgBefore.width(), self.lblImgBefore.height())
        self.lblImgBefore.setPixmap(pixmap_image)

    def set_histogram_image(self, histogram_image):
        histogram_pixmap = convert_cvImg_2_qImg(histogram_image, self.lblHistogram.width())
        self.lblHistogram.setPixmap(histogram_pixmap)

    def show_value_slider(self, value):
        self.lblTextGamma.setText(value)
