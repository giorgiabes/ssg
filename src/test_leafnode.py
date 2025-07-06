import unittest
from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_with_tag_and_value(self):
        # Given: A LeafNode with a tag and a value
        node = LeafNode("p", "This is a paragraph.")
        # When: Calling to_html()
        result = node.to_html()
        # Then: It should return proper HTML with opening and closing tag
        self.assertEqual(result, "<p>This is a paragraph.</p>")

    def test_to_html_with_tag_value_and_props(self):
        # Given: A LeafNode with a tag, value, and HTML attributes
        node = LeafNode("a", "Click here", {"href": "https://example.com"})
        # When: Calling to_html()
        result = node.to_html()
        # Then: It should include the attributes in the tag
        self.assertEqual(result, '<a href="https://example.com">Click here</a>')

    def test_to_html_without_tag_returns_raw_text(self):
        # Given: A LeafNode with no tag (raw text)
        node = LeafNode(None, "Just raw text")
        # When: Calling to_html()
        result = node.to_html()
        # Then: It should return the raw value
        self.assertEqual(result, "Just raw text")

    def test_to_html_raises_error_for_empty_value(self):
        # Given: An attempt to create a LeafNode with an empty value
        # Then: It should raise a ValueError
        with self.assertRaises(ValueError):
            LeafNode("p", "")

    def test_leafnode_is_instance_of_htmlnode(self):
        # Given: A LeafNode instance
        node = LeafNode("p", "Hello")
        # Then: It should also be an instance of HTMLNode
        from htmlnode import HTMLNode

        self.assertIsInstance(node, HTMLNode)

    def test_repr_output(self):
        # Given: A LeafNode with tag, value, and props
        node = LeafNode("span", "Hello", {"class": "highlight"})
        # When: Calling repr()
        result = repr(node)
        # Then: It should include all the field values
        expected = "HTMLNode(tag='span', value='Hello', props={'class': 'highlight'})"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
