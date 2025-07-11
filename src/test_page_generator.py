import unittest
from page_generator import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_valid_title(self):
        md = "# My Title"
        self.assertEqual(extract_title(md), "My Title")

    def test_extract_title_with_whitespace(self):
        md = "#   Spaced Title    "
        self.assertEqual(extract_title(md), "Spaced Title")

    def test_missing_title(self):
        md = "## Subtitle\nJust text"
        with self.assertRaises(Exception):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()
