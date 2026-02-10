import unittest

from documentutils import extract_title


class TestDocumentUtils(unittest.TestCase):

    def test_title_extraction(self):
        markdown = """# Title
This is some content."""
        title = extract_title(markdown)
        self.assertEqual(title, "Title")

    def test_no_title(self):
        markdown = """This is some content without a title."""
        with self.assertRaises(ValueError):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
