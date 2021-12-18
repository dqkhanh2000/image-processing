from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.lib import *
import src.handle_event as handle_event
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class ImageProcessing(QWidget):

    def __init__(self):
        super().__init__()
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height() - 100
        self.width = self.screenRect.width() / 2

        sshFile="src/style.css"
        with open(sshFile,"r") as fh:
            self.setStyleSheet(fh.read())

        self.title = 'Image processing'
        self.left = 20
        self.top = 40
        self.is_drawing = False
        self.show_sld_point_size = False
        self.is_editting_mask = False
        self.is_cropping = False
        self.bokeh_activated = False
        self.show_histogram = True
        self.cursor_pix = QPixmap('src/img/cursor_paint.png')
        self.cursor_crop = QPixmap('src/img/cursor_crop.png')
        self.initUI()
        handle_event.set_gui(self)
        # handle_event.open_image()
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        btn_open = QPushButton(self)
        btn_open.setToolTip("Open Image")
        btn_open.clicked.connect(handle_event.open_image)
        btn_open.setIcon(QIcon("src/img/icon_open.png"))
        btn_open.setIconSize(QSize(25,25))


        btn_save = QPushButton(self)
        btn_save.setToolTip("Save Image")
        btn_save.clicked.connect(handle_event.save_image)
        btn_save.setIcon(QIcon("src/img/icon_save.png"))
        btn_save.setIconSize(QSize(25, 25))

        self.lbl_image_origin = QLabel("Open image to start",self)
        self.lbl_image_origin.setToolTip("Image Before")
        self.lbl_image_origin.resize(self.width / 10, self.height)
        self.lbl_image_origin.setAlignment(QtCore.Qt.AlignCenter)

        self.lbl_image_process = QLabel("Open image to start", self)
        self.lbl_image_process.setToolTip("Image After")
        self.lbl_image_process.resize(self.width / 10, self.height)
        self.lbl_image_process.setAlignment(QtCore.Qt.AlignCenter)

        self.lbl_bg_separation = QLabel("Image after background separation")
        self.lbl_bg_separation.setToolTip("After Separation")
        self.lbl_bg_separation.resize(self.width / 10, self.height)
        self.lbl_bg_separation.setAlignment(QtCore.Qt.AlignCenter)


        self.vbox_result = QVBoxLayout()

        # label tittle result
        self.txt_result = QLabel("Result:")
        self.txt_result.setStyleSheet("color: rgb(0, 0, 0); "
                                    "font-size: 20px; "
                                    "margin: 20px; "
                                    "font-weight: bold; "
                                   )
        self.txt_result.setFixedHeight(70)
        self.txt_result.setFixedWidth(200)                 
        self.txt_result.setAlignment(Qt.AlignTop)
        self.vbox_result.addWidget(self.txt_result)

        # label tittle model
        self.txt_model = QLabel("- Model:")
        self.txt_model.setStyleSheet("color: rgb(0, 0, 0); "
                                    "font-size: 16px; "
                                    "margin-left: 30px; "
                                    "font-weight: 400; "
                                   )
        self.txt_model.setAlignment(Qt.AlignTop)
        self.vbox_result.addWidget(self.txt_model)

        #label title accuracy
        self.txt_accuracy = QLabel("- Accuracy:")
        self.txt_accuracy.setStyleSheet("color: rgb(0, 0, 0); "
                                    "font-size: 16px; "
                                    "margin-left: 30px; "
                                    "font-weight: 400; "
                                   )
        self.txt_accuracy.setAlignment(Qt.AlignTop)
        self.vbox_result.addWidget(self.txt_accuracy)


        self.lbl_image_origin.setStyleSheet("background-color: #282828;  ")
        self.lbl_image_process.setStyleSheet("background-color: #282828; ")
        self.lbl_bg_separation.setStyleSheet("background-color: #282828; ")


        hboxImg = QHBoxLayout()
        hboxImg.addWidget(self.lbl_image_origin)
        hboxImg.addWidget(self.lbl_image_process)

        hboxImg2 = QHBoxLayout()
        hboxImg2.addWidget(self.lbl_bg_separation)
        hboxImg2.addLayout(self.vbox_result)


        hboxTopTool = QHBoxLayout()
        hboxTopTool.addWidget(btn_open)
        hboxTopTool.addWidget(btn_save)
        hboxTopTool.addStretch(1)
        hboxTopTool.setContentsMargins(50, 10, 0, 10)

        vboxLeft = QVBoxLayout()
        vboxLeft.addLayout(hboxTopTool,1)
        vboxLeft.addLayout(hboxImg,9)
        vboxLeft.addLayout(hboxImg2, 9)

        hboxMain = QHBoxLayout()
        hboxMain.addLayout(vboxLeft,8)


        self.setLayout(hboxMain)
        self.center()
        self.show()

    
    def set_image_processed(self, image):
        pixmap_image = convert_cvImg_2_qImg(image, self.lbl_image_process.width(), self.lbl_image_process.height())
        self.lbl_image_process.setPixmap(pixmap_image)

    def set_image_root(self, image):
        pixmap_image = convert_cvImg_2_qImg(image, self.lbl_image_origin.width(), self.lbl_image_origin.height())
        self.lbl_image_origin.setPixmap(pixmap_image)
