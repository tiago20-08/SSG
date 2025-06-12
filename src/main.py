from textnode import TextNode, TextType
from copy_files import copy, generate_pages_recursive
import sys

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    copy("docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)



main()