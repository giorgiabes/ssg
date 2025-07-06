# src/test_parentnode.py

import unittest
from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_single_child(self):
        # Given: A ParentNode with one LeafNode child
        child = LeafNode("span", "Hello")
        parent = ParentNode("div", [child])

        # When: Calling to_html()
        result = parent.to_html()

        # Then: The HTML should wrap the child's output in the parent tag
        self.assertEqual(result, "<div><span>Hello</span></div>")

    def test_to_html_with_multiple_children(self):
        # Given: A ParentNode with several LeafNode children
        children = [
            LeafNode("b", "Bold"),
            LeafNode(None, " plain "),
            LeafNode("i", "italic"),
        ]
        parent = ParentNode("p", children)

        # When: Calling to_html()
        result = parent.to_html()

        # Then: All children should be rendered in sequence inside the parent tag
        self.assertEqual(result, "<p><b>Bold</b> plain <i>italic</i></p>")

    def test_to_html_with_nested_parent(self):
        # Given: A ParentNode with a nested ParentNode as child
        grandchild = LeafNode("b", "Nested")
        child = ParentNode("span", [grandchild])
        parent = ParentNode("div", [child])

        # When: Calling to_html()
        result = parent.to_html()

        # Then: Nested HTML should be rendered correctly
        self.assertEqual(result, "<div><span><b>Nested</b></span></div>")

    def test_constructor_raises_without_tag(self):
        # Given: A missing tag value
        # Then: Constructing the ParentNode should raise ValueError
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("span", "Hi")])  # type: ignore

    def test_to_html_with_props(self):
        # Given: A ParentNode with props and one child
        props = {"class": "container", "id": "main"}
        child = LeafNode("span", "content")
        parent = ParentNode("div", [child], props=props)

        # When: Calling to_html()
        result = parent.to_html()

        # Then: The props should appear in the opening tag
        self.assertEqual(result, '<div class="container" id="main"><span>content</span></div>')

    def test_constructor_with_invalid_child_type(self):
        # Given: A list of children that includes a non-HTMLNode
        children = [LeafNode("span", "Hi"), "not a node"]

        # Then: Creating a ParentNode should raise a TypeError or fail
        with self.assertRaises(AttributeError):
            ParentNode("div", children).to_html()

    def test_to_html_with_empty_children(self):
        # Given: A ParentNode with no children
        parent = ParentNode("div", [])

        # When: Calling to_html()
        result = parent.to_html()

        # Then: It should return just an empty tag pair
        self.assertEqual(result, "<div></div>")

    def test_deeply_nested_parent_nodes(self):
        # Given: Several layers of nested ParentNode -> ParentNode -> LeafNode
        leaf = LeafNode("b", "deep")
        level3 = ParentNode("span", [leaf])
        level2 = ParentNode("div", [level3])
        level1 = ParentNode("section", [level2])

        # When: Calling to_html()
        result = level1.to_html()

        # Then: It should render all nested levels properly
        self.assertEqual(result, "<section><div><span><b>deep</b></span></div></section>")



if __name__ == "__main__":
    unittest.main()

