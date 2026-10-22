import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        parts = old_node.text.split(delimiter)
        # An even number of parts means a delimiter was opened but never closed
        if len(parts) % 2 == 0:
            raise ValueError(
                f"Invalid Markdown: unmatched '{delimiter}' in text: {old_node.text!r}"
            )

        split_nodes = []
        for i, part in enumerate(parts):
            if part == "":
                continue
            # Odd-indexed parts sit between a pair of delimiters
            if i % 2 == 0:
                split_nodes.append(TextNode(part, TextType.TEXT))
            else:
                split_nodes.append(TextNode(part, text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


IMAGE_PATTERN = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
# The lookbehind skips image syntax, which also contains [text](url)
LINK_PATTERN = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(IMAGE_PATTERN, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(LINK_PATTERN, text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_pattern(old_nodes, IMAGE_PATTERN, TextType.IMAGE)


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_pattern(old_nodes, LINK_PATTERN, TextType.LINK)


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    # Code goes first so markdown inside backticks stays literal; images and
    # links go before bold/italic so underscores in URLs aren't read as italics
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    return nodes


def _split_nodes_pattern(old_nodes: list[TextNode], pattern: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        # Use match positions rather than str.split so that a link's markdown
        # can't accidentally match inside an identical-looking image
        last_end = 0
        for match in re.finditer(pattern, text):
            before = text[last_end:match.start()]
            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(match.group(1), text_type, match.group(2)))
            last_end = match.end()

        remaining = text[last_end:]
        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes
