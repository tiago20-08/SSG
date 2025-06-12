from textnode import TextNode, TextType
from extract import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        new = []
        text = node.text.split(delimiter)

        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        if len(text) % 2 == 0:
            raise Exception("matching closing delimeter not found")
        for i in range(len(text)):
            if i % 2 != 0:
                new.append(TextNode(text[i], text_type))
            else:
                new.append(TextNode(text[i],node.text_type))
        new_nodes.extend(new)
      
    return new_nodes

def split_nodes_image(old_node):
    new_nodes = []

    for node in old_node:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        if node.text == "":
            continue

        restante = node.text
        image =  extract_markdown_images(restante)

        if not image:
            new_nodes.append(node)
            continue
        else:
            for pair in image:
                text = restante.split(f"![{pair[0]}]({pair[1]})", 1)
                if text[0] != "":
                    new_nodes.append(TextNode(text[0],TextType.TEXT))
                new_nodes.append(TextNode(f"{pair[0]}",TextType.IMAGE,pair[1]))
                restante = text[1]

        if restante:
            new_nodes.append(TextNode(restante, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_node):
    new_nodes = []
    for node in old_node:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text == "":
            continue

        restante = node.text
        link =  extract_markdown_links(restante)   

        if not link:
            new_nodes.append(node)
            continue
        else:
            for pair in link:
                text = restante.split(f"[{pair[0]}]({pair[1]})", 1)
                if text[0] != "":
                    new_nodes.append(TextNode(text[0], TextType.TEXT))
                new_nodes.append(TextNode(f"{pair[0]}", TextType.LINK, pair[1]))
                restante = text[1]

        if restante:
            new_nodes.append(TextNode(restante, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    node = [TextNode(text, TextType.TEXT)]
    node = split_nodes_image(node)
    node = split_nodes_link(node)
    node = split_nodes_delimiter(node, "**", TextType.BOLD)
    node = split_nodes_delimiter(node, "_", TextType.ITALIC)
    node = split_nodes_delimiter(node, '`', TextType.CODE)
    return node