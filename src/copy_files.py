import os
import shutil
from markdown import markdown_to_html_node

camino = "static"
def copy(dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)

    def rec(src=""):
        pato = os.path.join(camino, src)
        for dir in os.listdir(pato):
            dest_copy = os.path.join(dest, src, dir)
            source = os.path.join(pato, dir)
            if not os.path.isfile(source):
                os.mkdir(dest_copy)
                rec(os.path.join(src, dir))
            else:
                shutil.copy(source, dest_copy)
    
    rec()

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("no h1 header...")

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    result = template.replace("{{ Title }}", title)
    result = result.replace("{{ Content }}", html)
    result = result.replace('href="/', f'href="{base_path}')
    result = result.replace('src="/', f'src="{base_path}')
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(result)

def generate_pages_recursive(content_dir, template_path, public_dir, basepath):
    with open(template_path, "r") as f:
        template = f.read()

    def rec(src=""):
        pato = os.path.join(content_dir, src)
        for dir in os.listdir(pato):
            source = os.path.join(pato, dir)
            relative = os.path.join(src, dir)

            if not os.path.isfile(source):
                rec(relative)
                
            elif dir.endswith(".md"):
                with open(source, "r") as f:
                    markdown = f.read()

                html = markdown_to_html_node(markdown).to_html()
                title = extract_title(markdown)

                result = template.replace("{{ Title }}", title)
                result = result.replace("{{ Content }}", html)
                result = result.replace('href="/', f'href="{basepath}')
                result = result.replace('src="/', f'src="{basepath}')

                dest_path = os.path.join(public_dir, relative.replace(".md", ".html"))
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                with open(dest_path, "w") as f:
                    f.write(result)

                print(f"Generated: {dest_path}")

    rec()