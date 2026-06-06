from enum import Enum, auto

class TextType(Enum):
    PLAIN = auto()
    BOLD = auto()
    ITALIC = auto()
    CODE = auto()
    LINK = auto()
    IMAGE = auto()

class TextNode():
    
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        
        return (
            self.text_type == other.text_type and
            self.url == other.url and
            self.text == other.text
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
