import unittest
from gencontent import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_strips_whitespace(self):
        self.assertEqual(extract_title("#    Hello world   "), "Hello world")

    def test_h1_not_on_first_line(self):
        md = """
Some intro text

# The Title

More text
"""
        self.assertEqual(extract_title(md), "The Title")

    def test_ignores_h2_before_h1(self):
        md = "## Subheading\n\n# Real Title"
        self.assertEqual(extract_title(md), "Real Title")

    def test_first_h1_wins(self):
        self.assertEqual(extract_title("# First\n\n# Second"), "First")

    def test_no_h1_raises(self):
        with self.assertRaises(ValueError):
            extract_title("## Only an h2\n\nAnd a paragraph")

    def test_hash_without_space_raises(self):
        with self.assertRaises(ValueError):
            extract_title("#NotATitle")

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            extract_title("")

if __name__ == "__main__":
    unittest.main()
