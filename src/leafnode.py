from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str | None, props: dict | None = None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        return str(self.value) if not self.tag else f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}> "
    
    def __repr__(self):
        return f'LeafNode(tag="{self.tag}", value="{self.value}", props={self.props})'
