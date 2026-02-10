import os
from text_utils import markdown_to_html_node


def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No title found in markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} using template {template_path} to {dest_path}")
    with open(from_path, 'r') as f:
        content = f.read()

    with open(template_path, 'r') as f:
        template = f.read()

    title = extract_title(content)
    content_node = markdown_to_html_node(content)
    content_html = content_node.to_html()

    page_content = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)
    with open(dest_path, 'w') as f:
        f.write(page_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path) -> None:
    for entry in os.scandir(dir_path_content):
        if entry.is_file() and entry.name.endswith(".md"):
            dest_path = os.path.join(dest_dir_path, entry.name[:-3] + ".html")
            generate_page(entry.path, template_path, dest_path)
        elif entry.is_dir():
            new_dest_dir = os.path.join(dest_dir_path, entry.name)
            os.makedirs(new_dest_dir, exist_ok=True)
            generate_pages_recursive(entry.path, template_path, new_dest_dir)
