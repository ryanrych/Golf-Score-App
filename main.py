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

from math import ceil

userData = {}
currUser = ""

class WindowManager(ScreenManager):
    pass

class LoginButtons(Widget):
    global currUser
    global userData

    userField = ObjectProperty(None)
    passwordField = ObjectProperty(None)
    loginFailed = ObjectProperty(None)
    loginPassed = BooleanProperty(False)

    def loginButtonPress(self):
        username = self.userField.text.lower()
        password = self.passwordField.text

        if (username in userData):
            if (password == userData[username]["password"]):
                self.loginPassed = True
                currUser = username
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

        if (username in userData):
            self.userFailStart()
        elif (password != confirm):
            self.passwordFailStart()
        else:
            userData[username] = {}
            userData[username]["password"] = password
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
    global currUser
    global userData

    mainGraph = ObjectProperty(None)

    def graphButtons(self, amount):
        self.mainGraph.tick_color = [0, 0, 0, 1]
        self.mainGraph._y_grid_label = range(100)
        self.mainGraph.padding = 5
        self.mainGraph.font_color = [0, 0, 0, 1]

        plot = LinePlot(color = [1,0,1,1])
        if (amount == 1):
            scores = userData[currUser]["scores"][-5:]
            points = scores
            self.mainGraph.xmin = 0
            self.mainGraph.xmax = 6
            self.mainGraph.x_ticks_major = 1
            r = max(scores) - min(scores)
            yTicks = ceil(r / 5)
            if (yTicks == 0): yTicks = 1
            self.mainGraph.ymin = min(scores) - yTicks
            self.mainGraph.ymax = max(scores) + yTicks
            self.mainGraph.y_ticks_major = yTicks

        elif (amount == 2):
            scores = userData[currUser]["scores"][-10:]
            points = scores
            self.mainGraph.xmin = 0
            self.mainGraph.xmax = 11
            self.mainGraph.x_ticks_major = 1
            r = max(scores) - min(scores)
            yTicks = ceil(r / 10)
            if (yTicks == 0): yTicks = 1
            self.mainGraph.ymin = min(scores) - yTicks
            self.mainGraph.ymax = max(scores) + yTicks
            self.mainGraph.y_ticks_major = yTicks
        else:
            scores = userData[currUser]["scores"]
            points = scores
            self.mainGraph.xmin = 0
            self.mainGraph.xmax = len(scores) + 1
            self.mainGraph.x_ticks_major = 1
            r = max(scores) - min(scores)
            yTicks = ceil(r / len(scores))
            if (yTicks == 0): yTicks = 1
            self.mainGraph.ymin = min(scores) - yTicks
            self.mainGraph.ymax = max(scores) + yTicks
            self.mainGraph.y_ticks_major = yTicks

        plot.points.append((0,points[0]))
        for i in range(1,len(points)+1):
            plot.points.append((i,points[i-1]))
        plot.points.append((len(points)+1,points[-1]))

        for x in self.mainGraph.plots:
            self.mainGraph.remove_plot(x)

        self.mainGraph.add_plot(plot)



class MainBackground(Widget):
    pass

class MainScreen(Screen):
    pass



class GolfApp(App):
    global userData

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
        userData[data[0].lower()] = {}
        userData[data[0]]["password"] = data[1]
        scores = list(map(int,data[2][1:-1].split(";")))
        userData[data[0]]["scores"] = scores
    users.close()

    def build(self):
        Window.size=(350,600)
        self.icon = "appIcon.png"
        self.title = "Rychlak International"
        return Builder.load_file("Style.kv")

if __name__=="__main__":
    GolfApp().run()