DIGITS = '0123456789'

class Token:
    def __init__(self, tok_type, val = None):
        self.type = tok_type
        self.val = val

    def __repr__(self):
        ret = self.type
        if self.val != None:
            ret = f'({ret}, {self.val})'
        return ret


TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MULTIPLY = 'MUL'
TT_DIVIDE = 'DIV'
TT_SQRT = 'SQRT'
TT_POWER = 'POW'
TT_LPARENTHESIS = 'LPAR'
TT_RPARENTHESIS = 'RPAR'
TT_NUMBER = 'NUM'
TT_EOF = 'EOF'


class Lexer:
    def __init__(self, text):
        self.text = text
        self.cur = None
        self.pos = -1
        self.tokens = []
        self.advance()

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.cur = None
        else:
            self.cur = self.text[self.pos]
    def run(self):
        tokens = []
        while self.cur != None:
            if self.cur == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.cur == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.cur == '*':
                tokens.append(Token(TT_MULTIPLY))
                self.advance()
            elif self.cur == '/':
                tokens.append(Token(TT_DIVIDE))
                self.advance()
            elif self.cur == '√':
                tokens.append(Token(TT_SQRT))
                self.advance()
            elif self.cur == '^':
                tokens.append(Token(TT_POWER))
                self.advance()
            elif self.cur == '(':
                tokens.append(Token(TT_LPARENTHESIS))
                self.advance()
            elif self.cur == ')':
                tokens.append(Token(TT_RPARENTHESIS))
                self.advance()
            elif self.cur in DIGITS:
                num_tok = self.make_number_token()
                tokens.append(num_tok)
        return tokens + [Token(TT_EOF)]

    def make_number_token(self):
        cur_str = ""
        dot = False
        while self.cur != None and self.cur in DIGITS+'.':
            cur_str += self.cur
            if self.cur == '.':
                dot = True
            self.advance()
        if dot:
            cur = float(cur_str)
        else:
            cur = int(cur_str)
        return Token(TT_NUMBER, cur)
