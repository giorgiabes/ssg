import unittest
from markdown_extractor import extract_markdown_images, extract_markdown_links


class TestMarkdownExtractor(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        # Given: A markdown string with multiple links
        text = "Here is a [link](https://example.com) and another [link2](https://test.com)"
        # When: extract_markdown_links is called
        matches = extract_markdown_links(text)
        # Then: It should return a list of (anchor_text, url) tuples
        self.assertListEqual(
            [("link", "https://example.com"), ("link2", "https://test.com")], matches
        )


if __name__ == "__main__":
    unittest.main()
