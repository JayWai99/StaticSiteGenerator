import os, shutil, sys
from webpage import generate_page_recursive

def copy_static_to_public(src_dir, dst_dir):
    src_dir_name = src_dir.rsplit('/', 1)
    dst_dir_name = dst_dir.rsplit('/', 1)
    if os.path.exists(src_dir):
        dir_list = os.listdir(src_dir)
        for entry in dir_list:
            entry_path = os.path.join(src_dir, entry)
            if os.path.isfile(entry_path):
                print(f"Copying {entry} from {src_dir_name[1]} to {dst_dir_name[1]}...")
                shutil.copy(entry_path, dst_dir)
            elif os.path.isdir(entry_path):
                entry_dst_path = os.path.join(dst_dir, entry)
                print(f"Creating {entry} in {dst_dir_name[1]}...")
                os.mkdir(entry_dst_path)
                print(f"Copying contents in {entry}...")
                copy_static_to_public(entry_path, entry_dst_path)

def main():
    basepath = ""
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    # root_dir = os.getcwd()
    content_dir = os.path.join(basepath, "content")
    static_dir = os.path.join(basepath, "static")
    if os.path.exists(static_dir) == False:
        raise Exception("Static directory not detected, exiting.")
    doc_dir = os.path.join(basepath, "doc")
    if os.path.exists(doc_dir):
        print("Doc directory detected.\nWiping all contents to create a fresh environment...")
        shutil.rmtree(doc_dir)
        os.mkdir(doc_dir)
        print("Old content has been removed from directory.")
    else:
        print("Doc directory not detected.\nCreating a new directory...")
        os.mkdir(doc_dir)
        print("Directory has been created.")
    copy_static_to_public(static_dir, doc_dir)
    template_path = os.path.join(basepath, "template.html")
    generate_page_recursive(content_dir, template_path, doc_dir)
    print("All webpages have been successfully generated. Launching local server now.")

main()
