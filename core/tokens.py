from enum import Enum

class TokenType(Enum):
    NUMBER  = 'NUMBER'
    PLUS    = 'PLUS'
    MINUS   = 'MINUS'
    MUL     = 'MUL'
    DIV     = 'DIV'
    LPAREN  = 'LPAREN'
    RPAREN  = 'RPAREN'
    EOF     = 'EOF'

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"