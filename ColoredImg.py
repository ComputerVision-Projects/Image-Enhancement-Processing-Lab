from HistogramOperations import HistogramOperations
import numpy as np
class ColoredImg:
    def __init__(self,widget1, widget2, colored_img=None,):
        self.widget1= widget1
        self.widget2=widget2
        self.HistogramOperations= HistogramOperations(widget1, widget2,)
        if colored_img:
            self.R, self.G, self.B = colored_img[:, :, 0], colored_img[:, :, 1], colored_img[:, :, 2]
      
    def convert_to_grayscale(self):
        #I=0.2989R+0.5870G+0.1140B 
        gray_img = (self.R.astype(np.float32) * 0.2989 +
            self.G.astype(np.float32) * 0.5870 +
            self.B.astype(np.float32) * 0.1140)
        gray_img = np.clip(gray_img, 0, 255).astype(np.uint8)
        return gray_img
    
    def histogram_channels(self,):
        histR, binsR= self.HistogramOperations.get_histogram(self.R,)
        histG, binsG= self.HistogramOperations.get_histogram(self.G,)
        histB, binsB= self.HistogramOperations.get_histogram(self.B,)

        return histR, binsR, histG, binsG, histB, binsB
    
    def plot_histograms(self,):
        histR, binsR, histG, binsG, histB, binsB = self.histogram_channels()
        self.HistogramOperations.plot_histogram(binsR,histR,self.widget1)
        self.HistogramOperations.plot_histogram(binsG,histG,self.widget1)
        self.HistogramOperations.plot_histogram(binsB,histB,self.widget1)
        cdf_R = histR.cumsum() / histR.sum()
        cdf_G = histG.cumsum() / histG.sum()
        cdf_B = histB.cumsum() / histB.sum()
        self.HistogramOperations.plot_histogram(binsR,cdf_R,self.widget2, key_show='distribution')
        self.HistogramOperations.plot_histogram(binsG,cdf_G,self.widget2, key_show='distribution')
        self.HistogramOperations.plot_histogram(binsB,cdf_B,self.widget2, key_show='distribution')
    
    def set_colored_img(self, colored_img):
        print("set image")
        self.B, self.G, self.R = colored_img[:, :, 0], colored_img[:, :, 1], colored_img[:, :, 2]

