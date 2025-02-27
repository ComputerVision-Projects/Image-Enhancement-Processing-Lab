import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from FrequencyFilter import FrequencyFilter  # Import the class

def load_image(image_path):
    """
    Load an image and convert it to grayscale.

    Parameters:
    image_path (str): Path to the image file.

    Returns:
    numpy.ndarray: 2D grayscale image.
    """
    img = plt.imread(image_path)
    if img.ndim == 3:  # Convert RGB to grayscale manually
        img = 0.2989 * img[:, :, 0] + 0.5870 * img[:, :, 1] + 0.1140 * img[:, :, 2]
    return img

# Load Image
image_path = "C:/mixer_beamforming/ImageMixer-BeamForming/Images/360_F_744363737_fQratit3182GzjiN1LbP7HuK9Z2vMc1C.jpg"
img = load_image(image_path)

# Initialize the FrequencyFilter class
filter_instance = FrequencyFilter(img)

# Default cutoff values
low_radius = 30
high_radius = 30

# Apply initial filters
low_filtered, low_mask = filter_instance.apply_filter('low', low_radius)
high_filtered, high_mask = filter_instance.apply_filter('high', high_radius)

# Create figure and axes
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
plt.subplots_adjust(left=0.1, bottom=0.25)

# Display images
axes[0, 0].imshow(img, cmap='gray')
axes[0, 0].set_title("Original Image")

ax_low_mask = axes[0, 1].imshow(low_mask, cmap='gray')
axes[0, 1].set_title("Low-pass Mask")

ax_low_filtered = axes[0, 2].imshow(low_filtered, cmap='gray')
axes[0, 2].set_title("Low-pass Filtered")

ax_high_mask = axes[1, 1].imshow(high_mask, cmap='gray')
axes[1, 1].set_title("High-pass Mask")

ax_high_filtered = axes[1, 2].imshow(high_filtered, cmap='gray')
axes[1, 2].set_title("High-pass Filtered")

# Create sliders
ax_slider_low = plt.axes([0.1, 0.1, 0.65, 0.03])
slider_low = Slider(ax_slider_low, "Low-pass Radius", 1, 100, valinit=low_radius)

ax_slider_high = plt.axes([0.1, 0.05, 0.65, 0.03])
slider_high = Slider(ax_slider_high, "High-pass Radius", 1, 100, valinit=high_radius)

def update(val):
    """
    Update function for sliders to dynamically change the filter radius.
    """
    global low_radius, high_radius

    low_radius = slider_low.val
    high_radius = slider_high.val

    # Update Low-pass filter
    low_filtered, low_mask = filter_instance.apply_filter('low', low_radius)
    ax_low_mask.set_data(low_mask)
    ax_low_filtered.set_data(low_filtered)

    # Update High-pass filter
    high_filtered, high_mask = filter_instance.apply_filter('high', high_radius)
    ax_high_mask.set_data(high_mask)
    ax_high_filtered.set_data(high_filtered)

    fig.canvas.draw_idle()

# Connect sliders to update function
slider_low.on_changed(update)
slider_high.on_changed(update)

plt.show()
