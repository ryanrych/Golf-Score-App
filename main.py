import kivy
from PIL.ImageQt import rgb
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, DictProperty, NumericProperty, StringProperty
from kivy.properties import BooleanProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
from kivy.clock import Clock
from kivy_garden.graph import Graph, LinePlot

from math import ceil

userData = {}
currUser = ""
mastersData = {}

userData = {}
users = open("Users.txt", "r")
for user in users:
    data = user.split(",")
    userData[data[0].lower()] = {}
    userData[data[0].lower()]["password"] = data[1]
    scores = list(map(int,data[2][1:-1].split(";")))
    userData[data[0].lower()]["scores"] = scores
users.close()

mastersData = {}
holes = open("MastersHoles.txt","r")
for hole in holes:
    data = hole.split(",")
    mastersData[data[0]] = {}
    mastersData[data[0]]["description"] = data[1]
    mastersData[data[0]]["scores"] = list(map(int,data[2][1:-1].split(";")))
    mastersData[data[0]]["low"] = int(data[3])
    mastersData[data[0]]["high"] = int(data[4])
    mastersData[data[0]]["average"] = float(data[5])
    mastersData[data[0]]["index"] = int(data[6])
holes.close()

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
        global currUser
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
        global currUser

        self.mainGraph.tick_color = [0, 0, 0, 1]
        self.mainGraph.font_color = [0, 0, 0, 1]
        self.mainGraph.label_options = {"color": GolfApp.hexToKivyColor(None,"#595959",1)}
        self.mainGraph.x_grid_label = True
        self.mainGraph.y_grid_label = True
        self.mainGraph.tick_color = GolfApp.hexToKivyColor(None,"#595959",1)

        plot = LinePlot(color = GolfApp.hexToKivyColor(None,"33aaff",1))
        if (amount == 1):
            self.mainGraph.padding = 5
            scores = userData[currUser]["scores"][-5:]
            points = scores
            self.mainGraph.xmin = 0
            self.mainGraph.xmax = 6
            self.mainGraph.x_ticks_major = 1
            self.mainGraph.x_ticks_minor = 1
            r = max(scores) - min(scores)
            yTicks = ceil(r / 5)
            if (yTicks == 0): yTicks = 1
            self.mainGraph.ymin = min(scores) - yTicks
            self.mainGraph.ymax = max(scores) + yTicks
            self.mainGraph.y_ticks_major = yTicks

        elif (amount == 2):
            self.mainGraph.padding = 1
            scores = userData[currUser]["scores"][-10:]
            points = scores
            self.mainGraph._trigger_size = ObjectProperty(None)
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



class GameButtons(Widget):
    global mastersData
    global userData

    hole = 1
    description = mastersData[str(hole)]["description"]
    bestScore = mastersData[str(hole)]["low"]
    averageScore = round(mastersData[str(hole)]["average"],1)
    strokeIndex = mastersData[str(hole)]["index"]

    def updateHole(self):
        self.hole += 1
        self.name.text = "Hole: " + str(self.hole)
        self.descriptionID.text = str(mastersData[str(self.hole)]["description"])
        self.best.text = str(mastersData[str(self.hole)]["low"])
        self.average.text = str(round(mastersData[str(self.hole)]["average"],1))
        self.index.text = str(mastersData[str(self.hole)]["index"])
        self.scoreField.text = ""
        self.puttField.text = ""

class GameBackground(Widget):
    pass

class GameScreen(Screen):
    pass



class GolfApp(App):
    global userData
    global mastersData

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
        self.icon = "appIcon.png"
        self.title = "Rychlak International"
        return Builder.load_file("Style.kv")

if __name__=="__main__":
    GolfApp().run()