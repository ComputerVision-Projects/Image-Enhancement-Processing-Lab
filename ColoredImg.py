from HistogramOperations import HistogramOperations
import numpy as np
class ColoredImg:
    def __init__(self,widget1, widget2,widget3, widget4,widget5, widget6, colored_img=None,):
        self.widget1= widget1
        self.widget2=widget2
        self.HistogramR= HistogramOperations(widget1, widget2,)
        self.HistogramG= HistogramOperations(widget3, widget4,)
        self.HistogramB= HistogramOperations(widget5, widget6,)
        if colored_img:
            self.R, self.G, self.B = colored_img[:, :, 0], colored_img[:, :, 1], colored_img[:, :, 2]
      
    def convert_to_grayscale(self):
        #I=0.2989R+0.5870G+0.1140B 
        
        gray_img = (self.R.astype(np.float32) * 0.2989 +
                    self.G.astype(np.float32) * 0.5870 +
                    self.B.astype(np.float32) * 0.1140)

        gray_img = np.clip(gray_img, 0, 255).astype(np.uint8)

        return gray_img
    
    # def histogram_channels(self,):
    #     histR, binsR= self.HistogramR.get_histogram(self.R,)
    #     histG, binsG= self.HistogramG.get_histogram(self.G,)
    #     histB, binsB= self.HistogramB.get_histogram(self.B,)

    #     return histR, binsR, histG, binsG, histB, binsB
    
    def plot_histograms(self,):
        self.HistogramR.show_plots(self.R)
        self.HistogramG.show_plots(self.G)
        self.HistogramB.show_plots(self.B)
    
    def set_colored_img(self, colored_img):
        print("set image")
        self.B, self.G, self.R = colored_img[:, :, 0], colored_img[:, :, 1], colored_img[:, :, 2]

