'''
TODO
[x] nice Name 😉 -> tourmutation (every possible permutation in a tournament)
[x] give user input option
   [x] insert competitors
   [x] print to file?
[~] print of results -> only for 4 and 8 competitors
[x] print command output optional to file
[x] Error check
   [x] If the user input is correct! (only 4, 8, 16, ... competitors)
[x] make a cli by using typer
    tourmutation --example
    tourmutation --help
    tourmutation --output
    tourmutation --example --output
''' 

import typer
from collections import UserString
import json
import os
import re
import math
from num2words import num2words

#define global variables
results = {}
printResults = False
debugingOutput = False

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

def getUserInput() -> list:
    noCorrectInput = True
    competitorslist = list()
    while noCorrectInput:
        userInput = input("How many competiors do your tournament have?\n")
        if re.match("[0-9]+", userInput):
            userInputInt = int(userInput)
            if userInputInt != 0 and float(math.log(userInputInt,2)).is_integer:
                for i in range(userInputInt):
                    competitor = input("Please insert your " + num2words(i+1, to="ordinal_num") + " competitor:\n")
                    competitorslist.append(competitor)
                noCorrectInput = False
            else:
                print("Please output only numbers that are a power of 2")
                noCorrectInput = True
        else:
            print("Please make a correct input!")
            noCorrectInput = True
    return competitorslist


def output(results: dir, competitorslist: list):
        #write json file
        if debugingOutput:
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

def mainCalculation(competitorslist: list):
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
        
    output(results, competitorslist)


def getExample(example: int) -> list:
    if example == 1:
        #Uefa Euro 2020 (Round of 4)
        competitorslist = [
            "Italy",
            "Spain",
            "England",
            "Denmark"
        ]
    elif example == 2:
        #Uefa Euro 2020 (Round of 8)
        competitorslist = [
            "Belgium",
            "Italy",
            "Switzerland",
            "Spain",
            "Ukraine",
            "England",
            "Czech Republic",
            "Denmark"
        ]
    elif example == 3:
        #Uefa Euro 2020 (Round of 16)
        competitorslist = [
            "Belgium",
            "Portugal",
            "Italy",
            "Austria",
            "France",
            "Switzerland",
            "Croatia",
            "Spain",
            "Sweden",
            "Ukraine",
            "England",
            "Germany",
            "Netherlands",
            "Czech Repbulic",
            "Walse",
            "Denmark"
        ]
    return competitorslist

def main(
        export: bool = typer.Option(False, help="Do you want an export of the result as txt?"),
        example: int = typer.Option(0, help="An example with the competiors of the Uefa 2021.\n 1 = Round of 4\n 2 = Round of 8\n 3 = Round of 16"),
        debug: bool = typer.Option(False, help="If you want to get the json of the permutations.")
    ):
        if export:
            printResults = True
        else:
            printResult = False
        if debug:
            debugingOutput = True
        else:
            debugingOutput = False
        
        if example != 0:
            competitorslist = getExample(example)
        else:
            competitorslist = getUserInput()
        mainCalculation(competitorslist)


if __name__ == "__main__":
    typer.run(main)