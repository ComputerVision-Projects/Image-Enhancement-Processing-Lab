# Image Enhancement and Processing Lab

This project is a modular GUI application for image processing, supporting both spatial and frequency domain operations. It allows users to upload and manipulate images through a user-friendly interface divided into three main tabs.

---

## Main Tabs

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
---

## Project Architecture

The system is modularized into **9 main classes**, each handling a specific processing component to promote reusability and clarity:

| Class | Description |
|-------|--------------|
| **NoiseAdder** | Adds Uniform, Gaussian, or Salt & Pepper noise to test filter robustness. |
| **NoiseFilter** | Applies Average, Gaussian, and Median filters for noise reduction. |
| **HistogramOperations** | Computes, visualizes, equalizes, and normalizes image histograms. |
| **ImageViewer** | Handles image loading, displaying, and double-click interactions within the GUI. |
| **ColoredImg** | Manages RGB histograms and converts color images to grayscale. |
| **EdgeDetectors** | Implements Sobel, Roberts, Prewitt, and Canny edge detection methods. |
| **FrequencyFilter** | Performs Fourier-based filtering (low-pass/high-pass) with adjustable cutoffs. |
| **HybridImage** | Blends two images using frequency-based hybrid image generation. |
| **SignalManager** | Manages global PyQt signals to synchronize events between UI components. |

---

## Key Features

- **Noise Manipulation:** Add and remove noise interactively.
- **Histogram Tools:** Equalization, normalization, and thresholding.
- **Edge Detection:** Compare multiple algorithms visually.
- **Frequency Analysis:** Visualize frequency filters and results.
- **Hybrid Image Creation:** Combine low and high-frequency details from two images.

---

## Technologies Used
- **Language:** Python  
- **Framework:** PyQt5  
- **Libraries:** NumPy, OpenCV, Matplotlib (for visualization)  

---

## Getting Started

### Prerequisites
Make sure you have Python 3.8+ installed.  
Install dependencies using:

```bash
pip install numpy opencv-python PyQt5 matplotlib
```

- Upload an Image: Double-click on the input image area in the GUI.
- Visual Feedback: Each step's output is displayed directly in the interface.
- Dynamic Updates: Histograms and curves update according to the selected operations.

