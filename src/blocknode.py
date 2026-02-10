import re
from enum import Enum

RE_HEADER = re.compile(r"^(#{1,6}) (.*)$", re.MULTILINE)
RE_ORDERED_LIST = re.compile(r"^(\d+)\. (.*)$", re.MULTILINE)

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    if RE_HEADER.match(block):
        return BlockType.HEADING
    elif block.startswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif RE_ORDERED_LIST.match(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
