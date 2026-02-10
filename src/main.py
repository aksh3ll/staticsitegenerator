import logging
import sys
from documentutils import generate_pages_recursive
from textnode import TextNode, TextType
from copyutils import copy_static_files, clear_directory

logger = logging.getLogger(__name__)

DESTINATION_DIR = './docs'


def main():
    logger.info("Starting static site generation")
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    clear_directory(DESTINATION_DIR)
    copy_static_files('./static', DESTINATION_DIR)
    generate_pages_recursive('./content', './template.html', DESTINATION_DIR, basepath)

if __name__ == "__main__":
    logging.basicConfig(filename='default.log', level=logging.INFO)
    main()
