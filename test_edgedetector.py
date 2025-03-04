import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QComboBox
from PyQt5.QtGui import QPixmap, QImage

class EdgeDetectionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edge Detection App")
        self.setGeometry(100, 100, 600, 500)
        
        self.image_label = QLabel(self)
        self.image_label.setText("Upload an image")
        self.image_label.setStyleSheet("border: 1px solid black;")
        
        self.upload_button = QPushButton("Upload Image", self)
        self.upload_button.clicked.connect(self.upload_image)
        
        self.filter_combo = QComboBox(self)
        self.filter_combo.addItems(["Canny", "Roberts", "Sobel", "Prewitt"])
        
        self.apply_button = QPushButton("Apply Filter", self)
        self.apply_button.clicked.connect(self.apply_filter)
        
        self.normalize_button = QPushButton("Normalize Image", self)
        self.normalize_button.clicked.connect(self.normalize_image)
        
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.filter_combo)
        layout.addWidget(self.apply_button)
        layout.addWidget(self.normalize_button)
        
        self.setLayout(layout)
        self.image = None

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.image = cv2.imread(file_path)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.display_image(self.image)

    def display_image(self, img):
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_image = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

    def apply_filter(self):
        if self.image is None:
            return
        
        filter_type = self.filter_combo.currentText()
        gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        
        if filter_type == "Canny":
            processed = cv2.Canny(gray, 100, 200)
        elif filter_type == "Roberts":
            kernel_x = np.array([[1, 0], [0, -1]], dtype=np.float32)
            kernel_y = np.array([[0, 1], [-1, 0]], dtype=np.float32)
            grad_x = cv2.filter2D(gray, -1, kernel_x)
            grad_y = cv2.filter2D(gray, -1, kernel_y)
            gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
            processed = np.clip(gradient_magnitude, 0, 255).astype(np.uint8)
        elif filter_type == "Sobel":
            grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
            processed = np.clip(gradient_magnitude, 0, 255).astype(np.uint8)
        elif filter_type == "Prewitt":
            kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
            kernel_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float32)
            grad_x = cv2.filter2D(gray, -1, kernel_x)
            grad_y = cv2.filter2D(gray, -1, kernel_y)
            gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
            processed = np.clip(gradient_magnitude, 0, 255).astype(np.uint8)
        
        self.display_image(cv2.cvtColor(processed, cv2.COLOR_GRAY2RGB))
    
    def normalize_image(self):
        if self.image is None:
            return
        
        gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY).astype(np.float32)
        normalized = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
        normalized = normalized.astype(np.uint8)
        self.display_image(cv2.cvtColor(normalized, cv2.COLOR_GRAY2RGB))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EdgeDetectionApp()
    window.show()
    sys.exit(app.exec_())