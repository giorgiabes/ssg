import unittest
from markdown_to_html import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_code_block(self):
        md = """```
This is text that _should_ remain
the **same** even with inline stuff
```"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_levels(self):
        md = "# Heading 1\n## Heading 2\n### Heading 3"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>",
        )

    def test_blockquote(self):
        md = """> This is a blockquote
> with multiple lines
> and **bold** text"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is a blockquote with multiple lines and <b>bold</b> text</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """- Item one
- Item two with _italic_
- Item three with **bold**"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>Item one</li><li>Item two with <i>italic</i></li><li>Item three with <b>bold</b></li></ul></div>",
        )

    def test_ordered_list(self):
        md = """1. First item
2. Second item with `code`
3. Third item"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>First item</li><li>Second item with <code>code</code></li><li>Third item</li></ol></div>",
        )


if __name__ == "__main__":
    unittest.main()
