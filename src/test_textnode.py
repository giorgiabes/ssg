import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_not_equal_different_text(self):
        # Given: Two TextNodes with different text but same type
        node1 = TextNode("some text", TextType.TEXT)
        node2 = TextNode("some other text", TextType.TEXT)
        # Then: They should not be considered equal
        self.assertNotEqual(node1, node2)

    def test_not_equal_different_text_type(self):
        # Given: Two TextNodes with same text but different text types
        node1 = TextNode("hello, word", TextType.BOLD)
        node2 = TextNode("hello, word", TextType.CODE)
        # Then: They should not be equal
        self.assertNotEqual(node1, node2)

    def test_not_equal_different_url(self):
        # Given: Two TextNodes with same text and type but different URLs
        node1 = TextNode("hello, word", TextType.LINK, "https://example.com")
        node2 = TextNode("hello, word", TextType.LINK, "http://example.com")
        # Then: They should not be equal
        self.assertNotEqual(node1, node2)

    def test_repr_output(self):
        # Given: A TextNode representing a link
        node = TextNode("This is some anchor text", TextType.LINK, "https://boot.dev")
        # When: Calling repr()
        # Then: It should return a formatted string of the node
        output = "TextNode(text='This is some anchor text', text_type='link', url='https://boot.dev')"
        self.assertEqual(repr(node), output)

    def test_equality_with_non_textnode(self):
        # Given: A TextNode
        node = TextNode("hello", TextType.TEXT)
        # Then: It should not be equal to unrelated types
        non_textnode = ["hello", 42, 3.14, None, True, str, dict, tuple]
        for item in non_textnode:
            with self.subTest(other=item):
                self.assertNotEqual(node, item)

    def test_textnode_with_url_equality(self):
        # Given: Two identical TextNodes with the same text, type, and URL
        node1 = TextNode("hello", TextType.LINK, "https://example.com")
        node2 = TextNode("hello", TextType.LINK, "https://example.com")
        # Then: They should be considered equal
        self.assertEqual(node1, node2)

    def test_textnode_inequality_due_to_url(self):
        # Given: Two TextNodes with same text and type but one has a URL
        node1 = TextNode("hello", TextType.LINK)
        node2 = TextNode("hello", TextType.LINK, "https://example.com")
        # Then: They should not be equal
        self.assertNotEqual(node1, node2)

    def test_textnode_empty_text(self):
        # Given: Two TextNodes with empty string as text and same type
        node1 = TextNode("", TextType.TEXT)
        node2 = TextNode("", TextType.TEXT)
        # Then: They should be considered equal
        self.assertEqual(node1, node2)

    def test_textnode_image_type_with_url(self):
        # Given: A TextNode of type IMAGE with a URL
        url = "https://example.com/image.png"
        node = TextNode("An image", TextType.IMAGE, url)
        # Then: The text_type and URL should match the inputs
        self.assertEqual(node.url, url)
        self.assertEqual(node.text_type, TextType.IMAGE)


if __name__ == "__main__":
    unittest.main()
