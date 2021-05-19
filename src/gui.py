    # """
    #     Created by hnphuong
    # """

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

        sshFile="src/style.css"
        with open(sshFile,"r") as fh:
            self.setStyleSheet(fh.read())

        self.title = 'Image processing'
        self.left = 20
        self.top = 40
        self.bokeh_activated = False
        self.initUI()
        handle_event.set_gui(self)
        handle_event.open_image()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        ################################ Top Tool ######################################
        # button open img
        btn_open = QPushButton(self)
        btn_open.setToolTip("Open Image")
        btn_open.clicked.connect(handle_event.open_image)
        btn_open.setIcon(QIcon("src/img/icon_open.png"))
        btn_open.setIconSize(QSize(25,25))

        btn_undo = QPushButton(self)
        btn_undo.setToolTip("Undo")
        btn_undo.clicked.connect(handle_event.undo)
        btn_undo.setIcon(QIcon("src/img/icon_undo.png"))
        btn_undo.setIconSize(QSize(25, 25))

        btn_histogram = QPushButton(self)
        btn_histogram.setToolTip("Show/Hide histogram")
        btn_histogram.clicked.connect(self.toggle_histogram)
        btn_histogram.setIcon(QIcon("src/img/icon_histogram.png"))
        btn_histogram.setIconSize(QSize(25, 25))

        btn_save = QPushButton(self)
        btn_save.setToolTip("Save Image")
        btn_save.clicked.connect(handle_event.save_image)
        btn_save.setIcon(QIcon("src/img/icon_save.png"))
        btn_save.setIconSize(QSize(25, 25))

        btn_crop = QPushButton(self)
        btn_crop.setToolTip("Crop image")
        btn_crop.clicked.connect(handle_event.crop_image)
        btn_crop.setIcon(QIcon("src/img/icon_crop.png"))
        btn_crop.setIconSize(QSize(25, 25))

        btn_draw = QPushButton(self)
        btn_draw.setToolTip("Draw")
        btn_draw.clicked.connect(handle_event.draw_image)
        btn_draw.setIcon(QIcon("src/img/icon_pencil.png"))
        btn_draw.setIconSize(QSize(25, 25))

        btn_bokeh = QPushButton(self)
        btn_bokeh.setToolTip("Bokeh")
        btn_bokeh.clicked.connect(self.toggle_bokeh_tool)
        btn_bokeh.setIcon(QIcon("src/img/icon_auto.png"))
        btn_bokeh.setIconSize(QSize(25, 25))

        self.lbl_image_origin = QLabel("Open image to start",self)
        self.lbl_image_origin.setToolTip("Image Before")
        self.lbl_image_origin.resize(self.width / 3, self.height)
        self.lbl_image_origin.setAlignment(QtCore.Qt.AlignCenter)

        self.lbl_image_process = QLabel("Open image to start", self)
        self.lbl_image_process.setToolTip("Image After")
        self.lbl_image_process.resize(self.width / 3, self.height)
        self.lbl_image_process.setAlignment(QtCore.Qt.AlignCenter)

        #line vertical
        line_vertical_top = QLabel(self)

        #img histogram
        self.lbl_histogram = QLabel(self)
        self.lbl_histogram.resize(200,100)
        self.lbl_histogram.setAlignment(QtCore.Qt.AlignCenter)

        self.ckb_gray = QCheckBox("Ảnh xám")
        self.ckb_gray.stateChanged.connect(handle_event.gray)
        self.ckb_invert = QCheckBox("Đảo ảnh")
        self.ckb_invert.stateChanged.connect(handle_event.invert)
        self.ckb_sharpen = QCheckBox("Làm sắc nét")
        self.ckb_sharpen.stateChanged.connect(handle_event.sharpen)
        self.ckb_edge_detection = QCheckBox("Tách biên")
        self.ckb_edge_detection.stateChanged.connect(handle_event.edge_detection)

        # checkbox group
        hbox_checkbox = QHBoxLayout()
        hbox_checkbox.addWidget(self.ckb_gray)
        hbox_checkbox.addWidget(self.ckb_invert)
        hbox_checkbox.addWidget(self.ckb_sharpen)
        hbox_checkbox.addWidget(self.ckb_edge_detection)

        # threshsold ###############################
        hbox_slider_process = QHBoxLayout()
        vbox_label_slider = QVBoxLayout()
        vbox_slider = QVBoxLayout()

        self.ckb_threshsold = QCheckBox("Threshsold")

        self.sld_threshsold = QSlider(Qt.Horizontal, self)
        self.sld_threshsold.setRange(0, 100)
        self.sld_threshsold.setValue(0)
        self.sld_threshsold.valueChanged.connect(handle_event.threshsold)
        self.sld_threshsold.sliderReleased.connect(
            lambda: handle_event.release("threshsold", self.sld_threshsold.value()))

        vbox_label_slider.addWidget(self.ckb_threshsold)
        vbox_slider.addWidget(self.sld_threshsold)
        vbox_label_slider.addStretch(1)
        vbox_slider.addStretch(1)
        
        # brightness ###############################

        self.sld_brightness = QSlider(Qt.Horizontal, self)
        self.sld_brightness.setRange(-150, 150)
        self.sld_brightness.setValue(0)
        self.sld_brightness.valueChanged.connect(
            lambda: handle_event.change_filter("brightness", self.sld_brightness.value()))
        self.sld_brightness.sliderReleased.connect(
            lambda: handle_event.release("brightness", self.sld_brightness.value()))

        self.lbl_text_brightness = QLabel('Brightness', self)
        self.lbl_text_brightness.setObjectName("lblSliderName")

        vbox_label_slider.addWidget(self.lbl_text_brightness)
        vbox_slider.addWidget(self.sld_brightness)
        vbox_label_slider.addStretch(1)
        vbox_slider.addStretch(1)

        # contrast ###############################
        self.sld_contrast = QSlider(Qt.Horizontal, self)
        self.sld_contrast.setRange(0, 127)
        self.sld_contrast.setValue(0)
        self.sld_contrast.valueChanged.connect(
            lambda: handle_event.change_filter("contrast", self.sld_contrast.value()))
        self.sld_contrast.sliderReleased.connect(
            lambda: handle_event.release("contrast", self.sld_contrast.value()))

        self.lbl_text_contrast = QLabel('Contrast', self)
        self.lbl_text_contrast.setObjectName("lblSliderName")

        vbox_label_slider.addWidget(self.lbl_text_contrast)
        vbox_slider.addWidget(self.sld_contrast)
        vbox_label_slider.addStretch(1)
        vbox_slider.addStretch(1)

        # hue ###############################
        self.sld_hue = QSlider(Qt.Horizontal, self)
        self.sld_hue.setRange(-150, 150)
        self.sld_hue.setValue(0)
        self.sld_hue.valueChanged.connect(
            lambda: handle_event.change_filter("hue", self.sld_hue.value()))
        self.sld_hue.sliderReleased.connect(
            lambda: handle_event.release("hue", self.sld_hue.value()))

        self.lbl_text_hue = QLabel('Hue', self)
        self.lbl_text_hue.setObjectName("lblSliderName")

        vbox_label_slider.addWidget(self.lbl_text_hue)
        vbox_slider.addWidget(self.sld_hue)
        vbox_label_slider.addStretch(1)
        vbox_slider.addStretch(1)

        # saturation ###############################
        self.sld_saturation = QSlider(Qt.Horizontal, self)
        self.sld_saturation.setRange(-150, 150)
        self.sld_saturation.setValue(0)
        self.sld_saturation.valueChanged.connect(
            lambda: handle_event.change_filter("saturation", self.sld_saturation.value()))
        self.sld_saturation.sliderReleased.connect(
            lambda: handle_event.release("saturation", self.sld_saturation.value()))

        self.lbl_text_saturation = QLabel('Saturation', self)
        self.lbl_text_saturation.setObjectName("lblSliderName")

        vbox_label_slider.addWidget(self.lbl_text_saturation)
        vbox_slider.addWidget(self.sld_saturation)
        vbox_label_slider.addStretch(6)
        vbox_slider.addStretch(6)

        # blur ###############################
        vbox_blur = QVBoxLayout()
        hbox_blur = QHBoxLayout()

        self.sld_blur = QSlider(Qt.Horizontal, self)
        self.sld_blur.setRange(0, 100)
        self.sld_blur.valueChanged.connect(
            lambda: handle_event.change_filter("blur", self.sld_blur.value()))
        self.sld_blur.sliderReleased.connect(
            lambda: handle_event.release("blur", self.sld_blur.value()))

        lblText_blur = QLabel('Blur', self)
        lblText_blur.setObjectName("lblSliderName")

        btn_group_blur = QButtonGroup(self)
        self.rb_blur1 = QRadioButton("Hàm lọc TB", self)
        self.rb_blur1.toggled.connect(handle_event.undo)
        self.rb_blur1.setChecked(True)
        rb_blur2 = QRadioButton("Hàm Gaussian", self)
        rb_blur2.toggled.connect(handle_event.undo)
        btn_group_blur.addButton(self.rb_blur1)
        btn_group_blur.addButton(rb_blur2)

        hbox_blur.addWidget(lblText_blur)
        hbox_blur.addWidget(self.rb_blur1)
        hbox_blur.addWidget(rb_blur2)
        vbox_blur.addLayout(hbox_blur)
        vbox_blur.addWidget(self.sld_blur)

        # mask_threshsold ###############################
        self.sld_mask_threshsold = QSlider(Qt.Horizontal, self)
        self.sld_mask_threshsold.setRange(-150, 150)
        self.sld_mask_threshsold.setValue(0)
        self.sld_mask_threshsold.valueChanged.connect(handle_event.mask_threshsold)
        self.sld_mask_threshsold.sliderReleased.connect(
            lambda: handle_event.release("mask_threshsold", self.sld_mask_threshsold.value()))

        self.lbl_text_mask_threshsold = QLabel('Mask threshsold', self)
        self.lbl_text_mask_threshsold.setObjectName("lblSliderName")

         # bokeh_blur ###############################
        self.sld_bokeh_blur = QSlider(Qt.Horizontal, self)
        self.sld_bokeh_blur.setRange(0, 100)
        self.sld_bokeh_blur.setValue(0)
        self.sld_bokeh_blur.valueChanged.connect(handle_event.mask_threshsold)
        self.sld_bokeh_blur.sliderReleased.connect(
            lambda: handle_event.release("bokeh_blur", self.sld_bokeh_blur.value()))

        self.lbl_text_bokeh_blur = QLabel('Bokeh blur', self)
        self.lbl_text_bokeh_blur.setObjectName("lblSliderName")

        vbox_bokeh_option = QVBoxLayout()
        btn_group_bokeh = QButtonGroup(self)
        self.rb_bokeh_option1 = QRadioButton("Only mask")
        self.rb_bokeh_option1.toggled.connect(handle_event.change_bokeh_option)
        self.rb_bokeh_option2 = QRadioButton("Only Object")
        self.rb_bokeh_option2.toggled.connect(handle_event.change_bokeh_option)
        self.rb_bokeh_option3 = QRadioButton("Bokeh")
        self.rb_bokeh_option3.toggled.connect(handle_event.change_bokeh_option)



        btn_group_bokeh.addButton(self.rb_bokeh_option1)
        btn_group_bokeh.addButton(self.rb_bokeh_option2)
        btn_group_bokeh.addButton(self.rb_bokeh_option3)

        self.btn_repaint_mask = QPushButton(self)
        self.btn_repaint_mask.setToolTip("Edit mask")
        self.btn_repaint_mask.clicked.connect(handle_event.repaint_mask)
        self.btn_repaint_mask.setIcon(QIcon("src/img/icon_mask.png"))
        self.btn_repaint_mask.setIconSize(QSize(25, 25))

        vbox_bokeh_option.addWidget(self.rb_bokeh_option1)
        vbox_bokeh_option.addWidget(self.rb_bokeh_option2)
        vbox_bokeh_option.addWidget(self.rb_bokeh_option3)
        vbox_bokeh_option.setSpacing(10)

        vbox_label_slider.addStretch(1)
        vbox_slider.addStretch(1)
        vbox_label_slider.addLayout(vbox_bokeh_option)
        vbox_slider.addWidget(self.btn_repaint_mask)
        vbox_label_slider.addWidget(self.lbl_text_mask_threshsold)
        vbox_slider.addWidget(self.sld_mask_threshsold)
        vbox_label_slider.addWidget(self.lbl_text_bokeh_blur)
        vbox_slider.addWidget(self.sld_bokeh_blur)

        hbox_slider_process.addLayout(vbox_label_slider)
        hbox_slider_process.addLayout(vbox_slider)

        vboxRight = QVBoxLayout()
        vboxRight.addWidget(self.lbl_histogram)
        vboxRight.addLayout(hbox_checkbox)
        vboxRight.addLayout(vbox_blur)
        vboxRight.addLayout(hbox_slider_process)

        ################################## set style ###########################################
        self.lbl_image_origin.setStyleSheet("background-color: #282828;  ")
        self.lbl_image_process.setStyleSheet("background-color: #282828; ")
        self.lbl_histogram.setStyleSheet("background-color: #282828; ")

        line_vertical_top.setStyleSheet("border-right : 1px solid black;")
        line_vertical_top.setGeometry(self.lbl_image_process.width() + self.lbl_image_origin.width() + 20, 0, 1, self.height)
        #################################### setup layout #####################################

        hboxImg = QHBoxLayout()
        hboxImg.addWidget(self.lbl_image_origin)
        hboxImg.addWidget(self.lbl_image_process)

        hboxTopTool = QHBoxLayout()
        hboxTopTool.addWidget(btn_open)
        hboxTopTool.addWidget(btn_save)
        hboxTopTool.addWidget(btn_undo)
        hboxTopTool.addWidget(btn_histogram)
        hboxTopTool.addStretch(1)
        hboxTopTool.addWidget(btn_crop)
        hboxTopTool.addWidget(btn_draw)
        hboxTopTool.addWidget(btn_bokeh)
        # hboxTopTool.addWidget(cbb, 2)
        hboxTopTool.setContentsMargins(50, 10, 0, 10)

        vboxLeft = QVBoxLayout()
        vboxLeft.addLayout(hboxTopTool,1)
        vboxLeft.addLayout(hboxImg,9)

        hboxMain = QHBoxLayout()
        hboxMain.addLayout(vboxLeft,8)
        hboxMain.addWidget(line_vertical_top)
        hboxMain.addLayout(vboxRight,2)

        #################################################################################
        self.setLayout(hboxMain)
        self.show()
        self.toggle_bokeh_tool()

    def toggle_bokeh_tool(self):
        if self.bokeh_activated:
            self.rb_bokeh_option1.show()
            self.rb_bokeh_option2.show()
            self.rb_bokeh_option3.show()
            self.btn_repaint_mask.show()
            self.sld_mask_threshsold.show()
            self.lbl_text_mask_threshsold.show()
            self.sld_bokeh_blur.show()
            self.lbl_text_bokeh_blur.show()
        else:
            self.rb_bokeh_option1.hide()
            self.rb_bokeh_option2.hide()
            self.rb_bokeh_option3.hide()
            self.btn_repaint_mask.hide()
            self.sld_mask_threshsold.hide()
            self.lbl_text_mask_threshsold.hide()
            self.sld_bokeh_blur.hide()
            self.lbl_text_bokeh_blur.hide()
        self.bokeh_activated = not self.bokeh_activated

    def toggle_histogram(self):
        pass

    def set_image_processed(self, image):
        pixmap_image = convert_cvImg_2_qImg(image, self.lbl_image_process.width(), self.lbl_image_process.height())
        self.lbl_image_process.setPixmap(pixmap_image)

    def set_image_root(self, image):
        pixmap_image = convert_cvImg_2_qImg(image, self.lbl_image_origin.width(), self.lbl_image_origin.height())
        self.lbl_image_origin.setPixmap(pixmap_image)

    def set_histogram_image(self, histogram_image):
        histogram_pixmap = convert_cvImg_2_qImg(histogram_image, self.lbl_histogram.width())
        self.lbl_histogram.setPixmap(histogram_pixmap)

    def show_value_slider(self, value):
        self.lblTextGamma.setText(value)
