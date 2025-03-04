from PyQt5.QtWidgets import QMainWindow,QComboBox,QTabWidget, QSpinBox, QWidget, QApplication, QPushButton, QLabel, QSlider,QProgressBar,QGraphicsView,QGraphicsScene
from PyQt5.QtGui import QIcon
import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from HistogramOperations import HistogramOperations
from ImageViewer import ImageViewer
from NoiseAdder import NoiseAdder
from NoiseFilter import NoiseFilter
from EdgeDetectors import EdgeDetectors 
from HybridImage import HybridImage
from PyQt5.QtGui import QImage, QPixmap
from ColoredImg import ColoredImg
from FrequencyFilter import FrequencyFilter
from SignalManager import signal_manager
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        loadUi("MainWindow.ui", self)

        self.input_view = self.findChild(QWidget, "inputImage")
        self.output_view = self.findChild(QWidget, "outputImage")
        
        #Fatma
        self.hist_widget= self.findChild(QWidget,'histogramWidget_5')
        self.dist_widget= self.findChild(QWidget,'distributionWidget')
        self.hist_operations= HistogramOperations(self.hist_widget,self.dist_widget)
        self.equalize_button= self.findChild(QPushButton, 'equalize')
        self.equalize_button.clicked.connect(self.equalize_func)
        self.normalize_button= self.findChild(QPushButton, 'normalize')
        self.normalize_button.clicked.connect(self.normalize_func)
        self.thresholdCombo = self.findChild(QComboBox, 'thresholdCombo')
        self.thresholdCombo.highlighted.connect(self.threshold)
        self.threshold_offset= self.findChild(QSlider, 'thresholdOffset')
        self.block_size= self.findChild(QSpinBox, 'blockSize')
        self.block_size.setValue(11)
        self.threshold_offset.valueChanged.connect(lambda: self.threshold(1))
        self.block_size.valueChanged.connect(lambda: self.threshold(1))
        self.threshold_label = self.findChild(QLabel, "thresoldLabel")

        self.spin_label = self.findChild(QLabel,"label1_2")
        self.thresholdlabel = self.findChild(QLabel,"label_5")
        self.threshold_label.setVisible(False)
        self.block_size.setVisible(False)
        self.threshold_offset.setVisible(False)
        self.spin_label.setVisible(False)
        self.thresholdlabel.setVisible(False) 
        #transformation tab
        self.histogramR= self.findChild(QWidget,'histogramR')
        self.distributionR= self.findChild(QWidget,'distributionR')
        self.histogramG= self.findChild(QWidget,'histogramG')
        self.distributionG= self.findChild(QWidget,'distributionG')
        self.histogramB= self.findChild(QWidget,'histogramB')
        self.distributionB= self.findChild(QWidget,'distributionB')
        self.inputRGB= self.findChild(QGraphicsView,'inputRGB')
        self.outputGrey = self.findChild(QGraphicsView,'outputGrey')
        self.transformation_tab= ColoredImg(self.histogramR, self.distributionR, self.histogramG, self.distributionG, self.histogramB, self.distributionB)


        self.tabWidget= self.findChild(QTabWidget, "tabWidget")
        self.tabWidget.currentChanged.connect(self.on_tab_changed)


        #joudy
        
        self.viewer_instance_tab1 = ImageViewer(self.hist_operations, None, self.input_view, self.output_view)
        self.viewer_instance_tab2 = ImageViewer(None, self.transformation_tab, self.inputRGB, self.outputGrey, index=1)
        self.viewer_instance =self.viewer_instance_tab1
        self.edge_detector= EdgeDetectors(self.viewer_instance.get_loaded_image)
        self.edges_combobox=self.findChild(QComboBox,"edgesCombo")
        self.edges_combobox.currentIndexChanged.connect(
            lambda index: self.apply_edge_detector(self.viewer_instance.get_loaded_image(), index)
        )


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

        self.apply_button = self.findChild(QPushButton, "applyButton")
        self.apply_button.clicked.connect(self.apply)
        self.filter = self.findChild(QComboBox, "filtersCombo")
        self.filter.currentIndexChanged.connect(self.apply)
        self.filter_slider1 = self.findChild(QSlider, "filterSlider1")
        self.filter_slider1.valueChanged.connect(self.update_filter_label)
        self.filter_slider2 = self.findChild(QSlider, "filterSlider2")
        self.filter_slider2.valueChanged.connect(self.update_filter_label)
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




    #hajar
        self.initial_cutoff = 30
        self.hybrid_processor = HybridImage() 
        self.filtered_image1 = None
        self.filtered_image2 = None
        self.filterimage1 = self.findChild(QWidget, "image1")
        self.filterimage2 = self.findChild(QWidget, "image2")
        self.filterimage_Out = self.findChild(QWidget, "output")
        self.filter_select1 = self.findChild(QComboBox, "frequencyCombo1")
        self.filter_select2 = self.findChild(QComboBox, "frequencyCombo2")
        
        self.radiusSlider1 = self.findChild(QSlider, "radiusSlider1")
        self.radiusSlider2 = self.findChild(QSlider, "radiusSlider2_2")
        self.sliderLabel1 = self.findChild(QLabel, "sliderLabel1")
        self.sliderLabel2 = self.findChild(QLabel, "sliderLabel2")
        self.hybird_button= self.findChild(QPushButton, 'hybridButton')
       

    # Update label text to reflect the initial cutoff value
        self.sliderLabel1.setText(f"Cutoff: {0 }")
        self.sliderLabel2.setText(f"Cutoff: {0 }")

       

        self.radiusSlider1.setSingleStep(10)  
        self.radiusSlider2.setSingleStep(10)  

        # Connect sliders to update function
        self.radiusSlider1.valueChanged.connect(lambda: self.update_filter(1))
        self.radiusSlider2.valueChanged.connect(lambda: self.update_filter(2))

        if self.filter_select1:
            self.filter_select1.currentIndexChanged.connect(lambda:self.update_filter(1))

        if self.filter_select2:
            self.filter_select2.currentIndexChanged.connect(lambda:self.update_filter(2))


        self.region1Widget = self.findChild(QWidget, "region1Widget")
        self.region2Widget = self.findChild(QWidget, "region2Widget")

        self.image_viewer_freq1 = ImageViewer(self.hist_operations,None, self.filterimage1, self.filterimage_Out,index=2,img_num=1)
        self.image_viewer_freq2 = ImageViewer(self.hist_operations,None, self.filterimage2, self.filterimage_Out,index=2,img_num=2)
        signal_manager.new_image_loaded.connect(self.reset_ui_for_new_image)

        self.hybird_button.clicked.connect(self.apply_hybird)

       
    def on_tab_changed(self, index):
        if index == 0:
            self.viewer_instance = self.viewer_instance_tab1  # Use existing instance
        elif index == 1:
            self.viewer_instance = self.viewer_instance_tab2  # Use existing instance
        elif index==2:
            self.viewer_instance1= self.image_viewer_freq1
            self.viewer_instance2= self.image_viewer_freq2

    def apply_edge_detector(self,img,index):
        self.viewer_instance.display_output_image(self.edge_detector.apply_filter(img,index))


    def normalize_func(self):
        normalized_img= self.hist_operations.normalize()
        self.viewer_instance.display_output_image(normalized_img)

    def equalize_func(self):
        equalized_img= self.hist_operations.equalize_histogram()
        self.viewer_instance.display_output_image(equalized_img)
    
    def threshold(self, index):
        if index==0:
            self.threshold_label.setVisible(False)
            self.block_size.setVisible(False)
            self.threshold_offset.setVisible(False)
            self.spin_label.setVisible(False)
            self.thresholdlabel.setVisible(False)

            threshold_img= self.hist_operations.global_threshold()
            self.viewer_instance.display_output_image(threshold_img)
        else:
            self.threshold_label.setVisible(True)
            self.block_size.setVisible(True)
            self.threshold_offset.setVisible(True)
            self.spin_label.setVisible(True)
            self.thresholdlabel.setVisible(True)
            self.threshold_label.setText(str(self.threshold_offset.value()))

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

    def update_filter_label(self):
        param1 = self.filter_slider1.value()
        if param1 % 2 == 0:
            param1 += 1
            self.filter_slider1.setValue(param1)  # Set to odd value

        param2 = self.filter_slider2.value()
        if self.filter_slider2.isVisible():
            self.filter_label2.setText(str(param2))

        self.filter_label1.setText(str(param1))

    def apply(self, index):
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

            filtered_image = noise_filter.average_filter(param1)

        elif filter_type == "Gaussian":
            self.filter_label2.setVisible(True)
            self.filter_slider2.setVisible(True)
            self.filter_param2.setVisible(True)     
         
            filtered_image = noise_filter.gaussian_filter(param1, param2)

        elif filter_type == "Median":
            self.filter_label2.setVisible(False)
            self.filter_slider2.setVisible(False)
            self.filter_param2.setVisible(False)   

            filtered_image = noise_filter.median_filter(param1)

        else:
            print("Invalid filter type.")
            return
        
        self.viewer_instance.display_image(filtered_image, self.output_view)






    #hajar
    def apply_frequency_filter(self, img_num,cutoff):
        """Apply selected filter dynamically when an image is loaded or when the user changes the combo box."""
        cutoff=cutoff
        if img_num == 1:
            img_data = self.image_viewer_freq1.get_loaded_image()
            filter_type = self.get_selected_filter(self.filter_select1)

            if img_data is not None:
                filter_obj = FrequencyFilter(img_data)
                self.filtered_image1, mask_image1 = filter_obj.apply_filter(filter_type, cutoff)
                self.image_viewer_freq1.apply_filtered_image(self.filtered_image1, freq=filter_type)
                if self.hybrid_processor is None:
                 self.hybrid_processor=HybridImage(self.filtered_image1, None)

                else:
                 self.hybrid_processor.img1 = self.filtered_image1

            self.display_mask_in_widget(self.region1Widget, mask_image1)

        elif img_num == 2:
            img_data =  self.image_viewer_freq2.get_loaded_image()
            filter_type = self.get_selected_filter(self.filter_select2)

            if img_data is not None:
                filter_obj = FrequencyFilter(img_data)
                self.filtered_image2, mask_image2 = filter_obj.apply_filter(filter_type, cutoff)
                self.image_viewer_freq2.apply_filtered_image(self.filtered_image2, freq=filter_type)

            if self.hybrid_processor is None:
                self.hybrid_processor = HybridImage(None, self.filtered_image2)
            else:
                self.hybrid_processor.img2 = self.filtered_image2  
           
            self.display_mask_in_widget(self.region2Widget, mask_image2)


    def apply_hybird(self):

        if self.hybrid_processor and self.hybrid_processor.img1 is not None and self.hybrid_processor.img2 is not None:
             self.display_hybrid_image()

    def get_selected_filter(self, combo_box):
        """Get selected filter type ('low' or 'high') from the combo box."""
        selected_text = combo_box.currentText().lower()
       # print (selected_text)
        return 'low pass' if "low pass" in selected_text else 'high pass'

    def display_mask_in_widget(self, widget, image):
     """Display a NumPy mask inside the given QWidget."""
     if image is None:
            if hasattr(widget, "label"):
                widget.label.clear()
            return
     height, width = image.shape
     bytes_per_line = width
     q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
     pixmap = QPixmap.fromImage(q_image)

    # Check if the widget already has a QLabel
     if not hasattr(widget, "label"):
        widget.label = QLabel(widget)  # Create QLabel inside the QWidget
        widget.label.setGeometry(0, 0, widget.width(), widget.height())  # Resize QLabel to fit

     widget.label.setPixmap(pixmap.scaled(widget.width(), widget.height()))
     widget.label.show()


    def update_filter(self, img_num):
     """Update the cutoff frequency when the slider is moved and reapply filtering."""
    
     if img_num == 1:
       

        new_cutoff = round(self.radiusSlider1.value() / 10) * 10 
        self.sliderLabel1.setText(f"Cutoff: {new_cutoff} Hz")

        # Reapply filter with updated cutoff
        self.apply_frequency_filter(img_num, new_cutoff)

     elif img_num == 2:
       
        new_cutoff = round(self.radiusSlider2.value() / 10) * 10
        self.sliderLabel2.setText(f"Cutoff: {new_cutoff} Hz")

        # Reapply filter with updated cutoff
        self.apply_frequency_filter(img_num, new_cutoff)

   


    def display_hybrid_image(self):
     """Generate and display the hybrid image."""
     hybrid_result = self.hybrid_processor.create_hybrid("low-high")

     if hybrid_result is not None:
        self.image_viewer_freq1.display_output_image(hybrid_result, self.filterimage_Out)





    def reset_ui_for_new_image(self, img_num):
        """ Reset slider and mask when a new image is loaded. """
        if img_num == 1:
            self.radiusSlider1.blockSignals(True)
            self.filter_select1.blockSignals(True)
            self.radiusSlider1.setValue(30)
            cutoff1 = self.radiusSlider1.value()   # Reset slider to 0
            self.sliderLabel1.setText(f"Cutoff: {cutoff1} Hz")
            self.filter_select1.setCurrentIndex(1)  
            self.radiusSlider1.blockSignals(False)
            self.filter_select1.blockSignals(False)

            self.apply_frequency_filter(1,cutoff1)
        elif img_num == 2:
            self.radiusSlider2.blockSignals(True)
            self.filter_select2.blockSignals(True)

            self.radiusSlider2.setValue(30)
            cutoff2 = self.radiusSlider2.value() 
            self.sliderLabel2.setText(f"Cutoff: {cutoff2} Hz")
            self.filter_select2.setCurrentIndex(2) 
            self.radiusSlider2.blockSignals(False)
            self.filter_select2.blockSignals(False)


            self.apply_frequency_filter(2,cutoff2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # window.showMaximized()
    sys.exit(app.exec_())