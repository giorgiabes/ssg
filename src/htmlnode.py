class HTMLNode:
    """
    Represents a node in an HTML document tree.

    This class is the core building block for rendering HTML content in a structured way.
    Each node can represent:
    - A standard HTML tag (like <p>, <a>, <h1>, etc.)
    - Raw text content
    - A parent element that contains other child nodes

    Parameters:
        tag (str | None): The HTML tag name (e.g. "p", "a", "div"). If None, this node is treated as raw text.
        value (str | None): The text content of the node. If None, children are assumed to provide content.
        children (list[HTMLNode] | None): Child HTMLNode objects nested inside this node.
        props (dict[str, str] | None): HTML attributes for the tag (e.g. {"href": "https://example.com"}).

    Methods:
        to_html(): Must be implemented by subclasses to convert the node to HTML.
        props_to_html(): Converts the props dictionary to a string of HTML attributes.
        __repr__(): Returns a developer-friendly representation of the node for debugging.

    Examples:
        HTMLNode("a", "Click me", props={"href": "https://example.com"})
        → Represents: <a href="https://example.com">Click me</a>

        HTMLNode(None, "Just some raw text")
        → Represents raw text without any wrapping tag

    Rendering Behavior:
        - If tag is None: The node will render as raw text.
        - If value is None: The node is assumed to contain child nodes (children will be rendered).
        - If children is None or empty: The node is assumed to render its value.
        - If props is None or empty: The HTML tag will have no attributes.
    """

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list | None = None,
        props: dict | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError(
            "Child classes will override this method to render themselves as HTML."
        )

    def props_to_html(self):
        return "".join(f' {key}="{value}"' for key, value in self.props.items())

    def __repr__(self) -> str:
        return (
            f"HTMLNode(tag={self.tag!r}, "
            f"value={self.value!r}, "
            f"children={self.children!r}, "
            f"props={self.props!r})"
        )


class LeafNode(HTMLNode):
    """
    Represents a leaf HTML node — an HTML element that contains no children.

    This class is a specialized version of HTMLNode used to render HTML tags
    that contain only a value (text content) and optional attributes, but no child nodes.

    A LeafNode requires a `value` and optionally accepts a `tag` and `props`.
    It does not allow child nodes.

    Examples:
        LeafNode("p", "This is a paragraph.").to_html()
        => "<p>This is a paragraph.</p>"

        LeafNode("a", "Click me!", {"href": "https://example.com"}).to_html()
        => '<a href="https://example.com">Click me!</a>'

        LeafNode(None, "Just raw text").to_html()
        => "Just raw text"

    Rules:
    - The `value` is required and must be a non-empty string.
    - The `tag` can be None (in which case only the raw value is returned).
    - The `props` dictionary represents HTML attributes and is optional.
    - LeafNode does not accept or support child nodes.
    """

    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict | None = None,
    ) -> None:
        if not value:
            raise ValueError("All leaf nodes must have a non-empty value.")
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return (
            f"HTMLNode(tag={self.tag!r}, "
            f"value={self.value!r}, "
            f"props={self.props!r})"
        )

class ParentNode(HTMLNode):
    """
    Represents an HTML node that contains other nested HTML nodes as children.

    A ParentNode is a non-leaf HTML node used to build complex, nested HTML structures.
    It requires a tag (e.g. "div", "p") and a list of children, which can be LeafNodes
    or other ParentNodes. The `value` field is always None because ParentNodes render
    their children instead of holding direct text content.

    Example:
        node = ParentNode("p", [
            LeafNode("b", "Bold text"),
            LeafNode(None, "normal text"),
            LeafNode("i", "italic text"),
        ])

        node.to_html()  # Returns: "<p><b>Bold text</b>normal text<i>italic text</i></p>"

    Attributes:
        tag (str): The HTML tag name (e.g., "div", "ul").
        children (list): A list of HTMLNode instances to render within the parent tag.
        props (dict, optional): HTML attributes like class, id, etc.
    """
    def __init__(
        self,
        tag: str,
        children: list,
        props: dict | None = None,
    ) -> None:
        if not tag:
            raise ValueError("ParentNode requires a tag.")
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

