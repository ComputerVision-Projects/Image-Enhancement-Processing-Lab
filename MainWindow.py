from PyQt5.QtWidgets import QMainWindow,QComboBox, QSpinBox, QWidget, QApplication, QPushButton, QLabel, QSlider,QProgressBar,QGraphicsView,QGraphicsScene
from PyQt5.QtGui import QIcon
import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from HistogramOperations import HistogramOperations
from ImageViewer import ImageViewer
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        loadUi("MainWindow.ui", self)
        
        #Fatma
        self.hist_widget= self.findChild(QWidget,'histogramWidget')
        self.dist_widget= self.findChild(QWidget,'distributionWidget')
        self.hist_operations= HistogramOperations(self.hist_widget,self.dist_widget)
        self.viewer_instance =ImageViewer(self.hist_operations) 
        self.equalize= self.findChild(QPushButton, 'equalize')
        self.equalize.clicked.connect(self.equalize())
        self.normalize= self.findChild(QPushButton, 'normalize')
        self.normalize.clicked.connect(self.normalize())
        self.thresholdCombo = self.findChild(QComboBox, 'thresholdCombo')
        self.thresholdCombo.currentIndexChanged.connect(self.threshold)
        self.threshold_offset= self.findChild(QSlider, 'threshold_offset')
        self.block_size= self.findChild(QSpinBox, 'block_size')
        self.threshold_offset.valueChanged.connect(lambda: self.threshold(1))
        self.block_size.valueChanged.connect(lambda: self.threshold(1))

    def normalize(self):
        normalized_img= self.hist_operations.normalize()
        self.viewer_instance.display_output_image(normalized_img)

    def equalize(self):
        equalized_img= self.hist_operations.equalize_histogram()
        self.viewer_instance.display_output_image(equalized_img)
    
    def threshold(self, index):
        if index==0:
            threshold_img= self.hist_operations.global_threshold()
            self.viewer_instance.display_output_image(threshold_img)
        else:
            threshold_img= self.hist_operations.local_threshold(self.block_size.value(), self.threshold_offset.value())
            self.viewer_instance.display_output_image(threshold_img)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # window.showMaximized()
    sys.exit(app.exec_())     