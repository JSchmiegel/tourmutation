#[ ] Error check
#   [ ] If the user input is correct! (only 4, 8, 16, ... competitors)
#[~] print of results -> only for 4 and 8 competitors
#[ ] print command output optional to file


import json
from os import rename

results = {}

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


##main

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

#calculate all options (parsed as binary number) (only semifinals!!)
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

#sort the dictonary by gameNumber
# resultsSorted = sorted(results["games"], key=lambda x : x["gameNumber"], reverse=False)

#write json file
with open("permutations.json", "w") as file:
    json.dump(results, file, indent=4)

#write output txt file
for permutation in results:
    print("#### " + permutation + " ####\n")
    
    if len(competitorslist) == 4:
        print(results[permutation][0]["competitors"]["1"])
        print("    |--------" + results[permutation][0]["winner"])
        print(fillString(results[permutation][0]["competitors"]["2"], 15) + "|")
        print(fillString("", 15) + "|--------" + results[permutation][0+2]["winner"])
        print(fillString(results[permutation][1]["competitors"]["1"], 15) + "|")
        print("    |--------" + results[permutation][1]["winner"])
        print(results[permutation][1]["competitors"]["2"])

    elif len(competitorslist) == 8:
        print(results[permutation][0]["competitors"]["1"])
        print("    |--------" + results[permutation][0]["winner"])
        print(fillString(results[permutation][0]["competitors"]["2"], 15) + "|")
        print(fillString("", 15) + "|--------" + results[permutation][0+4]["winner"])
        print(fillString(fillString(results[permutation][1]["competitors"]["1"], 15) + "|", 27) + "|")
        print(fillString("    |--------" + results[permutation][1]["winner"], 27) + "|")
        print(fillString(results[permutation][1]["competitors"]["2"], 27) + "|")
        print(fillString("", 27) + "|--------" + results[permutation][1+4]["winner"])
        print(fillString(results[permutation][2]["competitors"]["1"], 27) + "|")
        print(fillString("    |--------" + results[permutation][2]["winner"], 27) + "|")
        print(fillString(fillString(results[permutation][2]["competitors"]["2"], 15) + "|", 27) + "|")
        print(fillString("", 15) + "|--------" + results[permutation][2+3]["winner"])
        print(fillString(results[permutation][3]["competitors"]["1"], 15) + "|")
        print("    |--------" + results[permutation][3]["winner"])
        print(results[permutation][3]["competitors"]["2"])

    else:
        print("Saddly there is no nice output for this many games. 😥")

    # for entry in results[permutation]:
    #     if entry["level"] == 0:
    #         print(entry["competitors"]["1"])
    #         print("    |--------")
    #         print(entry["competitors"]["2"])
    print("\n\n")