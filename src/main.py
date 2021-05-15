from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.config import Config

class RootWidget(Widget):
    expression = ObjectProperty(None)


class CalculatorApp(App):
    def build(self):
        wid = RootWidget()
        wid.expression.text = "0"
        return wid

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', 500)
Config.set('graphics', 'height', 700)
CalculatorApp().run()