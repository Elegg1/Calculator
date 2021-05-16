from calc_lexer import TT_PLUS, TT_MINUS, TT_MULTIPLY, TT_DIVIDE, TT_SQRT, TT_POWER, TT_LPARENTHESIS, TT_RPARENTHESIS, TT_NUMBER, TT_EOF

"""
atom:    NUM
         LPAR expr RPAR
         SQRT atom
         MINUS atom

factor:  atom [POW atom] //Right-associative

term:    factor [MUL|DIV factor]

expr:    term [PLUS|MINUS term]
"""

class NumberNode:
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return f'(NUM: {self.val})'

class BinOpNode:
    def __init__(self, left, right, op_tok):
        self.left = left
        self.right = right
        self.op_tok = op_tok
    
    def __repr__(self):
        return f'({self.left}, {self.op_tok}, {self.right})'

class UnOpNode:
    def __init__(self, node, op_tok):
        self.node = node
        self.op_tok = op_tok
    
    def __repr__(self):
        return f'({self.op_tok}, {self.node})'

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.cur = None
        self.advance()

    def parse(self):
        res = self.expr()
        if self.cur.type == TT_EOF:
            return res
        raise Exception("Unexpected token")

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.tokens):
            self.cur = None
            return
        self.cur = self.tokens[self.pos]
    

    def atom(self):
        if self.cur.type == TT_NUMBER:
            res = NumberNode(self.cur.val)
            self.advance()
            return res
        elif self.cur.type == TT_LPARENTHESIS:
            self.advance()
            res = self.expr()
            if self.cur.type == TT_RPARENTHESIS:
                self.advance()
                return res
        elif self.cur.type == TT_SQRT or self.cur.type == TT_MINUS:
            return self.make_un_op_node()
        raise Exception("Unexpected EOF")

    def factor(self):
        return self.make_bin_op_node([TT_POWER], self.atom, True)
    
    def term(self):
        return self.make_bin_op_node([TT_MULTIPLY, TT_DIVIDE], self.factor)

    def expr(self):
        return self.make_bin_op_node([TT_PLUS, TT_MINUS], self.term)

    def make_bin_op_node(self, ops, func, right = False):
        if right:
            nodes = []
            opers = []
            node = func()
            nodes.append(node)
            while self.cur.type in ops:
                opers.append(self.cur)
                self.advance()
                node = func()
                nodes.append(node)
            res = nodes.pop()
            while len(opers) > 0:
                op = opers.pop()
                left = nodes.pop()
                res = BinOpNode(left, res, op)
            return res
        node = func()
        while self.cur.type in ops:
            op = self.cur
            self.advance()
            rnode = func()
            node = BinOpNode(node, rnode, op)
        return node
            
    def make_un_op_node(self):
        op = self.cur
        self.advance()
        node = self.atom()
        return UnOpNode(node, op)
            

