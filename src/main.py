from textnode import TextType, TextNode
from inline_parser import split_nodes_link


def main():
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )

    split_nodes_link([node])


if __name__ == "__main__":
    main()
