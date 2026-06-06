import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def not_eq(self):
        node = TextNode("Text node", TextType.ITALIC)
        node2 = TextNode("Another Text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_equal_different_type(self):
        node = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Hello", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_none_default(self):
        node = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Hello", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_url_difference(self):
        node = TextNode("Hello", TextType.BOLD, "url1")
        node2 = TextNode("Hello", TextType.BOLD, "url2")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
