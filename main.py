#fix bug with rates


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
    data = hole.split(",")
    mastersData[data[0]] = {}
    mastersData[data[0]]["description"] = data[1]
    mastersData[data[0]]["scores"] = list(map(int,data[2][1:-1].split(";")))
    mastersData[data[0]]["low"] = int(data[3])
    mastersData[data[0]]["high"] = int(data[4])
    mastersData[data[0]]["average"] = float(data[5])
    mastersData[data[0]]["index"] = int(data[6])
    mastersData[data[0]]["distance"] = int(data[7])
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

class MainBackground(Widget):
    pass

class MainScreen(Screen):
    pass



class GameButtons(Widget):
    global mastersData
    global userData
    global currUser

    hole = 1
    description = mastersData[str(hole)]["description"]
    bestScore = mastersData[str(hole)]["low"]
    averageScore = round(mastersData[str(hole)]["average"],1)
    yards = mastersData[str(hole)]["distance"]
    strokeIndex = mastersData[str(hole)]["index"]

    userBest = userData[currUser]["holes"][0].bestScore
    userAverage = round(userData[currUser]["holes"][0].avgScore,1)
    userPR = round(userData[currUser]["holes"][0].parRate,1) * 100
    userGR = round(userData[currUser]["holes"][0].parRate,1) * 100

    frontScore = 0
    frontPutts = 0
    backScore = 0
    backPutts = 0
    score = 0
    putts = 0

    def writeData(self):
        open("Users.txt","w").close()

        file = open("Users.txt","w")
        lines = []
        for user in userData:
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
                line += str(hole.saveRate) + ")-"
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

        file = open("User.txt","w")
        file.writelines(lines)
        file.close()



    def endGame(self):
        userData[currUser]["games"].append(Game(self.frontScore,self.frontPutts,self.bestScore,self.backPutts,self.score,self.putts,str(datetime.datetime.now().strftime("%x"))))

        sumScoreFront = userData[currUser]["games count"] * userData[currUser]["average front"]
        sumScoreBack = userData[currUser]["games count"] * userData[currUser]["average back"]
        sumScoreTotal = userData[currUser]["games count"] * userData[currUser]["average total"]
        userData[currUser]["games count"] += 1
        userData[currUser]["average front"] = (sumScoreFront + self.frontScore) / userData[currUser]["games count"]
        userData[currUser]["average back"] = (sumScoreBack + self.backScore) / userData[currUser]["games count"]
        userData[currUser]["average total"] = (sumScoreTotal + self.score) / userData[currUser]["games count"]

        if userData[currUser]["games count"] >= 5:
            total = 0
            for x in userData["games"][-5:]:
                total += x.totalScore
            userData[currUser]["average total last 5"] = total / 5

            if userData[currUser]["games count"] >= 10:
                total = 0
                for x in userData["games"][-10:]:
                    total += x.totalScore
                userData[currUser]["average total last 10"] = total / 10
            else:
                userData[currUser]["average total last 10"] = total / 5
        else:
            userData[currUser]["average total last 5"] = userData[currUser]["average total"]
            userData[currUser]["average total last 10"] = userData[currUser]["average total"]

        if self.frontScore < userData[currUser]["best front"]:
            userData[currUser]["best front"] = self.frontScore
        if self.backScore < userData[currUser]["best back"]:
            userData[currUser]["best back"] = self.backScore

        userData[currUser]["super 9"] = userData[currUser]["best front"] + userData[currUser]["best back"]

        score = 0
        for i in range(18):
            score += min(userData[currUser]["holes"][i].scores)
        userData[currUser]["super 1"] = score

        self.hole = 1
        self.description = mastersData[str(self.hole)]["description"]
        self.bestScore = mastersData[str(self.hole)]["low"]
        self.averageScore = round(mastersData[str(self.hole)]["average"], 1)
        self.yards = mastersData[str(self.hole)]["distance"]
        self.strokeIndex = mastersData[str(self.hole)]["index"]

        self.frontScore = 0
        self.frontPutts = 0
        self.backScore = 0
        self.backPutts = 0
        self.score = 0
        self.putts = 0

        self.name.text = "Hole: " + str(self.hole)
        self.descriptionID.text = str(mastersData[str(self.hole)]["description"])
        self.best.text = str(mastersData[str(self.hole)]["low"])
        self.average.text = str(round(mastersData[str(self.hole)]["average"], 1))
        self.index.text = str(mastersData[str(self.hole)]["index"])
        self.distance.text = str(mastersData[str(self.hole)]["distance"]) + " yds"
        self.scoreField.text = ""
        self.puttField.text = ""

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

        userData[currUser]["holes"][self.hole - 1].avgScore = sum(userData[currUser]["holes"][self.hole - 1].scores) / len(userData[currUser]["holes"][self.hole - 1].scores)

        if int(self.scoreField.text) < userData[currUser]["holes"][self.hole - 1].bestScore:
            userData[currUser]["holes"][self.hole - 1].bestScore = int(self.scoreField.text)

        if (int(self.scoreField.text) == 1):
            userData[currUser]["holes"][self.hole - 1].bulls += 1
            userData[currUser]["holes"][self.hole - 1].bullRate = userData[currUser]["holes"][self.hole - 1].bulls / (userData[currUser]["holes"][self.hole - 1].failedBulls + userData[currUser]["holes"][self.hole - 1].bulls)

            userData[currUser]["bulls"] += 1
            userData[currUser]["bull rate"] = userData[currUser]["bulls"] / userData[currUser]["failed bulls"]

            userData[currUser]["holes"][self.hole - 1].greens += 1
            userData[currUser]["holes"][self.hole - 1].greenRate = userData[currUser]["holes"][self.hole - 1].greens / (userData[currUser]["holes"][self.hole - 1].greens + userData[currUser]["holes"][self.hole - 1].failedGreens)

            userData[currUser]["greens"] += 1
            userData[currUser]["green rate"] = userData[currUser]["greens"] / (userData[currUser]["greens"] + userData[currUser]["failed greens"])
        elif (int(self.scoreField.text) == 2):
            if (int(self.puttField.text) == 0):
                userData[currUser]["holes"][self.hole - 1].saves += 1
                userData[currUser]["holes"][self.hole - 1].saveRate = userData[currUser]["holes"][self.hole - 1].saves / (userData[currUser]["holes"][self.hole - 1].failedSaves + userData[currUser]["holes"][self.hole - 1].saves)

                userData[currUser]["saves"] += 1
                userData[currUser]["save rate"] = userData[currUser]["saves"] / (userData[currUser]["failed saves"] + userData[currUser]["saves"])
                userData[currUser]["holes"][self.hole - 1].failedGreens += 1
                userData[currUser]["holes"][self.hole - 1].greenRate = userData[currUser]["holes"][self.hole - 1].greens / (userData[currUser]["holes"][self.hole - 1].greens +userData[currUser]["holes"][self.hole - 1].failedGreens)

                userData[currUser]["failed greens"] += 1
                userData[currUser]["green rate"] = userData[currUser]["greens"] / (userData[currUser]["greens"] + userData[currUser]["failed greens"])
            else:
                userData[currUser]["holes"][self.hole - 1].greens += 1
                userData[currUser]["holes"][self.hole - 1].greenRate = userData[currUser]["holes"][self.hole - 1].greens / (userData[currUser]["holes"][self.hole - 1].greens + userData[currUser]["holes"][self.hole - 1].failedGreens)

                userData[currUser]["greens"] += 1
                userData[currUser]["green rate"] = userData[currUser]["greens"] / (userData[currUser]["greens"] + userData[currUser]["failed greens"])


            userData[currUser]["holes"][self.hole - 1].pars += 1
            userData[currUser]["holes"][self.hole - 1].parRate = userData[currUser]["holes"][self.hole - 1].pars / (userData[currUser]["holes"][self.hole - 1].failedPars + userData[currUser]["holes"][self.hole - 1].pars)

            userData[currUser]["pars"] += 1
            userData[currUser]["par rate"] = userData[currUser]["pars"] / (userData[currUser]["failed pars"] + userData[currUser]["pars"])

            userData[currUser]["holes"][self.hole - 1].failedBulls += 1
            userData[currUser]["holes"][self.hole - 1].bullRate = userData[currUser]["holes"][self.hole - 1].bulls / (userData[currUser]["holes"][self.hole - 1].failedBulls + userData[currUser]["holes"][self.hole - 1].bulls)

            userData[currUser]["failed bulls"] += 1
            userData[currUser]["bull rate"] = userData[currUser]["bulls"] / (userData[currUser]["failed bulls"] + userData[currUser]["bulls"])
        else:
            if int(self.puttField.text) < int(self.scoreField.text) - 1:
                userData[currUser]["holes"][self.hole - 1].failedSaves += 1
                userData[currUser]["holes"][self.hole - 1].saveRate = userData[currUser]["holes"][self.hole - 1].saves / (userData[currUser]["holes"][self.hole - 1].failedSaves + userData[currUser]["holes"][self.hole - 1].saves)

                userData[currUser]["failed saves"] += 1
                userData[currUser]["save rate"] = userData[currUser]["saves"] / (userData[currUser]["failed saves"] + userData[currUser]["saves"])

            if int(self.puttField.text) == int(self.scoreField.text) - 1:
                userData[currUser]["holes"][self.hole - 1].greens += 1
                userData[currUser]["holes"][self.hole - 1].greenRate = userData[currUser]["holes"][self.hole - 1].greens / (userData[currUser]["holes"][self.hole - 1].greens + userData[currUser]["holes"][self.hole - 1].failedGreens)

                userData[currUser]["greens"] += 1
                userData[currUser]["green rate"] = userData[currUser]["greens"] / (userData[currUser]["greens"] + userData[currUser]["failed greens"])
            else:
                userData[currUser]["holes"][self.hole - 1].failedGreens += 1
                userData[currUser]["holes"][self.hole - 1].greenRate = userData[currUser]["holes"][self.hole - 1].greens / (userData[currUser]["holes"][self.hole - 1].greens + userData[currUser]["holes"][self.hole - 1].failedGreens)

                userData[currUser]["failed greens"] += 1
                userData[currUser]["green rate"] = userData[currUser]["greens"] / (userData[currUser]["greens"] + userData[currUser]["failed greens"])

            userData[currUser]["holes"][self.hole - 1].failedBulls += 1
            userData[currUser]["holes"][self.hole - 1].bullRate = userData[currUser]["holes"][self.hole - 1].bulls / (userData[currUser]["holes"][self.hole - 1].failedBulls + userData[currUser]["holes"][self.hole - 1].bulls)

            userData[currUser]["failed bulls"] += 1
            userData[currUser]["bull rate"] = userData[currUser]["bulls"] / (userData[currUser]["failed bulls"] + userData[currUser]["bulls"])

            userData[currUser]["holes"][self.hole - 1].failedPars += 1
            userData[currUser]["holes"][self.hole - 1].parRate = userData[currUser]["holes"][self.hole - 1].pars / (userData[currUser]["holes"][self.hole - 1].failedPars + userData[currUser]["holes"][self.hole - 1].pars)

            userData[currUser]["failed pars"] += 1
            userData[currUser]["par rate"] = userData[currUser]["pars"] / (userData[currUser]["failed pars"] + userData[currUser]["pars"])

    def updateHole(self):
        if self.scoreField.text in map(str,range(1,100)) and self.puttField.text in map(str,range(100)):
            self.updateData()
            self.hole += 1
            self.name.text = "Hole: " + str(self.hole)
            self.descriptionID.text = str(mastersData[str(self.hole)]["description"])
            self.userBestScore.text = "Best Score: " + str(userData[currUser]["holes"][self.hole].bestScore)
            self.average.text = "Average Score: " + str(round(mastersData[str(self.hole)]["average"],1))
            self.userAverageScore.text = "Average Score: " + str(round(userData[currUser]["holes"][self.hole].avgScore,1))
            self.index.text = "Stroke Index: " + str(mastersData[str(self.hole)]["index"])
            self.userPar.text = "Par Percent: " + str(round(userData[currUser]["holes"][self.hole].parRate) * 100) + "%"
            self.userPar.text = "On Percent: " + str(round(userData[currUser]["holes"][self.hole].greenRate) * 100) + "%"
            self.distance.text = "Distance: " + str(mastersData[str(self.hole)]["distance"]) + " yds"
            # add on percent and par percent for the hole after hole data is updated
            self.scoreField.text = ""
            self.puttField.text = ""
        else:
            if not self.scoreField.text in map(str,range(1,100)):
                self.errorMessage.text = "Enter Your Score"
            else:
                self.errorMessage.text = "Enter Your Putts"
            Clock.schedule_once(self.failInputEnd,2)

    def failInputEnd(self, dt):
        self.errorMessage.text = ""

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