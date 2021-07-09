    # """
    #     Created by hnphuong
    # """

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
        self.height = self.screenRect.height() - 150
        self.width = self.screenRect.width() - 50

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

        self.btn_change_background = QPushButton(self)
        self.btn_change_background.setToolTip("Change background")
        self.btn_change_background.clicked.connect(handle_event.change_background)
        self.btn_change_background.setIcon(QIcon("src/img/icon_background.png"))
        self.btn_change_background.setIconSize(QSize(25, 25))

        # point_size ###############################
        self.sld_point_size = QSlider(Qt.Horizontal, self)
        self.sld_point_size.setRange(1, 20)
        self.sld_point_size.setValue(1)
        self.sld_point_size.valueChanged.connect(lambda: self.change_cursor_size())

        self.lbl_point_size = QLabel('Point size', self)
        self.lbl_point_size.setObjectName("lblSliderName")


        self.btn_crop = QPushButton(self)
        self.btn_crop.setToolTip("Crop image")
        self.btn_crop.setIcon(QIcon("src/img/icon_crop.png"))
        self.btn_crop.setIconSize(QSize(25, 25))
        self.btn_crop.clicked.connect(self.toggle_crop_mode)

        self.btn_draw = QPushButton(self)
        self.btn_draw.setToolTip("Draw")
        self.btn_draw.clicked.connect(self.toggle_draw_mode)
        self.btn_draw.setIcon(QIcon("src/img/icon_pencil.png"))
        self.btn_draw.setIconSize(QSize(25, 25))

        self.btn_bokeh = QPushButton(self)
        self.btn_bokeh.setToolTip("Bokeh")
        self.btn_bokeh.clicked.connect(self.toggle_bokeh_tool)
        self.btn_bokeh.setIcon(QIcon("src/img/icon_auto.png"))
        self.btn_bokeh.setIconSize(QSize(25, 25))

        self.lbl_image_origin = QLabel("Open image to start",self)
        self.lbl_image_origin.setToolTip("Image Before")
        self.lbl_image_origin.resize(self.width / 3, self.height)
        self.lbl_image_origin.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_image_origin.mousePressEvent = handle_event.start_crop
        self.lbl_image_origin.mouseReleaseEvent = handle_event.crop_image
        self.lbl_image_origin.mouseMoveEvent = handle_event.crop_move

        self.lbl_image_process = QLabel("Open image to start", self)
        self.lbl_image_process.setToolTip("Image After")
        self.lbl_image_process.resize(self.width / 3, self.height)
        self.lbl_image_process.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_image_process.mouseMoveEvent = handle_event.draw_image

        #line vertical
        line_vertical_top = QLabel(self)

        #img histogram
        self.figure = plt.figure(figsize=(16,9))
        self.canvas_histogram = FigureCanvas(self.figure)
        self.canvas_histogram.figure.set_size_inches(3,1, forward=False)

        self.ckb_gray = QCheckBox("Ảnh xám")
        self.ckb_gray.stateChanged.connect(handle_event.gray)
        self.ckb_invert = QCheckBox("Đảo ảnh")
        self.ckb_invert.stateChanged.connect(handle_event.invert)

        # checkbox group
        hbox_checkbox1 = QHBoxLayout()
        hbox_checkbox1.addWidget(self.ckb_gray)
        hbox_checkbox1.addWidget(self.ckb_invert)

        hbox_checkbox2 = QHBoxLayout()

        self.ckb_sharpen = QCheckBox("Làm sắc nét")
        self.ckb_sharpen.stateChanged.connect(handle_event.sharpen)
        self.cbb_sharpen = QComboBox()
        self.cbb_sharpen.addItems(["Robert", "Laplacian", "Sobel"])
        self.cbb_sharpen.currentIndexChanged.connect(handle_event.combobox_sharpen_change)
        self.ckb_edge_detection = QCheckBox("Tách biên")
        self.ckb_edge_detection.stateChanged.connect(handle_event.edge_detection)
        self.cbb_edge_detection = QComboBox()
        self.cbb_edge_detection.addItems(["Robert", "Laplacian", "Sobel"])
        self.cbb_edge_detection.currentIndexChanged.connect(handle_event.combobox_edge_detection_change)

        hbox_checkbox2.addWidget(self.ckb_sharpen)
        hbox_checkbox2.addWidget(self.cbb_sharpen)
        hbox_checkbox2.addStretch(1)
        hbox_checkbox2.addWidget(self.ckb_edge_detection)
        hbox_checkbox2.addWidget(self.cbb_edge_detection)


        # threshsold ###############################
        hbox_slider_process = QHBoxLayout()
        vbox_label_slider = QVBoxLayout()
        vbox_slider = QVBoxLayout()
        
        lbl_threshsold = QLabel("Threshsold")
        lbl_threshsold.setObjectName("lblSliderName")

        self.sld_threshsold = QSlider(Qt.Horizontal, self)
        self.sld_threshsold.setRange(0, 255)
        self.sld_threshsold.setValue(0)
        self.sld_threshsold.valueChanged.connect(
            lambda: handle_event.change_filter("threshsold", self.sld_threshsold.value()))
        self.sld_threshsold.sliderReleased.connect(
            lambda: handle_event.release("threshsold", self.sld_threshsold.value()))

        vbox_label_slider.addWidget(lbl_threshsold)
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
        self.sld_contrast.setRange(-127, 127)
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
        self.rb_blur1.toggled.connect(lambda: handle_event.change_blur_method("average"))
        self.rb_blur1.setChecked(True)
        rb_blur2 = QRadioButton("Hàm Gaussian", self)
        rb_blur2.toggled.connect(lambda: handle_event.change_blur_method("gaussian"))
        btn_group_blur.addButton(self.rb_blur1)
        btn_group_blur.addButton(rb_blur2)

        hbox_blur.addWidget(lblText_blur)
        hbox_blur.addWidget(self.rb_blur1)
        hbox_blur.addWidget(rb_blur2)
        vbox_blur.addLayout(hbox_blur)
        vbox_blur.addWidget(self.sld_blur)

        # mask_threshsold ###############################
        self.sld_mask_threshsold = QSlider(Qt.Horizontal, self)
        self.sld_mask_threshsold.setRange(0, 100)
        self.sld_mask_threshsold.setValue(50)
        self.sld_mask_threshsold.valueChanged.connect(handle_event.mask_threshsold)
        self.sld_mask_threshsold.sliderReleased.connect(
            lambda: handle_event.release("mask_threshsold", self.sld_mask_threshsold.value()))

        self.lbl_text_mask_threshsold = QLabel('Mask threshsold', self)
        self.lbl_text_mask_threshsold.setObjectName("lblSliderName")

         # bokeh_blur ###############################
        self.sld_bokeh_blur = QSlider(Qt.Horizontal, self)
        self.sld_bokeh_blur.setRange(0, 70)
        self.sld_bokeh_blur.setValue(0)
        self.sld_bokeh_blur.valueChanged.connect(
            lambda: handle_event.change_segment_value("bokeh_blur_value", self.sld_bokeh_blur.value()))
        self.sld_bokeh_blur.sliderReleased.connect(
            lambda: handle_event.release("bokeh_blur", self.sld_bokeh_blur.value()))

        self.lbl_text_bokeh_blur = QLabel('Bokeh blur', self)
        self.lbl_text_bokeh_blur.setObjectName("lblSliderName")

        vbox_bokeh_option = QVBoxLayout()
        btn_group_bokeh = QButtonGroup(self)
        self.rb_bokeh_option1 = QRadioButton("Only mask")
        self.rb_bokeh_option1.toggled.connect(
            lambda: handle_event.change_segment_value("option","mask"))
        self.rb_bokeh_option2 = QRadioButton("Only Object")
        self.rb_bokeh_option2.toggled.connect(
            lambda: handle_event.change_segment_value("option","object"))
        self.rb_bokeh_option3 = QRadioButton("Bokeh")
        self.rb_bokeh_option3.setChecked(True)
        self.rb_bokeh_option3.toggled.connect(
            lambda: handle_event.change_segment_value("option","bokeh"))

        btn_group_bokeh.addButton(self.rb_bokeh_option1)
        btn_group_bokeh.addButton(self.rb_bokeh_option2)
        btn_group_bokeh.addButton(self.rb_bokeh_option3)

        self.btn_repaint_mask = QPushButton(self)
        self.btn_repaint_mask.setToolTip("Edit mask")
        self.btn_repaint_mask.clicked.connect(self.toggle_edit_mask)
        self.btn_repaint_mask.setIcon(QIcon("src/img/icon_mask.png"))
        self.btn_repaint_mask.setIconSize(QSize(25, 25))

        self.rb_add_mask = QRadioButton("Add pixel")
        self.rb_sub_mask = QRadioButton("Sub pixel")
        btn_group_edit_mask = QButtonGroup(self)
        btn_group_edit_mask.addButton(self.rb_add_mask)
        btn_group_edit_mask.addButton(self.rb_sub_mask)
        self.rb_add_mask.setChecked(True)

        hbox_edit_mask = QHBoxLayout()
        hbox_edit_mask.addWidget(self.btn_repaint_mask)
        hbox_edit_mask.addWidget(self.rb_add_mask)
        hbox_edit_mask.addWidget(self.rb_sub_mask)

        vbox_bokeh_option.addWidget(self.rb_bokeh_option1)
        vbox_bokeh_option.addWidget(self.rb_bokeh_option2)
        vbox_bokeh_option.addWidget(self.rb_bokeh_option3)
        vbox_bokeh_option.setSpacing(10)

        vbox_label_slider.addStretch(1)
        vbox_slider.addStretch(1)
        vbox_label_slider.addLayout(vbox_bokeh_option)
        vbox_slider.addLayout(hbox_edit_mask)
        vbox_label_slider.addWidget(self.lbl_text_mask_threshsold)
        vbox_slider.addWidget(self.sld_mask_threshsold)
        vbox_label_slider.addWidget(self.lbl_text_bokeh_blur)
        vbox_slider.addWidget(self.sld_bokeh_blur)

        hbox_slider_process.addLayout(vbox_label_slider)
        hbox_slider_process.addLayout(vbox_slider)

        vboxRight = QVBoxLayout()
        vboxRight.addWidget(self.canvas_histogram)
        vboxRight.addLayout(hbox_checkbox1)
        vboxRight.addLayout(hbox_checkbox2)
        vboxRight.addLayout(vbox_blur)
        vboxRight.addLayout(hbox_slider_process)

        ################################## set style ###########################################
        self.lbl_image_origin.setStyleSheet("background-color: #282828;  ")
        self.lbl_image_process.setStyleSheet("background-color: #282828; ")
        # self.canvas_histogram.setStyleSheet("background-color: #282828; ")

        line_vertical_top.setStyleSheet("border-right : 1px solid black;")
        line_vertical_top.setGeometry(self.lbl_image_process.width() + self.lbl_image_origin.width() + 20, 0, 1, self.height)
        #################################### setup layout #####################################

        hboxImg = QHBoxLayout()
        hboxImg.addWidget(self.lbl_image_origin)
        hboxImg.addWidget(self.lbl_image_process)

        hboxTopTool = QHBoxLayout()
        hboxTopTool.addWidget(btn_open)
        hboxTopTool.addWidget(btn_save)
        hboxTopTool.addWidget(btn_histogram)
        hboxTopTool.addWidget(self.btn_change_background)
        hboxTopTool.addStretch(1)
        hboxTopTool.addWidget(self.lbl_point_size)
        hboxTopTool.addWidget(self.sld_point_size)
        hboxTopTool.addWidget(self.btn_crop)
        hboxTopTool.addWidget(self.btn_draw)
        hboxTopTool.addWidget(self.btn_bokeh)
        # hboxTopTool.addWidget(cbb, 2)
        hboxTopTool.setContentsMargins(50, 10, 0, 10)

        vboxLeft = QVBoxLayout()
        vboxLeft.addLayout(hboxTopTool,1)
        vboxLeft.addLayout(hboxImg,9)

        hboxMain = QHBoxLayout()
        hboxMain.addLayout(vboxLeft,8)
        hboxMain.addWidget(line_vertical_top)
        hboxMain.addLayout(vboxRight,2)

        self.rb_bokeh_option1.hide()
        self.rb_bokeh_option2.hide()
        self.rb_bokeh_option3.hide()
        self.btn_repaint_mask.hide()
        self.sld_mask_threshsold.hide()
        self.lbl_text_mask_threshsold.hide()
        self.sld_bokeh_blur.hide()
        self.lbl_text_bokeh_blur.hide()
        self.lbl_point_size.hide()
        self.sld_point_size.hide()
        self.rb_sub_mask.hide()
        self.rb_add_mask.hide()
        self.btn_change_background.hide()

        #################################################################################
        self.setLayout(hboxMain)
        self.show()

    def toggle_bokeh_tool(self):
        self.bokeh_activated = not self.bokeh_activated
        if self.bokeh_activated:
            self.rb_bokeh_option1.show()
            self.rb_bokeh_option2.show()
            self.rb_bokeh_option3.show()
            self.btn_repaint_mask.show()
            self.sld_mask_threshsold.show()
            self.lbl_text_mask_threshsold.show()
            self.sld_bokeh_blur.show()
            self.lbl_text_bokeh_blur.show()
            self.btn_change_background.show()
        else:
            self.rb_bokeh_option1.hide()
            self.rb_bokeh_option2.hide()
            self.rb_bokeh_option3.hide()
            self.btn_repaint_mask.hide()
            self.sld_mask_threshsold.hide()
            self.lbl_text_mask_threshsold.hide()
            self.sld_bokeh_blur.hide()
            self.lbl_text_bokeh_blur.hide()
            self.btn_change_background.hide()
        handle_event.change_segment_value("option","bokeh")

    def toggle_histogram(self):
        self.show_histogram = not self.show_histogram
        if self.show_histogram:
            self.canvas_histogram.show()
        else:
            self.canvas_histogram.hide()

    def toggle_edit_mask(self):
        self.is_editting_mask = not self.is_editting_mask
        if self.is_editting_mask:
            if self.is_drawing:
                self.toggle_draw_mode()
            self.rb_sub_mask.show()
            self.rb_add_mask.show()
            self.btn_repaint_mask.setStyleSheet("background-color: #10bef3;")
        else:
            self.rb_sub_mask.hide()
            self.rb_add_mask.hide()
            self.btn_repaint_mask.setStyleSheet("background-color: #535353;  ")
        self.toggle_sld_point_size()

    def draw_histogram(self, img):
        if self.show_histogram:
            cal_histogram(img, self.figure)
            self.canvas_histogram.draw()

    def toggle_draw_mode(self):
        self.is_drawing = not self.is_drawing
        if self.is_drawing:
            if self.is_editting_mask:
                self.toggle_edit_mask()
            self.btn_draw.setStyleSheet("background-color: #10bef3;  ")
        else:    
            self.btn_draw.setStyleSheet("background-color: #535353;  ")
        self.toggle_sld_point_size()

    def toggle_crop_mode(self):
        self.is_cropping = not self.is_cropping
        if self.is_cropping:
            self.btn_crop.setStyleSheet("background-color: #10bef3;  ")
            self.lbl_image_origin.setCursor(
                self.change_cursor_size(self.cursor_crop, 20))
        else:
            self.btn_crop.setStyleSheet("background-color: #535353;  ")
            self.lbl_image_origin.setCursor(QCursor())

    def toggle_sld_point_size(self):
        self.show_sld_point_size = not self.show_sld_point_size
        if self.show_sld_point_size:
            self.lbl_point_size.show()
            self.sld_point_size.show()
            self.lbl_image_process.setCursor(
                self.change_cursor_size(self.cursor_pix))
        else:
            self.lbl_point_size.hide()
            self.sld_point_size.hide()
            self.lbl_image_process.setCursor(QCursor())

    def change_cursor_size(self, cursor_img = None, size = 0):
        if size == 0:
            size = self.sld_point_size.value()
            size = size*1.5
            cursor_img = self.cursor_pix
            cursor_scaled = cursor_img.scaled(QSize(size, size), Qt.KeepAspectRatio)
            cursor = QCursor(cursor_scaled)
            self.lbl_image_process.setCursor(cursor)
        else:
            cursor_scaled = cursor_img.scaled(QSize(size, size), Qt.KeepAspectRatio)
            cursor = QCursor(cursor_scaled)
        return cursor

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
