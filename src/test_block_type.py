import unittest
from block_type import BlockType, block_to_block_type


class TestBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Subheading"), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type("####### Too many"), BlockType.HEADING)

    def test_code(self):
        md = "```print('hi')```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)

    def test_quote(self):
        md = "> quoted line\n> another one"
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

    def test_unordered_list(self):
        md = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)

    def test_ordered_list_valid(self):
        md = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)

    def test_ordered_list_invalid_numbering(self):
        md = "1. First\n3. Skipped\n4. Bad"
        self.assertNotEqual(block_to_block_type(md), BlockType.ORDERED_LIST)

    def test_paragraph_default(self):
        self.assertEqual(
            block_to_block_type("Just some normal paragraph text."), BlockType.PARAGRAPH
        )

    def test_empty_block(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("\n\n"), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
