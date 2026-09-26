from enum import Enum
from htmlnode import LeafNode
from regex import extract_markdown_images, extract_markdown_links

class TextType(Enum):
    TEXT = "plain text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other:TextNode):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter:str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        elif delimiter not in node.text:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 != 1:
                raise Exception("invalid Markdown syntax")
            else:
                temp = []
                for i in range(len(split_text)):
                    if i % 2 == 0 and split_text[i] != "":
                        temp.append(TextNode(split_text[i], TextType.TEXT))
                    elif i % 2 == 1 and split_text[i] != "":
                        temp.append(TextNode(split_text[i], text_type))
                new_nodes.extend(temp)
    return new_nodes

def split_recursive(text, delimiter_list: list[str], index: int, split_list: list[str|None]):
    if index >= len(delimiter_list):
        return split_list
    else:
        if delimiter_list[index] in text:
            temp = text.split(delimiter_list[index], 1)
            if temp[0] != "" and temp[1] != "" and index < len(delimiter_list) - 1:
                split_list.extend([{'str':temp[0], 'type': 'text'}, {'str': delimiter_list[index], 'type': 'non-text'}])
                return split_recursive(temp[1], delimiter_list, index + 1, split_list)
            elif temp[0] != "" and temp[1] != "" and index == len(delimiter_list) - 1:
                split_list.extend([{'str':temp[0], 'type':'text'}, {'str':delimiter_list[index], 'type':'non-text'}, {'str':temp[1], 'type':'text'}])
                return split_list
            elif temp[1] == "":
                split_list.extend([{'str': temp[0], 'type': 'text'}, {'str': delimiter_list[index], 'type': 'non-text'}])
                return split_list
            elif temp[0] == "":
                split_list.extend([{'str': delimiter_list[index], 'type': 'non-text'}, {'str': temp[1], 'type': 'text'}])
                return split_list
        else:
            split_list.append({'str': text, 'type': 'text'})
            return split_list
        

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    output = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        delimiter_list = []
        text_list = []
        temp = []
        if links == node.text:
            output.append(node)
        else:
            for link_tuple in links:
                delimiter_list.append(f"[{link_tuple[0]}]({link_tuple[1]})")

            temp.extend(split_recursive(node.text, delimiter_list, 0, text_list))
            for item in temp:
                if item['type'] == 'text':
                    output.append(TextNode(item['str'], TextType.TEXT,))
                else:
                    for link_tuple in links:
                        if link_tuple[1] in item['str']:
                            output.append(TextNode(link_tuple[0], TextType.LINK, link_tuple[1]))
    return output


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    output = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        delimiter_list = []
        text_list = []
        temp = []
        if images == node.text:
            output.append(node)
        else:
            for image_tuple in images:
                delimiter_list.append(f"![{image_tuple[0]}]({image_tuple[1]})")

            temp.extend(split_recursive(node.text, delimiter_list, 0, text_list))
            for item in temp:
                if item['type'] == 'text':
                    output.append(TextNode(item['str'], TextType.TEXT,))
                else:
                    for image_tuple in images:
                        if image_tuple[1] in item['str']:
                            output.append(TextNode(image_tuple[0], TextType.IMAGE, image_tuple[1]))
    return output


def text_to_textnodes(text):
    node = TextNode(text.strip(), TextType.TEXT,)
    delimiter_list = [
        {'deli':'**', 'type':TextType.BOLD},
        {'deli':'_', 'type':TextType.ITALIC},
        {'deli':'`', 'type':TextType.CODE}
    ]
    node_list = [node]
    for delimiter_dict in delimiter_list:
        node_list = split_nodes_delimiter(node_list, delimiter_dict['deli'], delimiter_dict['type']) 
    node_list = split_nodes_image(split_nodes_link(node_list))
    return node_list
