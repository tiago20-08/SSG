import unittest
from splitnodes import *
from textnode import TextNode, TextType


class TestSplit(unittest.TestCase):
    def test_samu(self):
        node = split_nodes_delimiter(
            [TextNode("este texto no **tiene** delimetro", TextType.TEXT)],
            "**",
            TextType.BOLD,
        )
        res = [
            TextNode("este texto no ", TextType.TEXT),
            TextNode("tiene", TextType.BOLD),
            TextNode(" delimetro", TextType.TEXT),
        ]
        self.assertEqual(node, res)

    def test2_samunotequal(self):
        node = split_nodes_delimiter(
            [TextNode("hola mundo", TextType.BOLD)], "´", TextType.CODE
        )
        res = [TextNode("hola mundo", TextType.BOLD)]
        self.assertEqual(node, res)

    def test_error(self):
        with self.assertRaises(Exception):
            split_nodes_delimiter(
                [TextNode("este es un **nodo sin terminar.", TextType.TEXT)],
                "**",
                TextType.BOLD,
            )

    def test_3samu(self):
        node = split_nodes_delimiter(
            [
                TextNode("este texto **tiene** delimetro", TextType.TEXT),
                TextNode("samu cabeza de mil **pingo** puto **de** mierda", TextType.TEXT),
            ],
            "**",
            TextType.BOLD,
        )
        res = [
            TextNode("este texto ", TextType.TEXT),
            TextNode("tiene", TextType.BOLD),
            TextNode(" delimetro", TextType.TEXT),
            TextNode("samu cabeza de mil ", TextType.TEXT),
            TextNode("pingo", TextType.BOLD),
            TextNode(" puto ", TextType.TEXT),
            TextNode("de", TextType.BOLD),
            TextNode(" mierda", TextType.TEXT)
        ]
        self.assertEqual(node, res)


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
    def test_split_images_single(self):
        node = TextNode(
            "Image here ![img](https://example.com/img.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("Image here ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://example.com/img.png")
        ],
        new_nodes
    )

    def test_split_images_start_and_end(self):
        node = TextNode(
            "![start](url1) middle text ![end](url2)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("", TextType.TEXT),
                TextNode("start", TextType.IMAGE, "url1"),
                TextNode(" middle text ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "url2"),
            ],
            new_nodes
        )

    def test_split_images_no_images(self):
        node = TextNode("This text has no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This text has no images", TextType.TEXT)],
            new_nodes
        )

    def test_split_images_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("", TextType.TEXT)],
            new_nodes
        )
    def test_text_to_textnodes(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(result, expected)

    def test_text_to_textnodes_bold_only(self):
        text = "This is **bold** text"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_italic_only(self):
        text = "This is _italic_ text"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_code_only(self):
        text = "This is `code` block"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.TEXT),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_image_only(self):
        text = "Look at this ![cat](https://img.com/cat.png)"
        expected = [
            TextNode("Look at this ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "https://img.com/cat.png"),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_link_only(self):
        text = "Check [this out](https://example.com)"
        expected = [
            TextNode("Check ", TextType.TEXT),
            TextNode("this out", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    
    def test_text_to_textnodes_all_formats(self):
        text = "This is **bold** and _italic_ and `code` with ![img](https://img.com/img.png) and [a link](https://link.com)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" with ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://img.com/img.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "https://link.com"),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_plain(self):
        text = "Just plain text here."
        expected = [TextNode("Just plain text here.", TextType.TEXT)]
        self.assertListEqual(text_to_textnodes(text), expected)




if __name__ == "__main__":
    unittest.main()
