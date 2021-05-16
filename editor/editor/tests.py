import unittest
from editor.editor import Editor
from editor.exceptions import InvalidAxisFormatError, ImageOverflowError

class EditorTestCase(unittest.TestCase):
    """
    Editor class test suite.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.editor = None

    def setUp(self):
        self.editor = Editor()

    def tearDown(self):
        self.editor = None

    @property
    def empty_image(self):
        flatten = sum(self.editor.image, [])
        return True if sum(flatten) == 0 else False

    def test_create_drawing_board_success(self):
        """
        Make sure we can create an image.
        """
        self.assertIsNone(self.editor.image)
        image = self.editor.create_drawing_board(size=(10, 20))
        self.assertIsNotNone(self.editor.image)
        self.assertEqual(image, self.editor.image)
        # Make sure we have a matrix with the given dimensions
        self.assertEqual(len(self.editor.image), 10)
        self.assertEqual(len(self.editor.image[0]), 20)

    def test_clear_drawing_board_success(self):
        """
        Make sure we clear all image (set all pixel to 0)
        """
        image = self.editor.create_drawing_board(size=(10, 20))
        image[0][0] = 3
        self.assertEqual(self.editor.image[0][0], 3)
        self.editor.clear_drawing_board()
        self.assertEqual(self.editor.image[0][0], 0)
        # Make sure the image only contains zeros.
        self.assertTrue(self.empty_image)

    def test_draw_pixel_success(self):
        """
        Make sure we can draw pixel.
        """
        image = self.editor.create_drawing_board(size=(10, 20))
        # Make sure the image only contains zeros.
        self.assertTrue(self.empty_image)
        self.editor.draw_pixel(pixel=(5, 5), color=3)
        self.assertFalse(self.empty_image)
        self.assertEqual(self.editor.image[4][4], 3)

    def test_horizontal_segment_draw_success(self):
        """
        Make sure we can draw a segment.
        """
        color = 3
        image = self.editor.create_drawing_board(size=(10, 20))
        self.assertTrue(self.empty_image)
        self.editor.draw_segment(orientation=self.editor.valid_orientations[0],
        fixed_row=1, begin=1, end=10, color=color)
        # import pdb;pdb.set_trace()
        self.assertEqual(sum(self.editor.image[0][:10]), 10*color)
        self.assertFalse(self.empty_image)

        # make sure we can give sure we can swap begin and end if begin > end
        self.editor.clear_drawing_board()
        self.editor.draw_segment(orientation=self.editor.valid_orientations[0],
        fixed_row=1, begin=10, end=1, color=color)
        self.assertEqual(sum(self.editor.image[0][:10]), 10*color)
        self.assertFalse(self.empty_image)

    def test_vertical_segment_draw_success(self):
        """
        Make sure we can draw a segment.
        """
        color = 3
        image = self.editor.create_drawing_board(size=(10, 20))
        self.assertTrue(self.empty_image)
        self.editor.draw_segment(orientation=self.editor.valid_orientations[1],
        fixed_row=1, begin=1, end=10, color=color)
        self.assertEqual(sum(item[0] for item in self.editor.image[0:10]), 10*color)
        self.assertFalse(self.empty_image)

        # make sure we can give sure we can swap begin and end if begin > end
        self.editor.clear_drawing_board()
        # import pdb;pdb.set_trace()
        self.editor.draw_segment(orientation=self.editor.valid_orientations[1],
        fixed_row=1, begin=10, end=1, color=color)
        self.assertEqual(sum(item[0] for item in self.editor.image[0:10]), 10*color)
        self.assertFalse(self.empty_image)

    def test_create_drawing_board_failure(self):
        """
        Make sure invalid data are well checked.
        """
        self.assertIsNone(self.editor.image)
        with self.assertRaises(InvalidAxisFormatError):
            self.editor.create_drawing_board(size=(10,))

        with self.assertRaises(InvalidAxisFormatError):
            self.editor.create_drawing_board(size=[10, 10])

        with self.assertRaises(ImageOverflowError):
            self.editor.create_drawing_board(size=(256, 256))

    def test_show_image(self):
        """
        Make sure the image is well formatted.
        """
        image = self.editor.create_drawing_board(size=(5, 5))
        self.editor.draw_pixel(pixel=(4,4), color=3)
        self.editor.draw_pixel(pixel=(4,3), color=3)
        self.editor.draw_pixel(pixel=(3,4), color=3)
        self.editor.draw_pixel(pixel=(3,3), color=3)
        self.editor.draw_pixel_region(pixel=(2,2), color=4)
        import pdb; pdb.set_trace()
        self.editor.show_image("simple")
        # import pdb; pdb.set_trace()

if __name__ == "__main__":
    unittest.main()
