
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


StyleSheet = '''
#bar{
    border: 1px solid grey;
    min-height: 12px;
    max-height: 12px;
    border-radius: 6px;
}
#bar::chunk{
    border-radius: 6px;
    background-color: #05B8CC;
}
'''



class ImageProcessing(QWidget):

    def __init__(self):
        super().__init__()
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height() - 150
        self.width = self.screenRect.width() - 50

        self.title = 'PyQt5 image '
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
        btnOpenImg.clicked.connect(self.getImage)
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
        self.lblImgBefore = QLabel("BEFORE",self)
        self.lblImgBefore.setToolTip("Image Before")
        self.lblImgBefore.resize(self.width / 3, self.height)
        pixmapImgBefore = QPixmap('bg-66.jpg')
        if (pixmapImgBefore.width() > self.lblImgBefore.width()):
            pixmapImgBefore = pixmapImgBefore.scaledToWidth(self.lblImgBefore.width())
        self.lblImgBefore.setPixmap(pixmapImgBefore)
        self.lblImgBefore.setAlignment(QtCore.Qt.AlignCenter)

        #img after
        self.lblImgAfter = QLabel(self)
        self.lblImgAfter.setToolTip("Image After")
        # self.lblImgAfter.setGeometry(self.lblImgBefore.width(), 0, self.lblImgBefore.width(), self.height)
        self.lblImgAfter.resize(self.width / 3, self.height)
        pixmapImgAfter = QPixmap('Capture.PNG')
        if (pixmapImgAfter.width() > self.lblImgAfter.width()):
            pixmapImgAfter = pixmapImgAfter.scaledToWidth(self.lblImgBefore.width())
        self.lblImgAfter.setPixmap(pixmapImgAfter)
        self.lblImgAfter.setAlignment(QtCore.Qt.AlignCenter)

        #line vertical
        lineVertical = QLabel(self)
        lineHorizone = QLabel(self)



        #img histogram
        lblHistogram = QLabel(self)
        lblHistogram.resize(200,100)
        pixmapImg = QPixmap('bg-66.jpg')
        if (pixmapImg.width() > lblHistogram.width()):
            pixmapImg = pixmapImg.scaledToHeight(lblHistogram.width())
        lblHistogram.setPixmap(pixmapImg)
        lblHistogram.setAlignment(QtCore.Qt.AlignCenter)

        #đảo ảnh
        lblDaoAnh =QLabel("Âm bản",self)
        btnDaoAnh = QPushButton("OK", self)
        btnDaoAnh.clicked.connect(self.daoAnh)
        hboxDaoAnh = QHBoxLayout()
        hboxDaoAnh.addWidget(lblDaoAnh,5)
        hboxDaoAnh.addWidget(btnDaoAnh,5)
        hboxDaoAnh.addStretch(4)

    ################################## AI ######################################

        lblSubject = QLabel("Phương Đẹp trai", self)

        btnDeleteBackground = QPushButton("Xóa Phông", self)
        btnDeleteBackground.clicked.connect(self.deleteBackground)

        btnAutoEdit = QPushButton("Auto")
        btnAutoEdit.clicked.connect(self.autoEdit)

    ################################ Slider #####################################

        #slider tăng chỉnh garma #####################
        vboxGarma = QVBoxLayout()

        sldGarma = QSlider(Qt.Horizontal, self)
        sldGarma.setRange(0, 100)
        sldGarma.setFocusPolicy(Qt.NoFocus)
        sldGarma.setPageStep(5)
        sldGarma.valueChanged.connect(self.garma)

        lblTextGarma = QLabel('Tăng chỉnh độ sáng', self)

        vboxGarma.addWidget(lblTextGarma)
        vboxGarma.addWidget(sldGarma)

        # slider làm mịn ###############################
        vboxSmoothing = QVBoxLayout()

        sldSmoothing = QSlider(Qt.Horizontal, self)
        sldSmoothing.setRange(0, 100)

        sldSmoothing.setFocusPolicy(Qt.NoFocus)
        sldSmoothing.setPageStep(5)

        sldSmoothing.valueChanged.connect(self.smoothing)

        lblTextSmoothing = QLabel('Làm mịn', self)

        vboxSmoothing.addWidget(lblTextSmoothing)
        vboxSmoothing.addWidget(sldSmoothing)

        # slider làm sắc nét #########################
        vboxSharpen = QVBoxLayout()

        sldSharpen = QSlider(Qt.Horizontal, self)
        sldSharpen.setRange(0, 100)

        sldSharpen.setFocusPolicy(Qt.NoFocus)
        sldSharpen.setPageStep(5)

        sldSharpen.valueChanged.connect(self.sharpen)

        lblTextSharpen = QLabel('Làm sắc nét', self)

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

        vboxReduceNoise.addWidget(lblTextReduceNoise)
        vboxReduceNoise.addWidget(sldReduceNoise)

    ################################## set style ###########################################
        self.lblImgBefore.setStyleSheet("background-color: #282828;  ")
                                   # "margin-top: 80px;"
                                   # "margin-bottom: 150px;"
                                   # "margin-left: 50px;"
                                   # "margin-right: 0px;"
        ################################ Top tool ############################

        btnOpenImg.setStyleSheet(
            "border-radius : 5; border : 1px solid #c1c1c1; background-color: #535353; color: #c1c1c1; font-weight: bold;"
            "min-height: 40px;"
            "max-height: 40px;"
            "min-width: 40px;"
            "max-width: 40px;"
        )

        btnUndo.setStyleSheet(
            "border-radius : 5; border : 1px solid #c1c1c1; background-color: #535353; color: #c1c1c1; font-weight: bold;"
            "min-height: 40px;"
            "max-height: 40px;"
            "min-width: 40px;"
            "max-width: 40px;"
        )

        btnRedo.setStyleSheet(
            "border-radius : 5; border : 1px solid #c1c1c1; background-color: #535353; color: #c1c1c1; font-weight: bold;"
            "min-height: 40px;"
            "max-height: 40px;"
            "min-width: 40px;"
            "max-width: 40px;"
        )

        btnSave.setStyleSheet(
            "border-radius : 5; border : 1px solid #c1c1c1; background-color: #535353; color: #c1c1c1; font-weight: bold;"
            "min-height: 40px;"
            "max-height: 40px;"
            "min-width: 40px;"
            "max-width: 40px;"
        )
        ################################# img ###################################

        self.lblImgAfter.setStyleSheet("background-color: #282828; ")
                                  # "margin-top: 80px;"
                                  # "margin-bottom: 150px;"
                                  # "margin-left: 50px;"
                                  # "margin-right: 0px;"

        lineVertical.setStyleSheet("border-right : 1px solid black;")
        lineVertical.setGeometry(self.lblImgAfter.width() + self.lblImgBefore.width() + 20, 0, 1, self.height)

        lineHorizone.setStyleSheet("border-top : 1px solid black;")
        lineHorizone.setGeometry(self.lblImgAfter.width() + self.lblImgBefore.width() + 20, self.height / 4, self.width / 5, 1)

        lblHistogram.setStyleSheet("background-color: #282828; ")

        ########################### Ai ############################

        lblSubject.setStyleSheet("color: #c1c1c1; font-weight: bold;margin-left: 10px")

        btnDeleteBackground.setStyleSheet(
            "border-radius : 10; border : 1px solid #c1c1c1; background-color: #535353; color: #c1c1c1; font-weight: bold;"
            "min-height: 40px;"
            "max-height: 40px;")

        btnAutoEdit.setStyleSheet(
            "border-radius : 10; border : 1px solid #c1c1c1; background-color: #535353; color: #c1c1c1; font-weight: bold;"
            "min-height: 40px;"
            "max-height: 40px;")


        ######## Đảo ảnh ################
        lblDaoAnh.setStyleSheet("color: #c1c1c1; font-weight: bold; margin-left: 10px")

        btnDaoAnh.setStyleSheet(
            "border-radius : 7; border : 1px solid #c1c1c1; background-color: #535353; color: #c1c1c1; font-weight: bold;"
            "min-height: 30px;"
            "max-height: 30px;")

        ######## Garma ################
        sldGarma.setStyleSheet("QSlider::groove:horizontal {\n"
                          "    border-radius: 9px;\n"
                          "    height: 18px;\n"
                          "	margin: 10px;\n"
                          "	background-color: rgb(52, 59, 72);\n"
                          "}\n"
                          "QSlider::groove:horizontal:hover {\n"
                          "	background-color: rgb(55, 62, 76);\n"
                          "}\n"
                          "QSlider::handle:horizontal {\n"
                          "    background-color: rgb(85, 170, 255);\n"
                          "    border: none;\n"
                          "    height: 18px;\n"
                          "    width: 18px;\n"
                          "    margin: 0px;\n"
                          "	border-radius: 9px;\n"
                          "}\n"
                          "QSlider::handle:horizontal:hover {\n"
                          "    background-color: rgb(105, 180, 255);\n"
                          "}\n"
                          "QSlider::handle:horizontal:pressed {\n"
                          "    background-color: rgb(65, 130, 195);\n"
                          "}\n"
                          "\n")
        lblTextGarma.setStyleSheet("color: #c1c1c1; font-weight: bold;margin-left: 10px")

        ############## Sharpen ##########################3
        sldSharpen.setStyleSheet("QSlider::groove:horizontal {\n"
                               "    border-radius: 9px;\n"
                               "    height: 18px;\n"
                               "	margin: 10px;\n"
                               "	background-color: rgb(52, 59, 72);\n"
                               "}\n"
                               "QSlider::groove:horizontal:hover {\n"
                               "	background-color: rgb(55, 62, 76);\n"
                               "}\n"
                               "QSlider::handle:horizontal {\n"
                               "    background-color: rgb(85, 170, 255);\n"
                               "    border: none;\n"
                               "    height: 18px;\n"
                               "    width: 18px;\n"
                               "    margin: 0px;\n"
                               "	border-radius: 9px;\n"
                               "}\n"
                               "QSlider::handle:horizontal:hover {\n"
                               "    background-color: rgb(105, 180, 255);\n"
                               "}\n"
                               "QSlider::handle:horizontal:pressed {\n"
                               "    background-color: rgb(65, 130, 195);\n"
                               "}\n"
                               "\n")
        lblTextSharpen.setStyleSheet("color: #c1c1c1; font-weight: bold;margin-left: 10px")

        ############## Smoothing ##########################3
        sldSmoothing.setStyleSheet("QSlider::groove:horizontal {\n"
                                   "    border-radius: 9px;\n"
                                   "    height: 18px;\n"
                                   "	margin: 10px;\n"
                                   "	background-color: rgb(52, 59, 72);\n"
                                   "}\n"
                                   "QSlider::groove:horizontal:hover {\n"
                                   "	background-color: rgb(55, 62, 76);\n"
                                   "}\n"
                                   "QSlider::handle:horizontal {\n"
                                   "    background-color: rgb(85, 170, 255);\n"
                                   "    border: none;\n"
                                   "    height: 18px;\n"
                                   "    width: 18px;\n"
                                   "    margin: 0px;\n"
                                   "	border-radius: 9px;\n"
                                   "}\n"
                                   "QSlider::handle:horizontal:hover {\n"
                                   "    background-color: rgb(105, 180, 255);\n"
                                   "}\n"
                                   "QSlider::handle:horizontal:pressed {\n"
                                   "    background-color: rgb(65, 130, 195);\n"
                                   "}\n"
                                   "\n")
        lblTextSmoothing.setStyleSheet("color: #c1c1c1; font-weight: bold;margin-left: 10px")

        ############## ReduceNoise ##########################3
        sldReduceNoise.setStyleSheet("QSlider::groove:horizontal {\n"
                                   "    border-radius: 9px;\n"
                                   "    height: 18px;\n"
                                   "	margin: 10px;\n"
                                   "	background-color: rgb(52, 59, 72);\n"
                                   "}\n"
                                   "QSlider::groove:horizontal:hover {\n"
                                   "	background-color: rgb(55, 62, 76);\n"
                                   "}\n"
                                   "QSlider::handle:horizontal {\n"
                                   "    background-color: rgb(85, 170, 255);\n"
                                   "    border: none;\n"
                                   "    height: 18px;\n"
                                   "    width: 18px;\n"
                                   "    margin: 0px;\n"
                                   "	border-radius: 9px;\n"
                                   "}\n"
                                   "QSlider::handle:horizontal:hover {\n"
                                   "    background-color: rgb(105, 180, 255);\n"
                                   "}\n"
                                   "QSlider::handle:horizontal:pressed {\n"
                                   "    background-color: rgb(65, 130, 195);\n"
                                   "}\n"
                                   "\n")
        lblTextReduceNoise.setStyleSheet("color: #c1c1c1; font-weight: bold;margin-left: 10px")

        self.setStyleSheet("background-color: #535353; ")

    #################################################################################

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
        vboxRight.addWidget(lblHistogram)
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

    def garma(self, value):
        return 0
        #self.lblTextGarma.setText(str(value))

    def smoothing(self, value):
        return 0

    def sharpen(self, value):
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

    def getImage(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.jpg *.gif)")
        imagePath = fname[0]
        pixmapImgBefore = QPixmap(imagePath)
        if (pixmapImgBefore.width() > self.lblImgBefore.width()):
            pixmapImgBefore = pixmapImgBefore.scaledToWidth(self.lblImgBefore.width())
        self.lblImgBefore.setPixmap(pixmapImgBefore)
        self.lblImgAfter.setPixmap(pixmapImgBefore)


def main():
    app = QApplication(sys.argv)
    ex = ImageProcessing()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
