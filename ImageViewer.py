from PyQt5.QtWidgets import QFileDialog, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QImage, QPixmap
import cv2
import numpy as np

class ImageViewer:
    def __init__(self, histogram_cls=None, transformation_cls=None,  input_view=None, output_view=None, index=0):
        self._input_view = input_view
        self._output_view = output_view
        self._image_path = None
        self.img_data=None 
        self.histogram_cls = histogram_cls 
        self.transformation_cls=transformation_cls
        self.index=index

        self._input_scene = QGraphicsScene() if input_view else None
        self._output_scene = QGraphicsScene() if output_view else None

        if self._input_view:
            self._input_view.setScene(self._input_scene)

        if self._output_view:
            self._output_view.setScene(self._output_scene)

        self.setup_double_click_event()

    def setup_double_click_event(self):
        if self._input_view:
            self._input_view.mouseDoubleClickEvent = self.handle_double_click

    def handle_double_click(self, event):
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
        )
        if file_path:
            self.browse_image(file_path)

    def browse_image(self, image_path):
        self._image_path = image_path  
        if self.check_extension():
            if self.index ==0:
                self.img_data = cv2.imread(self._image_path, cv2.IMREAD_GRAYSCALE)
            else:
                self.img_data = cv2.imread(self._image_path, cv2.IMREAD_COLOR)  
                # self.img_data = cv2.cvtColor(self.img_data, cv2.COLOR_BGR2RGB)

            if self.img_data is None:
                print("Error loading image.")
                return
            

            self._processed_image = self.img_data  
            if self.histogram_cls:
                self.histogram_cls.set_image(self.img_data)
                self.histogram_cls.show_plots()
            
            if self._input_view:
                if self.index==0:
                    self.display_image(self.img_data, self._input_view)
                elif self.index==1:
                    self.display_RGB_image(self.img_data, self._input_view)
        

    def display_output_image(self, processed_img=None,output=None):
        """ Displays the processed image in the output view when explicitly called. """
        if processed_img is None:
            processed_img = self._processed_image  

        if processed_img is None:
            print("No processed image to display.")
            return



        if output:
            self.display_image(processed_img,output)

        elif self._output_view:
            self.display_image(processed_img, self._output_view)


       
    def display_image(self, img, target):
        """ Display a 2D NumPy array (grayscale image) in either a QGraphicsView or QGraphicsScene. """
        if img is None or not isinstance(img, np.ndarray):
            print("Invalid image data.") 
            return 

        height, width = img.shape
        bytes_per_line = width  

        q_image = QImage(img.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_image)

       
        if isinstance(target, QGraphicsView):
            scene = target.scene() or QGraphicsScene() 
            target.setScene(scene)
            scene.clear()
            scene.addItem(QGraphicsPixmapItem(pixmap))
        elif isinstance(target, QGraphicsScene):
            target.clear()
            target.addItem(QGraphicsPixmapItem(pixmap))
        else:
            print("Invalid target for image display.")


    def display_RGB_image(self, img, target):
        if img is None or not isinstance(img, np.ndarray):
            print("Invalid image data.")
            return 
       
        height, width,channels = img.shape
        bytes_per_line = 3 * width  
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.transformation_cls.set_colored_img(img)
        gray_img=self.transformation_cls.convert_to_grayscale()
        self.display_output_image(gray_img)
        self.transformation_cls.plot_histograms()
        q_image = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
       
        print("entered here")

        pixmap = QPixmap.fromImage(q_image)

        if isinstance(target, QGraphicsView):
            scene = target.scene() or QGraphicsScene()
            target.setScene(scene)
            scene.clear()
            scene.addItem(QGraphicsPixmapItem(pixmap))
        elif isinstance(target, QGraphicsScene):
            target.clear()
            target.addItem(QGraphicsPixmapItem(pixmap))
        else:
            print("Invalid target for image display.")

         

    def check_extension(self):
        valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff']
        if not any(self._image_path.lower().endswith(ext) for ext in valid_extensions):
            print("Invalid image file extension.")
            self._image_path = None  
            return False
        print("Valid image file extension.")
        return True
    
    def get_loaded_image(self):
        return self.img_data
 


    def apply_filtered_image(self, filtered_img, freq=None):
        """ Update the input view if a frequency string is provided, otherwise use the output view. """
        if filtered_img is not None:
            if freq:  
                # If a frequency string is provided, replace the input image
                print(f"Applying frequency filter: {freq}, updating input view.")
                self.display_image(filtered_img, self._input_view)
            else:
                # Otherwise, display in the output view
                print("No frequency specified, displaying in output view.")
                self.display_image(filtered_img, self._output_view)

   