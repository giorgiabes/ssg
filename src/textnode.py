from enum import Enum
from typing import Optional


class TextType(Enum):
    """Represents the type of inline text in a markdown document."""

    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    """
    Represents a piece of inline text with optional formatting and URL.

    This class is used to represent formatted text elements found inside Markdown or other markup languages.
    These elements include things like bold text, italic text, inline code, hyperlinks, and images.

    Attributes:
        text (str): The raw text content.
        text_type (TextType): The formatting type (e.g., plain text, bold, code, link, image).
        url (Optional[str]): Optional URL used for LINK or IMAGE nodes.

    Behavior:
        - If text_type is LINK or IMAGE, the `url` should be provided.
        - For all other text types, the `url` is typically None.
        - Two TextNode instances are equal (`==`) if all three fields match: `text`, `text_type`, and `url`.

    Examples:
        TextNode("OpenAI", TextType.LINK, "https://openai.com")
        → Represents a hyperlink.

        TextNode("**bold**", TextType.BOLD)
        → Represents bolded text.

    Methods:
        __eq__(other): Checks equality based on text, type, and URL.
        __repr__(): Developer-friendly string representation of the node.
    """

    def __init__(
        self, text: str, text_type: TextType, url: Optional[str] = None
    ) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return NotImplemented
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return (
            f"TextNode(text={self.text!r}, "
            f"text_type={self.text_type.value!r}, "
            f"url={self.url!r})"
        )
