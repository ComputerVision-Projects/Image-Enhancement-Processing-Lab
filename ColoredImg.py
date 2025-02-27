import Histogram
class ColoredImg:
    def __init__(self,colored_img,):
        self.R, self.G, self.B = colored_img[:, :, 0], colored_img[:, :, 1], colored_img[:, :, 2]
      
    def convert_to_grayscale(self):
        #I=0.2989R+0.5870G+0.1140B 
        gray_img=  self.R*0.2989 +  self.G*0.5870+  self.B*0.1140
        return gray_img
    
    def histogram_channels(self,):
        histR, binsR= Histogram.get_histogram(self.R,)
        histG, binsG= Histogram.get_histogram(self.G,)
        histB, binsB= Histogram.get_histogram(self.B,)

        return histR, binsR, histG, binsG, histB, binsB
    
    def plot_histograms(self, wid1, wid2, wid3, wid4, wid5, wid6):
        histR, binsR, histG, binsG, histB, binsB = self.histogram_channels()
        Histogram.plot_histogram(binsR,histR,wid1)
        Histogram.plot_histogram(binsG,histG,wid2)
        Histogram.plot_histogram(binsB,histB,wid3)
        cdf_R = histR.cumsum() / histR.sum()
        cdf_G = histG.cumsum() / histG.sum()
        cdf_B = histB.cumsum() / histB.sum()
        Histogram.plot_histogram(binsR,cdf_R,wid4, key_show='distribution')
        Histogram.plot_histogram(binsG,cdf_G,wid5, key_show='distribution')
        Histogram.plot_histogram(binsB,cdf_B,wid6, key_show='distribution')
    
    