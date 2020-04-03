import kivy
from kivy.app import App
from kivy.uix.label import Label

class GolfApp(App):
    def build(self):
        return Label(text="This is a test")



if __name__=="__main__":
    GolfApp().run()