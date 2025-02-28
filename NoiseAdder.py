import numpy as np
import random

class NoiseAdder:
    def __init__(self, image_data):
        self.image = image_data

    def uniform_noise(self, intensity=30):
        noise = np.random.randint(-intensity, intensity + 1, self.image.shape, dtype=np.int16)
        noisy_image = np.clip(self.image + noise, 0, 255).astype(np.uint8)
        return noisy_image

    def gaussian_noise(self, mean=100, stddev=1):
        noise = np.random.normal(mean, stddev, self.image.shape).astype(np.int16)
        noisy_image = np.clip(self.image + noise, 0, 255).astype(np.uint8)
        return noisy_image
    
    def salt_and_pepper_noise(self, salt_prob=0.05, pepper_prob=0.05):
        random_matrix = np.random.rand(*self.image.shape)
        noisy_image = self.image.copy()
        noisy_image[random_matrix < pepper_prob] = 0  # Pepper
        noisy_image[random_matrix > 1 - salt_prob] = 255  # Salt
        return noisy_image
