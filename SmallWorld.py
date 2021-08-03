# Small World Simulator
import requests
import json
import pprint


# Step 1: YDK Extractor
stack =[]
stack.append("A")
stack.append("B")
stack.append("C")
stack2 = stack.copy()
stack.pop()
print(stack)
print(stack2)
str1 = "bob"
str2 = "bob"
if str1 == str2:
    print("yessir")
with open('VW.ydk') as f:  # Change to your deck file name here
    deck = f.read().splitlines()
deck.pop(0)
deck.pop(0)
decksize = deck.index("#extra")
deck = deck[:decksize]
deck = list(set(deck))

deckmonsters = {}
monsterbridges = {}
print("hello ")
# Step 2: API Calls
for card in deck:
    response = requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?id={card}")
    info = json.loads(response.text)
    info = info["data"][0]

    if "Monster" in info["type"]:
        deckmonsters[info["name"]] = {"ATK": info["atk"], "DEF": info["def"], "Attribute": info["attribute"],
                                      "Type": info["race"], "Level": info["level"]}

pprint.pprint(deckmonsters)


# Step 3: Actual Logic

def getScore(card, comparison):
    score = 0
    for key in card:
        if card[key] == comparison[key]:
            score = score + 1
    return score


for card in deckmonsters:
    monsterbridges[card] = []
    for key in deckmonsters:
        score = getScore(deckmonsters[card], deckmonsters[key])
        if score == 1:
            print(f"Card {card} bridges with {key}")
            monsterbridges[card].append(key)

pprint.pprint(monsterbridges)
# Right Now, monster-bridges is a dict with all cards that connect to each other. Now, we want to output all the cards each card can search

f = open("output.txt", "a")
f.truncate(0)
for card in monsterbridges:
    for key in monsterbridges[card]:
        for target in monsterbridges[key]:
            print(f"Banish {card} ---> Reveal {key} ---> Add {target}")
            f.write(f"Banish {card} ---> Reveal {key} ---> Add {target}\n")