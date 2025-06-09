import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def not_eq(self):
        node = TextNode("hola mundo", TextType.LINK, "www.x.com")
        node2 = TextNode("hello world", TextType.LINK, "www.x.com")
        self.assertNotEqual(node, node2)




if __name__ == "__main__":
    unittest.main()