import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget

class Background(Widget):
    pass

class LoginButtons(Widget):
    pass

class LoginScreen(App):
    def build(self):
        Window.size=(350,600)
        return Background()



if __name__=="__main__":
    LoginScreen().run()