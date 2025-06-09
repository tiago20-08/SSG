from textnode import *


class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        return " ".join(list(map(lambda prop: f'{prop}="{self.props[prop]}"',self.props)))

    def __repr__(self):
        print(f"tag = {self.tag}.\nvalue = {self.value}.\nchildren = {self.children}.\nprops = {self.props}.")



class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError
        
        if self.tag is None:
            return self.value
        
        if self.props is not None:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("no tag")
        if not self.children:
            raise ValueError("missing children value")
        
        children_html = "".join(child.to_html() for child in self.children)
        
        if self.props is not None:
            return f"<{self.tag} {self.props_to_html()}>{children_html}</{self.tag}>"
        else:
            return f"<{self.tag}>{children_html}</{self.tag}>"
        
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if not text_node.url:
                raise ValueError("no url")
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            if not text_node.url:
                raise ValueError("img no url")
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"tipo de texto inválido {text_node.text_type}")
            

