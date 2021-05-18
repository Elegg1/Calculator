from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.config import Config
from calc_lexer import Lexer
from calc_parser import Parser
from calc_interpreter import Interpreter
from expression import Expression

class RootWidget(Widget):
    text = ObjectProperty(None)
    memory = None
    expr = Expression('0')
    def handle_button(self, instance):
        btn_text = instance.text
        if btn_text == 'C':
            self.text.text = '0'
            self.expr = Expression('0')
        elif btn_text == '<-':
            self.expr.del_sym()
            self.text.text = self.expr.text
        elif btn_text == '=':
            if (self.expr.is_valid()):
                lexer = Lexer(self.expr.text)
                toks = lexer.run()
                parser = Parser(toks)
                ast = parser.parse()
                interpreter = Interpreter()
                res = interpreter.visit(ast)
                self.expr = Expression(str(res))
                self.expr.cleanup()
                self.text.text = self.expr.text
        else:
            self.expr.add_sym(btn_text)
            self.text.text = self.expr.text


class CalculatorApp(App):
    def build(self):
        wid = RootWidget()
        wid.text.text = '0'
        return wid

if __name__ == '__main__':
    Config.set('graphics', 'resizable', False)
    Config.set('graphics', 'width', 500)
    Config.set('graphics', 'height', 700)
    CalculatorApp().run()