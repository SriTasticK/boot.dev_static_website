from block_markdown import BlockType, markdown_to_blocks, block_to_block_type
from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


def markdown_to_html_node(markdown: str) -> ParentNode:
    children = [block_to_html_node(block) for block in markdown_to_blocks(markdown)]
    return ParentNode("div", children)


def block_to_html_node(block: str) -> HTMLNode:
    match block_to_block_type(block):
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case _:
            raise ValueError(f"Unknown block type for block: {block!r}")


def text_to_children(text: str) -> list[HTMLNode]:
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def paragraph_to_html_node(block: str) -> HTMLNode:
    # Lines inside a paragraph are joined with spaces, like a browser would
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))


def heading_to_html_node(block: str) -> HTMLNode:
    level = len(block) - len(block.lstrip("#"))
    text = block[level + 1:]
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block: str) -> HTMLNode:
    # Drop the opening "```\n" and closing "```"; the text is not parsed for inline markdown
    text = block[4:-3]
    code = text_node_to_html_node(TextNode(text, TextType.CODE))
    return ParentNode("pre", [code])


def quote_to_html_node(block: str) -> HTMLNode:
    lines = [line.lstrip(">").strip() for line in block.split("\n")]
    return ParentNode("blockquote", text_to_children(" ".join(lines)))


def unordered_list_to_html_node(block: str) -> HTMLNode:
    items = [ParentNode("li", text_to_children(line[2:])) for line in block.split("\n")]
    return ParentNode("ul", items)


def ordered_list_to_html_node(block: str) -> HTMLNode:
    items = [
        ParentNode("li", text_to_children(line.split(". ", 1)[1]))
        for line in block.split("\n")
    ]
    return ParentNode("ol", items)
