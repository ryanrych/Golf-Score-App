


import kivy
from PIL.ImageQt import rgb
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, DictProperty, NumericProperty, StringProperty, ListProperty
from kivy.properties import BooleanProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
from kivy.clock import Clock
from kivy_garden.graph import Graph, LinePlot

from math import ceil
import datetime

from PlayedData import Game, Hole

userData = {}
currUser = ""
mastersData = {}

users = open("Users.txt", "r")
for user in users:
    data = user.split(";")
    userData[data[0].lower()] = {}
    userData[data[0].lower()]["password"] = data[1]
    userData[data[0].lower()]["games"] = []
    for x in data[2][1:-1].split("-"):
        userData[data[0].lower()]["games"].append(Game(x[1:-1].split(",")[0],x[1:-1].split(",")[1],x[1:-1].split(",")[2],x[1:-1].split(",")[3],x[1:-1].split(",")[4],x[1:-1].split(",")[5],x[1:-1].split(",")[6]))
    userData[data[0].lower()]["best front"] = int(data[3])
    userData[data[0].lower()]["best back"] = int(data[4])
    userData[data[0].lower()]["average front"] = float(data[5])
    userData[data[0].lower()]["average back"] = float(data[6])
    userData[data[0].lower()]["best total"] = int(data[7])
    userData[data[0].lower()]["average total"] = float(data[8])
    userData[data[0].lower()]["average last 5"] = float(data[9])
    userData[data[0].lower()]["average last 10"] = float(data[10])
    userData[data[0].lower()]["super 9"] = int(data[11])
    userData[data[0].lower()]["super 1"] = int(data[12])
    userData[data[0].lower()]["holes"] = []
    for x in data[13][1:-1].split("-"):
        scores = []
        putts = []
        for y in x[1:-1].split(",")[0][1:-1].split("."):
            scores.append(int(y))
        for y in x[1:-1].split(",")[1][1:-1].split("."):
            putts.append(int(y))
        userData[data[0].lower()]["holes"].append(Hole(scores,putts,int(x[1:-1].split(",")[2]),float(x[1:-1].split(",")[3]),int(x[1:-1].split(",")[4]),int(x[1:-1].split(",")[5]),int(x[1:-1].split(",")[6]),int(x[1:-1].split(",")[7]),int(x[1:-1].split(",")[8]),int(x[1:-1].split(",")[9]),float(x[1:-1].split(",")[10]),float(x[1:-1].split(",")[11]),float(x[1:-1].split(",")[12]),int(x[1:-1].split(",")[13]),int(x[1:-1].split(",")[14]),float(x[1:-1].split(",")[15])))
    userData[data[0].lower()]["games count"] = int(data[14])
    userData[data[0].lower()]["pars"] = int(data[15])
    userData[data[0].lower()]["bulls"] = int(data[16])
    userData[data[0].lower()]["saves"] = int(data[17])
    userData[data[0].lower()]["failed pars"] = int (data[18])
    userData[data[0].lower()]["failed bulls"] = int(data[19])
    userData[data[0].lower()]["failed saves"] = int(data[20])
    userData[data[0].lower()]["par rate"] = float(data[21])
    userData[data[0].lower()]["bull rate"] = float(data[22])
    userData[data[0].lower()]["save rate"] = float(data[23])
    userData[data[0].lower()]["greens"] = int(data[24])
    userData[data[0].lower()]["failed greens"] = int(data[25])
    userData[data[0].lower()]["green rate"] = float(data[26])
users.close()

mastersData = {}
holes = open("MastersHoles.txt","r")
for hole in holes:
    data = hole.split(";")
    mastersData[data[0]] = {}
    mastersData[data[0]]["description"] = data[1]
    mastersData[data[0]]["scores"] = list(map(int,data[2][1:-1].split(",")))
    mastersData[data[0]]["low"] = int(data[3])
    mastersData[data[0]]["high"] = int(data[4])
    mastersData[data[0]]["average"] = float(data[5])
    mastersData[data[0]]["index"] = int(data[6])
    mastersData[data[0]]["distance"] = int(data[7])
    mastersData[data[0]]["pars"] = int(data[8])
    mastersData[data[0]]["bulls"] = int(data[9])
    mastersData[data[0]]["saves"] = int(data[10])
    mastersData[data[0]]["greens"] = int(data[11])
    mastersData[data[0]]["failed pars"] = int(data[12])
    mastersData[data[0]]["failed bulls"] = int(data[13])
    mastersData[data[0]]["failed saves"] = int(data[14])
    mastersData[data[0]]["failed greens"] = int(data[15])
    mastersData[data[0]]["par rate"] = float(data[16])
    mastersData[data[0]]["bull rate"] = float(data[17])
    mastersData[data[0]]["save rate"] = float(data[18])
    mastersData[data[0]]["on rate"] = float(data[19])
holes.close()

courseData = {}
file = open("Course.txt","r")
for line in file:
    data = line.split(";")
    courseData["scores"] = []
    for x in data[0][1:-1].split(","):
        courseData["scores"].append(int(x))
    courseData["average"] = data[1]
    courseData["best score"] = [data[2].split(",")[0],int(data[2].split(",")[1])]
    courseData["best average"] = [data[3].split(",")[0], float(data[3].split(",")[1])]
    courseData["best front"] = [data[4].split(",")[0], int(data[4].split(",")[1])]
    courseData["best front average"] = [data[5].split(",")[0], float(data[5].split(",")[1])]
    courseData["best back"] = [data[6].split(",")[0], int(data[6].split(",")[1])]
    courseData["best back average"] = [data[7].split(",")[0], float(data[7].split(",")[1])]
    courseData["best par"] = [data[8].split(",")[0], float(data[8].split(",")[1])]
    courseData["best save"] = [data[9].split(",")[0], float(data[9].split(",")[1])]
    courseData["best on"] = [data[10].split(",")[0], float(data[10].split(",")[1])]
    courseData["most bulls"] = [data[11].split(",")[0], int(data[11].split(",")[1])]
    courseData["most games"] = [data[12].split(",")[0], int(data[12].split(",")[1])]
