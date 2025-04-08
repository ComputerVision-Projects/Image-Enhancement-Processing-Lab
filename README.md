# Image Enhancement and Processing Lab

This project is a modular GUI application for image processing, supporting both spatial and frequency domain operations. It allows users to upload and manipulate images through a user-friendly interface divided into three main tabs.

---

## Main Features

### 1. Spatial Domain Filters
- **Add Noise**: Uniform, Gaussian, Salt & Pepper (with adjustable intensity).
- **Apply Filters**: Average, Gaussian, Median (custom kernel size).
- **Edge Detection**: Prewitt, Robert, Sobel.
- **Thresholding**: Global and Local methods.
- **Histogram Operations**: Equalization and normalization.

### 2. Transformation to Grayscale
- Convert RGB images to grayscale.
- Display histograms and distribution curves for each RGB channel.

### 3. Frequency Domain Filters
- Combine two images to create a hybrid image using frequency-based filtering.
- Apply low-pass or high-pass filters with adjustable cutoff radius.

---

## Backend Architecture

The application is built with **9 modular classes** for clarity, reusability, and scalability:

- **NoiseAdder**: Adds different types of noise to test filtering techniques.
- **NoiseFilter**: Applies noise removal filters (Average, Gaussian, Median).
- **HistogramOperations**: Handles histogram equalization, normalization, and thresholding.
- **ImageViewer**: Manages image loading, displaying, RGB/grayscale conversion, and user interaction.
- **ColoredImg**: Extends histogram functionality to RGB images by processing each channel separately.
- **EdgeDetector**: Implements edge detection algorithms.
- **FrequencyFilter**: Applies frequency domain filters (high-pass and low-pass).

> All image processing functionalities are implemented **from scratch** to ensure full control and learning value.

---

## User Interaction

- **Upload an Image**: Double-click on the input image area in the GUI.
- **Visual Feedback**: Each step's output is displayed directly in the interface.
- **Dynamic Updates**: Histograms and curves update according to the selected operations.

