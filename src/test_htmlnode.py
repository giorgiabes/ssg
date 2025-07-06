import unittest
from htmlnode import HTMLNode
import htmlnode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_empty_props(self):
        # Given: An HTMLNode with no attributes (empty props)
        node = HTMLNode("p", "hello, world", children=None, props={})
        # When: props_to_html() is called
        # Then: It should return an empty string
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_attribute(self):
        # Given: An HTMLNode with one HTML attribute
        node = HTMLNode("p", "hello, world", props={"href": "https://example.com"})
        # When: props_to_html() is called
        # Then: It should return a string with one formatted attribute
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_multiple_attributes(self):
        # Given: An HTMLNode with multiple HTML attributes
        node = HTMLNode(
            "p",
            "hello, world",
            props={"href": "https://example.com", "target": "_blank"},
        )
        # When: props_to_html() is called
        # Then: It should return a space-separated string of all attributes
        self.assertEqual(
            node.props_to_html(), ' href="https://example.com" target="_blank"'
        )

    def test_constructor_all_fields(self):
        # Given: All fields explicitly provided to the constructor
        node = HTMLNode(
            tag="p",
            value="hello, world",
            children=["child1", "child2"],
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        # Then: All fields should be set correctly
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "hello, world")
        self.assertEqual(node.children, ["child1", "child2"])
        self.assertEqual(
            node.props,
            {"href": "https://www.google.com", "target": "_blank"},
        )

    def test_constructor_only_tag_and_value(self):
        # Given: Only tag and value are provided
        node = HTMLNode(tag="p", value="hello, world")
        # Then: children and props should default to empty list/dict
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_constructor_defaults(self):
        # Given: No arguments are passed to the constructor
        node = HTMLNode()
        # Then: All fields should default to None or empty
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_constructor_mutable_defaults_are_unique(self):
        # Given: Two separate HTMLNode instances created without children or props
        node1 = HTMLNode()
        node2 = HTMLNode()
        # When: One node's children and props are modified
        node1.children = ["child1", "child2"]
        node1.props = {"href": "https://www.google.com"}
        # Then: The second node should remain unaffected (no shared mutable defaults)
        self.assertNotEqual(node2.children, ["child1", "child2"])
        self.assertNotEqual(node2.props, {"href": "https://www.google.com"})

    def test_repr_with_all_fields(self):
        # Given: An HTMLNode with tag, value, children, and props
        node = HTMLNode(
            tag="p",
            value="hello, world",
            children=["child1", "child2"],
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        # When: Calling repr() on the node
        result = repr(node)
        # Then: The output should include all values in a readable format
        expected = (
            "HTMLNode(tag='p', value='hello, world', "
            "children=['child1', 'child2'], "
            "props={'href': 'https://www.google.com', 'target': '_blank'})"
        )
        self.assertEqual(result, expected)

    def test_repr_with_minimal_fields(self):
        # Given: An HTMLNode with only tag and value
        node = HTMLNode(
            tag="p",
            value="hello, world",
        )
        # When: Calling repr() on the node
        result = repr(node)
        # Then: Children and props should show as empty in the output
        expected = (
            "HTMLNode(tag='p', value='hello, world', " "children=[], " "props={})"
        )
        self.assertEqual(result, expected)

    def test_repr_with_no_fields(self):
        # Given: An HTMLNode created with no arguments
        node = HTMLNode()
        # When: Calling repr()
        result = repr(node)
        # Then: All fields should show as None or empty
        expected = "HTMLNode(tag=None, value=None, " "children=[], " "props={})"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