file.close()

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
                self.userField.text = ""
                self.passwordField.text = ""

                sm = App.get_running_app().root
                screen = sm.get_screen("MainScreen")
                screen.ids.background.ids.buttons.graphButtons(1)

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

    def resetLogin(self):
        self.loginPassed = False

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
            userData[username]["games"] = []
            userData[username]["best front"] = 99
            userData[username]["best back"] = 99
            userData[username]["average front"] = 99
            userData[username]["average back"] = 99
            userData[username]["best total"] = 99
            userData[username]["average total"] = 99
            userData[username]["average last 5"] = 99
            userData[username]["average last 10"] = 99
            userData[username]["super 9"] = 99
            userData[username]["super 1"] = 99
            userData[username]["holes"] = []
            for i in range(18):
                userData[username]["holes"].append(Hole([],[],99,99,0,0,0,0,0,0,0,0,0,0,0,0))
            userData[username]["games count"] = 0
            userData[username]["pars"] = 0
            userData[username]["bulls"] = 0
            userData[username]["saves"] = 0
            userData[username]["failed pars"] = 0
            userData[username]["failed bulls"] = 0
            userData[username]["failed saves"] = 0
            userData[username]["par rate"] = 0
            userData[username]["bull rate"] = 0
            userData[username]["save rate"] = 0
            userData[username]["greens"] = 0
            userData[username]["failed greens"] = 0
            userData[username]["green rate"] = 0

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

        if (userData[currUser]["games count"] == 0):
            return

        userScores = []
        for x in userData[currUser]["games"]:
            userScores.append(int(x.totalScore))

        plot = LinePlot(color = GolfApp.hexToKivyColor(None,"33aaff",1))
        if (amount == 1):
            self.mainGraph.padding = 5
            scores = userScores[-5:]
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
            scores = userScores[-10:]
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

        plot.points.append((0,points[0]))
        for i in range(1,len(points)+1):
            plot.points.append((i,points[i-1]))
        plot.points.append((len(points)+1,points[-1]))

        for x in self.mainGraph.plots:
            self.mainGraph.remove_plot(x)

        self.mainGraph.add_plot(plot)

    def updateRecordScreen(self):
        sm = App.get_running_app().root
        screen = sm.get_screen("CourseScreen2")

        screen.ids.background.ids.stats.ids.bestScore.text = "Best Score: " + str(courseData["best score"][1])
        screen.ids.background.ids.stats.ids.bestScoreUser.text = "Set By: " + str(courseData["best score"][0])

        screen.ids.background.ids.stats.ids.bestAverage.text = "Best Average Score: " + str(round(courseData["best average"][1],2))
        screen.ids.background.ids.stats.ids.bestAverageUser.text = "Set By: " + str(courseData["best average"][0])

        screen.ids.background.ids.stats.ids.bestFront.text = "Best Front Score: " + str(courseData["best front"][1])
        screen.ids.background.ids.stats.ids.bestFrontUser.text = "Set By: " + str(courseData["best front"][0])

        screen.ids.background.ids.stats.ids.bestFrontAverage.text = "Best Average Front Score: " + str(round(courseData["best front average"][1],2))
        screen.ids.background.ids.stats.ids.bestFrontAverageUser.text = "Set By: " + str(courseData["best front average"][0])

        screen.ids.background.ids.stats.ids.bestBack.text = "Best Back Score: " + str(courseData["best back"][1])
        screen.ids.background.ids.stats.ids.bestBackUser.text = "Set By: " + str(courseData["best back"][0])

        screen.ids.background.ids.stats.ids.bestBackAverage.text = "Best Average Back Score: " + str(round(courseData["best back average"][1],2))
        screen.ids.background.ids.stats.ids.bestBackAverageUser.text = "Set By: " + str(courseData["best back average"][0])

        screen.ids.background.ids.stats.ids.bestPR.text = "Best Par Rate: " + str(round(courseData["best par"][1] * 100, 1)) + "%"
        screen.ids.background.ids.stats.ids.bestPRUser.text = "Set By: " + str(courseData["best par"][0])

        screen.ids.background.ids.stats.ids.bestGR.text = "Best Green Rate: " + str(round(courseData["best on"][1] * 100, 1)) + "%"
        screen.ids.background.ids.stats.ids.bestGRUser.text = "Set By: " + str(courseData["best on"][0])

        screen.ids.background.ids.stats.ids.bestSR.text = "Best Save Rate: " + str(round(courseData["best save"][1] * 100, 1)) + "%"
        screen.ids.background.ids.stats.ids.bestSRUser.text = "Set By: " + str(courseData["best save"][0])

        screen.ids.background.ids.stats.ids.mostBulls.text = "Most Bulls: " + str(courseData["most bulls"][1])
        screen.ids.background.ids.stats.ids.mostBullsUser.text = "Set By: " + str(courseData["most bulls"][0])

        screen.ids.background.ids.stats.ids.mostGames.text = "Most Games: " + str(courseData["most games"][1])
        screen.ids.background.ids.stats.ids.mostGamesUser.text = "Set By: " + str(courseData["most games"][0])

    def updateCourseScreen(self):
        sm = App.get_running_app().root
        screen = sm.get_screen("CourseScreen")

        screen.ids.background.ids.stats.ids.hole1Best.text = str(mastersData["1"]["low"])
        screen.ids.background.ids.stats.ids.hole1Average.text = str(round(mastersData["1"]["average"], 1))
        screen.ids.background.ids.stats.ids.hole1PR.text = str(
            round(mastersData["1"]["par rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole1GR.text = str(
            round(mastersData["1"]["on rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole1SR.text = str(
            round(mastersData["1"]["save rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole1Bulls.text = str(mastersData["1"]["bulls"])
        screen.ids.background.ids.stats.ids.hole1Index.text = str(mastersData["1"]["index"])

        screen.ids.background.ids.stats.ids.hole2Best.text = str(mastersData["2"]["low"])
        screen.ids.background.ids.stats.ids.hole2Average.text = str(round(mastersData["2"]["average"], 1))
        screen.ids.background.ids.stats.ids.hole2PR.text = str(round(mastersData["2"]["par rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole2GR.text = str(
            round(mastersData["2"]["on rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole2SR.text = str(
            round(mastersData["2"]["save rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole2Bulls.text = str(mastersData["2"]["bulls"])
        screen.ids.background.ids.stats.ids.hole2Index.text = str(mastersData["2"]["index"])

        screen.ids.background.ids.stats.ids.hole3Best.text = str(mastersData["3"]["low"])
        screen.ids.background.ids.stats.ids.hole3Average.text = str(round(mastersData["3"]["average"], 1))
        screen.ids.background.ids.stats.ids.hole3PR.text = str(
            round(mastersData["3"]["par rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole3GR.text = str(
            round(mastersData["3"]["on rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole3SR.text = str(
            round(mastersData["3"]["save rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole3Bulls.text = str(mastersData["3"]["bulls"])
        screen.ids.background.ids.stats.ids.hole3Index.text = str(mastersData["3"]["index"])

        screen.ids.background.ids.stats.ids.hole4Best.text = str(mastersData["4"]["low"])
        screen.ids.background.ids.stats.ids.hole4Average.text = str(round(mastersData["4"]["average"], 1))
        screen.ids.background.ids.stats.ids.hole4PR.text = str(
            round(mastersData["4"]["par rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole4GR.text = str(
            round(mastersData["4"]["on rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole4SR.text = str(
            round(mastersData["4"]["save rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole4Bulls.text = str(mastersData["4"]["bulls"])
        screen.ids.background.ids.stats.ids.hole4Index.text = str(mastersData["4"]["index"])

        screen.ids.background.ids.stats.ids.hole5Best.text = str(mastersData["5"]["low"])
        screen.ids.background.ids.stats.ids.hole5Average.text = str(round(mastersData["5"]["average"], 1))
        screen.ids.background.ids.stats.ids.hole5PR.text = str(
            round(mastersData["5"]["par rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole5GR.text = str(
            round(mastersData["5"]["on rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole5SR.text = str(
            round(mastersData["5"]["save rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole5Bulls.text = str(mastersData["5"]["bulls"])
        screen.ids.background.ids.stats.ids.hole5Index.text = str(mastersData["5"]["index"])

        screen.ids.background.ids.stats.ids.hole6Best.text = str(mastersData["6"]["low"])
        screen.ids.background.ids.stats.ids.hole6Average.text = str(round(mastersData["6"]["average"], 1))
        screen.ids.background.ids.stats.ids.hole6PR.text = str(
            round(mastersData["6"]["par rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole6GR.text = str(
            round(mastersData["6"]["on rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole6SR.text = str(
            round(mastersData["6"]["save rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole6Bulls.text = str(mastersData["6"]["bulls"])
        screen.ids.background.ids.stats.ids.hole6Index.text = str(mastersData["6"]["index"])

        screen.ids.background.ids.stats.ids.hole7Best.text = str(mastersData["7"]["low"])
        screen.ids.background.ids.stats.ids.hole7Average.text = str(round(mastersData["7"]["average"], 1))
        screen.ids.background.ids.stats.ids.hole7PR.text = str(
            round(mastersData["7"]["par rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole7GR.text = str(
            round(mastersData["7"]["on rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole7SR.text = str(
            round(mastersData["7"]["save rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole7Bulls.text = str(mastersData["7"]["bulls"])
        screen.ids.background.ids.stats.ids.hole7Index.text = str(mastersData["7"]["index"])

        screen.ids.background.ids.stats.ids.hole8Best.text = str(mastersData["8"]["low"])
        screen.ids.background.ids.stats.ids.hole8Average.text = str(round(mastersData["8"]["average"], 1))
        screen.ids.background.ids.stats.ids.hole8PR.text = str(
            round(mastersData["8"]["par rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole8GR.text = str(
            round(mastersData["8"]["on rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole8SR.text = str(
            round(mastersData["8"]["save rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole8Bulls.text = str(mastersData["8"]["bulls"])
        screen.ids.background.ids.stats.ids.hole8Index.text = str(mastersData["8"]["index"])

        screen.ids.background.ids.stats.ids.hole9Best.text = str(mastersData["9"]["low"])
        screen.ids.background.ids.stats.ids.hole9Average.text = str(round(mastersData["9"]["average"], 1))
        screen.ids.background.ids.stats.ids.hole9PR.text = str(
            round(mastersData["9"]["par rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole9GR.text = str(
            round(mastersData["9"]["on rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole9SR.text = str(
            round(mastersData["9"]["save rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole9Bulls.text = str(mastersData["9"]["bulls"])
        screen.ids.background.ids.stats.ids.hole9Index.text = str(mastersData["9"]["index"])

        screen.ids.background.ids.stats.ids.hole10Best.text = str(mastersData["10"]["low"])
        screen.ids.background.ids.stats.ids.hole10Average.text = str(round(mastersData["10"]["average"], 1))
        screen.ids.background.ids.stats.ids.hole10PR.text = str(
            round(mastersData["10"]["par rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole10GR.text = str(
            round(mastersData["10"]["on rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole10SR.text = str(
            round(mastersData["10"]["save rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole10Bulls.text = str(mastersData["10"]["bulls"])
        screen.ids.background.ids.stats.ids.hole10Index.text = str(mastersData["10"]["index"])

        screen.ids.background.ids.stats.ids.hole11Best.text = str(mastersData["11"]["low"])
        screen.ids.background.ids.stats.ids.hole11Average.text = str(round(mastersData["11"]["average"], 1))
        screen.ids.background.ids.stats.ids.hole11PR.text = str(
            round(mastersData["11"]["par rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole11GR.text = str(
            round(mastersData["11"]["on rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole11SR.text = str(
            round(mastersData["11"]["save rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole11Bulls.text = str(mastersData["11"]["bulls"])
        screen.ids.background.ids.stats.ids.hole11Index.text = str(mastersData["11"]["index"])

        screen.ids.background.ids.stats.ids.hole12Best.text = str(mastersData["12"]["low"])
        screen.ids.background.ids.stats.ids.hole12Average.text = str(round(mastersData["12"]["average"], 1))
        screen.ids.background.ids.stats.ids.hole12PR.text = str(
            round(mastersData["12"]["par rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole12GR.text = str(
            round(mastersData["12"]["on rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole12SR.text = str(
            round(mastersData["12"]["save rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole12Bulls.text = str(mastersData["12"]["bulls"])
        screen.ids.background.ids.stats.ids.hole12Index.text = str(mastersData["12"]["index"])

        screen.ids.background.ids.stats.ids.hole13Best.text = str(mastersData["13"]["low"])
        screen.ids.background.ids.stats.ids.hole13Average.text = str(round(mastersData["13"]["average"], 1))
        screen.ids.background.ids.stats.ids.hole13PR.text = str(
            round(mastersData["13"]["par rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole13GR.text = str(
            round(mastersData["13"]["on rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole13SR.text = str(
            round(mastersData["13"]["save rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole13Bulls.text = str(mastersData["13"]["bulls"])
        screen.ids.background.ids.stats.ids.hole13Index.text = str(mastersData["13"]["index"])

        screen.ids.background.ids.stats.ids.hole14Best.text = str(mastersData["14"]["low"])
        screen.ids.background.ids.stats.ids.hole14Average.text = str(round(mastersData["14"]["average"], 1))
        screen.ids.background.ids.stats.ids.hole14PR.text = str(
            round(mastersData["14"]["par rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole14GR.text = str(
            round(mastersData["14"]["on rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole14SR.text = str(
            round(mastersData["14"]["save rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole14Bulls.text = str(mastersData["14"]["bulls"])
        screen.ids.background.ids.stats.ids.hole14Index.text = str(mastersData["14"]["index"])

        screen.ids.background.ids.stats.ids.hole15Best.text = str(mastersData["15"]["low"])
        screen.ids.background.ids.stats.ids.hole15Average.text = str(round(mastersData["15"]["average"], 1))
        screen.ids.background.ids.stats.ids.hole15PR.text = str(
            round(mastersData["15"]["par rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole15GR.text = str(
            round(mastersData["15"]["on rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole15SR.text = str(
            round(mastersData["15"]["save rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole15Bulls.text = str(mastersData["15"]["bulls"])
        screen.ids.background.ids.stats.ids.hole15Index.text = str(mastersData["15"]["index"])

        screen.ids.background.ids.stats.ids.hole16Best.text = str(mastersData["16"]["low"])
        screen.ids.background.ids.stats.ids.hole16Average.text = str(round(mastersData["16"]["average"], 1))
        screen.ids.background.ids.stats.ids.hole16PR.text = str(
            round(mastersData["16"]["par rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole16GR.text = str(
            round(mastersData["16"]["on rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole16SR.text = str(
            round(mastersData["16"]["save rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole16Bulls.text = str(mastersData["16"]["bulls"])
        screen.ids.background.ids.stats.ids.hole16Index.text = str(mastersData["16"]["index"])

        screen.ids.background.ids.stats.ids.hole17Best.text = str(mastersData["17"]["low"])
        screen.ids.background.ids.stats.ids.hole17Average.text = str(round(mastersData["17"]["average"], 1))
        screen.ids.background.ids.stats.ids.hole17PR.text = str(
            round(mastersData["17"]["par rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole17GR.text = str(
            round(mastersData["17"]["on rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole17SR.text = str(
            round(mastersData["17"]["save rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole17Bulls.text = str(mastersData["17"]["bulls"])
        screen.ids.background.ids.stats.ids.hole17Index.text = str(mastersData["17"]["index"])

        screen.ids.background.ids.stats.ids.hole18Best.text = str(mastersData["18"]["low"])
        screen.ids.background.ids.stats.ids.hole18Average.text = str(round(mastersData["18"]["average"], 1))
        screen.ids.background.ids.stats.ids.hole18PR.text = str(
            round(mastersData["18"]["par rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole18GR.text = str(
            round(mastersData["18"]["on rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole18SR.text = str(
            round(mastersData["18"]["save rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole18Bulls.text = str(mastersData["18"]["bulls"])
        screen.ids.background.ids.stats.ids.hole18Index.text = str(mastersData["18"]["index"])

    def updateStatsScreen(self):
        global userData
        global currUser

        sm = App.get_running_app().root
        screen = sm.get_screen("StatsScreenHoles")

        screen.ids.background.ids.stats.ids.hole1Best.text = str(userData[currUser]["holes"][0].bestScore)
        screen.ids.background.ids.stats.ids.hole1Average.text = str(round(userData[currUser]["holes"][0].avgScore, 1))
        screen.ids.background.ids.stats.ids.hole1PR.text = str(
            round(userData[currUser]["holes"][0].parRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole1GR.text = str(
            round(userData[currUser]["holes"][0].greenRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole1SR.text = str(
            round(userData[currUser]["holes"][0].saveRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole1Bulls.text = str(userData[currUser]["holes"][0].bulls)

        screen.ids.background.ids.stats.ids.hole2Best.text = str(userData[currUser]["holes"][1].bestScore)
        screen.ids.background.ids.stats.ids.hole2Average.text = str(round(userData[currUser]["holes"][1].avgScore, 1))
        screen.ids.background.ids.stats.ids.hole2PR.text = str(
            round(userData[currUser]["holes"][1].parRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole2GR.text = str(
            round(userData[currUser]["holes"][1].greenRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole2SR.text = str(
            round(userData[currUser]["holes"][1].saveRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole2Bulls.text = str(userData[currUser]["holes"][1].bulls)

        screen.ids.background.ids.stats.ids.hole3Best.text = str(userData[currUser]["holes"][2].bestScore)
        screen.ids.background.ids.stats.ids.hole3Average.text = str(round(userData[currUser]["holes"][2].avgScore, 1))
        screen.ids.background.ids.stats.ids.hole3PR.text = str(
            round(userData[currUser]["holes"][2].parRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole3GR.text = str(
            round(userData[currUser]["holes"][2].greenRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole3SR.text = str(
            round(userData[currUser]["holes"][2].saveRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole3Bulls.text = str(userData[currUser]["holes"][2].bulls)

        screen.ids.background.ids.stats.ids.hole4Best.text = str(userData[currUser]["holes"][3].bestScore)
        screen.ids.background.ids.stats.ids.hole4Average.text = str(round(userData[currUser]["holes"][3].avgScore, 1))
        screen.ids.background.ids.stats.ids.hole4PR.text = str(
            round(userData[currUser]["holes"][3].parRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole4GR.text = str(
            round(userData[currUser]["holes"][3].greenRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole4SR.text = str(
            round(userData[currUser]["holes"][3].saveRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole4Bulls.text = str(userData[currUser]["holes"][3].bulls)

        screen.ids.background.ids.stats.ids.hole5Best.text = str(userData[currUser]["holes"][4].bestScore)
        screen.ids.background.ids.stats.ids.hole5Average.text = str(round(userData[currUser]["holes"][4].avgScore, 1))
        screen.ids.background.ids.stats.ids.hole5PR.text = str(
            round(userData[currUser]["holes"][4].parRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole5GR.text = str(
            round(userData[currUser]["holes"][4].greenRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole5SR.text = str(
            round(userData[currUser]["holes"][4].saveRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole5Bulls.text = str(userData[currUser]["holes"][4].bulls)

        screen.ids.background.ids.stats.ids.hole6Best.text = str(userData[currUser]["holes"][5].bestScore)
        screen.ids.background.ids.stats.ids.hole6Average.text = str(round(userData[currUser]["holes"][5].avgScore, 1))
        screen.ids.background.ids.stats.ids.hole6PR.text = str(
            round(userData[currUser]["holes"][5].parRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole6GR.text = str(
            round(userData[currUser]["holes"][5].greenRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole6SR.text = str(
            round(userData[currUser]["holes"][5].saveRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole6Bulls.text = str(userData[currUser]["holes"][5].bulls)

        screen.ids.background.ids.stats.ids.hole7Best.text = str(userData[currUser]["holes"][6].bestScore)
        screen.ids.background.ids.stats.ids.hole7Average.text = str(round(userData[currUser]["holes"][6].avgScore, 1))
        screen.ids.background.ids.stats.ids.hole7PR.text = str(
            round(userData[currUser]["holes"][6].parRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole7GR.text = str(
            round(userData[currUser]["holes"][6].greenRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole7SR.text = str(
            round(userData[currUser]["holes"][6].saveRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole7Bulls.text = str(userData[currUser]["holes"][6].bulls)

        screen.ids.background.ids.stats.ids.hole8Best.text = str(userData[currUser]["holes"][7].bestScore)
        screen.ids.background.ids.stats.ids.hole8Average.text = str(round(userData[currUser]["holes"][7].avgScore, 1))
        screen.ids.background.ids.stats.ids.hole8PR.text = str(
            round(userData[currUser]["holes"][7].parRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole8GR.text = str(
            round(userData[currUser]["holes"][7].greenRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole8SR.text = str(
            round(userData[currUser]["holes"][7].saveRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole8Bulls.text = str(userData[currUser]["holes"][7].bulls)

        screen.ids.background.ids.stats.ids.hole9Best.text = str(userData[currUser]["holes"][8].bestScore)
        screen.ids.background.ids.stats.ids.hole9Average.text = str(round(userData[currUser]["holes"][8].avgScore, 1))
        screen.ids.background.ids.stats.ids.hole9PR.text = str(
            round(userData[currUser]["holes"][8].parRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole9GR.text = str(
            round(userData[currUser]["holes"][8].greenRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole9SR.text = str(
            round(userData[currUser]["holes"][8].saveRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole9Bulls.text = str(userData[currUser]["holes"][8].bulls)

        screen.ids.background.ids.stats.ids.hole10Best.text = str(userData[currUser]["holes"][9].bestScore)
        screen.ids.background.ids.stats.ids.hole10Average.text = str(round(userData[currUser]["holes"][9].avgScore, 1))
        screen.ids.background.ids.stats.ids.hole10PR.text = str(
            round(userData[currUser]["holes"][9].parRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole10GR.text = str(
            round(userData[currUser]["holes"][9].greenRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole10SR.text = str(
            round(userData[currUser]["holes"][9].saveRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole10Bulls.text = str(userData[currUser]["holes"][9].bulls)

        screen.ids.background.ids.stats.ids.hole11Best.text = str(userData[currUser]["holes"][10].bestScore)
        screen.ids.background.ids.stats.ids.hole11Average.text = str(round(userData[currUser]["holes"][10].avgScore, 1))
        screen.ids.background.ids.stats.ids.hole11PR.text = str(
            round(userData[currUser]["holes"][10].parRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole11GR.text = str(
            round(userData[currUser]["holes"][10].greenRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole11SR.text = str(
            round(userData[currUser]["holes"][10].saveRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole11Bulls.text = str(userData[currUser]["holes"][10].bulls)

        screen.ids.background.ids.stats.ids.hole12Best.text = str(userData[currUser]["holes"][11].bestScore)
        screen.ids.background.ids.stats.ids.hole12Average.text = str(round(userData[currUser]["holes"][11].avgScore, 1))
        screen.ids.background.ids.stats.ids.hole12PR.text = str(
            round(userData[currUser]["holes"][11].parRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole12GR.text = str(
            round(userData[currUser]["holes"][11].greenRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole12SR.text = str(
            round(userData[currUser]["holes"][11].saveRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole12Bulls.text = str(userData[currUser]["holes"][11].bulls)

        screen.ids.background.ids.stats.ids.hole13Best.text = str(userData[currUser]["holes"][12].bestScore)
        screen.ids.background.ids.stats.ids.hole13Average.text = str(round(userData[currUser]["holes"][12].avgScore, 1))
        screen.ids.background.ids.stats.ids.hole13PR.text = str(
            round(userData[currUser]["holes"][12].parRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole13GR.text = str(
            round(userData[currUser]["holes"][12].greenRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole13SR.text = str(
            round(userData[currUser]["holes"][12].saveRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole13Bulls.text = str(userData[currUser]["holes"][12].bulls)

        screen.ids.background.ids.stats.ids.hole14Best.text = str(userData[currUser]["holes"][13].bestScore)
        screen.ids.background.ids.stats.ids.hole14Average.text = str(round(userData[currUser]["holes"][13].avgScore, 1))
        screen.ids.background.ids.stats.ids.hole14PR.text = str(
            round(userData[currUser]["holes"][13].parRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole14GR.text = str(
            round(userData[currUser]["holes"][13].greenRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole14SR.text = str(
            round(userData[currUser]["holes"][13].saveRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole14Bulls.text = str(userData[currUser]["holes"][13].bulls)

        screen.ids.background.ids.stats.ids.hole15Best.text = str(userData[currUser]["holes"][14].bestScore)
        screen.ids.background.ids.stats.ids.hole15Average.text = str(round(userData[currUser]["holes"][14].avgScore, 1))
        screen.ids.background.ids.stats.ids.hole15PR.text = str(
            round(userData[currUser]["holes"][14].parRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole15GR.text = str(
            round(userData[currUser]["holes"][14].greenRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole15SR.text = str(
            round(userData[currUser]["holes"][14].saveRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole15Bulls.text = str(userData[currUser]["holes"][14].bulls)

        screen.ids.background.ids.stats.ids.hole16Best.text = str(userData[currUser]["holes"][15].bestScore)
        screen.ids.background.ids.stats.ids.hole16Average.text = str(round(userData[currUser]["holes"][15].avgScore, 1))
        screen.ids.background.ids.stats.ids.hole16PR.text = str(
            round(userData[currUser]["holes"][15].parRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole16GR.text = str(
            round(userData[currUser]["holes"][15].greenRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole16SR.text = str(
            round(userData[currUser]["holes"][15].saveRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole16Bulls.text = str(userData[currUser]["holes"][15].bulls)

        screen.ids.background.ids.stats.ids.hole17Best.text = str(userData[currUser]["holes"][16].bestScore)
        screen.ids.background.ids.stats.ids.hole17Average.text = str(round(userData[currUser]["holes"][16].avgScore, 1))
        screen.ids.background.ids.stats.ids.hole17PR.text = str(
            round(userData[currUser]["holes"][16].parRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole17GR.text = str(
            round(userData[currUser]["holes"][16].greenRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole17SR.text = str(
            round(userData[currUser]["holes"][16].saveRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole17Bulls.text = str(userData[currUser]["holes"][16].bulls)

        screen.ids.background.ids.stats.ids.hole18Best.text = str(userData[currUser]["holes"][17].bestScore)
        screen.ids.background.ids.stats.ids.hole18Average.text = str(round(userData[currUser]["holes"][17].avgScore, 1))
        screen.ids.background.ids.stats.ids.hole18PR.text = str(
            round(userData[currUser]["holes"][17].parRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole18GR.text = str(
            round(userData[currUser]["holes"][17].greenRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole18SR.text = str(
            round(userData[currUser]["holes"][17].saveRate * 100)) + "%"
        screen.ids.background.ids.stats.ids.hole18Bulls.text = str(userData[currUser]["holes"][17].bulls)



        screen = sm.get_screen("StatsScreenCourse")

        date = ""
        for x in userData[currUser]["games"]:
            if int(x.frontScore) == int(userData[currUser]["best front"]):
                date = x.datePlayed
                break
        screen.ids.background.ids.stats.ids.frontBest.text = "Best Score: " + str(userData[currUser]["best front"]) + "\nSet on " + date
        date = ""
        for x in userData[currUser]["games"]:
            if int(x.backScore) == int(userData[currUser]["best back"]):
                date = x.datePlayed
                break
        screen.ids.background.ids.stats.ids.backBest.text = "Best Score: " + str(userData[currUser]["best back"]) + "\nSet on " + date

        screen.ids.background.ids.stats.ids.frontAverage.text = "Average Score: " + str(round(userData[currUser]["average front"],1))
        screen.ids.background.ids.stats.ids.backAverage.text = "Average Score: " + str(round(userData[currUser]["average back"],1))

        screen.ids.background.ids.stats.ids.played.text = "Games Played: " + str(userData[currUser]["games count"])

        date = ""
        for x in userData[currUser]["games"]:
            if int(x.totalScore) == int(userData[currUser]["best total"]):
                date = x.datePlayed
                break
        screen.ids.background.ids.stats.ids.fullBest.text = "Best Score: " + str(userData[currUser]["best total"])
        screen.ids.background.ids.stats.ids.fullBestDate.text = "Set on " + date

        screen.ids.background.ids.stats.ids.fullAverage.text = "Average Score: " + str(round(userData[currUser]["average total"],1)) + "  5: " + str(round(userData[currUser]["average last 5"],1)) + "  10: " + str(round(userData[currUser]["average last 10"],1))

        screen.ids.background.ids.stats.ids.super9.text = "Front/Back Super: " + str(userData[currUser]["super 9"])
        screen.ids.background.ids.stats.ids.super1.text = "18 Hole Super: " + str(userData[currUser]["super 1"])

        screen.ids.background.ids.stats.ids.userPR.text = "Par Rate: " + str(round(userData[currUser]["par rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.userBulls.text = "Bulls: " + str(userData[currUser]["bulls"])
        screen.ids.background.ids.stats.ids.userGR.text = "Green Rate: " + str(round(userData[currUser]["green rate"] * 100)) + "%"
        screen.ids.background.ids.stats.ids.userSR.text = "Save Rate: " + str(round(userData[currUser]["save rate"] * 100)) + "%"


class MainBackground(Widget):
    pass

class MainScreen(Screen):
    pass



class GameButtons(Widget):
    global mastersData
    global userData
    global currUser
    global courseData

    hole = 0
    description = mastersData[str(hole + 1)]["description"]
    yards = mastersData[str(hole + 1)]["distance"]
    onRate = int(round(mastersData[str(hole + 1)]["on rate"] * 100,0))
    parRate = int(round(mastersData[str(hole + 1)]["par rate"] * 100,0))
    averageScore = round(mastersData[str(hole + 1)]["average"],1)
    strokeIndex = mastersData[str(hole + 1)]["index"]

    userBest = userData[currUser]["holes"][0].bestScore
    userAverage = round(userData[currUser]["holes"][0].avgScore,1)
    userPR = int(round(userData[currUser]["holes"][0].parRate * 100,0))
    userGR = int(round(userData[currUser]["holes"][0].parRate * 100,0))

    frontScore = 0
    frontPutts = 0
    backScore = 0
    backPutts = 0
    score = 0
    putts = 0
    pars = 0
    bulls = 0
    greens = 0
    saves = 0

    def updateEndScreen(self):
        global userData
        global currUser

        sm = App.get_running_app().root
        screen = sm.get_screen("EndScreen")

        screen.ids.backgroundEnd.ids.end.ids.score.text = "You Shot a " + str(self.score)
        screen.ids.backgroundEnd.ids.end.ids.pars.text = "Pars: " + str(self.pars)
        screen.ids.backgroundEnd.ids.end.ids.bulls.text = "Bulls: " + str(self.bulls)
        screen.ids.backgroundEnd.ids.end.ids.greens.text = "Greens: " + str(self.greens)
        screen.ids.backgroundEnd.ids.end.ids.saves.text = "Saves: " + str(self.saves)

        self.endGame()

    def writeData(self):
        open("Users.txt","w").close()

        file = open("Users.txt","w")
        lines = []
        for user in userData:
            if userData[user]["games count"] == 0:
                continue
            line = ""
            line += user + ";"
            line += userData[user]["password"] + ";"
            line += "["
            for game in userData[user]["games"]:
                line += "("
                line += str(game.frontScore) + ","
                line += str(game.frontPutts) + ","
                line += str(game.backScore) + ","
                line += str(game.backPutts) + ","
                line += str(game.totalScore) + ","
                line += str(game.totalPutts) + ","
                line += str(game.datePlayed) + ")-"
            line = line[:-1]
            line += "];"
            line += str(userData[user]["best front"]) + ";"
            line += str(userData[user]["best back"]) + ";"
            line += str(userData[user]["average front"]) + ";"
            line += str(userData[user]["average back"]) + ";"
            line += str(userData[user]["best total"]) + ";"
            line += str(userData[user]["average total"]) + ";"
            line += str(userData[user]["average last 5"]) + ";"
            line += str(userData[user]["average last 10"]) + ";"
            line += str(userData[user]["super 9"]) + ";"
            line += str(userData[user]["super 1"]) + ";"
            line += "["
            for hole in userData[user]["holes"]:
                line += "("
                line += "{"
                for score in hole.scores:
                    line += str(score) + "."
                line = line[:-1]
                line += "}"
                line += ","
                line += "{"
                for putt in hole.putts:
                    line += str(putt) + "."
                line = line[:-1]
                line += "}"
                line += ","
                line += str(hole.bestScore) + ","
                line += str(hole.avgScore) + ","
                line += str(hole.pars) + ","
                line += str(hole.bulls) + ","
                line += str(hole.saves) + ","
                line += str(hole.failedPars) + ","
                line += str(hole.failedBulls) + ","
                line += str(hole.failedSaves) + ","
                line += str(hole.parRate) + ","
                line += str(hole.bullRate) + ","
                line += str(hole.saveRate) + ","
                line += str(hole.greens) + ","
                line += str(hole.failedGreens) + ","
                line += str(hole.greenRate) + ")-"
            line = line[:-1]
            line += "];"
            line += str(userData[user]["games count"]) + ";"
            line += str(userData[user]["pars"]) + ";"
            line += str(userData[user]["bulls"]) + ";"
            line += str(userData[user]["saves"]) + ";"
            line += str(userData[user]["failed pars"]) + ";"
            line += str(userData[user]["failed bulls"]) + ";"
            line += str(userData[user]["failed saves"]) + ";"
            line += str(userData[user]["par rate"]) + ";"
            line += str(userData[user]["bull rate"]) + ";"
            line += str(userData[user]["save rate"]) + ";"
            line += str(userData[user]["greens"]) + ";"
            line += str(userData[user]["failed greens"]) + ";"
            line += str(userData[user]["green rate"])

            file.write(line + "\n")

        file.close()

        open("MastersHoles.txt","w").close()

        lines = []
        file = open("MastersHoles.txt","w")
        for i in range(1,19):
            line = ""
            line += str(i) + ";"
            line += mastersData[str(i)]["description"] + ";"
            line += "["
            for x in mastersData[str(i)]["scores"]:
                line += str(x) + ","
            line = line[:-1]
            line += "];"
            line += str(mastersData[str(i)]["low"]) + ";"
            line += str(mastersData[str(i)]["high"]) + ";"
            line += str(mastersData[str(i)]["average"]) + ";"
            line += str(mastersData[str(i)]["index"]) + ";"
            line += str(mastersData[str(i)]["distance"]) + ";"
            line += str(mastersData[str(i)]["pars"]) + ";"
            line += str(mastersData[str(i)]["bulls"]) + ";"
            line += str(mastersData[str(i)]["saves"]) + ";"
            line += str(mastersData[str(i)]["greens"]) + ";"
            line += str(mastersData[str(i)]["failed pars"]) + ";"
            line += str(mastersData[str(i)]["failed bulls"]) + ";"
            line += str(mastersData[str(i)]["failed saves"]) + ";"
            line += str(mastersData[str(i)]["failed greens"]) + ";"
            line += str(mastersData[str(i)]["par rate"]) + ";"
            line += str(mastersData[str(i)]["bull rate"]) + ";"
            line += str(mastersData[str(i)]["save rate"]) + ";"
            line += str(mastersData[str(i)]["on rate"]) + ";"
            lines.append(line)
            file.write(line + "\n")

        file.close()

        open("Course.txt","w").close()

        file = open("Course.txt","w")

        line = "["
        for x in courseData["scores"]:
            line += str(x) + ","
        line = line[:-1]
        line += "];"
        line += str(sum(courseData["scores"])/len(courseData["scores"])) + ";"
        line += courseData["best score"][0] + "," + str(courseData["best score"][1]) + ";"
        line += courseData["best average"][0] + "," + str(courseData["best average"][1]) + ";"
        line += courseData["best front"][0] + "," + str(courseData["best front"][1]) + ";"
        line += courseData["best front average"][0] + "," + str(courseData["best front average"][1]) + ";"
        line += courseData["best back"][0] + "," + str(courseData["best back"][1]) + ";"
        line += courseData["best back average"][0] + "," + str(courseData["best back average"][1]) + ";"
        line += courseData["best par"][0] + "," + str(courseData["best par"][1]) + ";"
        line += courseData["best save"][0] + "," + str(courseData["best save"][1]) + ";"
        line += courseData["best on"][0] + "," + str(courseData["best on"][1]) + ";"
        line += courseData["most bulls"][0] + "," + str(courseData["most bulls"][1]) + ";"
        line += courseData["most games"][0] + "," + str(courseData["most games"][1])
        file.write(line)

        file.close()

    def endGame(self):
        userData[currUser]["games"].append(Game(self.frontScore,self.frontPutts,self.backScore,self.backPutts,self.score,self.putts,str(datetime.datetime.now().strftime("%x"))))

        sumScoreFront = userData[currUser]["games count"] * userData[currUser]["average front"]
        sumScoreBack = userData[currUser]["games count"] * userData[currUser]["average back"]
        sumScoreTotal = userData[currUser]["games count"] * userData[currUser]["average total"]
        userData[currUser]["games count"] += 1
        userData[currUser]["average front"] = (sumScoreFront + self.frontScore) / userData[currUser]["games count"]
        userData[currUser]["average back"] = (sumScoreBack + self.backScore) / userData[currUser]["games count"]
        userData[currUser]["average total"] = (sumScoreTotal + self.score) / userData[currUser]["games count"]

        if userData[currUser]["games count"] >= 5:
            total = 0
            for x in userData[currUser]["games"][-5:]:
                total += int(x.totalScore)
            userData[currUser]["average last 5"] = total / 5

            if userData[currUser]["games count"] >= 10:
                total = 0
                for x in userData[currUser]["games"][-10:]:
                    total += int(x.totalScore)
                userData[currUser]["average last 10"] = total / 10
            else:
                userData[currUser]["average last 10"] = total / 5
        else:
            userData[currUser]["average total last 5"] = userData[currUser]["average total"]
            userData[currUser]["average total last 10"] = userData[currUser]["average total"]

        if self.frontScore < userData[currUser]["best front"]:
            userData[currUser]["best front"] = self.frontScore
        if self.backScore < userData[currUser]["best back"]:
            userData[currUser]["best back"] = self.backScore
        if self.score < userData[currUser]["best total"]:
            userData[currUser]["best total"] = self.score

        userData[currUser]["super 9"] = userData[currUser]["best front"] + userData[currUser]["best back"]

        averages = []
        for x in mastersData:
            averages.append(mastersData[x]["average"])
        averages = sorted(averages)
        averages = averages[::-1]

        for x in mastersData:
            mastersData[x]["index"] = averages.index(mastersData[x]["average"]) + 1

        score = 0
        for i in range(18):
            score += min(userData[currUser]["holes"][i].scores)
        userData[currUser]["super 1"] = score

        if (self.score < courseData["best score"][1]):
            courseData["best score"][0] = currUser
            courseData["best score"][1] = self.score
        if (self.frontScore < courseData["best front"][1]):
            courseData["best front"][0] = currUser
            courseData["best front"][1] = self.frontScore
        if (self.backScore < courseData["best back"][1]):
            courseData["best back"][0] = currUser
            courseData["best back"][1] = self.backScore
        if (userData[currUser]["bulls"] > courseData["most bulls"][1]):
            courseData["most bulls"][0] = currUser
            courseData["most bulls"][1] = userData[currUser]["bulls"]
        if (userData[currUser]["bulls"] > courseData["most bulls"][1]):
            courseData["most bulls"][0] = currUser
            courseData["most bulls"][1] = userData[currUser]["bulls"]
        if (userData[currUser]["games count"] > courseData["most games"][1]):
            courseData["most games"][0] = currUser
            courseData["most games"][1] = userData[currUser]["games count"]

        l = []
        for x in userData:
            if userData[x]["games count"] >= 5:
                l.append((x,userData[x]["average front"]))
        l = sorted(l, key=lambda x: x[-1])
        courseData["best front average"] = (l[0][0],l[0][1])

        l = []
        for x in userData:
            if userData[x]["games count"] >= 5:
                l.append((x, userData[x]["average back"]))
        l = sorted(l, key=lambda x: x[-1])
        courseData["best back average"] = (l[0][0], l[0][1])

        l = []
        for x in userData:
            if userData[x]["games count"] >= 5:
                l.append((x, userData[x]["average total"]))
        l = sorted(l, key=lambda x: x[-1])
        courseData["best average"] = (l[0][0], l[0][1])

        l = []
        for x in userData:
            if userData[x]["games count"] >= 5:
                l.append((x, userData[x]["par rate"]))
        l = sorted(l, key=lambda x: x[-1])[::-1]
        courseData["best par"] = (l[0][0], l[0][1])

        l = []
        for x in userData:
            if userData[x]["games count"] >= 5:
                l.append((x, userData[x]["save rate"]))
        l = sorted(l, key=lambda x: x[-1])[::-1]
        courseData["best save"] = (l[0][0], l[0][1])

        l = []
        for x in userData:
            if userData[x]["games count"] >= 5:
                l.append((x, userData[x]["green rate"]))
        l = sorted(l, key=lambda x: x[-1])[::-1]
        courseData["best on"] = (l[0][0], l[0][1])

        self.hole = 0
        self.description = mastersData[str(self.hole + 1)]["description"]
        self.bestScore = mastersData[str(self.hole + 1)]["low"]
        self.averageScore = round(mastersData[str(self.hole + 1)]["average"], 1)
        self.yards = mastersData[str(self.hole + 1)]["distance"]
        self.strokeIndex = mastersData[str(self.hole + 1)]["index"]

        self.frontScore = 0
        self.frontPutts = 0
        self.backScore = 0
        self.backPutts = 0
        self.score = 0
        self.putts = 0
        self.pars = 0
        self.bulls = 0
        self.saves = 0
        self.greens = 0

        self.name.text = "Welcome!"
        self.descriptionID.text = "This app will guide you through your round at Rychlak International. Please record all scores honestly for fair course data."
        self.course.text = ""
        self.user.text = ""
        self.average.text = ""
        self.index.text = ""
        self.distance.text = ""
        self.courseGreen.text = ""
        self.userGreen.text = ""
        self.coursePar.text = ""
        self.userPar.text = ""
        self.userBestScore.text = ""
        self.userAverageScore.text = ""
        self.scoreField.text = ""
        self.puttField.text = ""
        self.scoreLabel.text = ""
        self.puttLabel.text = ""
        self.scoreField.background_normal = "Blank.png"
        self.scoreField.background_active = "Blank.png"
        self.puttField.background_normal = "Blank.png"
        self.puttField.background_active = "Blank.png"

        self.writeData()



    def updateData(self):
        self.score += int(self.scoreField.text)
        self.putts += int(self.puttField.text)

        if self.hole < 10:
            self.frontScore += int(self.scoreField.text)
            self.frontPutts += int(self.puttField.text)
        else:
            self.backScore += int(self.scoreField.text)
            self.backPutts += int(self.puttField.text)

        userData[currUser]["holes"][self.hole - 1].scores.append(int(self.scoreField.text))
        userData[currUser]["holes"][self.hole - 1].putts.append(int(self.puttField.text))

        mastersData[str(self.hole)]["scores"].append(int(self.scoreField.text))

        userData[currUser]["holes"][self.hole - 1].avgScore = sum(userData[currUser]["holes"][self.hole - 1].scores) / len(userData[currUser]["holes"][self.hole - 1].scores)

        mastersData[str(self.hole)]["average"] = sum(mastersData[str(self.hole)]["scores"]) / len(mastersData[str(self.hole)]["scores"])

        if int(self.scoreField.text) < userData[currUser]["holes"][self.hole - 1].bestScore:
            userData[currUser]["holes"][self.hole - 1].bestScore = int(self.scoreField.text)

        if int(self.scoreField.text) < mastersData[str(self.hole)]["low"]:
            mastersData[str(self.hole)]["low"] = int(self.scoreField.text)

        if (int(self.scoreField.text) == 1):
            self.bulls += 1

            userData[currUser]["holes"][self.hole - 1].bulls += 1
            userData[currUser]["holes"][self.hole - 1].bullRate = userData[currUser]["holes"][self.hole - 1].bulls / (userData[currUser]["holes"][self.hole - 1].failedBulls + userData[currUser]["holes"][self.hole - 1].bulls)

            userData[currUser]["bulls"] += 1
            userData[currUser]["bull rate"] = userData[currUser]["bulls"] / (userData[currUser]["failed bulls"] + userData[currUser]["bulls"])

            userData[currUser]["holes"][self.hole - 1].greens += 1
            userData[currUser]["holes"][self.hole - 1].greenRate = userData[currUser]["holes"][self.hole - 1].greens / (userData[currUser]["holes"][self.hole - 1].greens + userData[currUser]["holes"][self.hole - 1].failedGreens)

            userData[currUser]["greens"] += 1
            userData[currUser]["green rate"] = userData[currUser]["greens"] / (userData[currUser]["greens"] + userData[currUser]["failed greens"])

            mastersData[str(self.hole)]["bulls"] += 1
            mastersData[str(self.hole)]["bull rate"] = mastersData[str(self.hole)]["bulls"] / (mastersData[str(self.hole)]["bulls"] + mastersData[str(self.hole)]["failed bulls"])

            mastersData[str(self.hole)]["greens"] += 1
            mastersData[str(self.hole)]["green rate"] = mastersData[str(self.hole)]["greens"] / (mastersData[str(self.hole)]["greens"] + mastersData[str(self.hole)]["failed greens"])
        elif (int(self.scoreField.text) == 2):
            if (int(self.puttField.text) == 0):
                self.saves += 1

                userData[currUser]["holes"][self.hole - 1].saves += 1
                userData[currUser]["holes"][self.hole - 1].saveRate = userData[currUser]["holes"][self.hole - 1].saves / (userData[currUser]["holes"][self.hole - 1].failedSaves + userData[currUser]["holes"][self.hole - 1].saves)

                userData[currUser]["saves"] += 1
                userData[currUser]["save rate"] = userData[currUser]["saves"] / (userData[currUser]["failed saves"] + userData[currUser]["saves"])

                userData[currUser]["holes"][self.hole - 1].failedGreens += 1
                userData[currUser]["holes"][self.hole - 1].greenRate = userData[currUser]["holes"][self.hole - 1].greens / (userData[currUser]["holes"][self.hole - 1].greens +userData[currUser]["holes"][self.hole - 1].failedGreens)

                userData[currUser]["failed greens"] += 1
                userData[currUser]["green rate"] = userData[currUser]["greens"] / (userData[currUser]["greens"] + userData[currUser]["failed greens"])

                mastersData[str(self.hole)]["saves"] += 1
                mastersData[str(self.hole)]["save rate"] = mastersData[str(self.hole)]["saves"] / (mastersData[str(self.hole)]["saves"] + mastersData[str(self.hole)]["failed saves"])

                mastersData[str(self.hole)]["failed greens"] += 1
                mastersData[str(self.hole)]["on rate"] = mastersData[str(self.hole)]["greens"] / (mastersData[str(self.hole)]["greens"] + mastersData[str(self.hole)]["failed greens"])
            else:
                userData[currUser]["holes"][self.hole - 1].greens += 1
                userData[currUser]["holes"][self.hole - 1].greenRate = userData[currUser]["holes"][self.hole - 1].greens / (userData[currUser]["holes"][self.hole - 1].greens + userData[currUser]["holes"][self.hole - 1].failedGreens)

                userData[currUser]["greens"] += 1
                userData[currUser]["green rate"] = userData[currUser]["greens"] / (userData[currUser]["greens"] + userData[currUser]["failed greens"])

                mastersData[str(self.hole)]["greens"] += 1
                mastersData[str(self.hole)]["on rate"] = mastersData[str(self.hole)]["greens"] / (mastersData[str(self.hole)]["greens"] + mastersData[str(self.hole)]["failed greens"])

            self.pars += 1
            self.greens += 1

            userData[currUser]["holes"][self.hole - 1].pars += 1
            userData[currUser]["holes"][self.hole - 1].parRate = userData[currUser]["holes"][self.hole - 1].pars / (userData[currUser]["holes"][self.hole - 1].failedPars + userData[currUser]["holes"][self.hole - 1].pars)

            userData[currUser]["pars"] += 1
            userData[currUser]["par rate"] = userData[currUser]["pars"] / (userData[currUser]["failed pars"] + userData[currUser]["pars"])

            mastersData[str(self.hole)]["pars"] += 1
            mastersData[str(self.hole)]["par rate"] = mastersData[str(self.hole)]["pars"] / (mastersData[str(self.hole)]["pars"] + mastersData[str(self.hole)]["failed pars"])

            userData[currUser]["holes"][self.hole - 1].failedBulls += 1
            userData[currUser]["holes"][self.hole - 1].bullRate = userData[currUser]["holes"][self.hole - 1].bulls / (userData[currUser]["holes"][self.hole - 1].failedBulls + userData[currUser]["holes"][self.hole - 1].bulls)

            userData[currUser]["failed bulls"] += 1
            userData[currUser]["bull rate"] = userData[currUser]["bulls"] / (userData[currUser]["failed bulls"] + userData[currUser]["bulls"])

            mastersData[str(self.hole)]["failed bulls"] += 1
            mastersData[str(self.hole)]["bull rate"] = mastersData[str(self.hole)]["bulls"] / (mastersData[str(self.hole)]["bulls"] + mastersData[str(self.hole)]["failed bulls"])
        else:
            if int(self.puttField.text) < int(self.scoreField.text) - 1:
                userData[currUser]["holes"][self.hole - 1].failedSaves += 1
                userData[currUser]["holes"][self.hole - 1].saveRate = userData[currUser]["holes"][self.hole - 1].saves / (userData[currUser]["holes"][self.hole - 1].failedSaves + userData[currUser]["holes"][self.hole - 1].saves)

                userData[currUser]["failed saves"] += 1
                userData[currUser]["save rate"] = userData[currUser]["saves"] / (userData[currUser]["failed saves"] + userData[currUser]["saves"])

                mastersData[str(self.hole)]["failed saves"] += 1
                mastersData[str(self.hole)]["save rate"] = mastersData[str(self.hole)]["saves"] / (mastersData[str(self.hole)]["saves"] + mastersData[str(self.hole)]["failed saves"])

            if int(self.puttField.text) == int(self.scoreField.text) - 1:
                self.greens += 1

                userData[currUser]["holes"][self.hole - 1].greens += 1
                userData[currUser]["holes"][self.hole - 1].greenRate = userData[currUser]["holes"][self.hole - 1].greens / (userData[currUser]["holes"][self.hole - 1].greens + userData[currUser]["holes"][self.hole - 1].failedGreens)

                userData[currUser]["greens"] += 1
                userData[currUser]["green rate"] = userData[currUser]["greens"] / (userData[currUser]["greens"] + userData[currUser]["failed greens"])

                mastersData[str(self.hole)]["greens"] += 1
                mastersData[str(self.hole)]["green rate"] = mastersData[str(self.hole)]["greens"] / (mastersData[str(self.hole)]["bulls"] + mastersData[str(self.hole)]["failed greens"])
            else:
                userData[currUser]["holes"][self.hole - 1].failedGreens += 1
                userData[currUser]["holes"][self.hole - 1].greenRate = userData[currUser]["holes"][self.hole - 1].greens / (userData[currUser]["holes"][self.hole - 1].greens + userData[currUser]["holes"][self.hole - 1].failedGreens)

                userData[currUser]["failed greens"] += 1
                userData[currUser]["green rate"] = userData[currUser]["greens"] / (userData[currUser]["greens"] + userData[currUser]["failed greens"])

                mastersData[str(self.hole)]["failed greens"] += 1
                mastersData[str(self.hole)]["green rate"] = mastersData[str(self.hole)]["greens"] / (mastersData[str(self.hole)]["greens"] + mastersData[str(self.hole)]["failed greens"])

            userData[currUser]["holes"][self.hole - 1].failedBulls += 1
            userData[currUser]["holes"][self.hole - 1].bullRate = userData[currUser]["holes"][self.hole - 1].bulls / (userData[currUser]["holes"][self.hole - 1].failedBulls + userData[currUser]["holes"][self.hole - 1].bulls)

            userData[currUser]["failed bulls"] += 1
            userData[currUser]["bull rate"] = userData[currUser]["bulls"] / (userData[currUser]["failed bulls"] + userData[currUser]["bulls"])

            mastersData[str(self.hole)]["failed bulls"] += 1
            mastersData[str(self.hole)]["bull rate"] = mastersData[str(self.hole)]["bulls"] / (mastersData[str(self.hole)]["bulls"] + mastersData[str(self.hole)]["failed bulls"])

            userData[currUser]["holes"][self.hole - 1].failedPars += 1
            userData[currUser]["holes"][self.hole - 1].parRate = userData[currUser]["holes"][self.hole - 1].pars / (userData[currUser]["holes"][self.hole - 1].failedPars + userData[currUser]["holes"][self.hole - 1].pars)

            userData[currUser]["failed pars"] += 1
            userData[currUser]["par rate"] = userData[currUser]["pars"] / (userData[currUser]["failed pars"] + userData[currUser]["pars"])

            mastersData[str(self.hole)]["pars"] += 1
            mastersData[str(self.hole)]["pars rate"] = mastersData[str(self.hole)]["bulls"] / (mastersData[str(self.hole)]["pars"] + mastersData[str(self.hole)]["failed pars"])

    def updateHole(self):
        if self.scoreField.text in map(str,range(1,100)) and self.puttField.text in map(str,range(100)) and int(self.scoreField.text) > int(self.puttField.text):
            self.updateData()
            self.hole += 1
            self.name.text = "Hole: " + str(self.hole)
            self.descriptionID.text = str(mastersData[str(self.hole)]["description"])
            self.userBestScore.text = "Best Score: " + str(userData[currUser]["holes"][self.hole - 1].bestScore)
            self.average.text = "Average Score: " + str(round(mastersData[str(self.hole)]["average"],1))
            self.userAverageScore.text = "Average Score: " + str(round(userData[currUser]["holes"][self.hole - 1].avgScore,1))
            self.index.text = "Stroke Index: " + str(mastersData[str(self.hole)]["index"])
            self.userPar.text = "Par Percent: " + str(round(userData[currUser]["holes"][self.hole - 1].parRate * 100,0)) + "%"
            self.userGreen.text = "On Percent: " + str(round(userData[currUser]["holes"][self.hole - 1].greenRate * 100,0)) + "%"
            self.coursePar.text = "Par Percent: " + str(round(mastersData[str(self.hole - 1)]["par rate"] * 100,0)) + "%"
            self.courseGreen.text = "On Percent: " + str(round(mastersData[str(self.hole - 1)]["on rate"] * 100, 0)) + "%"
            self.distance.text = "Distance: " + str(mastersData[str(self.hole)]["distance"]) + " yds"
            self.scoreField.text = ""
            self.puttField.text = ""
        else:
            if not self.scoreField.text in map(str,range(1,100)):
                self.errorMessage.text = "Enter Your Score"
            else:
                self.errorMessage.text = "Enter Your Putts"
            Clock.schedule_once(self.failInputEnd,2)

    def startGame(self):
        self.hole += 1
        self.name.text = "Hole: " + str(self.hole)
        self.descriptionID.text = str(mastersData[str(self.hole)]["description"])
        self.course.text = "Course:"
        self.user.text = "You:"
        self.userBestScore.text = "Best Score: " + str(userData[currUser]["holes"][self.hole - 1].bestScore)
        self.average.text = "Average Score: " + str(round(mastersData[str(self.hole)]["average"], 1))
        self.userAverageScore.text = "Average Score: " + str(round(userData[currUser]["holes"][self.hole - 1].avgScore, 1))
        self.index.text = "Stroke Index: " + str(mastersData[str(self.hole)]["index"])
        self.userPar.text = "Par Percent: " + str(round(userData[currUser]["holes"][self.hole - 1].parRate * 100, 0)) + "%"
        self.userGreen.text = "On Percent: " + str(round(userData[currUser]["holes"][self.hole - 1].greenRate * 100, 0)) + "%"
        self.coursePar.text = "Par Percent: " + str(round(mastersData[str(self.hole)]["par rate"] * 100, 0)) + "%"
        self.courseGreen.text = "On Percent: " + str(round(mastersData[str(self.hole)]["on rate"] * 100, 0)) + "%"
        self.distance.text = "Distance: " + str(mastersData[str(self.hole)]["distance"]) + " yds"
        self.scoreField.background_normal = "White.png"
        self.scoreField.background_active = "White.png"
        self.puttField.background_normal = "White.png"
        self.puttField.background_active = "White.png"
        self.scoreLabel.text = "Score: "
        self.puttLabel.text = "Putts: "
        self.scoreField.text = ""
        self.puttField.text = ""


    def failInputEnd(self, dt):
        self.errorMessage.text = ""

class GameBackground(Widget):
    pass

class GameScreen(Screen):
    pass



class StatsButtonsHoles(Widget):
    global userData
    global currUser

class StatsBackgroundHoles(Widget):
    pass

class StatsScreenHoles(Screen):
    pass



class StatsButtonsCourse(Widget):
    pass

class StatsBackgroundCourse(Widget):
    pass

class StatsScreenCourse(Screen):
    pass




class EndScreenButtons(Widget):
    pass

class EndScreenBackground(Widget):
    pass

class EndScreen(Screen):
    pass



class CourseButtons(Widget):
    pass

class CourseBackground(Widget):
    pass

class CourseScreen(Screen):
    pass



class CourseButtons2(Widget):
    pass

class CourseBackground2(Widget):
    pass

class CourseScreen2(Screen):
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