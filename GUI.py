
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from lib import *
import handle_event

class ImageProcessing(QWidget):

    def __init__(self):
        super().__init__()
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height() - 150
        self.width = self.screenRect.width() - 50

        sshFile="style.qss"
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
        btnOpenImg.setIcon(QIcon("icon_OpenImg.png"))
        btnOpenImg.setIconSize(QSize(25,25))

        btnUndo = QPushButton(self)
        btnUndo.setToolTip("Undo")
        btnUndo.clicked.connect(self.undoEdit)
        btnUndo.setIcon(QIcon("icon_Undo.png"))
        btnUndo.setIconSize(QSize(25, 25))

        btnRedo = QPushButton(self)
        btnRedo.setToolTip("Redo")
        btnRedo.clicked.connect(self.redoEdit)
        btnRedo.setIcon(QIcon("icon_Redo.png"))
        btnRedo.setIconSize(QSize(25, 25))

        btnSave = QPushButton(self)
        btnSave.setToolTip("Save Image")
        btnSave.setToolTip("Save Image")
        btnSave.clicked.connect(self.saveImage)
        btnSave.setIcon(QIcon("icon_SaveImg.png"))
        btnSave.setIconSize(QSize(25, 25))

        ################################ Img ##########################################
        # img before
        self.lblImgBefore = QLabel("Open image to start",self)
        self.lblImgBefore.setToolTip("Image Before")
        self.lblImgBefore.resize(self.width / 3, self.height)
        self.lblImgBefore.setAlignment(QtCore.Qt.AlignCenter)

        #img after
        self.lblImgAfter = QLabel("Open image to start", self)
        self.lblImgAfter.setToolTip("Image After")
        # self.lblImgAfter.setGeometry(self.lblImgBefore.width(), 0, self.lblImgBefore.width(), self.height)
        self.lblImgAfter.resize(self.width / 3, self.height)
        self.lblImgAfter.setAlignment(QtCore.Qt.AlignCenter)

        #line vertical
        lineVertical = QLabel(self)
        lineHorizone = QLabel(self)



        #img histogram
        self.lblHistogram = QLabel(self)
        self.lblHistogram.resize(200,100)
        self.lblHistogram.setAlignment(QtCore.Qt.AlignCenter)

        #đảo ảnh
        lblDaoAnh =QLabel("Âm bản",self)
        btnDaoAnh = QPushButton("OK", self)
        btnDaoAnh.setObjectName("btnAutoFunction")
        btnDaoAnh.clicked.connect(self.daoAnh)
        hboxDaoAnh = QHBoxLayout()
        hboxDaoAnh.addWidget(lblDaoAnh,5)
        hboxDaoAnh.addWidget(btnDaoAnh,5)
        hboxDaoAnh.addStretch(4)

        ################################## AI ######################################

        lblSubject = QLabel("", self)

        btnDeleteBackground = QPushButton("Xóa Phông", self)
        btnDeleteBackground.setObjectName("btnAutoFunction")
        btnDeleteBackground.clicked.connect(self.deleteBackground)

        btnAutoEdit = QPushButton("Auto")
        btnAutoEdit.setObjectName("btnAutoFunction")
        btnAutoEdit.clicked.connect(self.autoEdit)

        ################################ Slider #####################################

        #slider tăng chỉnh garma #####################
        vboxGarma = QVBoxLayout()

        sldGarma = QSlider(Qt.Horizontal, self)
        sldGarma.setRange(0, 100)
        sldGarma.setFocusPolicy(Qt.NoFocus)
        sldGarma.setValue(50)
        sldGarma.valueChanged.connect(handle_event.contrast)

        lblTextGarma = QLabel('Tăng chỉnh độ sáng', self)
        lblTextGarma.setObjectName("lblSliderName")

        vboxGarma.addWidget(lblTextGarma)
        vboxGarma.addWidget(sldGarma)

        # slider làm mịn ###############################
        vboxSmoothing = QVBoxLayout()

        sldSmoothing = QSlider(Qt.Horizontal, self)
        sldSmoothing.setRange(0, 100)

        sldSmoothing.setFocusPolicy(Qt.NoFocus)
        sldSmoothing.setPageStep(5)

        sldSmoothing.valueChanged.connect(handle_event.smoothing)

        lblTextSmoothing = QLabel('Làm mịn', self)
        lblTextSmoothing.setObjectName("lblSliderName")

        vboxSmoothing.addWidget(lblTextSmoothing)
        vboxSmoothing.addWidget(sldSmoothing)

        # slider làm sắc nét #########################
        vboxSharpen = QVBoxLayout()

        sldSharpen = QSlider(Qt.Horizontal, self)
        sldSharpen.setRange(0, 100)

        sldSharpen.setFocusPolicy(Qt.NoFocus)
        sldSharpen.setPageStep(5)

        sldSharpen.valueChanged.connect(handle_event.sharpening)

        lblTextSharpen = QLabel('Làm sắc nét', self)
        lblTextSharpen.setObjectName("lblSliderName")

        vboxSharpen.addWidget(lblTextSharpen)
        vboxSharpen.addWidget(sldSharpen)

        # slider Giảm nhiễu #########################
        vboxReduceNoise = QVBoxLayout()

        sldReduceNoise = QSlider(Qt.Horizontal, self)
        sldReduceNoise.setRange(0, 100)

        sldReduceNoise.setFocusPolicy(Qt.NoFocus)
        sldReduceNoise.setPageStep(5)

        sldReduceNoise.valueChanged.connect(self.reduceNoise)

        lblTextReduceNoise = QLabel('Giảm nhiễu', self)
        lblTextReduceNoise.setObjectName("lblSliderName")

        vboxReduceNoise.addWidget(lblTextReduceNoise)
        vboxReduceNoise.addWidget(sldReduceNoise)

        ################################## set style ###########################################
        self.lblImgBefore.setStyleSheet("background-color: #282828;  ")
        self.lblImgAfter.setStyleSheet("background-color: #282828; ")

        lineVertical.setStyleSheet("border-right : 1px solid black;")
        lineVertical.setGeometry(self.lblImgAfter.width() + self.lblImgBefore.width() + 20, 0, 1, self.height)

        lineHorizone.setStyleSheet("border-top : 1px solid black;")
        lineHorizone.setGeometry(self.lblImgAfter.width() + self.lblImgBefore.width() + 20, self.height / 4, self.width / 5, 1)

        self.lblHistogram.setStyleSheet("background-color: #282828; ")

        ########################### Ai ############################

        lblSubject.setStyleSheet("color: #c1c1c1; font-weight: bold;margin-left: 10px")


        ######## Đảo ảnh ################
        lblDaoAnh.setStyleSheet("color: #c1c1c1; font-weight: bold; margin-left: 10px")

        #################################### setup layout #####################################

        hboxImg = QHBoxLayout()
        hboxImg.addWidget(self.lblImgBefore)
        hboxImg.addWidget(self.lblImgAfter)
        # hbox.addStretch(1)

        hboxImg.setContentsMargins(50, 0, 0, 10)

        hboxTopTool = QHBoxLayout()
        hboxTopTool.addWidget(btnOpenImg, 2)
        hboxTopTool.addWidget(btnUndo, 2)
        hboxTopTool.addWidget(btnRedo, 2)
        hboxTopTool.addWidget(btnSave, 2)
        hboxTopTool.addStretch(20)
        hboxTopTool.setContentsMargins(50, 10, 0, 10)

        hboxAi = QHBoxLayout()
        hboxAi.addWidget(lblSubject,2)
        hboxAi.addWidget(btnDeleteBackground,4)
        hboxAi.addWidget(btnAutoEdit,4)
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
        vboxRight.addLayout(vboxGarma)
        vboxRight.addStretch(1)
        vboxRight.addLayout(vboxSmoothing)
        vboxRight.addStretch(1)
        vboxRight.addLayout(vboxSharpen)
        vboxRight.addStretch(1)
        vboxRight.addLayout(vboxReduceNoise)
        vboxRight.addStretch(6)

        hboxMain = QHBoxLayout()
        hboxMain.addLayout(vboxLeft,8)
        hboxMain.addWidget(lineVertical)
        hboxMain.addLayout(vboxRight,2)

        #################################################################################
        self.setLayout(hboxMain)
        self.show()

    def daoAnh(self):
        return 0

    def reduceNoise(self, value):
        return 0

    def deleteBackground(self):
        return 0

    def autoEdit(self):
        return 0

    def undoEdit(self):
        return 0

    def redoEdit(self):
        return 0

    def saveImage(self):
        return 0

    def set_image_processed(self, image):
        pixmap_image = convert_cvImg_2_qImg(image, self.lblImgAfter.width(), self.lblImgAfter.height())
        self.lblImgAfter.setPixmap(pixmap_image)

    def set_image_root(self, image):
        pixmap_image = convert_cvImg_2_qImg(image, self.lblImgBefore.width(), self.lblImgBefore.height())
        self.lblImgBefore.setPixmap(pixmap_image)

    def set_histogram_image(self, histogram_image):
        histogram_pixmap = convert_cvImg_2_qImg(histogram_image, self.lblHistogram.width())
        self.lblHistogram.setPixmap(histogram_pixmap)
        
        
