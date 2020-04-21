import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory

from time import sleep

class WindowManager(ScreenManager):
    pass

class LoginButtons(Widget):
    pass

class LoginBackground(Widget):
    pass

class LoginScreen(Screen):
    pass

class CreateAccountButtons(Widget):
    pass

class CreateAccountBackground(Screen):
    pass

class CreateAccountScreen(Screen):
    pass



class GolfApp(App):
    def hexToKivyColor(Object, hex, alpha):
        values = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11,
                  'c': 12,
                  'd': 13, 'e': 14, 'f': 15}

        if hex[0] == '#':
            hex = hex[1:]

        decimalValueRed = (16 * values[hex[0]]) + (values[hex[1]])
        decimalValueGreen = (16 * values[hex[2]]) + (values[hex[3]])
        decimalValueBlue = (16 * values[hex[4]]) + (values[hex[5]])

        returnList = [decimalValueRed/255.0, decimalValueGreen/255.0, decimalValueBlue/255.0, alpha]

        return returnList

    def build(self):
        Window.size=(350,600)
        return Builder.load_file("Style.kv")

if __name__=="__main__":
    GolfApp().run()