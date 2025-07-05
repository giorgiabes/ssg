## src/test_textnode.py
import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_not_equal_different_text(self):
        node1 = TextNode("some text", TextType.TEXT)
        node2 = TextNode("some other text", TextType.TEXT)
        self.assertNotEqual(node1, node2)

    def test_not_equal_different_text_type(self):
        node1 = TextNode("hello, word", TextType.BOLD)
        node2 = TextNode("hello, word", TextType.CODE)
        self.assertNotEqual(node1, node2)

    def test_not_equal_different_url(self):
        node1 = TextNode("hello, word", TextType.LINK, "https://example.com")
        node2 = TextNode("hello, word", TextType.LINK, "http://example.com")
        self.assertNotEqual(node1, node2)

    def test_repr_output(self):
        node = TextNode("This is some anchor text", TextType.LINK, "https://boot.dev")
        output = "TextNode(text='This is some anchor text', text_type='link', url='https://boot.dev')"
        self.assertEqual(repr(node), output)

    def test_equality_with_non_textnode(self):
        node = TextNode("hello", TextType.TEXT)
        non_textnode = ["hello", 42, 3.14, None, True, str, dict, tuple]
        for item in non_textnode:
            with self.subTest(other=item):
                self.assertNotEqual(node, item)

    def test_textnode_with_url_equality(self):
        node1 = TextNode("hello", TextType.LINK, "https://example.com")
        node2 = TextNode("hello", TextType.LINK, "https://example.com")
        self.assertEqual(node1, node2)

    def test_textnode_inequality_due_to_url(self):
        node1 = TextNode("hello", TextType.LINK)
        node2 = TextNode("hello", TextType.LINK, "https://example.com")
        self.assertNotEqual(node1, node2)

    def test_textnode_empty_text(self):
        node1 = TextNode("", TextType.TEXT)
        node2 = TextNode("", TextType.TEXT)
        self.assertEqual(node1, node2)

    def test_textnode_image_type_with_url(self):
        url = "https://example.com/image.png"
        node = TextNode("An image", TextType.IMAGE, url)
        self.assertEqual(node.url, url)
        self.assertEqual(node.text_type, TextType.IMAGE)


if __name__ == "__main__":
    unittest.main()
