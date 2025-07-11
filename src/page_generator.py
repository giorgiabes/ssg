import os
from markdown_to_html import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        md = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    content_html = markdown_to_html_node(md).to_html()
    title = extract_title(md)

    result = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", content_html
    )

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(result)


def extract_title(markdown: str) -> str:
    """
    This function returns the text of the first line that
    starts with a single #.
    """
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No H1 title found in markdown.")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isdir(entry_path):
            generate_pages_recursive(entry_path, template_path, dest_path)

        elif entry.endswith(".md"):
            output_file_path = os.path.join(dest_dir_path, "index.html")
            generate_page(entry_path, template_path, output_file_path)
