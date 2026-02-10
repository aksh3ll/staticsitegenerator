import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_eq(self):
        node = HTMLNode('div', 'content', None)
        node2 = HTMLNode('div', 'content', None)
        self.assertEqual(node, node2)

    def test_eq_tag(self):
        node = HTMLNode('div', 'content', None)
        node2 = HTMLNode('blockquote', 'content', None)
        self.assertNotEqual(node, node2)

    def test_eq_value(self):
        node = HTMLNode('div', 'content')
        node2 = HTMLNode('div', 'different content')
        self.assertNotEqual(node, node2)

    def test_eq_props(self):
        node = HTMLNode('div', 'content', [], {'class': 'container'})
        node2 = HTMLNode('div', 'content', None)
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode('div', 'content', [], {'class': 'container', 'id': 'main'})
        excepted = ' class="container" id="main"'
        self.assertEqual(node.props_to_html(), excepted)


if __name__ == "__main__":
    unittest.main()
