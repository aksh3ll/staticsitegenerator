import unittest

from leafnode import LeafNode
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_text(self):
        node = TextNode("This", TextType.BOLD, "url")
        node2 = TextNode("That", TextType.BOLD, "url")
        self.assertNotEqual(node, node2)

    def test_eq_type(self):
        node = TextNode("Text", TextType.BOLD)
        node2 = TextNode("Text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("Link", TextType.LINK, "url1")
        node2 = TextNode("Link", TextType.LINK, "url2")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
