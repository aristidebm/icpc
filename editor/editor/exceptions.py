class ImageOverflowError(Exception):
    """
    Throws when the the provided image size is greater than the limit (256x256).
    """
    def __init__(self, message=None):
        self.message = message or f"The max image size is {self.max_size}x{self.max_size}"
        super().__init__(message)

class InvalidAxisFormatError(Exception):
    """
    Throws when an invalid axis format is provided, axis format is
    a 2-tuple.
    """
    def __init__(self, message=f"Invalid format."):
        super().__init__(message)
