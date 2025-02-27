from PyQt5.QtWidgets import QMainWindow,QComboBox, QCheckBox, QRadioButton, QApplication, QPushButton, QLabel, QSlider,QProgressBar, QWidget,QLineEdit
from PyQt5.QtWidgets import QMainWindow,QComboBox, QCheckBox, QRadioButton, QApplication, QPushButton, QLabel, QSlider,QProgressBar,QGraphicsView,QGraphicsScene
from PyQt5.QtGui import QIcon
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        loadUi("MainWindow.ui", self)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # window.showMaximized()
    sys.exit(app.exec_())     