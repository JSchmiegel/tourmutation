from random import *


class game:
    
    def __init__(self, contestant1, contestant2):
        self.contestant1 = contestant1
        self.contestant2 = contestant2
        self.winner = None
        self.loser = None


    def play(self, overheadPrint):
        i = randint(1,2)
        if (i > 1):
            self.winner = self.contestant2
            self.loser = self.contestant1
        else:
            self.winner = self.contestant1
            self.loser = self.contestant2
        tmp = " "
        for i in range(overheadPrint):
            tmp += " "
        print(tmp + str(self.contestant1) + " vs. " + str(self.contestant2) + " --> " + str(self.winner))

def playLayer(layer, overheadPrint):
    newLayer = list()

    for g in layer:
        g.play(overheadPrint)
    if len(layer) > 1:
        i = 0
        while i < len(layer):
            newLayer.append(game(layer[i].winner,layer[i+1].winner))
            i = i + 2
        playLayer(newLayer, overheadPrint + 20)

#Uefa Euro 2016 (Round of 16)
playerslist = [
    "Schweiz",
    "Polen",
    "Kroatien",
    "Portugal",
    "Wales",
    "Nordirland",
    "Ungarn",
    "Belgien",
    "Deutschland",
    "Slowakei",
    "Italien",
    "Spanien",
    "Frankreich",
    "Irland",
    "England",
    "Island"
]

##main
games = list()
i = 0
while i < len(playerslist):
    games.append(game(playerslist[i], playerslist[i+1]))
    i = i + 2
playLayer(games, 0)