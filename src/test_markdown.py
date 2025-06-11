import unittest
from markdown import markdown_to_blocks

class TestMark(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_paragraph(self):
        md = "Single paragraph without any breaks."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Single paragraph without any breaks."])

    def test_multiple_paragraphs_with_spaces(self):
        md = "Para 1\n\n  Para 2 with leading spaces  \n\n\nPara 3 with extra breaks"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "Para 1",
            "Para 2 with leading spaces",
            "Para 3 with extra breaks"
        ])

    def test_lines_within_paragraph(self):
        md = "Line 1 of para\nLine 2 of para\n\nLine 1 of next para"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "Line 1 of para\nLine 2 of para",
            "Line 1 of next para"
        ])

    def test_paragraph_with_only_whitespace(self):
        md = "Para 1\n\n   \n\nPara 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "Para 1",
            "",
            "Para 2"
        ])








if __name__ == "__main__":
    unittest.main()