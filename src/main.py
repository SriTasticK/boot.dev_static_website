from copystatic import copy_directory
from gencontent import generate_pages_recursive

STATIC_DIR = "./static"
PUBLIC_DIR = "./public"
CONTENT_DIR = "./content"
TEMPLATE_PATH = "./template.html"

def main():
    copy_directory(STATIC_DIR, PUBLIC_DIR)
    generate_pages_recursive(CONTENT_DIR, TEMPLATE_PATH, PUBLIC_DIR)

if __name__ == "__main__":
    main()
