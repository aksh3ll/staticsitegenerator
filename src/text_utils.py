from email.mime import image
import re
from pydoc import text
from blocknode import BlockType, block_to_block_type, RE_HEADER, RE_ORDERED_LIST
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case _:
            raise ValueError("Unknown TextType: " + str(text_node.text_type) + " for text: " + text_node.text)


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part:
                    result.append(TextNode(part, TextType.TEXT))
            else:
                if part:
                    result.append(TextNode(part, text_type))            
    return result

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\!\[([^]]+)\]\(([^)]+)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[([^]]+)\]\(([^)]+)\)", text)

def split_nodes_image(old_nodes) -> list[TextNode]:
    result = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if not images:
            result.append(node)
            continue
        text_remaining = node.text
        for image in images:
            parts = text_remaining.split(f"![{image[0]}]({image[1]})", 1)
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
            result.append(TextNode(image[0], TextType.IMAGE, url=image[1]))
            text_remaining = parts[1]
        if text_remaining:
            result.append(TextNode(text_remaining, TextType.TEXT))
    return result

def split_nodes_link(old_nodes) -> list[TextNode]:
    result = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            result.append(node)
            continue
        text_remaining = node.text
        for link in links:
            parts = text_remaining.split(f"[{link[0]}]({link[1]})", 1)
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
            result.append(TextNode(link[0], TextType.LINK, url=link[1]))
            text_remaining = parts[1]
        if text_remaining:
            result.append(TextNode(text_remaining, TextType.TEXT))
    return result

def text_to_textnodes(text: str) -> list[TextNode]:
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes

def markdown_to_blocks(markdown: str) -> list[str]:
    return [line.strip() for line in markdown.split("\n\n") if line.strip()]

def list_items_to_parent_node(list_items: list[str]) -> list[ParentNode]:
    return [ParentNode("li", [text_node_to_html_node(text_node) for text_node in text_to_textnodes(item)]) for item in list_items]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                header_match = RE_HEADER.match(block)
                if header_match:
                    level = len(header_match.group(1))
                    content = header_match.group(2)
                    html_nodes.append(LeafNode(f"h{level}", content))
            case BlockType.CODE:
                code_content = block[3:-3].strip()
                html_nodes.append(ParentNode("pre", [ParentNode("code", [text_node_to_html_node(TextNode(code_content, TextType.TEXT))])]))
            case BlockType.QUOTE:
                quote_content = block[1:].strip()
                html_nodes.append(LeafNode("blockquote",  quote_content))
            case BlockType.UNORDERED_LIST:
                list_items = [item.strip()[2:] for item in block.split("\n") if item.strip()]
                html_nodes.append(ParentNode("ul", list_items_to_parent_node(list_items)))
            case BlockType.ORDERED_LIST:
                list_items = [RE_ORDERED_LIST.match(item.strip()).group(2) for item in block.split("\n") if item.strip()]
                html_nodes.append(ParentNode("ol", list_items_to_parent_node(list_items)))
            case BlockType.PARAGRAPH:
                text_nodes = text_to_textnodes(block.replace("\n", " "))
                html_nodes.append(ParentNode("p", [text_node_to_html_node(tn) for tn in text_nodes]))
    return ParentNode("div", html_nodes)
