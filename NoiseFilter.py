import numpy as np
import math

class NoiseFilter:
    def __init__(self, noisy_image):
        self.image = noisy_image 

    def average_filter(self, kernel_size=3):
        height, width = self.image.shape
        pad = kernel_size // 2
        padded_image = np.pad(self.image, pad, mode='edge')
        filtered_image = np.zeros((height, width), dtype=np.uint8)
        
        for i in range(height):
            for j in range(width):
                region = padded_image[i:i + kernel_size, j:j + kernel_size]
                avg_value = np.mean(region)
                filtered_image[i, j] = int(avg_value)
        
        return filtered_image
    
    def gaussian_filter(self, kernel_size=3, sigma=1.0):
        height, width = self.image.shape
        pad = kernel_size // 2
        x, y = np.mgrid[-pad:pad+1, -pad:pad+1]
        gaussian_kernel = np.exp(-(x**2 + y**2) / (2 * sigma**2)) / (2 * np.pi * sigma**2)
        gaussian_kernel /= gaussian_kernel.sum()
        
        padded_image = np.pad(self.image, pad, mode='edge')
        filtered_image = np.zeros((height, width), dtype=np.uint8)
        
        for i in range(height):
            for j in range(width):
                region = padded_image[i:i + kernel_size, j:j + kernel_size]
                gaussian_sum = np.sum(region * gaussian_kernel)
                filtered_image[i, j] = int(gaussian_sum)
        
        return filtered_image
             
    def median_filter(self, kernel_size=3):
        height, width = self.image.shape
        pad = kernel_size // 2
        padded_image = np.pad(self.image, pad, mode='edge')
        filtered_image = np.zeros((height, width), dtype=np.uint8)
        
        for i in range(height):
            for j in range(width):
                region = padded_image[i:i + kernel_size, j:j + kernel_size].flatten()
                median_value = np.median(region)
                filtered_image[i, j] = int(median_value)
        
        return filtered_image
