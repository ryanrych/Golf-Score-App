import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget

class Background(Widget):
    pass

class LoginButtons(Widget):
    pass

class LoginScreen(App):
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
        return Background()



if __name__=="__main__":
    LoginScreen().run()