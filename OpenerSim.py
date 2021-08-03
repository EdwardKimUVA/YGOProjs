import requests
import json
import pprint
import random
from anytree import Node, RenderTree

xorindex = 0
xorlist = []

orindex = 0
orlist = []

andindex = 0
andlist = []

notindex = 0
notlist = []

testhand = []
success = 0

def xor_(str1, str2):
    if duplicates(str1) > 1 and str1 == str2:
        return "F"
    elif str1 == "T" and str2 == "F":
        return "T"
    elif str1 == "F" and str2 == "T":
        return "T"
    elif str1 == "T" and not contains(str2):
        return "T"
    elif str2 == "T" and not contains(str1):
        return "T"
    elif contains(str1) and not contains(str2):
        return "T"
    elif contains(str1) and not contains(str2):
        return "T"
    return "F"

def or_(str1, str2):
    if str1 == "T" or str2 == "T":
        return "T"
    elif contains(str1) or contains(str2):
        return "T"
    return "F"

def and_(str1, str2):
    if duplicates(str1) > 1 and str1 == str2:
        #print(testhand)
        return "T"
    elif contains(str1) and str1 != str2:
        if contains(str2):
            return "T"
    elif str1 == "T" and str2 == "T":
        return "T"
    elif str1 =="T" and contains(str2):
        return "T"
    elif str2 =="T" and contains(str1):
        return "T"
    return "F"

def not_(str1):
    if str1 == "T":
        return "F"
    elif str1 == "F":
        return "T"
    elif contains(str1):
        return "F"
    else:
        return "T"

def triple(str1):
    count = 0
    for x in testhand:
        if x == str1:
            count += 1
    if count == 3:
        return "T"
    return "F"

def newhand():
    if testhand:
        testhand.clear()
    for x in range(handsize):
        random.shuffle(deckTranslated)
        testhand.append(deckTranslated[x])
def contains (str):
    for x in testhand:
        if x == str:
            return True
    return False
def duplicates(str):
    countdupes = 0
    #print(testhand)
    for x in testhand:
        if x == str:
            countdupes +=1
    return countdupes
# Step 1: YDK Extractor
from Tools.scripts.treesync import raw_input

with open('VW.ydk') as f: #Change to your deck file name here
    deck = f.read().splitlines()
#print(deck[0])
deck.pop(0)
#print(deck[0])
deck.pop(0)
#print(deck)
decksize = deck.index("#extra")
deck = deck[:decksize]
#print(deck)
deckTranslated = []
#deck = list(set(deck))
# Step 2: API Calls
for card in deck:
    response = requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?id={card}")
    info = json.loads(response.text)
    info = info["data"][0]
    deckTranslated.append(info["name"])
    #if "Monster" in info["type"]:
        #deckmonsters[info["name"]] = {"ATK": info["atk"],"DEF": info["def"], "Attribute": info["attribute"],"Type": info["race"], "Level": info["level"]}
print("Cards in deck: ")
pprint.pprint(deckTranslated)
#random.shuffle(deckTranslated)
#pprint.pprint(deckTranslated)
print("Welcome to the opener simulator")
simNum = int(input("insert number of simulations that you would like to run: "))
handsize = int(input("number of cards drawn for hand?: "))
again = True
inputstack = []
denom = simNum
while again:
    print("Type in the logic expression in postfix order by inserting the name of the card one by one OR by inputting")
    print("XOR, AND, NOR, or OR. In addition, you can type 'triple' for the logical equivalence of A & A & A")
    print("Type in 'DONE' when you want to run simulations")
    simOption = input("insert card name or logic operator here: ")
    if simOption == "DONE" or simOption =="done":
        again = False
    else:
        inputstack.append(simOption)
stack = []
#inputcopy = inputstack.copy()
combofound = 0
while(simNum > 0):
    newhand()
    inputcopy = inputstack.copy()
    while(inputcopy):
        itemstack = inputcopy.pop(0)
        if itemstack == "AND":
            item1 = stack.pop()
            item2 = stack.pop()
            stack.append(and_(item1, item2))
        elif itemstack == "OR":
            item1 = stack.pop()
            item2 = stack.pop()
            stack.append(or_(item1, item2))
        elif itemstack == "XOR":
            item1 = stack.pop()
            item2 = stack.pop()
            stack.append(xor_(item1, item2))
        elif itemstack == "NOT":
            item1 = stack.pop()
            stack.append(not_(item1))
        elif itemstack == "triple":
            item1 = stack.pop()
            stack.append(triple(item1))
        else:
            stack.append(itemstack)
    simNum -= 1
    finalitem = stack.pop()
    if finalitem == "T":
        combofound+=1
print(f'{combofound/denom*100} percent success rate at drawing this combination')
#simulate(simNum)

print("Done")
#print (deck)