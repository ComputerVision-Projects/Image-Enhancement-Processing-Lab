import numpy as np

class FrequencyFilter:
    """
    A class to apply frequency domain filtering (low-pass and high-pass) to an image.
    """

    def __init__(self, image):
        """
        Initialize the FrequencyFilter with a given grayscale image.

        Parameters:
        image (numpy.ndarray): 2D array representing the grayscale image.
        """
        self.image = image
        self.shape = image.shape

    def create_filter(self, filter_type='low pass', cutoff=30):
        """
        Create a frequency domain filter (low-pass or high-pass).

        Parameters:
        filter_type (str): 'low' for low-pass, 'high' for high-pass.
        cutoff (int): Cutoff frequency radius.

        Returns:
        numpy.ndarray: 2D filter mask.
        """
        rows, cols = self.shape
        crow, ccol = rows // 2, cols // 2  # Center of the frequency domain
        mask = np.zeros((rows, cols))

        for i in range(rows):
            for j in range(cols):
                distance = np.sqrt((i - crow) ** 2 + (j - ccol) ** 2)
                if filter_type == 'low pass' and distance <= cutoff:
                    mask[i, j] = 1
                elif filter_type == 'high pass' and distance > cutoff:
                    mask[i, j] = 1

        return mask

    def apply_filter(self, filter_type='low pass', cutoff=30):
        """
        Apply a low-pass or high-pass filter in the frequency domain.

        Parameters:
        filter_type (str): 'low' or 'high' to specify filter type.
        cutoff (int): Cutoff frequency radius.

        Returns:
        tuple: (filtered_image, filter_mask)
        """
        # Compute 2D Fourier Transform and shift zero frequency(low frequencies) to center
        dft = np.fft.fft2(self.image)
        dft_shift = np.fft.fftshift(dft)

        mask = self.create_filter(filter_type, cutoff)
        filtered_dft = dft_shift * mask

        # Inverse Fourier Transform to get the filtered image
        dft_inverse_shift = np.fft.ifftshift(filtered_dft)
        img_filtered = np.fft.ifft2(dft_inverse_shift)
        img_filtered = np.abs(img_filtered) 
        min_val = np.min(img_filtered)
        max_val = np.max(img_filtered)

        if max_val > min_val:
         img_filtered = (img_filtered - min_val) / (max_val - min_val)
        else:
         img_filtered = np.zeros_like(img_filtered) 

        img_filtered = (img_filtered * 255).astype(np.uint8)

        mask_display = (mask * 255).astype(np.uint8)
        return img_filtered, mask_display
