class HTMLNode():
    def __init__(self, tag :str|None =None, value :str|None =None, children :list[HTMLNode]|None =None, props :dict[str, str]|None =None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag == 'div':
            output = "<div>"
            output_end = "</div>"
            for node in self.children:
                output = output + node.to_html()
            output = output + output_end
            return output
        else:
            return "<div>Feature is not yet implemented</div>"

    def props_to_html(self):
        output = ""
        if self.props is None or self.props == {}:
            return ""
        for k in self.props:
            output = output + f' {k}="{self.props[k]}"'
        return output

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

class LeafNode(HTMLNode):
    def __init__(self, tag :str|None =None, value :str|None =None, props :dict[str,str]|None =None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if (self.value is None or self.value == "") and self.tag != 'img':
            raise ValueError("leaf node has no value")
        if self.tag is None or self.tag == "":
            return self.value
        output = f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        return output

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag :str, children :list[HTMLNode], props :dict[str,str]|None =None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError("parent node has no tag")
        if self.children is None or self.children == []:
            raise ValueError("parent node has no children")
        open_tag = f"<{self.tag}{self.props_to_html()}>"
        closed_tag = f"</{self.tag}>"
        output = open_tag
        for i in range(len(self.children)):
            output = output + self.children[i].to_html()
        output = output + closed_tag
        return output
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
