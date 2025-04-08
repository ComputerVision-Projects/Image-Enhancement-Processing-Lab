from HistogramOperations import HistogramOperations
import numpy as np

class ColoredImg:
    """
    This class handles operations on a colored image, such as converting it to grayscale
    and plotting histograms for the red, green, and blue channels.
    
    Attributes:
        widget1, widget2, widget3, widget4, widget5, widget6: UI elements for displaying histograms.
        HistogramR, HistogramG, HistogramB: Instances of HistogramOperations for each color channel.
        R, G, B: Arrays representing the red, green, and blue channels of the image.
    """
    
    def __init__(self, widget1, widget2, widget3, widget4, widget5, widget6, colored_img=None):
        """
        Initializes the ColoredImg object with given widgets and an optional colored image.

        Args:
            widget1, widget2, widget3, widget4, widget5, widget6: UI widgets for histogram visualization.
            colored_img (numpy.ndarray, optional): The input colored image as a NumPy array (Height x Width x 3).
        """
        self.widget1 = widget1
        self.widget2 = widget2
        self.HistogramR = HistogramOperations(widget1, widget2)
        self.HistogramG = HistogramOperations(widget3, widget4)
        self.HistogramB = HistogramOperations(widget5, widget6)
        
        # If an image is provided, extract the R, G, and B channels
        if colored_img is not None:
            self.R, self.G, self.B = colored_img[:, :, 0], colored_img[:, :, 1], colored_img[:, :, 2]
    
    def convert_to_grayscale(self):
        """
        Converts the colored image to grayscale using the luminance formula:
        I = 0.2989 * R + 0.5870 * G + 0.1140 * B

        Returns:
            numpy.ndarray: The grayscale image as a NumPy array with values in the range [0, 255].
        """
        gray_img = (self.R.astype(np.float32) * 0.2989 +
                    self.G.astype(np.float32) * 0.5870 +
                    self.B.astype(np.float32) * 0.1140)
        
        # Ensure pixel values are within the valid range [0, 255]
        gray_img = np.clip(gray_img, 0, 255).astype(np.uint8)
        return gray_img
    




    # def histogram_channels(self,):
    #     histR, binsR= self.HistogramR.get_histogram(self.R,)
    #     histG, binsG= self.HistogramG.get_histogram(self.G,)
    #     histB, binsB= self.HistogramB.get_histogram(self.B,)

    #     return histR, binsR, histG, binsG, histB, binsB
    
    def plot_histograms(self):
        """
        Plots histograms for each color channel (Red, Green, and Blue) using the HistogramOperations class.
        """
        self.HistogramR.show_plots(self.R, color='red')
        self.HistogramG.show_plots(self.G, color='green')
        self.HistogramB.show_plots(self.B, color='blue')
    
    def set_colored_img(self, colored_img):
        """
        Sets a new colored image and extracts its red, green, and blue channels.

        Args:
            colored_img (numpy.ndarray): The input colored image as a NumPy array (Height x Width x 3).
        """
        print("Setting new image")
        self.B, self.G, self.R = colored_img[:, :, 0], colored_img[:, :, 1], colored_img[:, :, 2]