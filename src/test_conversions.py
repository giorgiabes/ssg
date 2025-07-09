import unittest
from conversions import text_node_to_html_node
import htmlnode
from textnode import TextNode, TextType


class TestConversions(unittest.TestCase):
    def test_text_type_text(self):
        # Given: A TextNode with type TEXT and sample text
        node = TextNode("This is a text node", TextType.TEXT)
        # When: Passing it to text_node_to_html_node
        html_node = text_node_to_html_node(node)
        # Then: Should return a LeafNode with no tag and the same text as value
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_type_bold(self):
        # Given: A TextNode with type BOLD and some bold text
        node = TextNode("This is a bold text node", TextType.BOLD)
        # When: Passing it to text_node_to_html_node
        html_node = text_node_to_html_node(node)
        # Then: Should return a LeafNode with tag "b" and same text as value
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_text_type_italic(self):
        # Given: A TextNode with type TextType.ITALIC and some italic text
        node = TextNode("This is an italic text node", TextType.ITALIC)
        # When: it passed to text_node_to_html_node()
        html_node = text_node_to_html_node(node)
        # Then: it should return a LeafNode with tag "i" and the same text as value
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_text_type_code(self):
        # Given: A TextNode with type CODE and some code
        node = TextNode("print('hello, world')", TextType.CODE)
        # When: passing it to text_node_to_httml_node
        html_node = text_node_to_html_node(node)
        # Then: it should return LeafNode with tag "i" and the same text as value
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello, world')")

    def test_text_type_link(self):
        pass
        # Given: A TextNode with text_type = TextType.LINK, some anchor
        # text (e.g. "Click here") and a valid URL (e.g. "https://example.com")
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        # When: The node is passed to text_node_to_html_node()
        html_node = text_node_to_html_node(node)
        # Then: It should return a LeafNode with:
        # - tag = "a"
        # - value = "Click here"
        # - props = {"href": "https://example.com"}
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_text_type_image(self):
        # Given: A TextNode with text_type = IMAGE, alt text, and valid image URL
        node = TextNode("An image", TextType.IMAGE, "https://example.com/image.png")

        # When: The node is passed to text_node_to_html_node()
        html_node = text_node_to_html_node(node)

        # Then: It should return a LeafNode with:
        #   - tag = "img"
        #   - value = "An image" (used only to satisfy constructor, not in final HTML)
        #   - props = {"src": ..., "alt": ...}
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "An image")
        self.assertEqual(
            html_node.props,
            {
                "src": "https://example.com/image.png",
                "alt": "An image",
            },
        )


if __name__ == "__main__":
    unittest.main()
