'''
TODO
[ ] nice Name 😉
[ ] give user input option
   [ ] insert competitors
   [x] print to file?
[~] print of results -> only for 4 and 8 competitors
[x] print command output optional to file
[ ] Error check
   [ ] If the user input is correct! (only 4, 8, 16, ... competitors)
''' 


from collections import UserString
import json
import os
import re

#define global variables
results = {}
printResults = True

class game:
    
    def __init__(self, competitors1, competitors2):
        self.competitors1 = competitors1
        self.competitors2 = competitors2
        self.winner = None
        self.loser = None


    def play(self, binary):
        if (binary > 0):
            self.winner = self.competitors2
            self.loser = self.competitors1
        else:
            self.winner = self.competitors1
            self.loser = self.competitors2

def playLayer(layer, level, binary, gameNumber):
    global results
    
    newLayer = list()
    for g in layer:
        winner = int(str(binary)[-1])
        g.play(winner)
        results["Permutation "+ str(gameNumber)].append({
            "competitors": {
                "1": str(g.competitors1),
                "2": str(g.competitors2)
            },
            "level": level, 
            "winner": g.winner
        })
        binary = bin(int(binary, 2) >> 1)
    if len(layer) > 1:
        i = 0
        while i < len(layer)-1:
            newLayer.append(game(layer[i].winner,layer[i+1].winner))
            i = i + 2
        playLayer(newLayer, level + 1, binary, gameNumber)
    newLayer.clear()


def fillString(insert, end):
    while len(insert) < end:
        insert += " "
    return insert

def printResult(output):
    if printResults:
        with open("output.txt", "a") as f:
            f.write (output + "\n")
    print(output)

def getUserInput():
    noCorrectInput = True
    while noCorrectInput:
        userInput = input("Do you want to save the result as txt file? [Y/N]")
        if re.match("(Y|y)((E|e)(S|s))?", userInput):
            printResults = True
            noCorrectInput = False
        elif re.match("(N|n)(O|o)?", userInput):
            printResults = False
            noCorrectInput = False
        else:
            print("Please make a correct input!")
            noCorrectInput = True



##main

getUserInput()

#Uefa Euro 2016 (Round of 16)
# competitorslist = [
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
# competitorslist = [
#     "Polen",
#     "Portugal",
#     "Wales",
#     "Belgien",
#     "Deutschland",
#     "Italien",
#     "Frankreich",
#     "Island"
# ]
#Uefa Euro 2016 (Round of 4)
competitorslist = [
    "Portugal",
    "Wales",
    "Deutschland",
    "Frankreich"
]

games = list()

#calculate all options (parsed as binary number)
probability = list()
numberOfPermutation = 2**(len(competitorslist)-1)
for i in range(numberOfPermutation):
    probability.append(bin(i))

j = 0
for el in probability:
    games.clear()
    i = 0
    while i < len(competitorslist):
        games.append(game(competitorslist[i], competitorslist[i+1]))
        i = i + 2
    results.update({
        "Permutation " + str(j): []
    })
    playLayer(games, 0, el, j)
    j = j + 1



#####output

#write json file
with open("permutations.json", "w") as file:
    json.dump(results, file, indent=4)

#write output commandline and file
toManyGames = False

if os.path.exists("output.txt"):
    os.remove("output.txt")
for permutation in results:
    printResult("#### " + permutation + " ####\n")
    
    if len(competitorslist) == 4:
        printResult(results[permutation][0]["competitors"]["1"])
        printResult("    |--------" + results[permutation][0]["winner"])
        printResult(fillString(results[permutation][0]["competitors"]["2"], 15) + "|")
        printResult(fillString("", 15) + "|--------" + results[permutation][0+2]["winner"])
        printResult(fillString(results[permutation][1]["competitors"]["1"], 15) + "|")
        printResult("    |--------" + results[permutation][1]["winner"])
        printResult(results[permutation][1]["competitors"]["2"])
    elif len(competitorslist) == 8:
        printResult(results[permutation][0]["competitors"]["1"])
        printResult("    |--------" + results[permutation][0]["winner"])
        printResult(fillString(results[permutation][0]["competitors"]["2"], 15) + "|")
        printResult(fillString("", 15) + "|--------" + results[permutation][0+4]["winner"])
        printResult(fillString(fillString(results[permutation][1]["competitors"]["1"], 15) + "|", 27) + "|")
        printResult(fillString("    |--------" + results[permutation][1]["winner"], 27) + "|")
        printResult(fillString(results[permutation][1]["competitors"]["2"], 27) + "|")
        printResult(fillString("", 27) + "|--------" + results[permutation][1+4]["winner"])
        printResult(fillString(results[permutation][2]["competitors"]["1"], 27) + "|")
        printResult(fillString("    |--------" + results[permutation][2]["winner"], 27) + "|")
        printResult(fillString(fillString(results[permutation][2]["competitors"]["2"], 15) + "|", 27) + "|")
        printResult(fillString("", 15) + "|--------" + results[permutation][2+3]["winner"])
        printResult(fillString(results[permutation][3]["competitors"]["1"], 15) + "|")
        printResult("    |--------" + results[permutation][3]["winner"])
        printResult(results[permutation][3]["competitors"]["2"])
    else:
        toManyGames = True

    printResult("\n\n")
    
if toManyGames:
    printResult("Saddly there is no nice output for this many games. 😥")