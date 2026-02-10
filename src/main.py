import logging
from documentutils import generate_pages_recursive
from textnode import TextNode, TextType
from copyutils import copy_static_files, clear_directory

logger = logging.getLogger(__name__)


def main():
    logger.info("Starting static site generation")
    clear_directory('./public')
    copy_static_files('./static', './public')
    generate_pages_recursive('./content', './template.html', './public')

if __name__ == "__main__":
    logging.basicConfig(filename='default.log', level=logging.INFO)
    main()
