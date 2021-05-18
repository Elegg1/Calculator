from calc_lexer import Lexer
from calc_parser import Parser
"""
ops: + - * / √ ^
dot: .
num: full number
pars: lpar, rpar: (, )
"""


"""
DEPRECATED:                                                         //FIXES:
    0.if it is only 0 or NaN and sym is DIGIT or lpar or √ then sym replaces it
    1.number of rpars > lpars
    2.>=2 dots in num
    3.empty pars
    4.dot not in middle of num                                      //put 0 if dot in start of num, or in the end of num
    5.rpar after op
    6.lpar or √ after num or rpar                                   //insert * between
    7.num have leading 0 except one before dot
    8.num after rpar                                                //insert * between
    9.op(not √) after op
"""

DIGITS = '1234567890'


class Expression:
    def __init__(self, text):
        self.text = text
        self.update_vals()
    
    def update_vals(self):
        self.par_diff = self.count_par_diff()
        self.have_dot = self.last_num_have_dots()
        self.last_zero = self.is_last_num_zero()
        self.get_last()

    def get_last(self):
        ls = self.text[-1]
        if ls in ('+', '-', '*', '/', '√', '^'):
            self.last = 'op'
        elif ls == '.':
            self.last = 'dot'
        elif ls == '(':
            self.last = 'lpar'
        elif ls == ')':
            self.last = 'rpar'
        else:
            self.last = 'num'

    def count_par_diff(self):
        par_diff = 0
        for ch in self.text:
            if ch == '(':
                par_diff += 1
            if ch == ')':
                par_diff -= 1
        return par_diff
        
    def last_num_have_dots(self):
        for ch in reversed(self.text):
            if ch in DIGITS:
                continue
            if ch == '.':
                return True
            break
        return False
    
    def is_last_num_zero(self):
        return self.text[-1] == '0' and (len(self.text) == 1 or self.text[-2] not in DIGITS+'.')


    def cleanup(self):
        if self.text == 'NaN':
            return
        try:
            num = float(self.text)
            num = round(num, 12)
            strnum = str(num)
            if strnum.endswith('.0'):
                strnum = strnum[:-2]
            self.text = strnum
        except Exception as e:
            print(f"Trying to cleanup not a result: {e}")
    
    def add_sym(self, sym):
        # 0th rule
        if self.text == '0' and (sym in DIGITS or sym == '(' or sym == '√'):
            self.text = sym
            self.update_vals()
            return
        # if it is NaN, then just start new input, if can
        if self.text == 'NaN':
            if sym in DIGITS or sym == '(' or sym == '√':
                self.text = sym
                self.update_vals()
                return
            self.text = '0'
            self.update_vals()
            return
        # if last was dot, then we check 4th rule (dot in end of num)
        if self.last == 'dot':
            if sym not in DIGITS:
                self.text += '0'
                self.update_vals()
                return self.add_sym(sym)
            self.text += sym
            self.update_vals()
            return
        # if it is dot, then we check 2nd rule and 4th rule (dot in start of num)
        if sym == '.':
            # 4th rule
            if self.last != 'num':
                self.add_sym('0')
                if self.text[-1] == '0':
                    self.text += sym
                    self.update_vals()
                    return
                return
            # 2nd rule
            if self.have_dot:
                return
            self.text += sym
            self.update_vals()
            return
        # if it is rpar, then we check 1st rule, 3rd rule and 5th rule
        if sym == ')':
            # 1st rule
            if self.par_diff == 0:
                return
            # 3rd rule
            if self.last == 'lpar':
                return
            # 5th rule
            if self.last == 'op':
                return
            
            self.text += sym
            self.update_vals()
            return
        # if it is lpar, then we check 6th rule (lpar after num or rpar)
        if sym == '(':
            if self.last == 'num' or self.last == 'rpar':
                self.text += '*('
                self.update_vals()
                return
            self.text += sym
            self.update_vals()
            return
        # if it is op, then we check 6th (√ after num or rpar) and 9th rule
        if sym in ('+', '-', '*', '/', '√', '^'):
            # 6th rule
            if sym == '√':
                if self.last == 'num' or self.last == 'rpar':
                    self.text += '*√'
                    self.update_vals()
                    return
                self.text += sym
                self.update_vals()
                return
            # 9th rule
            if self.last == 'op':
                return
            self.text += sym
            self.update_vals()
            return
        # else it is digit, then we check 7th and 8th rule
        # 7th rule
        if self.last_zero:
            self.text = self.text[:-1] + sym
            self.update_vals()
            return
        # 8th rule
        if self.last == 'rpar':
            self.text += '*' + sym
            self.update_vals()
            return
        self.text += sym
        self.update_vals()
        return

    def del_sym(self):
        if self.text == 'NaN' or len(self.text) == 1:
            self.text = '0'
            self.update_vals()
            return
        self.text = self.text[:-1]
        self.update_vals()
        return

    def is_valid(self):
        try:
            Parser(Lexer(self.text).run()).parse()
            return True
        except Exception:
            return False
