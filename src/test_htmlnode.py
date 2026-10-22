import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "link", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_none(self):
        node = HTMLNode("p", "text")
        self.assertEqual(node.props_to_html(), "")

    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "text")
        with self.assertRaises(NotImplementedError):
            node.to_html()


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Heading")
        self.assertEqual(node.to_html(), "<h1>Heading</h1>")

    def test_leaf_to_html_img_multiple_props(self):
        node = LeafNode("img", "", {"src": "cat.png", "alt": "A cat"})
        self.assertEqual(node.to_html(), '<img src="cat.png" alt="A cat"></img>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just raw text")
        self.assertEqual(node.to_html(), "Just raw text")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_has_no_children(self):
        node = LeafNode("p", "text")
        self.assertIsNone(node.children)

    def test_leaf_repr(self):
        node = LeafNode("a", "Click", {"href": "x"})
        self.assertEqual(repr(node), "LeafNode(a, Click, {'href': 'x'})")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_deep_nesting(self):
        node = ParentNode(
            "div",
            [ParentNode("section", [ParentNode("p", [LeafNode("em", "deep")])])],
        )
        self.assertEqual(
            node.to_html(),
            "<div><section><p><em>deep</em></p></section></div>",
        )

    def test_to_html_mixed_parent_and_leaf_children(self):
        node = ParentNode(
            "ul",
            [
                ParentNode("li", [LeafNode("b", "one")]),
                ParentNode("li", [LeafNode(None, "two")]),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<ul><li><b>one</b></li><li>two</li></ul>",
        )

    def test_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("a", "link", {"href": "https://boot.dev"})],
            {"class": "container", "id": "main"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="container" id="main"><a href="https://boot.dev">link</a></div>',
        )

    def test_to_html_empty_children(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode("b", "text")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_error_messages_differ(self):
        with self.assertRaises(ValueError) as no_tag:
            ParentNode(None, []).to_html()
        with self.assertRaises(ValueError) as no_children:
            ParentNode("div", None).to_html()
        self.assertNotEqual(str(no_tag.exception), str(no_children.exception))

    def test_to_html_nested_child_error_propagates(self):
        node = ParentNode("div", [ParentNode("p", [LeafNode("b", None)])])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_has_no_value(self):
        node = ParentNode("div", [])
        self.assertIsNone(node.value)

if __name__ == "__main__":
    unittest.main()
