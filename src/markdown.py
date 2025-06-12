from blocktype import *
from htmlnode import *
from splitnodes import text_to_textnodes

def markdown_to_blocks(markdown):
    parr = (markdown.split("\n\n"))
    blocks = []
    for line in parr:
        if line.strip() != "":
            blocks.append(line.strip())
    return blocks

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(t) for t in text_nodes]

def markdown_to_html_node(markdown):
    final = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)

        if block == "":
            continue

        if block_type == BlockType.PARAGRAPH:
            final.append(ParentNode("p", text_to_children(block.replace("\n", " "))))
        
        if block_type == BlockType.HEADING:
            num = 0
            while num<len(block) and block[num] == "#":
                num = num + 1
            text = block[num + 1:].strip()
            final.append(ParentNode(f"h{num}", text_to_children(text)))
        
        if block_type == BlockType.CODE:
            lines = block.split("\n")[1:-1]
            final.append(ParentNode("pre", [LeafNode("code", "\n".join(lines) + "\n")]))

        if block_type == BlockType.QUOTE:
            res = []
            lines = block.split("\n")
            for line in lines:
                res.append(line[1:].strip())
            text = " ".join(res)
            final.append(ParentNode("blockquote", text_to_children(text)))
        
        if block_type == BlockType.UNORDER:
            lines = block.split("\n")
            res = [ParentNode("li", text_to_children(line[2:].strip())) for line in lines]
            final.append(ParentNode("ul", res))
        
        if block_type == BlockType.ORDER:
            lines = block.split("\n")
            res = [ParentNode("li", text_to_children(line[2:].strip())) for line in lines]
            final.append(ParentNode("ol", res))
    
    return ParentNode("div", final)