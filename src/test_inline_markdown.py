import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_multiple_delimited_sections(self):
        node = TextNode("One **two** three **four** five", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("One ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
                TextNode(" three ", TextType.TEXT),
                TextNode("four", TextType.BOLD),
                TextNode(" five", TextType.TEXT),
            ],
        )

    def test_delimiter_at_start_and_end(self):
        node = TextNode("**bold** middle **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" middle ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
        )

    def test_whole_text_delimited(self):
        node = TextNode("`all code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("all code", TextType.CODE)])

    def test_no_delimiter(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("Just plain text", TextType.TEXT)])

    def test_non_text_nodes_unchanged(self):
        nodes = [
            TextNode("already bold", TextType.BOLD),
            TextNode("a link", TextType.LINK, "https://boot.dev"),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, nodes)

    def test_non_text_node_with_delimiter_not_split(self):
        node = TextNode("code with `backticks` inside", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("First `code`", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("`more` code", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("First ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode("bold", TextType.BOLD),
                TextNode("more", TextType.CODE),
                TextNode(" code", TextType.TEXT),
            ],
        )

    def test_chained_bold_then_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
        )

    def test_chained_code_then_bold(self):
        node = TextNode("Run `x**2` for **power**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Run ", TextType.TEXT),
                TextNode("x**2", TextType.CODE),
                TextNode(" for ", TextType.TEXT),
                TextNode("power", TextType.BOLD),
            ],
        )

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This has an `unclosed code block", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_unmatched_bold_raises(self):
        node = TextNode("**one** and **two", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_empty_list(self):
        self.assertEqual(split_nodes_delimiter([], "`", TextType.CODE), [])


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            extract_markdown_images(text),
        )

    def test_no_images(self):
        self.assertListEqual([], extract_markdown_images("Just plain text"))

    def test_empty_alt_text(self):
        self.assertListEqual(
            [("", "https://example.com/a.png")],
            extract_markdown_images("![](https://example.com/a.png)"),
        )

    def test_images_ignores_links(self):
        text = "A [link](https://boot.dev) and an ![image](https://example.com/a.png)"
        self.assertListEqual(
            [("image", "https://example.com/a.png")],
            extract_markdown_images(text),
        )

    def test_image_with_nested_brackets_not_matched(self):
        self.assertListEqual(
            [], extract_markdown_images("![alt [nested]](https://example.com/a.png)")
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_multiple_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            extract_markdown_links(text),
        )

    def test_no_links(self):
        self.assertListEqual([], extract_markdown_links("Just plain text"))

    def test_links_ignores_images(self):
        text = "An ![image](https://example.com/a.png) and a [link](https://boot.dev)"
        self.assertListEqual(
            [("link", "https://boot.dev")],
            extract_markdown_links(text),
        )

    def test_link_at_start_of_text(self):
        self.assertListEqual(
            [("start", "https://boot.dev")],
            extract_markdown_links("[start](https://boot.dev) of text"),
        )

    def test_brackets_without_url_not_matched(self):
        self.assertListEqual([], extract_markdown_links("Some [bracketed] text"))


