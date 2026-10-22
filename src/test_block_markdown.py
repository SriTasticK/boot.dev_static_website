import unittest
from block_markdown import BlockType, markdown_to_blocks, block_to_block_type

class TestMarkdownToBlocks(unittest.TestCase):
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

    def test_heading_paragraph_list(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_excessive_newlines(self):
        md = """
First block



Second block





Third block
"""
        self.assertEqual(
            markdown_to_blocks(md),
            ["First block", "Second block", "Third block"],
        )

    def test_strips_surrounding_whitespace(self):
        md = "   First block   \n\n\t Second block \t"
        self.assertEqual(markdown_to_blocks(md), ["First block", "Second block"])

    def test_whitespace_only_blocks_removed(self):
        md = "First\n\n   \n\nSecond"
        self.assertEqual(markdown_to_blocks(md), ["First", "Second"])

    def test_single_block(self):
        self.assertEqual(markdown_to_blocks("Just one block"), ["Just one block"])

    def test_single_newlines_stay_in_block(self):
        md = "Line one\nLine two\nLine three"
        self.assertEqual(markdown_to_blocks(md), ["Line one\nLine two\nLine three"])

    def test_code_block(self):
        md = """Intro

```
def hello():
    print("hi")
```

Outro"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "Intro",
                '```\ndef hello():\n    print("hi")\n```',
                "Outro",
            ],
        )

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_only_newlines(self):
        self.assertEqual(markdown_to_blocks("\n\n\n\n"), [])


class TestBlockToBlockType(unittest.TestCase):
    # Headings
    def test_heading_levels_1_to_6(self):
        for level in range(1, 7):
            block = "#" * level + " Heading"
            self.assertEqual(block_to_block_type(block), BlockType.HEADING, block)

    def test_heading_seven_hashes_is_paragraph(self):
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)

    def test_heading_without_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_heading_without_text_is_paragraph(self):
        self.assertEqual(block_to_block_type("# "), BlockType.PARAGRAPH)

    def test_hash_not_at_start_is_paragraph(self):
        self.assertEqual(block_to_block_type("Not a # heading"), BlockType.PARAGRAPH)

    # Code
    def test_code_block(self):
        block = "```\ndef hello():\n    print('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_with_markdown_inside(self):
        block = "```\n# not a heading\n- not a list\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_without_newline_after_opening_is_paragraph(self):
        self.assertEqual(block_to_block_type("```code```"), BlockType.PARAGRAPH)

    def test_code_without_closing_is_paragraph(self):
        self.assertEqual(block_to_block_type("```\nsome code"), BlockType.PARAGRAPH)

    # Quote
    def test_quote_with_space(self):
        block = "> This is a quote\n> on two lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_without_space(self):
        block = ">No space here\n>Or here"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_with_unmarked_line_is_paragraph(self):
        block = "> First line\nSecond line has no marker"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Unordered list
    def test_unordered_list(self):
        block = "- one\n- two\n- three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_single_item(self):
        self.assertEqual(block_to_block_type("- only item"), BlockType.UNORDERED_LIST)

    def test_unordered_list_missing_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("- one\n-two"), BlockType.PARAGRAPH)

    def test_unordered_list_with_unmarked_line_is_paragraph(self):
        self.assertEqual(block_to_block_type("- one\ntwo"), BlockType.PARAGRAPH)

    # Ordered list
    def test_ordered_list(self):
        block = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_double_digits(self):
        block = "\n".join(f"{i}. item" for i in range(1, 12))
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_not_starting_at_1_is_paragraph(self):
        self.assertEqual(block_to_block_type("2. two\n3. three"), BlockType.PARAGRAPH)

    def test_ordered_list_skipping_number_is_paragraph(self):
        self.assertEqual(block_to_block_type("1. one\n3. three"), BlockType.PARAGRAPH)

    def test_ordered_list_missing_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("1. one\n2.two"), BlockType.PARAGRAPH)

    # Paragraph
    def test_paragraph(self):
        block = "Just some text\nover two lines"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_with_inline_markdown(self):
        block = "Some **bold** and _italic_ and `code`"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
