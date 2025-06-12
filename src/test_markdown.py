import unittest
from markdown import markdown_to_blocks, markdown_to_html_node

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
            "Para 2"
        ])

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        
    def test_headings(self):
        md = """
# Heading 1

## Heading 2

### Heading 3
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>"
        )

    def test_unordered_list(self):
        md = """
- Item one
- Item two with **bold**
- Item three with _italic_
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item one</li><li>Item two with <b>bold</b></li><li>Item three with <i>italic</i></li></ul></div>"
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item with `code`
3. Third item
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <code>code</code></li><li>Third item</li></ol></div>"
        )

    def test_blockquote(self):
        md = """
> This is a quote
> with **bold** and _italic_ text
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with <b>bold</b> and <i>italic</i> text</blockquote></div>"
        )

    def test_mixed_content(self):
        md = """
# Header

Paragraph with **bold**, _italic_, and `code`.

- List item 1
- List item 2

> A blockquote with _italic_ text

```
def foo():
    pass
```
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Header</h1><p>Paragraph with <b>bold</b>, <i>italic</i>, and <code>code</code>.</p><ul><li>List item 1</li><li>List item 2</li></ul><blockquote>A blockquote with <i>italic</i> text</blockquote><pre><code>def foo():\n    pass\n</code></pre></div>"
        )






if __name__ == "__main__":
    unittest.main()