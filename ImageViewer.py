from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QEvent, Qt
import cv2
import numpy as np
from SignalManager import signal_manager

class ImageViewer(QWidget):
    def __init__(self, histogram_cls=None, transformation_cls=None, input_view=None, output_view=None, index=0, img_num=None):
        super().__init__()
        self.img_num = img_num
        self.index = index
        self._image_path = None
        self.img_data = None
        self._is_grey = False
        self.histogram_cls = histogram_cls
        self.transformation_cls = transformation_cls
        self.input_view = input_view
        self.output_view = output_view

        self.setup_double_click_event()

       
    
    def setup_double_click_event(self):
        if self.input_view:
            self.input_view.mouseDoubleClickEvent = self.handle_double_click
    
    def eventFilter(self, obj, event):
        if obj == self.input_view and event.type() == QEvent.MouseButtonDblClick:
            self.handle_double_click()
            return True
        return super().eventFilter(obj, event)
    
    def handle_double_click(self, event=None):
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
        )
        if file_path:
            self.browse_image(file_path)
    
    def browse_image(self, image_path):
        self._image_path = image_path
        if self.check_extension():
            if self.index in [0, 2]:
                self.img_data = cv2.imread(self._image_path, cv2.IMREAD_GRAYSCALE)
                self._is_grey = True
            else:
                self.img_data = cv2.imread(self._image_path, cv2.IMREAD_COLOR)
                self._is_grey = False

            if self.img_data is None:
                print("Error loading image.")
                return

            

            self._processed_image = self.img_data  # Store the processed image

            if self.histogram_cls:
                self.histogram_cls.set_image(self.img_data)
                self.histogram_cls.show_plots()
            if self.input_view:
                if self.index==0:
                        self.display_image(self.img_data, self.input_view)
                elif self.index==1:
                        self.display_RGB_image(self.img_data, self.input_view)
                elif self.index==2:
                    self.display_image(self.img_data, self.input_view)
                    signal_manager.new_image_loaded.emit(self.img_num)

            
    
    def display_output_image(self, processed_img=None, output=None):
        if processed_img is None:
            processed_img = self._processed_image  
        if processed_img is None:
            print("No processed image to display.")
            return
        if output:
            self.display_image(processed_img, output)
        elif self.output_view:
            self.display_image(processed_img, self.output_view)
    
    
    def display_image(self, img, target):
        
        if img is None or not isinstance(img, np.ndarray):
            print("Invalid image data.")
            return

        # Ensure the image is grayscale
        if len(img.shape) == 3:  # If it's a color image, convert to grayscale
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        height, width = img.shape
        bytes_per_line = width

       
        if not img.flags['C_CONTIGUOUS']:
            img = np.ascontiguousarray(img)

       
        q_image = QImage(img.data, width, height, bytes_per_line, QImage.Format_Grayscale8)

        if q_image.isNull():
            print("Failed to create QImage.")
            return

       
        pixmap = QPixmap.fromImage(q_image)

        
        for child in target.findChildren(QLabel):
            child.deleteLater()

        label = QLabel(target)
        label.setPixmap(pixmap.scaled(target.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        label.setScaledContents(True)
        label.setGeometry(0, 0, target.width(), target.height())

        # Ensure the label is visible and on top
        label.show()
        label.raise_()

        print(f"Grayscale image displayed in widget with size: {target.size()}")


    def display_RGB_image(self, img, target):
        if img is None or not isinstance(img, np.ndarray):
            print("Invalid image data.")
            return

        # Ensure the image is in BGR format (OpenCV default)
        if len(img.shape) == 2:  # If it's grayscale, convert to BGR
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        height, width, channels = img.shape
        bytes_per_line = 3 * width  # RGB images have 3 channels


        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.transformation_cls.set_colored_img(img)
        gray_img=self.transformation_cls.convert_to_grayscale()
        self.display_output_image(gray_img)
        self.transformation_cls.plot_histograms()

        
        q_image = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)

        if q_image.isNull():
            print("Failed to create QImage.")
            return

        # Convert QImage to QPixmap
        pixmap = QPixmap.fromImage(q_image)

        # Clear any existing QLabel in the widget
        for child in target.findChildren(QLabel):
            child.deleteLater()

        # Create a new QLabel and add it to the widget
        label = QLabel(target)
        label.setPixmap(pixmap.scaled(target.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        label.setScaledContents(True)
        label.setGeometry(0, 0, target.width(), target.height())

        # Ensure the label is visible and on top
        label.show()
        label.raise_()

        print(f"RGB image displayed in widget with size: {target.size()}")      
    def check_extension(self):
        valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff']
        if not any(self._image_path.lower().endswith(ext) for ext in valid_extensions):
            print("Invalid image file extension.")
            self._image_path = None  
            return False
        print("Valid image file extension.")
        return True
    

    def apply_filtered_image(self, filtered_img, freq=None):
        """ Update the input view if a frequency string is provided, otherwise use the output view. """
        if filtered_img is not None:
            if freq:  
                self.display_image(filtered_img, self.input_view)
            else:
                
                self.display_image(filtered_img, self.output_view)
    
    def check_grey_scale(self, image):
        if len(image.shape) == 2:
            return True  
        b, g, r = cv2.split(image)
        return cv2.countNonZero(b - g) == 0 and cv2.countNonZero(b - r) == 0
    
    def get_loaded_image(self):
        return self.img_data
