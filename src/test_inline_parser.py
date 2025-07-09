import unittest
from inline_parser import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_backtick_delimiter(self):
        node = TextNode("Text with `inline code` example", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("inline code", TextType.CODE),
                TextNode(" example", TextType.TEXT),
            ],
        )

    def test_bold_double_asterisks(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_multiple_code_sections(self):
        node = TextNode("This has `code` and more `code` here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" and more ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" here", TextType.TEXT),
            ],
        )

    def test_leading_and_trailing_delimiters(self):
        node = TextNode("`code` in start and `end`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" in start and ", TextType.TEXT),
                TextNode("end", TextType.CODE),
                TextNode("", TextType.TEXT),
            ],
        )

    def test_empty_delimited_section(self):
        node = TextNode("This is empty `` code", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("This is empty ", TextType.TEXT),
                TextNode("", TextType.CODE),
                TextNode(" code", TextType.TEXT),
            ],
        )

    def test_non_text_node_passthrough(self):
        node = TextNode("Some code", TextType.CODE)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [node])

    def test_raises_on_odd_delimiter_count(self):
        node = TextNode("Unclosed `code block", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("delimiter count is odd", str(context.exception))


class TestSplitImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_no_markdown(self):
        node = TextNode("Just some plain text", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [node])

    def test_image_at_start(self):
        node = TextNode("![start](url) then text", TextType.TEXT)
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("start", TextType.IMAGE, "url"),
                TextNode(" then text", TextType.TEXT),
            ],
        )

    def test_image_at_end(self):
        node = TextNode("Text before ![end](url)", TextType.TEXT)
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "url"),
            ],
        )

    def test_back_to_back_images(self):
        node = TextNode("![a](url1)![b](url2)", TextType.TEXT)
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("a", TextType.IMAGE, "url1"),
                TextNode("b", TextType.IMAGE, "url2"),
            ],
        )

    def test_multiple_textnodes_mixed(self):
        nodes = [
            TextNode("No image here", TextType.TEXT),
            TextNode("![yes](img)", TextType.TEXT),
            TextNode("Still no image", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_image(nodes),
            [
                TextNode("No image here", TextType.TEXT),
                TextNode("yes", TextType.IMAGE, "img"),
                TextNode("Still no image", TextType.TEXT),
            ],
        )

    def test_empty_string(self):
        node = TextNode("", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [node])

    def test_only_image(self):
        node = TextNode("![solo](img)", TextType.TEXT)
        self.assertEqual(
            split_nodes_image([node]), [TextNode("solo", TextType.IMAGE, "img")]
        )

    def test_image_with_special_chars(self):
        node = TextNode("![alt-1_2!@#](url.com/img)", TextType.TEXT)
        self.assertEqual(
            split_nodes_image([node]),
            [TextNode("alt-1_2!@#", TextType.IMAGE, "url.com/img")],
        )


class TestSplitLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_no_markdown(self):
        node = TextNode("Just some plain text", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [node])

    def test_link_at_start(self):
        node = TextNode("[start](url) then text", TextType.TEXT)
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("start", TextType.LINK, "url"),
                TextNode(" then text", TextType.TEXT),
            ],
        )

    def test_link_at_end(self):
        node = TextNode("Text before [end](url)", TextType.TEXT)
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("end", TextType.LINK, "url"),
            ],
        )

    def test_back_to_back_links(self):
        node = TextNode("[a](url1)[b](url2)", TextType.TEXT)
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("a", TextType.LINK, "url1"),
                TextNode("b", TextType.LINK, "url2"),
            ],
        )

    def test_multiple_textnodes_mixed(self):
        nodes = [
            TextNode("No link here", TextType.TEXT),
            TextNode("[yes](link)", TextType.TEXT),
            TextNode("Still no link", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_link(nodes),
            [
                TextNode("No link here", TextType.TEXT),
                TextNode("yes", TextType.LINK, "link"),
                TextNode("Still no link", TextType.TEXT),
            ],
        )

    def test_empty_string(self):
        node = TextNode("", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [node])

    def test_only_link(self):
        node = TextNode("[solo](link)", TextType.TEXT)
        self.assertEqual(
            split_nodes_link([node]), [TextNode("solo", TextType.LINK, "link")]
        )

    def test_link_with_special_chars(self):
        node = TextNode("[text-1_2!@#](url.com/page)", TextType.TEXT)
        self.assertEqual(
            split_nodes_link([node]),
            [TextNode("text-1_2!@#", TextType.LINK, "url.com/page")],
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_full_markdown_line(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
            "[link](https://boot.dev)"
        )
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_only_plain_text(self):
        text = "Just some plain text without markdown."
        expected = [TextNode("Just some plain text without markdown.", TextType.TEXT)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_markdown_at_edges(self):
        text = "**bold** in the beginning and at the end **endbold**"
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" in the beginning and at the end ", TextType.TEXT),
            TextNode("endbold", TextType.BOLD),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_back_to_back_markdown(self):
        text = "**bold1****bold2**"
        expected = [TextNode("bold1", TextType.BOLD), TextNode("bold2", TextType.BOLD)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_empty_string(self):
        self.assertEqual(text_to_textnodes(""), [])

    def test_only_image(self):
        text = "![alt](https://image.com/img.png)"
        expected = [TextNode("alt", TextType.IMAGE, "https://image.com/img.png")]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_special_characters(self):
        text = "_italic_ and **bold!** and [weird text?](https://url.com/?q=a)"
        expected = [
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold!", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("weird text?", TextType.LINK, "https://url.com/?q=a"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_mixed_order(self):
        text = "`code` before **bold** and _italic_ with ![img](url)"
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" before ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" with ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)


if __name__ == "__main__":
    unittest.main()
