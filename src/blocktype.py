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

    if lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    if len(lines) == 1:
        line = lines[0]
        if line.startswith("#"):
            i = 0
            while i < len(line) and line[i] == "#":
                i += 1
            if 1 <= i <= 6 and i < len(line) and line[i] == " ":
                return BlockType.HEADING

    for line in lines:
        if not line.startswith(">"):
            break
    else:
        return BlockType.QUOTE

    for line in lines:
        if not line.startswith("- "):
            break
    else:
        return BlockType.UNORDER

    expected = 1
    for line in lines:
        dot_index = line.find(". ")
        if dot_index == -1:
            break
        number_str = line[:dot_index]
        if not number_str.isdigit() or int(number_str) != expected:
            break
        expected += 1
    else:
        return BlockType.ORDER

    return BlockType.PARAGRAPH