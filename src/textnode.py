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
    """Represents a piece of inline text with optional formatting and URL."""

    def __init__(self, text: str, text_type: TextType, url: Optional[str] = None):
        """
        Initialize a TextNode.

        Args:
            text (str): The actual text content.
            text_type (TextType): The formatting type of the text.
            url (Optional[str]): Optional URL (used for links or images).
        """
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
