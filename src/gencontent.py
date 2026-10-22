import os

from markdown_to_html import markdown_to_html_node


def extract_title(markdown: str) -> str:
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No h1 header found in markdown")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(page)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    for name in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, name)
        if os.path.isfile(source_path):
            if not name.endswith(".md"):
                continue
            dest_name = name[:-len(".md")] + ".html"
            generate_page(source_path, template_path, os.path.join(dest_dir_path, dest_name))
        else:
            generate_pages_recursive(source_path, template_path, os.path.join(dest_dir_path, name))
