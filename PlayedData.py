class Game:
    def __init__(self,frontScore,frontPutts,backScore,backPutts,totalScore,totalPutts,datePlayed):
        self.frontScore = frontScore
        self.frontPutts = frontPutts
        self.backScore = backScore
        self.backPutts = backPutts
        self.totalScore = totalScore
        self.totalPutts = totalPutts
        self.datePlayed = datePlayed

class Hole:
    def __init__(self,scores,putts,bestScore,avgScore,pars,bulls,saves,parRate,bullRate,saveRate):
        self.scores = scores
        self.putts = putts
        self.bestScore = bestScore
        self.avgScore = avgScore
        self.pars = pars
        self.bulls = bulls
        self.saves = saves
        self.parRate = parRate
        self.bullRate = bullRate
        self.saveRate = saveRate