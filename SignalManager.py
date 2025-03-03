from PyQt5.QtCore import QObject, pyqtSignal

class SignalManager(QObject):
    """Global signal manager to handle UI updates across multiple classes."""
    
    new_image_loaded = pyqtSignal(int)  # Signal to reset UI when a new image is loaded
    
    def __init__(self):
        super().__init__()

# Create a global instance of SignalManager
signal_manager = SignalManager()
