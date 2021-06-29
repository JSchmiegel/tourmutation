from random import *
import json

results = {"games": []}

class game:
    
    def __init__(self, contestant1, contestant2):
        self.contestant1 = contestant1
        self.contestant2 = contestant2
        self.winner = None
        self.loser = None


    def play(self, binary):
        if (binary > 0):
            self.winner = self.contestant2
            self.loser = self.contestant1
        else:
            self.winner = self.contestant1
            self.loser = self.contestant2

def playLayer(layer, level, binary, gameNumber):
    global results
    
    newLayer = list()
    for g in layer:
        winner = int(str(binary)[-1])
        g.play(winner)
        tmpstr = str(g.contestant1) + " vs. " + str(g.contestant2)
        results["games"].append({
            "contestant": tmpstr, 
            "level": level, 
            "winner": g.winner, 
            "gameNumber": int(gameNumber)
        })
        binary = bin(int(binary, 2) >> 1)
    if len(layer) > 1:
        i = 0
        while i < len(layer)-1:
            newLayer.append(game(layer[i].winner,layer[i+1].winner))
            i = i + 2
        playLayer(newLayer, level + 1, binary, gameNumber)
    newLayer.clear()

#Uefa Euro 2016 (Round of 16)
# playerslist = [
#     "Schweiz",
#     "Polen",
#     "Kroatien",
#     "Portugal",
#     "Wales",
#     "Nordirland",
#     "Ungarn",
#     "Belgien",
#     "Deutschland",
#     "Slowakei",
#     "Italien",
#     "Spanien",
#     "Frankreich",
#     "Irland",
#     "England",
#     "Island"
# ]
#Uefa Euro 2016 (Round of 8)
playerslist = [
    "Polen",
    "Portugal",
    "Wales",
    "Belgien",
    "Deutschland",
    "Italien",
    "Frankreich",
    "Island"
]
#Uefa Euro 2016 (Round of 4)
# playerslist = [
#     "Portugal",
#     "Wales",
#     "Deutschland",
#     "Frankreich"
# ]

##main
games = list()

#calculate all options (parsed as binary number) (only semifinals!!)
probability = list()
numberOfPermutation = 2**(len(playerslist)-1)
for i in range(numberOfPermutation):
    probability.append(bin(i))

j = 0
for el in probability:
    games.clear()
    i = 0
    while i < len(playerslist):
        games.append(game(playerslist[i], playerslist[i+1]))
        i = i + 2
    playLayer(games, 0, el, j)
    j = j+1

#output
resultsSort = sorted(results["games"], key=lambda x : x["gameNumber"], reverse=False)
with open("permutations.json", "w") as file:
    json.dump(resultsSort, file)
for entry in resultsSort:
    tmp = ""
    for i in range(entry["level"] * 20):
        tmp += " "
    print(tmp + str(entry["gameNumber"]) +  " " + entry["contestant"] + " --> " + entry["winner"])
print()