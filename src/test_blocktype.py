import unittest
from blocktype import block_to_block_type, BlockType

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a normal paragraph with multiple lines.\nStill the same paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_level_3(self):
        block = "### Subheading level 3"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block(self):
        block = "```\nprint('Hello')\nprint('World')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> This is a quote\n> still quoting\n> one more line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- Item one\n- Item two\n- Item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDER)

    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDER)

    def test_invalid_ordered_list(self):
        block = "1. First\n3. Wrong number"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_invalid_heading_no_space(self):
        block = "##Invalid heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()