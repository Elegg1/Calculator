from calc_parser import NumberNode, UnOpNode, BinOpNode
from calc_lexer import TT_PLUS, TT_MINUS, TT_MULTIPLY, TT_DIVIDE, TT_SQRT, TT_POWER


class Interpreter:
    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)
    
    def no_visit_method(self, node):
        print(f"No method called visit_{type(node).__name__}")

    def visit_NumberNode(self, node):
        return node.val
    
    def visit_UnOpNode(self, node):
        op_tok = node.op_tok
        val = self.visit(node.node)
        if val=='NaN':
            return 'NaN'
        if op_tok.type == TT_MINUS:
            return -val
        if op_tok.type == TT_SQRT:
            if val < 0:
                return 'NaN'
            if val == 0:
                return 0
            return val ** 0.5
        
    def visit_BinOpNode(self, node):
        op_tok = node.op_tok
        left = self.visit(node.left)
        right = self.visit(node.right)
        if left == 'NaN' or right == 'NaN':
            return 'NaN'
        if op_tok.type == TT_PLUS:
            return left + right
        if op_tok.type == TT_MINUS:
            return left - right
        if op_tok.type == TT_MULTIPLY:
            return left * right
        if op_tok.type == TT_DIVIDE:
            if right == 0:
                return 'NaN'
            return left / right
        if op_tok.type == TT_POWER:
            if left <= 0:
                if isinstance(right, int):
                    if left == 0:
                        if right > 0:
                            return 0
                        return 'NaN'
                    if right % 2 == 0:
                        return (-left)**right
                    return -((-left)**right)
                return 'NaN'
            return left**right
