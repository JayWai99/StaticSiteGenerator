from blocks import markdown_to_html_node
import os

def extract_title(markdown):
    with open(markdown, 'r') as file:
        md_text = file.read()
        md_lines = md_text.split("\n")
        for line in md_lines:
            if line[:2] == "# ":
                return line[2:].strip()
        raise Exception("No h1 header found")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_text = ""
    template_text = ""
    with open(from_path, 'r') as file:
        md = file.read()
        md_text = md_text + md
    with open(template_path, 'r') as file:
        template = file.read()
        template_text = template_text + template
    node = markdown_to_html_node(md_text)
    html = node.to_html()
    title = extract_title(from_path)
    if "{{ Title }}" in template_text:
        template_text = template_text.replace("{{ Title }}", title)
    if "{{ Content }}" in template_text:
        template_text = template_text.replace("{{ Content }}", html)
    if 'href="/' in template_text:
        template_text = template_text.replace('href="/', f'href="{basepath}')
    if 'src="/' in template_text:
        template_text = template_text.replace('src="/', f'src="{basepath}')
    with open(dest_path, 'w', encoding="utf-8") as file:
        # for line in template_lines:
        file.write(template_text)
    print("Webpage generation is complete. Launching local server now.")


def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    md_text = ""
    template_text = ""
    if os.path.exists(dir_path_content) == False:
        raise Exception("Content directory does not exist. Exiting...")
    elif os.path.exists(template_path) == False:
        raise Exception("Template file does not exist. Exiting...")
    elif os.path.exists(dest_dir_path) == False:
        print(f"{dest_dir_path} was not found. Making a new directory now...")
        os.mkdir(dest_dir_path)
    print(f"Reading data from {template_path}...")
    with open(template_path, 'r') as file:
        template = file.read()
        template_text = template_text + template
    dir_list = os.listdir(dir_path_content)
    if not dir_list:
        raise Exception(f"{dir_path_content} is empty. Exiting...")
    for item in dir_list:
        dir_text = os.path.splitext(item)
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path) and dir_text[1] == ".md":
            print("Generating webpage for current directory...")
            with open(item_path, 'r') as file:
                md = file.read()
                md_text = md_text + md
            node = markdown_to_html_node(md_text)
            html = node.to_html()
            title = extract_title(item_path)
            if "{{ Title }}" in template_text:
                template_text = template_text.replace("{{ Title }}", title)
            if "{{ Content }}" in template_text:
                template_text = template_text.replace("{{ Content }}", html)
            if 'href="/' in template_text:
                template_text = template_text.replace('href="/', f'href="{basepath}')
            if 'src="/' in template_text:
                template_text = template_text.replace('src="/', f'src="{basepath}')
            html_dir = os.path.join(dest_dir_path, "index.html")
            with open(html_dir, 'w', encoding="utf-8") as file:
                file.write(template_text)
            print(f"Webpage for {item} has been succesfully generated.")
        if os.path.isdir(item_path):
            new_dest_dir_path = os.path.join(dest_dir_path, item)
            new_cont_dir_path = os.path.join(dir_path_content, item)
            os.mkdir(new_dest_dir_path)
            generate_page_recursive(new_cont_dir_path, template_path, new_dest_dir_path, basepath)
