"""
uva online graph editor problem.
"""
import sys
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
            self.image[pixel[0] - 1][pixel[1] - 1] = color

    def draw_segment(self, orientation, fixed_row, begin, end, color):
        """
        Function to draw a segment (a segment is a line of pixel)
        """
        if begin > end:
            begin, end = end, begin

        is_segment_valid, _ = self.is_valid_segment(orientation, fixed_row, begin, end)

        if is_segment_valid:
            self._draw_segment(orientation, fixed_row, begin, end, color)

    def draw_rectangle(self, upper_corner, bottom_corner, color):
        """
        Function to draw rectangle on drawing board.
        """
        if not self.is_valid_diagonal(upper_corner, bottom_corner):
            return
        # A rectangle is fully determine by his upper left corner and his bottom
        # right one, with constitute his diagonal.
        # given (x1, y1) and (x2, y2), the rectangle is in (x2 - x1) lines and (y2 - y1) lines
        for item in self.image[upper_corner[0] - 1: bottom_corner[0]]:
            item[upper_corner[1] - 1 : bottom_corner[1]] = [color]*(bottom_corner[1] - upper_corner[1] + 1)


    def draw_pixel_region(self, pixel, color, visited=None):
        """
        A region is defined like above :
        1. Pixel(pix) belongs to the region
        2. Each pixel that are neigbour of to the region pixel and shares the same color
        also belongs to the region.
        Approach : The problem can be seen as  a tree traversal problem
        where (pix) is the root and other pixel are his childrens.
        DFS is the approach used for graph traversal
        """
        if visited is None:
            visited = set()
        visited.add(pixel)
        children = self._construct_adjency_list(pixel)
        self.image[pixel[0] - 1][pixel[1] - 1] = color

        for pix in children - visited:
            self.draw_pixel_region(pix, color, visited)

    def show_image(self, filename):
        print(f"\n{filename}")
        print("-"*(2*len(self.image[0]) + 1))
        for line in self.image:
            print("|", end="")
            for item in line:
                print(f"{item}|", end="")
            print()
            print("-"*(2*len(self.image[0]) + 1))

    def quit_editor(self):
        self.image = None
        sys.exit()

    def _create_image(self, size):
        self.is_valid_size(size, with_trace=True)
        return [[0] * size[1] for _ in range(size[0])]

    def _draw_segment(self, orientation, fixed_row, begin, end, color):
        """
        Internal function to draw a segment.
        """
        if orientation == self.valid_orientations[0]:
            self.image[fixed_row - 1][begin - 1 : end] = [color] * (end - begin + 1)
            return

        for item in self.image[begin - 1 : end]:
            item[fixed_row - 1] = color

    def _construct_adjency_list(self, pixel):
        children = set()
        self.is_valid_pixel(pixel, with_trace=True)
        # import pdb; pdb.set_trace()

        # top pixel
        top = (pixel[0] - 1, pixel[1])
        if self.is_valid_pixel(top):
            if self.image[top[0] - 1][top[1] - 1] == self.image[pixel[0] - 1][pixel[1] - 1]:
                children.add(top)

        # bottom pixel
        bottom = (pixel[0] + 1, pixel[1])
        if self.is_valid_pixel(bottom):
            if self.image[bottom[0] - 1][bottom[1] - 1] == self.image[pixel[0] - 1][pixel[1] - 1]:
                children.add(bottom)

        # right pixel
        right = (pixel[0], pixel[1] + 1)
        if self.is_valid_pixel(right):
            if self.image[right[0] - 1][right[1] - 1] == self.image[pixel[0] - 1][pixel[1] - 1]:
                children.add(right)

        # left pixel
        left = (pixel[0], pixel[1] - 1)
        if self.is_valid_pixel(left):
            if self.image[left[0] - 1][left[1] - 1] == self.image[pixel[0] - 1][pixel[1] - 1]:
                children.add(left)

        return children



    def is_valid_diagonal(self, upper_right, bottom_left):
        """
        A diagonal is valid if each given pixel belongs on the drawing
        board and if the above  boolean function is true
        f: upper_right_x < bottom_left_x and upper_right_y < bottom_left_y
        """
        if not (is_valid_pixel(upper_right) and is_valid_pixel(bottom_left)):
            return False

        if not (upper_right[0] < bottom_left[0] and upper_right[1] < bottom_left[1]):
            return False

        return True


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
            # import pdb; pdb.set_trace()
            # negative indices are allowed in python, but we don't
            # want that functionality here.
            x = pixel[0] - 1
            y = pixel[1] - 1
            if not (x >= 0 and y >= 0):
                raise InvalidAxisFormatError
            # try to get the pixel
            self.image[x][y]
        except (IndexError, TypeError, InvalidAxisFormatError) as exp:
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
                raise InvalidAxisFormatError
            if sum(size) > 2*self.max_size:
                # import pdb; pdb.set_trace()
                is_valid_size = False
                raise ImageOverflowError
        except (InvalidAxisFormatError, ImageOverflowError) as e:
            if with_trace:
                raise e

        return is_valid_size
