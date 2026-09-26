import unittest, os
from webpage import extract_title

class TestWebpage(unittest.TestCase):
    def test_extract_title(self):
        md = os.path.join(os.getcwd(), "src/example.md")
        title = extract_title(md)
        self.assertEqual(
            title,
            "This is heading 1")
