from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDER = "unorder"
    ORDER = "order"


def block_to_block_type(block):
    lines = block.split("\n")

    if lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE

    if len(lines) == 1:
        line = lines[0]
        if line.startswith("#"):
            i = 0
            while i < len(line) and line[i] == "#":
                i += 1
            if 1 <= i <= 6 and i < len(line) and line[i] == " ":
                return BlockType.HEADING

    isQuote = True
    print(lines)
    for line in lines:
        if not line.startswith(">"):
            isQuote = False
    if isQuote:
        return BlockType.QUOTE
    
    unorder = True
    for line in lines:
        if not line.startswith("- "):
            unorder = False
    if unorder:
        return BlockType.UNORDER

    expected = 1
    order = True
    for line in lines:
        dot_index = line.find(". ")
        if dot_index == -1:
            order = False
        number_str = line[:dot_index]
        if not number_str.isdigit() or int(number_str) != expected:
            order = False
        expected += 1
    if order:
        return BlockType.ORDER

    return BlockType.PARAGRAPH