import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, ListProperty
from kivy.properties import BooleanProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
from kivy.clock import Clock
from kivy_garden.graph import Graph, LinePlot


class WindowManager(ScreenManager):
    pass

class MainScreenGraph(Graph):
    graph = Graph(xlabel='', ylabel='',
                  x_ticks_major=1, y_ticks_major=4,
                  y_grid_label=True, x_grid_label=True, padding=5,
                  x_grid=True, y_grid=True, xmin=1, xmax=5, ymin=32, ymax=44)
    plot = LinePlot(color=[0,1,0,1])
    plot.points = [(x,36) for x in range(100)]
    graph.add_plot(plot)

class LoginButtons(Widget):
    userField = ObjectProperty(None)
    passwordField = ObjectProperty(None)
    loginFailed = ObjectProperty(None)
    loginPassed = BooleanProperty(False)

    def loginButtonPress(self):
        username = self.userField.text.lower()
        password = self.passwordField.text

        if (username in GolfApp.userData):
            if (password == GolfApp.userData[username]["password"]):
                self.loginPassed = True
            else:
                self.loginFailedStart()
                Clock.schedule_once(self.loginFailedEnd, 3)
        else:
            self.loginFailedStart()
            Clock.schedule_once(self.loginFailedEnd, 3)

    def loginFailedStart(self):
        self.loginFailed.text = "Invalid Login"

    def loginFailedEnd(self, dt):
        self.loginFailed.text = ""

class LoginBackground(Widget):
    pass

class LoginScreen(Screen):
    pass



class CreateAccountButtons(Widget):
    userField = ObjectProperty(None)
    passwordField = ObjectProperty(None)
    confirmField = ObjectProperty(None)
    createFailed = ObjectProperty(None)

    def createButtonPress(self):
        username = self.userField.text.lower()
        password = self.passwordField.text
        confirm = self.confirmField.text

        if (username in GolfApp.userData):
            self.userFailStart()
        elif (password != confirm):
            self.passwordFailStart()
        else:
            GolfApp.userData[username] = {}
            GolfApp.userData[username]["password"] = password
            self.userField.text = ""
            self.passwordField.text = ""
            self.confirmField.text = ""
            return "LoginScreen"
        return "CreateAccountScreen"


    def userFailStart(self):
        self.createFailed.text = "Username Taken"
        Clock.schedule_once(self.failEnd,3)

    def passwordFailStart(self):
        self.createFailed.text = "Passwords Don't Match"
        Clock.schedule_once(self.failEnd,3)

    def failEnd(self,dt):
        self.createFailed.text = ""

class CreateAccountBackground(Screen):
    pass

class CreateAccountScreen(Screen):
    pass

class MainButtons(Widget):
    mainGraph = ObjectProperty(None)

    graph = Graph(xlabel='', ylabel='',
                  x_ticks_major=1, y_ticks_major=4,
                  y_grid_label=True, x_grid_label=True, padding=5,
                  x_grid=True, y_grid=True, xmin=1, xmax=5, ymin=32, ymax=44)

    def fill(self):
        self.mainGraph.xmin = 1
        self.mainGraph.xmax = 5
        self.mainGraph.ymin = 32
        self.mainGraph.ymax = 44
        self.mainGraph.x_ticks_major=1
        self.mainGraph.x_ticks_minor = 1
        self.mainGraph.y_ticks_major = 4
        self.mainGraph.y_ticks_minor = 4
        self.mainGraph.tick_color = [0, 0, 0, 1]
        self.mainGraph.y_label = True
        #self.mainGraph._y_grid_label = ListProperty([2])
        self.mainGraph.padding = 5
        self.mainGraph.font_color = [0,0,0,1]
        plot = LinePlot(color=[0, 138, 230, 1])
        plot.points = [(1, 36), (2, 37), (3, 33), (3, 40), (4, 36), (5, 34)]
        self.mainGraph.add_plot(plot)

class MainBackground(Widget):
    pass

class MainScreen(Screen):
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

    userData = {}
    users = open("Users.txt", "r")
    for user in users:
        data = user.split(",")
        userData[data[0].lower()]={}
        userData[data[0]]["password"] = data[1]
    users.close()


    def build(self):
        Window.size=(350,600)
        self.icon = "appIcon.png"
        self.title = "Rychlak International"
        return Builder.load_file("Style.kv")

if __name__=="__main__":
    GolfApp().run()