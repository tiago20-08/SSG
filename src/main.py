from textnode import TextNode, TextType
from copy_files import copy, generate_pages_recursive

def main():

    copy("./public")

    generate_pages_recursive("content", "template.html", "public")



main()