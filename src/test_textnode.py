import unittest
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_not_eq_link(self):
        node = TextNode("Next page", TextType.LINK, "https://www.abc.com")
        node2 = TextNode("Next page", TextType.LINK)
        self.assertNotEqual(node, node2)
    def test_eq_image(self):
        node = TextNode("Image 1", TextType.IMAGE, "../static/image1.jpg")
        node2 = TextNode("Image 1", TextType.IMAGE, "../static/image1.jpg")
        self.assertEqual(node, node2)
    def test_not_eq_code(self):
        node = TextNode("int x = 1", TextType.TEXT)
        node2 = TextNode("int x = 1", TextType.CODE)
        self.assertNotEqual(node, node2)

class Test_text_to_html(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Testing testing 123", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Testing testing 123")

    def test_link(self):
        node = TextNode("Click me for some free goods...", TextType.LINK, "https://www.shadyshit.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me for some free goods...")
        self.assertEqual(html_node.props, {"href":"https://www.shadyshit.com"})

    def test_image(self):
        node = TextNode("My obviously not AI generated photo", TextType.IMAGE, "../static/image2.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"../static/image2.jpg", "alt":"My obviously not AI generated photo"})

class Test_split_nodes_delimiter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_bold(self):
        bold_nodes = [
            TextNode("This text is so **bold**, we had to highlight it to show how **bold** it was.", TextType.TEXT),
            TextNode("Testing **bold text** 123", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(bold_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This text is so ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", we had to highlight it to show how ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" it was.", TextType.TEXT),
            TextNode("Testing ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" 123", TextType.TEXT)
            ])

    def test_split_beginning_and_end(self):
        nodes = [
            TextNode("_Safe driving_ is a very important skill to have in the modern times", TextType.TEXT),
            TextNode("A great man once said: _'All wahmen are queen, but if she breaths, she is a thot.'_", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("Safe driving", TextType.ITALIC),
            TextNode(" is a very important skill to have in the modern times", TextType.TEXT),
            TextNode("A great man once said: ", TextType.TEXT),
            TextNode("'All wahmen are queen, but if she breaths, she is a thot.'", TextType.ITALIC)
            ])

class Test_split_nodes_image_and_link(unittest.TestCase):
    def test_link(self):
        node = TextNode("Ahoy to [Google](https://www.google.com)", TextType.TEXT, )
        node2 = TextNode("No links spotted here", TextType.TEXT)
        node3 = TextNode("Don't click [here], I got no links for you", TextType.TEXT)
        self.assertEqual([TextNode("Ahoy to ", TextType.TEXT, None), TextNode("Google", TextType.LINK, "https://www.google.com"), TextNode("No links spotted here", TextType.TEXT, None), TextNode("Don't click [here], I got no links for you", TextType.TEXT, None)], split_nodes_link([node, node2, node3]))

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        print(new_nodes)
        self.assertEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes
            )

class Test_text_to_textnodes(unittest.TestCase):
    def test_regular_text_only(self):
        text = "This is just a regular text KEKL"
        self.assertEqual(text_to_textnodes(text), [TextNode("This is just a regular text KEKL", TextType.TEXT, None)])

    def test_bold_only(self):
        text = "Say something **feisty** here"
        self. assertEqual(text_to_textnodes(text), [
            TextNode("Say something ", TextType.TEXT, None),
            TextNode("feisty", TextType.BOLD, None),
            TextNode(" here", TextType.TEXT, None)
        ])

    def test_italic_link(self):
        text = "[Click here](https://www.shadysite6969.com) for some _tasty and succulent Italiano spaghetti_"
        self.assertEqual(text_to_textnodes(text), [
            TextNode("Click here", TextType.LINK, "https://www.shadysite6969.com"),
            TextNode(" for some ", TextType.TEXT, None),
            TextNode("tasty and succulent Italiano spaghetti", TextType.ITALIC, None)
        ])

    def test_bold_code_image(self):
        text = "`print('Hello World!')` is one of the **most commonly used code** in the coding industry. If you don't trust me, [click here](https://www.google.com) to ask Google instead."
        self.assertEqual(text_to_textnodes(text), [
            TextNode("print('Hello World!')", TextType.CODE, None),
            TextNode(" is one of the ", TextType.TEXT, None),
            TextNode("most commonly used code", TextType.BOLD, None),
            TextNode(" in the coding industry. If you don't trust me, ", TextType.TEXT, None),
            TextNode("click here", TextType.LINK, "https://www.google.com"),
            TextNode(" to ask Google instead.", TextType.TEXT, None)
        ])

    def test_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(text), [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
])

if __name__ == "__main__":
    unittest.main()
