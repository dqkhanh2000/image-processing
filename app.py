
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog
from os.path import expanduser
from src.gui import ImageProcessing

def main():
    app = QApplication(sys.argv)
    gui = ImageProcessing()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()