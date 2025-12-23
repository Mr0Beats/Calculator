class Node:
    def evaluate(self):
        raise NotImplementedError

class NumberNode(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

    def __repr__(self):
        return f"{self.value}"

class BinOpNode(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def evaluate(self):
        left_val = self.left.evaluate()
        right_val = self.right.evaluate()

        if self.op.type.name == 'PLUS':
            return left_val + right_val
        elif self.op.type.name == 'MINUS':
            return left_val - right_val
        elif self.op.type.name == 'MUL':
            return left_val * right_val
        elif self.op.type.name == 'DIV':
            if right_val == 0:
                raise ZeroDivisionError("Division by zero")
            return left_val / right_val

    def __repr__(self):
        return f"({self.left} {self.op.type.name} {self.right})"

class UnaryOpNode(Node):
    def __init__(self, op, node):
        self.op = op
        self.node = node

    def evaluate(self):
        val = self.node.evaluate()
        if self.op.type.name == 'MINUS':
            return -val
        return val