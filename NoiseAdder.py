import numpy as np
import random

class NoiseAdder:
    def __init__(self, image_data):
        """
        Initialize the NoiseAdder class with an image.
        
        :param image_data: NumPy array representing the image.
        """
        self.image = image_data

    def uniform_noise(self, intensity=30):
        """
        Add uniform noise to the image.

        :param intensity: Maximum deviation from the original pixel value.
        :return: Noisy image with values clipped between 0 and 255.
        """

        # Generate noise values randomly between -intensity and +intensity        
        noise = np.random.randint(-intensity, intensity + 1, self.image.shape, dtype=np.int16)
        # Add noise to the image and clip values to ensure they stay in the 0-255 range
        noisy_image = np.clip(self.image + noise, 0, 255).astype(np.uint8)
        return noisy_image

    def gaussian_noise(self, mean=100, stddev=1):
        """
        Add Gaussian noise to the image.

        :param mean: Mean of the Gaussian distribution.
        :param stddev: Standard deviation of the Gaussian distribution.
        :return: Noisy image with values clipped between 0 and 255.
        """   
        # Generate Gaussian-distributed noise with the given mean and standard deviation     
        noise = np.random.normal(mean, stddev, self.image.shape).astype(np.int16)
        noisy_image = np.clip(self.image + noise, 0, 255).astype(np.uint8)
        return noisy_image
    
    def salt_and_pepper_noise(self, salt_prob=0.05, pepper_prob=0.05):
        """
        Add salt-and-pepper noise to the image.

        :param salt_prob: Probability of setting a pixel to white (salt).
        :param pepper_prob: Probability of setting a pixel to black (pepper).
        :return: Noisy image with randomly placed salt and pepper noise.
        """
        # Create a random matrix with values between 0 and 1
        random_matrix = np.random.rand(*self.image.shape)
        noisy_image = self.image.copy()
        noisy_image[random_matrix < pepper_prob] = 0  # Pepper
        noisy_image[random_matrix > 1 - salt_prob] = 255  # Salt
        return noisy_image