class TestSplitNodesImage(unittest.TestCase):
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
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_image_only(self):
        node = TextNode("![alone](https://example.com/a.png)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("alone", TextType.IMAGE, "https://example.com/a.png")],
            split_nodes_image([node]),
        )

    def test_image_at_start_with_trailing_text(self):
        node = TextNode("![start](https://example.com/a.png) then text", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "https://example.com/a.png"),
                TextNode(" then text", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_adjacent_images(self):
        node = TextNode(
            "![a](https://example.com/a.png)![b](https://example.com/b.png)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "https://example.com/a.png"),
                TextNode("b", TextType.IMAGE, "https://example.com/b.png"),
            ],
            split_nodes_image([node]),
        )

    def test_duplicate_images(self):
        node = TextNode(
            "![x](https://example.com/x.png) and ![x](https://example.com/x.png)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("x", TextType.IMAGE, "https://example.com/x.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("x", TextType.IMAGE, "https://example.com/x.png"),
            ],
            split_nodes_image([node]),
        )

    def test_no_images(self):
        node = TextNode("Just plain text", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_images_leaves_links_alone(self):
        node = TextNode("A [link](https://boot.dev) here", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_non_text_nodes_unchanged(self):
        nodes = [
            TextNode("![img](https://example.com/a.png)", TextType.CODE),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertListEqual(nodes, split_nodes_image(nodes))

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("One ![a](https://example.com/a.png)", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("![b](https://example.com/b.png) two", TextType.TEXT),
        ]
        self.assertListEqual(
            [
                TextNode("One ", TextType.TEXT),
                TextNode("a", TextType.IMAGE, "https://example.com/a.png"),
                TextNode("bold", TextType.BOLD),
                TextNode("b", TextType.IMAGE, "https://example.com/b.png"),
                TextNode(" two", TextType.TEXT),
            ],
            split_nodes_image(nodes),
        )

    def test_empty_list(self):
        self.assertListEqual([], split_nodes_image([]))


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            split_nodes_link([node]),
        )

    def test_link_only(self):
        node = TextNode("[alone](https://boot.dev)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("alone", TextType.LINK, "https://boot.dev")],
            split_nodes_link([node]),
        )

    def test_link_with_trailing_text(self):
        node = TextNode("[start](https://boot.dev) and more", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("start", TextType.LINK, "https://boot.dev"),
                TextNode(" and more", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_no_links(self):
        node = TextNode("Just plain text", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_links_leaves_images_alone(self):
        node = TextNode(
            "An ![image](https://example.com/a.png) and a [link](https://boot.dev)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("An ![image](https://example.com/a.png) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            split_nodes_link([node]),
        )

    def test_link_and_image_with_same_markdown(self):
        node = TextNode(
            "![same](https://boot.dev) then [same](https://boot.dev)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("![same](https://boot.dev) then ", TextType.TEXT),
                TextNode("same", TextType.LINK, "https://boot.dev"),
            ],
            split_nodes_link([node]),
        )

    def test_non_text_nodes_unchanged(self):
        nodes = [
            TextNode("[link](https://boot.dev)", TextType.CODE),
            TextNode("already", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(nodes, split_nodes_link(nodes))

    def test_images_then_links(self):
        node = TextNode(
            "See ![pic](https://example.com/a.png) and [site](https://boot.dev).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link(split_nodes_image([node]))
        self.assertListEqual(
            [
                TextNode("See ", TextType.TEXT),
                TextNode("pic", TextType.IMAGE, "https://example.com/a.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("site", TextType.LINK, "https://boot.dev"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_empty_list(self):
        self.assertListEqual([], split_nodes_link([]))


class TestTextToTextNodes(unittest.TestCase):
    def test_all_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(
            [
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
            ],
            text_to_textnodes(text),
        )

    def test_plain_text(self):
        self.assertListEqual(
            [TextNode("Just plain text", TextType.TEXT)],
            text_to_textnodes("Just plain text"),
        )

    def test_only_bold(self):
        self.assertListEqual(
            [TextNode("bold", TextType.BOLD)],
            text_to_textnodes("**bold**"),
        )

    def test_bold_and_italic_adjacent(self):
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
            ],
            text_to_textnodes("**bold**_italic_"),
        )

    def test_markdown_inside_code_stays_literal(self):
        self.assertListEqual(
            [
                TextNode("Use ", TextType.TEXT),
                TextNode("**kwargs and my_var", TextType.CODE),
                TextNode(" here", TextType.TEXT),
            ],
            text_to_textnodes("Use `**kwargs and my_var` here"),
        )

    def test_underscores_in_url_not_italic(self):
        self.assertListEqual(
            [
                TextNode("See ", TextType.TEXT),
                TextNode("docs", TextType.LINK, "https://example.com/my_page_name"),
                TextNode(" and ", TextType.TEXT),
                TextNode("pic", TextType.IMAGE, "https://example.com/my_pic.png"),
            ],
            text_to_textnodes(
                "See [docs](https://example.com/my_page_name) and ![pic](https://example.com/my_pic.png)"
            ),
        )

    def test_multiple_of_each(self):
        self.assertListEqual(
            [
                TextNode("a", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("b", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("c", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("d", TextType.ITALIC),
            ],
            text_to_textnodes("**a** **b** _c_ _d_"),
        )

    def test_unclosed_delimiter_raises(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("This **never closes")

    def test_empty_string(self):
        self.assertListEqual([], text_to_textnodes(""))

if __name__ == "__main__":
    unittest.main()
