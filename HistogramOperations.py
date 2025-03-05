import numpy as np
from scipy.interpolate import interp1d
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import cv2


class HistogramOperations:
    def __init__(self, widget1, widget2):
        self.image_data=None
        self.widget1= widget1 #histogran widget
        self.widget2= widget2 #distribution curve widget
        
    def get_histogram(self, img, key=None):
       # Compute histogram (256 values) and bin edges (257 values)
        if key =='normalize':
            rangee=(0,1)
        else:
            rangee =(0,256)
        histogram, bins = np.histogram(img, bins=256, range=rangee)
        # Ensure both have 256 elements
        if bins.shape[0] != histogram.shape[0]:  
            bins = bins[:-1]  # Remove the last bin edge to match histogram size
        # Final shape check
        assert histogram.shape == bins.shape, f"Shape mismatch: {histogram.shape} vs {bins.shape}"
        return histogram, bins
    
    def get_distribution_curve(self, bins, histogram):
        #one method is interpolation
        # Compute bin centers
        # bin_centers = (bins[:-1] + bins[1:]) / 2
        # #creates a continuous function that can estimate histogram values at any intensity between 0-255
        # interpolated_hist= interp1d(bin_centers, histogram, 'cubic', fill_value='extrapolate')
        # x_smooth = np.linspace(0, 255, 1000)  # Fine grid
        # y_smooth= interpolated_hist(x_smooth)

        #other method is KDE
        # kde= gaussian_kde(histogram)
        # x_values = np.linspace(min(bins), max(bins), 1000)
        # pdf= kde(x_values)


        #other method is CDF
        cdf = histogram.cumsum() / histogram.sum()
        assert cdf.shape == bins.shape, f"Shape mismatch: {cdf.shape} vs {bins.shape}"
        return bins, cdf

    def show_plots(self, img_data=None, key=None):
        if img_data is None:
            img_data= self.image_data
        if key=='normalize':
            key2='normalize'
        else:
            key2 =None
        bins, histogram= self.get_histogram(img_data, key)
        self.plot_histogram(bins, histogram,self.widget1, key_show='histogram', key2=key2)
        x_values, pdf= self.get_distribution_curve(bins, histogram)
        self.plot_histogram(x_values, pdf, self.widget2, key_show='distribution')

    def plot_histogram(self, bins, histogram, parent_widget, key_show='histogram', key2=None):
        if parent_widget is None:
            print("Error: parent_widget is None. Cannot plot histogram.")
            return
        figure= plt.Figure(figsize= (5,5))
        ax=figure.add_subplot(111) 
        if parent_widget.layout() is not None:
            # Remove old widgets in the layout
            while parent_widget.layout().count():
                item = parent_widget.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()  # Delete the old canvas

        if key_show=='histogram':
            ax.bar(histogram, bins, label='Histogram')
        else:
            #bins and histogram here means bins and pdf values
            ax.plot(histogram, bins, color='red', linewidth=2, label="CDF")

        ax.set_xlabel("Pixel Intensity")
        ax.set_ylabel("Frequency")
        ax.set_title("Histogram & Distribution")
        if key2 =='normalize':
            ax.set_xlim(0,1)
        ax.legend()

        #embed it into canvas
        canvas= FigureCanvas(figure)
        layout = parent_widget.layout()
        if layout is None:
            layout = QVBoxLayout(parent_widget)
            parent_widget.setLayout(layout)
    
        layout.addWidget(canvas)
        canvas.draw()
        
    def equalize_histogram(self):
        histogram, _ = self.get_histogram(self.image_data)
        #compute CDF from histogram
        histogram_cdf=  histogram.cumsum()
        min_cdf=histogram_cdf.min()
        max_cdf= histogram_cdf.max()
        #map each pixel to new value from 0-255
        cdf_equalized=((histogram_cdf-min_cdf) /(max_cdf - min_cdf))*255
        cdf_equalized= cdf_equalized.astype(np.uint8)
        #each pixel value is mapped to its new value after equalization
        image_data_equalized = cdf_equalized[self.image_data.astype(np.uint8)]  #numpy vectorization facilitate the mapping, it maps pixels all at once

        self.show_plots(image_data_equalized)
        return image_data_equalized

    def normalize(self):
        min_val = self.image_data.min()
        max_val = self.image_data.max()
        
        # Avoid division by zero
        if max_val - min_val == 0:
            return np.zeros_like(self.image_data, dtype=np.float32)
    
        image_data_normalized =((self.image_data - min_val) / (max_val - min_val)).astype(np.float32)
         
        #image_data_normalized= cv2.normalize(self.image_data,None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        self.show_plots(image_data_normalized, key='normalize')
        return image_data_normalized

    def set_image(self, image_data):
        self.image_data= image_data
    

    def global_threshold(self):
        threshold_value = np.mean(self.image_data)  # Set threshold dynamically
        return np.where(self.image_data > threshold_value, 255, 0).astype(np.uint8)
    
    def local_threshold(self, block_size=11, C= 4): #adaptive thresholding, C-->Threshold Offset
        height, width = self.image_data.shape
        binary_image = np.zeros_like(self.image_data)  # Output image

        for i in range(0, height, block_size):
             for j in range(0, width, block_size):
                # Handle edge cases where block size exceeds image dimensions
                block_end_i = min(i + block_size, height)
                block_end_j = min(j + block_size, width)
                
                block = self.image_data[i:block_end_i, j:block_end_j]
                block_mean = np.mean(block)
                binary_image[i:block_end_i, j:block_end_j] = np.where(block > block_mean - C, 255, 0).astype(np.uint8)
    
        return binary_image

    
