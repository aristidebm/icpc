"""
uva online graph editor problem.
"""

from editor.exceptions import ImageOverflowError, InvalidAxisFormatError


class Editor(object):

    valid_orientations = ["Horizontal", "Vertical"]

    def __init__(self, image=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = image
        # the max size image that can be edit with this editor
        self.max_size = 250

    def create_drawing_board(self, size):
        """
        create a new image and set it as editor image.
        """
        image = self._create_image(size)
        self.image = image
        return image

    def clear_drawing_board(self):
        """
        clear the image by setting it to zero.
        """
        for item in self.image:
            for index, _ in enumerate(item):
                item[index] = 0


    def draw_pixel(self, pixel, color):
        if self.is_valid_pixel(pixel):
            self.image[pixel[1]][pixel[0]] = color

    def draw_segment(self, orientation, fixed_row, begin, end, color):
        """
        Function to draw a segment (a segment is a line of pixel)
        """
        is_segment_valid, _ = self.is_valid_segment(orientation, fixed_row, begin, end)

        if is_segment_valid:
            self._draw_segment(orientation, fixed_row, begin, end, color)

    def draw_rectangle(self, upper_corner, bottom_corner, color):
        pass

    def draw_pixel_region(self, pixel, color):
        pass

    def quit_editor(self):
        pass

    def _create_image(self, size):
        if self.is_valid_size(size):
            return [[0] * size[1] for _ in range(size[0])]

    def _draw_segment(self, orientation, fixed_row, begin, end, color):
        """
        Internal function to draw a segment.
        """
        # import pdb;pdb.set_trace()
        if orientation == self.valid_orientations[0]:
            self.image[fixed_row - 1][begin - 1 : end] = [color] * (end - begin + 1)
            return

        for item in self.image[begin - 1 : end]:
            item[fixed_row - 1] = color


    def is_valid_segment(self, orientation, fixed_row, begin, end):
        """
        Check whether we can draw the specified segement.
        """
        is_valid = True
        error = {}

        if orientation not in self.valid_orientations:
            error["orientation"] = "Invalid orientation"
            is_valid = False
            return is_valid, error

        if orientation == self.valid_orientations[0]:
            if not 0 <= begin <= end <= len(self.image[0]):
                error["begin-end"] = "Invalid begin or end."
                is_valid = False
                return is_valid, error

            if  fixed_row > len(self.image):
                error["fixed_row"] = "Invalid fixed row."
                is_valid = False
                return is_valid, error
        else:
            if not 0 <= begin <= end <= len(self.image):
                error["begin-end"] = "Invalid begin or end."
                is_valid = False
                return is_valid, error

            if fixed_row > len(self.image[0]):
                error["fixed_row"] = "Invalid fixed row."
                is_valid = False
                return is_valid, error

        return is_valid, error

    def is_valid_pixel(self, pixel=(), with_trace=False):
        """
        calls to check if the provided pixel is valid.
        """
        is_valid_pixel = True

        try:
            if not isinstance(pixel, tuple) or len(pixel) != 2 :
                raise InvalidAxisFormatError
            # try to get the pixel
            self.image[pixel[0] - 1][pixel[1] - 1]
        except (IndexError, TypeError, InvalidPixelError) as exp:
            is_valid_pixel = False
            if with_trace:
                raise exp

        return is_valid_pixel
#
    def is_valid_size(self, size, with_trace=False):
        """
        calls to check if the provided size is valid.
        The maximum image size that is considered is 256x256.
        """
        is_valid_size = True

        try:
            if not isinstance(size, tuple) or len(size) !=2:
                is_valid_size = False
                raise InvalidImageSizeError
            if sum(size) > 2*self.max_size:
                is_valid_size = False
                raise ImageOverflowError
        except (InvalidImageSizeError, ImageOverflowError) as e:
            if with_trace:
                raise e

        return is_valid_size

def main():
    """
    The application entry point
    """
    pass

if __name__ == "__main__":
    main()
