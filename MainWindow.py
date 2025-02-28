from PyQt5.QtWidgets import QMainWindow,QComboBox, QSpinBox, QWidget, QApplication, QPushButton, QLabel, QSlider,QProgressBar,QGraphicsView,QGraphicsScene
from PyQt5.QtGui import QIcon
import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from HistogramOperations import HistogramOperations
from ImageViewer import ImageViewer
from NoiseAdder import NoiseAdder
from NoiseFilter import NoiseFilter

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        loadUi("MainWindow.ui", self)
        
        #Fatma
        self.hist_widget= self.findChild(QWidget,'histogramWidget')
        self.dist_widget= self.findChild(QWidget,'distributionWidget')
        self.hist_operations= HistogramOperations(self.hist_widget,self.dist_widget)
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

        #joudy
        self.input_view = self.findChild(QGraphicsView, "inputGraphicsView")
        self.output_view = self.findChild(QGraphicsView, "outputGraphicsView")
        self.viewer_instance =ImageViewer(self.hist_operations, self.input_view, self.output_view) 

        #Laila
        self.noise = self.findChild(QComboBox, "noisesCombo_2")
        self.noise.currentIndexChanged.connect(self.apply_noise)
        self.noise_slider1 = self.findChild(QSlider, "noiseSlider1")
        self.noise_slider1.valueChanged.connect(self.apply_noise)
        self.noise_slider2 = self.findChild(QSlider, "noiseSlider2")
        self.noise_slider2.setVisible(False)
        self.noise_slider2.valueChanged.connect(self.apply_noise)
        self.slider_label1 = self.findChild(QLabel, "percentLabel1")
        self.slider_label2 = self.findChild(QLabel, "percentLabel2")
        self.slider_label2.setVisible(False)
        self.noise_param1 = self.findChild(QLabel, "label1")
        self.noise_param2 = self.findChild(QLabel, "label2")
        self.noise_param2.setVisible(False)

        self.filter = self.findChild(QComboBox, "filtersCombo")
        self.filter.currentIndexChanged.connect(self.apply_filter)
        self.filter_slider1 = self.findChild(QSlider, "filterSlider1")
        self.filter_slider1.valueChanged.connect(self.apply_filter)
        self.filter_slider2 = self.findChild(QSlider, "filterSlider2")
        self.filter_slider2.valueChanged.connect(self.apply_filter)
        self.filter_slider2.setVisible(False)
        self.filter_param2 = self.findChild(QLabel, "filterLabel3")
        self.filter_param2.setVisible(False)
        self.filter_label1 = self.findChild(QLabel, "filterLabel1")
        self.filter_label2 = self.findChild(QLabel, "filterLabel2")
        self.filter_label2.setVisible(False)
        self.filter_slider1.setMinimum(3)
        self.filter_slider1.setMaximum(15)
        self.filter_slider1.setSingleStep(2) 
        self.filter_slider2.setMinimum(1) 
        self.filter_slider2.setMaximum(10) 
        self.filter_slider2.setSingleStep(1)  

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

    def apply_noise(self, index):
        loaded_image = self.viewer_instance.get_loaded_image()
        if loaded_image is None:
            print("No image loaded.")
            return
        noise_type = self.noise.currentText()
        noise_adder = NoiseAdder(loaded_image)

        param1 = self.noise_slider1.value()
        param2 = self.noise_slider2.value()
        self.slider_label2.setText(str(param2))
        self.slider_label1.setText(str(param1))        

        if noise_type == "Salt & Pepper":
            self.noise_param2.setText("Pepper")
            self.noise_param2.setVisible(True)
            self.noise_param1.setText("Salt") 
            self.noise_slider2.setVisible(True)
            param1 = self.noise_slider1.value() / 100.0
            param2 = self.noise_slider2.value() / 100.0
            self.slider_label2.setVisible(True)
            self.slider_label2.setText(str(param2))
            self.slider_label1.setText(str(param1))

            noisy_image = noise_adder.salt_and_pepper_noise(param1, param2)

        elif noise_type == "Gaussian":
            self.slider_label2.setVisible(True)
            self.noise_param2.setText("Stddev")
            self.noise_param2.setVisible(True)
            self.noise_param1.setText("Mean") 
            self.noise_slider2.setVisible(True)     

            noisy_image = noise_adder.gaussian_noise(param1, param2)

        elif noise_type == "Uniform":
            self.slider_label2.setVisible(False)
            self.noise_slider2.setVisible(False)
            self.noise_param2.setVisible(False)
            self.noise_param1.setText("Intensity")
            param1 = self.noise_slider1.value() 

            noisy_image = noise_adder.uniform_noise(param1)        

        else:
            print("Invalid noise type.")
            return
        
        self.noisy_image = noisy_image
        # Display the noisy image in the output view
        self.viewer_instance.display_image(noisy_image, self.output_view)

    def apply_filter(self, index):
        if not hasattr(self, "noisy_image") or self.noisy_image is None:
            print("No noisy image to filter.")
            return

        filter_type = self.filter.currentText()
        noise_filter = NoiseFilter(self.noisy_image)

        param1 = self.filter_slider1.value()
        param2 = self.filter_slider2.value()

        if filter_type == "Average":
            self.filter_label2.setVisible(False)
            self.filter_slider2.setVisible(False)
            self.filter_param2.setVisible(False)   
            self.filter_label1.setText(str(param1)) 

            filtered_image = noise_filter.average_filter(param1)

        elif filter_type == "Gaussian":
            self.filter_label2.setVisible(True)
            self.filter_slider2.setVisible(True)
            self.filter_param2.setVisible(True)     
            self.filter_label1.setText(str(param1))  
            self.filter_label2.setText(str(param2))
         
            filtered_image = noise_filter.gaussian_filter(param1, param2)

        elif filter_type == "Median":
            self.filter_label2.setVisible(False)
            self.filter_slider2.setVisible(False)
            self.filter_param2.setVisible(False)
            self.filter_label1.setText(str(param1))  
            self.filter_label2.setText(str(param2))     

            filtered_image = noise_filter.median_filter(param1)

        else:
            print("Invalid filter type.")
            return
        
        self.viewer_instance.display_image(filtered_image, self.output_view)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # window.showMaximized()
    sys.exit(app.exec_())     