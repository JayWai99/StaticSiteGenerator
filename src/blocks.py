from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node, text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDEREDLIST = "unordered_list"
    ORDEREDLIST = "ordered_list"


def markdown_to_blocks(markdown :str):
    temp = markdown.split("\n\n")
    output = []
    for line in temp:
        if line != "\n" and line != "":
            output.append(line.strip())
    return output

def block_to_block_type(block):
    if "# " in block[:7]:
        return BlockType.HEADING
    elif "```\n" == block[:4] and "```" == block[-3:]:
        return BlockType.CODE
    elif "> " in block[0:2]: 
        return BlockType.QUOTE
    elif "- " == block[:2]:
        return BlockType.UNORDEREDLIST
    lines = block.split("\n")
    for i in range(len(lines)):
        if lines[i][:3] == f"{i+1}. ":
            return BlockType.ORDEREDLIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                counter = 0
                for letter in block:
                    if letter == "#":
                        counter += 1
                heading_text = block.split(" ", 1)
                nodes = text_to_textnodes(heading_text[1])
                leaf_nodes = []
                for node in nodes:
                    leaf_nodes.append(text_node_to_html_node(node))
                p_node = ParentNode(f"h{counter}", leaf_nodes)
                block_nodes.append(p_node)
            case BlockType.ORDEREDLIST:
                ol_items = block.split('\n')
                item_nodes = []
                ol_nodes = []
                for ol_item in ol_items:
                    ol_text = ol_item.split(" ", 1)
                    text_nodes = text_to_textnodes(ol_text[1])
                    nodes_list = []
                    for node in text_nodes:
                        if node.text_type != 'image' and node.text == "":
                            continue
                        else:
                            nodes_list.append(node)
                    item_nodes.append(nodes_list)
                for item in item_nodes:
                    leaf_nodes = []
                    for node in item:
                        leaf_nodes.append(text_node_to_html_node(node))
                    p_node = ParentNode("li", leaf_nodes)
                    ol_nodes.append(p_node)
                gp_node = ParentNode("ol", ol_nodes)
                block_nodes.append(gp_node)
            case BlockType.UNORDEREDLIST:
                ul_items = block.split('\n')
                item_nodes = []
                ul_nodes = []
                for ul_item in ul_items:
                    ul_text = ul_item.split(" ", 1)
                    text_nodes = text_to_textnodes(ul_text[1])
                    nodes_list = []
                    for node in text_nodes:
                        if node.text_type != 'image' and node.text == "":
                            continue
                        else:
                            nodes_list.append(node)
                    item_nodes.append(nodes_list)
                for item in item_nodes:
                    leaf_nodes = []
                    for node in item:
                        leaf_nodes.append(text_node_to_html_node(node))
                    p_node = ParentNode("li", leaf_nodes)
                    ul_nodes.append(p_node)
                gp_node = ParentNode("ul", ul_nodes)
                block_nodes.append(gp_node)
            case BlockType.CODE:
                code_raw_text = block[4:-3]
                code_processed_text = ""
                for letter in code_raw_text:
                    if letter != "\n":
                        code_processed_text = code_processed_text + letter
                    else:
                        code_processed_text = code_processed_text + "\n"
                if code_processed_text[-1] != "\n":
                    code_processed_text = code_processed_text + "\n"
                code_node = TextNode(code_processed_text, TextType.CODE, )
                p_node = ParentNode("pre", [text_node_to_html_node(code_node)], )
                block_nodes.append(p_node)
            case BlockType.QUOTE:
                quote_text = block.split(" ", 1)
                nodes = text_to_textnodes(quote_text[1])
                leaf_nodes = []
                for node in nodes:
                    leaf_nodes.append(text_node_to_html_node(node))
                p_node = ParentNode("blockquote", leaf_nodes, )
                block_nodes.append(p_node)
            case BlockType.PARAGRAPH:
                text = block.replace("\n", " ")
                nodes = text_to_textnodes(text)
                leaf_nodes = []
                for node in nodes:
                    if node.text_type != 'image' and node.text == "":
                        continue
                    else:
                        leaf_nodes.append(text_node_to_html_node(node))
                p_node = ParentNode("p", leaf_nodes, ) 
                block_nodes.append(p_node)
    output = HTMLNode("div", None, block_nodes, None)
    return output
