import sys

from copystatic import copy_directory
from gencontent import generate_pages_recursive

STATIC_DIR = "./static"
OUTPUT_DIR = "./docs"
CONTENT_DIR = "./content"
TEMPLATE_PATH = "./template.html"

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_directory(STATIC_DIR, OUTPUT_DIR)
    generate_pages_recursive(CONTENT_DIR, TEMPLATE_PATH, OUTPUT_DIR, basepath)

if __name__ == "__main__":
    main()
