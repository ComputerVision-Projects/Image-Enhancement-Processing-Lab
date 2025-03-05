import numpy as np
import math

class NoiseFilter:
    def __init__(self, noisy_image):
        """
        Initialize the NoiseFilter class with a noisy image.

        :param noisy_image: NumPy array representing the grayscale image with noise.
        """
        self.image = noisy_image 

    def average_filter(self, kernel_size=3):
        """
        Apply an Average Filter to smooth the image by replacing each pixel 
        with the average of its surrounding pixels.

        :param kernel_size: Size of the square filter kernel (must be an odd number).
        :return: Filtered image as a NumPy array.
        """        
        height, width = self.image.shape
        pad = kernel_size // 2
        # Pad the image to handle edge cases by extending edge values
        padded_image = np.pad(self.image, pad, mode='edge')
        # Initialize an empty image for the filtered output
        filtered_image = np.zeros((height, width), dtype=np.uint8)
        
        # Iterate over each pixel in the original image
        for i in range(height):
            for j in range(width):
                # Extract the local region from the padded image
                region = padded_image[i:i + kernel_size, j:j + kernel_size]
                avg_value = np.mean(region)
                # Assign the averaged value to the corresponding pixel in the output
                filtered_image[i, j] = int(avg_value)
        
        return filtered_image
    
    def gaussian_filter(self, kernel_size=3, sigma=1.0):
        """
        Apply a Gaussian Filter to smooth the image while preserving edges 
        by using a weighted average with a Gaussian distribution.

        :param kernel_size: Size of the square filter kernel (must be an odd number).
        :param sigma: Standard deviation of the Gaussian distribution.
        :return: Filtered image as a NumPy array.
        """        
        height, width = self.image.shape
        pad = kernel_size // 2
        # Create a Gaussian kernel using the 2D Gaussian function
        x, y = np.mgrid[-pad:pad+1, -pad:pad+1]
        gaussian_kernel = np.exp(-(x**2 + y**2) / (2 * sigma**2)) / (2 * np.pi * sigma**2)
        gaussian_kernel /= gaussian_kernel.sum() # Normalize the kernel
        
        padded_image = np.pad(self.image, pad, mode='edge')
        filtered_image = np.zeros((height, width), dtype=np.uint8)
        
        for i in range(height):
            for j in range(width):
                region = padded_image[i:i + kernel_size, j:j + kernel_size]
                # Apply the Gaussian kernel by performing element-wise multiplication and summing
                gaussian_sum = np.sum(region * gaussian_kernel)
                filtered_image[i, j] = int(gaussian_sum)
        
        return filtered_image
             
    def median_filter(self, kernel_size=3):
        """
        Apply a Median Filter to reduce noise while preserving edges 
        by replacing each pixel with the median of its surrounding pixels.

        :param kernel_size: Size of the square filter kernel (must be an odd number).
        :return: Filtered image as a NumPy array.
        """        
        height, width = self.image.shape
        pad = kernel_size // 2
        padded_image = np.pad(self.image, pad, mode='edge')
        filtered_image = np.zeros((height, width), dtype=np.uint8)
        
        for i in range(height):
            for j in range(width):
                # Extract the local region from the padded image and flatten it into a 1D array to get the median
                region = padded_image[i:i + kernel_size, j:j + kernel_size].flatten()
                # Compute the median value of the region
                median_value = np.median(region)
                filtered_image[i, j] = int(median_value)
        
        return filtered_image
