import unittest
from editor.editor import Editor

class EditorTestCase(unittest.TestCase):
    """
    Editor class test suite.
    """
    def __init__(self, *args, **kwargs):
        self.editor = None

    def setUp(self):
        self.editor = Editor()

    def tearDown(self):
        self.editor = None

    def test_create_drawing_board_success(self):
        """
        Make sure we can create an image.
        """
        self.assertIsNone(self.editor.image)
        image = self.create_drawing_board(size=(10, 20))
        self.assertIsNotNone(self.editor.image)
        self.assertEqual(image, self.editor.image)


if __name__ == "__main__":
    unittest.main()
