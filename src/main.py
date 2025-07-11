import os
import shutil
from page_generator import generate_pages_recursive


def main():
    copy_static_files()
    generate_pages_recursive("content", "template.html", "public")


def copy_static_files(src_dir="static", dest_dir="public"):
    # Step 1: Remove old public directory
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
        print(f"Deleted old '{dest_dir}' directory.")

    # Step 2: Recreate destination directory
    os.mkdir(dest_dir)

    # Step 3: Walk through source and copy
    def recursive_copy(src, dst):
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dst_path = os.path.join(dst, item)

            if os.path.isdir(src_path):
                os.mkdir(dst_path)
                recursive_copy(src_path, dst_path)
            else:
                shutil.copy(src_path, dst_path)
                print(f"Copied: {src_path} -> {dst_path}")

    recursive_copy(src_dir, dest_dir)


if __name__ == "__main__":
    main()
