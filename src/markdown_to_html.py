from htmlnode import ParentNode, LeafNode
from inline_parser import text_to_textnodes
from conversions import text_node_to_html_node
from block_type import block_to_block_type, BlockType
from block_parser import markdown_to_blocks


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        # Special case: multiple heading lines in one block
        if block_type == BlockType.HEADING and "\n" in block:
            for line in block.splitlines():
                if not line.strip():
                    continue
                heading_level = line.count("#", 0, line.find(" "))
                text = line[heading_level + 1 :].strip()
                inline_nodes = text_to_textnodes(text)
                html_children = [text_node_to_html_node(n) for n in inline_nodes]
                children.append(ParentNode(f"h{heading_level}", html_children))
            continue

        if block_type == BlockType.PARAGRAPH:
            text = block.replace("\n", " ")
            inline_nodes = text_to_textnodes(text)
            html_children = [text_node_to_html_node(n) for n in inline_nodes]
            children.append(ParentNode("p", html_children))

        elif block_type == BlockType.HEADING:
            heading_level = block.count("#", 0, block.find(" "))
            text = block[heading_level + 1 :].strip()
            inline_nodes = text_to_textnodes(text)
            html_children = [text_node_to_html_node(n) for n in inline_nodes]
            children.append(ParentNode(f"h{heading_level}", html_children))

        elif block_type == BlockType.CODE:
            code_lines = block.splitlines()
            code = "\n".join(code_lines[1:-1]) + "\n"
            children.append(ParentNode("pre", [LeafNode("code", code)]))

        elif block_type == BlockType.QUOTE:
            quote_text = " ".join([line[1:].lstrip() for line in block.splitlines()])
            inline_nodes = text_to_textnodes(quote_text)
            html_children = [text_node_to_html_node(n) for n in inline_nodes]
            children.append(ParentNode("blockquote", html_children))

        elif block_type == BlockType.UNORDERED_LIST:
            li_nodes = []
            for item in block.splitlines():
                item_text = item[2:]  # Remove "- "
                inline_nodes = text_to_textnodes(item_text)
                html_children = [text_node_to_html_node(n) for n in inline_nodes]
                li_nodes.append(ParentNode("li", html_children))
            children.append(ParentNode("ul", li_nodes))

        elif block_type == BlockType.ORDERED_LIST:
            li_nodes = []
            for item in block.splitlines():
                _, item_text = item.split(". ", 1)
                inline_nodes = text_to_textnodes(item_text)
                html_children = [text_node_to_html_node(n) for n in inline_nodes]
                li_nodes.append(ParentNode("li", html_children))
            children.append(ParentNode("ol", li_nodes))

    return ParentNode("div", children)
