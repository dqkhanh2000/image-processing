    """
        Created by dqkhanh2000
    """
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog
import src.execute as execute
from os.path import expanduser

def main():
    app = QApplication(sys.argv)
    gui = execute.get_gui()

    fname = QFileDialog.getOpenFileName(None, 'Open file', expanduser("~"), "Image files (*.jpg *.png *.gif)")
    if len(fname[0]) != 0:
        execute.root_image_path = fname[0]
        execute.load_image_from_file()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()