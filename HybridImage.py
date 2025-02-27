import numpy as np
from PIL import Image
from FrequencyFilter import FrequencyFilter
class HybridImage:
   

    @staticmethod
    def fft_transform(image):
        """Compute FFT, shift it to center, and return magnitude, phase, real, and imaginary components."""
        dft = np.fft.fft2(image)
        dft_shift = np.fft.fftshift(dft)
        magnitude = np.abs(dft_shift)
        phase = np.angle(dft_shift)
        real = dft_shift.real
        imaginary = dft_shift.imag
        return magnitude, phase, real, imaginary

    @staticmethod
    def ifft_transform(magnitude, phase):
        """Reconstruct image from magnitude and phase."""
        complex_spectrum = magnitude * np.exp(1j * phase)
        inverse_shift = np.fft.ifftshift(complex_spectrum)
        return np.abs(np.fft.ifft2(inverse_shift))

    @staticmethod
    def ifft_from_real_imag(real, imaginary):
        """Reconstruct image from real and imaginary parts."""
        complex_spectrum = real + 1j * imaginary
        inverse_shift = np.fft.ifftshift(complex_spectrum)
        return np.abs(np.fft.ifft2(inverse_shift))

    def create_hybrid_image(self, image1, image2, method="low-high", low_cutoff=20, high_cutoff=20):
        """
        Create hybrid image using different frequency domain techniques.

        Parameters:
        image1 (numpy.ndarray): First grayscale image.
        image2 (numpy.ndarray): Second grayscale image.
        method (str): Hybridization method ('low-high', 'magnitude-phase', or 'real-imaginary').
        low_cutoff (int): Cutoff frequency for low-pass filtering.
        high_cutoff (int): Cutoff frequency for high-pass filtering.

        Returns:
        numpy.ndarray: The resulting hybrid image.
        """
        # Ensure both images have the same size
        image2 = np.array(Image.fromarray(image2).resize(image1.shape[::-1], Image.LANCZOS))

        if method == "low-high":
            low_frequencies, _ = FrequencyFilter(image1).apply_filter('low', low_cutoff)
            high_frequencies, _ = FrequencyFilter(image2).apply_filter('high', high_cutoff)
            hybrid = low_frequencies + high_frequencies

        elif method == "magnitude-phase":
            mag1, phase1, _, _ = self.fft_transform(image1)
            _, phase2, _, _ = self.fft_transform(image2)
            hybrid = self.ifft_transform(mag1, phase2)

        elif method == "real-imaginary":
            _, _, real1, _ = self.fft_transform(image1)
            _, _, _, imag2 = self.fft_transform(image2)
            hybrid = self.ifft_from_real_imag(real1, imag2)

        else:
            raise ValueError("Invalid method. Choose 'low-high', 'magnitude-phase', or 'real-imaginary'.")
        
        return hybrid
