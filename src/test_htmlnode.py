import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "HTML sucks as always, so click here to try this instead", None, {"href": "https://www.how2markup.com", "target": "_blank"})
        html_out = ' href="https://www.how2markup.com" target="_blank"'
        self.assertEqual(node.props_to_html(), html_out)

    def test_props_to_html_empty(self):
        node = HTMLNode("p", "There is nothing here", None, None)
        html_out = ""
        self.assertEqual(node.props_to_html(), html_out) 

    def test_props_to_html_mismatch(self):
        node = HTMLNode("h1", "Something is wrong here", None, None)
        html_out = "https://www.youarewrong.com"
        self.assertNotEqual(node.props_to_html(), html_out)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Ahoy To Google!", {"href":"https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Ahoy To Google!</a>')

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Testing 123")
        self.assertNotEqual(node.to_html(), "<h2>Testing 123</h2>")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_children(self):
        child = []
        parent = ParentNode("p", child)
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_multiple_children(self):
        child = [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "Italic text"),
                    LeafNode(None, "Normal text"),
                ]
        parent = ParentNode("p", child,)
        self.assertEqual(parent.to_html(), "<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p>")



if __name__ == "__main__":
    unittest.main()
