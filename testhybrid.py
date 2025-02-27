import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from HybridImage import HybridImage

def load_image(image_path):
    """ Load image as grayscale """
    return np.array(Image.open(image_path).convert("L"))

# Load images
image1 = load_image("C:/mixer_beamforming/ImageMixer-BeamForming/Images/360_F_744363737_fQratit3182GzjiN1LbP7HuK9Z2vMc1C.jpg")
image2 = load_image("C:/mixer_beamforming/ImageMixer-BeamForming/Images/Michael-Moore2.jpg")

# Create hybrid images using different methods
hybrid_generator = HybridImage()

hybrid_low_high = hybrid_generator.create_hybrid_image(image1, image2, method="low-high", low_cutoff=20, high_cutoff=20)
hybrid_mag_phase = hybrid_generator.create_hybrid_image(image1, image2, method="magnitude-phase")
hybrid_real_imag = hybrid_generator.create_hybrid_image(image1, image2, method="real-imaginary")

# Display results
plt.figure(figsize=(12, 6))
plt.subplot(2, 3, 1), plt.imshow(image1, cmap='gray'), plt.title("Original Image 1")
plt.subplot(2, 3, 2), plt.imshow(image2, cmap='gray'), plt.title("Original Image 2")
plt.subplot(2, 3, 3), plt.imshow(hybrid_low_high, cmap='gray'), plt.title("Hybrid (Low-High)")

plt.subplot(2, 3, 4), plt.imshow(hybrid_mag_phase, cmap='gray'), plt.title("Hybrid (Magnitude-Phase)")
plt.subplot(2, 3, 5), plt.imshow(hybrid_real_imag, cmap='gray'), plt.title("Hybrid (Real-Imaginary)")

plt.show()
