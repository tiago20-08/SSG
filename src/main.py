from textnode import TextNode, TextType

def main():
    node = TextNode("ejemplo de onda", TextType.LINK, "www.boot.dev")
    print(node)

main()