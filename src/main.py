from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.config import Config
from calc_lexer import Lexer
from calc_parser import Parser
from calc_interpreter import Interpreter

class RootWidget(Widget):
    expression = ObjectProperty(None)
    memory = None
    def handle_button(self, instance):
        btn_text = instance.text
        if btn_text == 'C':
            self.expression.text = '0'
        elif btn_text == '<-':
            pass
        elif btn_text == '=':
            txt = self.expression.text
            try:
                res = Interpreter().visit(Parser(Lexer(txt).run()).parse())
                self.expression.text = str(res)
            except Exception as e:
                print(f'Error: {e}')
        else:
            self.expression.text += btn_text


class CalculatorApp(App):
    def build(self):
        wid = RootWidget()
        wid.expression.text = '0'
        return wid

if __name__ == '__main__':
    Config.set('graphics', 'resizable', False)
    Config.set('graphics', 'width', 500)
    Config.set('graphics', 'height', 700)
    CalculatorApp().run()