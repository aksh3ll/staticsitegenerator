class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None,
                 children: list | None = None, props: dict | None=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self) -> str:
        raise NotImplementedError("to_html method not implemented for tag: " + str(self.tag) + " with value: " + str(self.value))
    
    def props_to_html(self) -> str:
        return ''.join([f' {key}="{value}"' for key, value in self.props.items()])
    
    def __eq__(self, other):
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
