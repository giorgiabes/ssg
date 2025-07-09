from textnode import TextNode, TextType
from markdown_extractor import extract_markdown_images, extract_markdown_links


def text_to_textnodes(text: str) -> list[TextNode]:
    """
    Convert a raw markdown string into a list of TextNode objects.
    Applies all the splitting functions to parse markdown inline syntax.
    """
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return [
        node
        for node in nodes
        if not (node.text == "" and node.text_type == TextType.TEXT)
    ]


def split_nodes_delimiter(
    old_node: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for node in old_node:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            count = node.text.count(delimiter)
            if count % 2 != 0:
                raise Exception("delimiter count is odd")
            lst = node.text.split(delimiter)
            for i in range(len(lst)):
                # Don't skip empty strings here — they are significant in Markdown
                if i % 2 == 0:
                    new_nodes.append(TextNode(lst[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(lst[i], text_type))
    return new_nodes


def split_nodes_image(old_node: list[TextNode]) -> list[TextNode]:
    final_list = []
    for node in old_node:
        if node.text_type != TextType.TEXT:
            final_list.append(node)
            continue
        text = node.text
        images = extract_markdown_images(text)
        if not images:
            final_list.append(node)
            continue
        remaining = text
        for alt, url in images:
            parts = remaining.split(f"![{alt}]({url})", 1)
            if parts[0]:
                final_list.append(TextNode(parts[0], TextType.TEXT))
            final_list.append(TextNode(alt, TextType.IMAGE, url))
            remaining = parts[1]
        if remaining:
            final_list.append(TextNode(remaining, TextType.TEXT))
    return final_list


def split_nodes_link(old_node: list[TextNode]) -> list[TextNode]:
    final_list = []
    for node in old_node:
        if node.text_type != TextType.TEXT:
            final_list.append(node)
            continue
        text = node.text
        links = extract_markdown_links(text)
        if not links:
            final_list.append(node)
            continue
        remaining = text
        for link_text, link_url in links:
            parts = remaining.split(f"[{link_text}]({link_url})", 1)
            if parts[0]:
                final_list.append(TextNode(parts[0], TextType.TEXT))
            final_list.append(TextNode(link_text, TextType.LINK, link_url))
            remaining = parts[1]
        if remaining:
            final_list.append(TextNode(remaining, TextType.TEXT))
    return final_list
