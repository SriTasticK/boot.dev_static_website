import unittest
from markdown_to_html import markdown_to_html_node

class TestMarkdownToHTMLNode(unittest.TestCase):
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

## Heading **2**

###### Heading 6
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><h1>Heading 1</h1><h2>Heading <b>2</b></h2><h6>Heading 6</h6></div>",
        )

    def test_quote(self):
        md = """
> This is a quote
> with _italic_ text
>and no space
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><blockquote>This is a quote with <i>italic</i> text and no space</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- First item
- Second with **bold**
- Third with `code`
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><ul><li>First item</li><li>Second with <b>bold</b></li><li>Third with <code>code</code></li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second with _italic_
3. Third
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><ol><li>First item</li><li>Second with <i>italic</i></li><li>Third</li></ol></div>",
        )

    def test_links_and_images(self):
        md = "A [link](https://boot.dev) and ![pic](https://example.com/a.png)"
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            '<div><p>A <a href="https://boot.dev">link</a> and <img src="https://example.com/a.png" alt="pic"></img></p></div>',
        )

    def test_code_block_keeps_html_like_markdown(self):
        md = """
```
# not a heading
- not a list
```
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><pre><code># not a heading\n- not a list\n</code></pre></div>",
        )

    def test_mixed_document(self):
        md = """
# Title

Intro paragraph with **bold**.

> A wise quote

- one
- two

1. first
2. second

```
code here
```
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div>"
            "<h1>Title</h1>"
            "<p>Intro paragraph with <b>bold</b>.</p>"
            "<blockquote>A wise quote</blockquote>"
            "<ul><li>one</li><li>two</li></ul>"
            "<ol><li>first</li><li>second</li></ol>"
            "<pre><code>code here\n</code></pre>"
            "</div>",
        )

    def test_empty_document(self):
        self.assertEqual(markdown_to_html_node("").to_html(), "<div></div>")

if __name__ == "__main__":
    unittest.main()
