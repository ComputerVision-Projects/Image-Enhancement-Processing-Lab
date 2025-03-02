import numpy as np
import cv2

class HybridImage:
    def __init__(self, img1=None, img2=None):
        self.img1 = img1  # Low-pass filtered image
        self.img2 = img2  # High-pass filtered image

    def create_hybrid(self, blend_type="low-high", low_cutoff=None, high_cutoff=None):
        """Combine the two filtered images into a hybrid image."""
        if self.img1 is None or self.img2 is None:
            print("Error: Both images must be provided for hybrid image creation.")
            return None
        
        # Ensure both images are the same size
        min_shape = (min(self.img1.shape[0], self.img2.shape[0]), 
                     min(self.img1.shape[1], self.img2.shape[1]))
        img1_resized = cv2.resize(self.img1, min_shape[::-1])
        img2_resized = cv2.resize(self.img2, min_shape[::-1])

        hybrid_image = np.clip(img1_resized + img2_resized, 0, 255).astype(np.uint8)
        return hybrid_image
