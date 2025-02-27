from PyQt5.QtWidgets import QFileDialog, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QImage, QPixmap
import cv2
import numpy as np

class BrowseImage:
    def __init__(self, input_view=None, output_view=None):
        self._input_view = input_view
        self._output_view = output_view
        self._image_path = None  

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
            gray_img = cv2.imread(self._image_path, cv2.IMREAD_GRAYSCALE)
            if gray_img is None:
                print("Error loading image.")
                return
            
            self._processed_image = gray_img  

            
            if self._input_view:
                self.display_image(gray_img, self._input_view)

    def display_output_image(self, processed_img=None):
        """ Displays the processed image in the output view when explicitly called. """
        if processed_img is None:
            processed_img = self._processed_image  

        if processed_img is None:
            print("No processed image to display.")
            return

        if self._output_view:
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

    def check_extension(self):
        """Check if the file has a valid image extension."""
        valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff']
        if not any(self._image_path.lower().endswith(ext) for ext in valid_extensions):
            print("Invalid image file extension.")
            self._image_path = None  
            return False
        print("Valid image file extension.")
        return True
