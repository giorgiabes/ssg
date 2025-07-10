from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif re.match(r"^```[\s\S]*```$", block):
        return BlockType.CODE
    else:
        lines = block.splitlines()
        if lines and all(line.startswith(">") for line in lines):
            return BlockType.QUOTE
        elif lines and all(re.match(r"^- ", line) for line in lines):
            return BlockType.UNORDERED_LIST
        elif is_ordered_list_block(block):
            return BlockType.ORDERED_LIST
        else:
            return BlockType.PARAGRAPH


def is_ordered_list_block(block: str) -> bool:
    lines = block.strip().splitlines()
    if not lines:  # no lines means no ordered list
        return False
    for i, line in enumerate(lines):
        if not re.match(rf"^{i+1}\. ", line):
            return False
    return True
