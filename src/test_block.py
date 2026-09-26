import unittest
from blocks import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node

class Test_markdown_to_blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class Test_blocks(unittest.TestCase):
    def test_block_headings(self):
        text = "### This is heading 3"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_block_code(self):
        text = """```
print('Hello World!')
```"""
        self.assertEqual(block_to_block_type(text), BlockType.CODE)

    def test_block_quote(self):
        text = "> Flat is justice. It just is."
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)

    def test_block_unordered_list(self):
        text = "- This is line 1. \n- This is line 2. \n- This is line 3."
        self.assertEqual(block_to_block_type(text), BlockType.UNORDEREDLIST)

    def test_block_ordered_list(self):
        text = "1. This is line 1. \n2. This is line 2. \n3. This is line 3."
        self.assertEqual(block_to_block_type(text), BlockType.ORDEREDLIST)

    def test_block_paragraph(self):
        text = "This is just a regular paragraph KEKL"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

class Test_markdown_to_html(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print("output: " + html)
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
### This is heading 3

I will throw in a paragraph for **free**, _don't be shy_.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is heading 3</h3><p>I will throw in a paragraph for <b>free</b>, <i>don't be shy</i>.</p></div>"
        )

    def test_quote(self):
        md = """
> Premature optimisation is the root of all evil

I dunno, apparently said by some guy who prematurely optimise the code structure of their code base.

Here's a hello world for free:

```
print('Hello World!')
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Premature optimisation is the root of all evil</blockquote><p>I dunno, apparently said by some guy who prematurely optimise the code structure of their code base.</p><p>Here's a hello world for free:</p><pre><code>print('Hello World!')\n</code></pre></div>"
        )

    def test_lists(self):
        md = """
## The Legendary Laundry List

- The
- Legendary

1. Laundry
2. List
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>The Legendary Laundry List</h2><ul><li>The</li><li>Legendary</li></ul><ol><li>Laundry</li><li>List</li></ol></div>"
        )

if __name__ == "main.py":
    main()
