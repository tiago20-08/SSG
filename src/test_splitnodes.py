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


if __name__ == "__main__":
    unittest.main()
