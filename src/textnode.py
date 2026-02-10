from enum import Enum
from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text (plain)"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "Links, in this format: [anchor text](url)"
    IMAGE = "Images, in this format: ![alt text](url)"


class TextNode:

    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
    
    def __repr__(self):
        return f'TextNode(text="{self.text}", text_type="{self.text_type.value}", url="{self.url}")'

