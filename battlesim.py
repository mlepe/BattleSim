import os
import sys
import math
import random
import numpy
import pygame
pygame.init()

e = numpy.arange(15).reshape(3, 5)
print(e)

# Game and classes init
isRunning = True
command = ""
turn = 0
turnIncrement = 0
battleTurn = 0
random.seed()  # Init random number generator seed
global numberOfItems
global numberOfBattles
global numberOfActors
numberOfItems = 0
numberOfBattles = 0
numberOfActors = 0
global battles
battles = []


class Battle:
    def __init__(self, persons=[]):
        global numberOfBattles
        global battles
        numberOfBattles = numberOfBattles + 1
        self.id = numberOfBattles
        self.persons = persons
        battles.append(self)

    def setTurnOrder(self):
        self.turnOrder = []
        self.toCheck = []
        for i in range(0, len(self.persons), 1):
            roll, ir = roll2d6o()
            self.persons[i].initAndRoll = self.persons[i].initiative + roll
            self.toCheck.append(self.persons[i].initAndRoll)
        self.initiative = 0
        for i in range(0, len(self.persons), 1):
            self.maxInitiative = max(self.toCheck)
            if self.persons[i].initAndRoll == self.maxInitiative:
                self.turnOrder.append(self.persons[i])
                self.toCheck.remove(self.persons[i].initAndRoll)
        print(self.turnOrder[0].initiative, self.turnOrder[0].initAndRoll, self.turnOrder[0].name, self.turnOrder[1].initiative, self.turnOrder[1].initAndRoll, self.turnOrder[1].name)


# Item class and subclasses
class Item:
    def __init__(self, name, tier):
        global numberOfItems
        numberOfItems = numberOfItems + 1
        self.id = numberOfItems
        self.name = name
        self.tier = tier
        self.category = "item"
        self.subcategory = "miscellaneous"


# Armor class and subclasses
class Armor(Item):
    def __init__(self, name, armor, defense, tier):
        Item.__init__(self, name, tier)
        self.name = name
        self.armor = armor
        self.defense = defense
        self.tier = tier
        self.category = "armor"
        self.subcategory = "miscellaneous"

    def printInfo(self):
        print(self.id, self.name, self.armor, self.defense, self.tier, self.category + "/" + self.subcategory)


class Clothes(Armor):
    def __init__(self, name="clothes", armor=0, defense=5, tier=1):
        Armor.__init__(self, name, 0, 5, 1)
        self.name = name
        self.armor = armor
        self.defense = defense
        self.tier = tier
        self.subcategory = "clothes"


class LightArmor(Armor):
    def __init__(self, name="light armor", armor=3, defense=2, tier=1):
        Armor.__init__(self, name, 3, 2, 1)
        self.name = name
        self.armor = armor
        self.defense = defense
        self.tier = tier
        self.subcategory = "light"


class MediumArmor(Armor):
    def __init__(self, name="medium armor", armor=5, defense=0, tier=1):
        Armor.__init__(self, name, 5, 0, 1)
        self.name = name
        self.armor = armor
        self.defense = defense
        self.tier = tier
        self.subcategory = "medium"


class HeavyArmor(Armor):
    def __init__(self, name="heavy armor", armor=10, defense=-5, tier=1):
        Armor.__init__(self, name, 10, 5, 1)
        self.name = name
        self.armor = armor
        self.defense = defense
        self.tier = tier
        self.subcategory = "heavy"


# Weapon class and subclasses
class Weapon(Item):
    def __init__(self, name, strPower, dexPower, cunPower, tier):
        Item.__init__(self, name, tier)
        self.name = name
        self.strPower = strPower
        self.dexPower = dexPower
        self.cunPower = cunPower
        self.tier = tier
        self.category = "weapon"

    def printInfo(self):
        print(self.id, self.name, self.strPower, self.dexPower, self.cunPower, self.tier, self.category + "/" + self.subcategory)


class Sword(Weapon):
    def __init__(self, name="sword", strPower=100, dexPower=0, cunPower=0, tier=1):
        Weapon.__init__(self, name, 100, 0, 0, 1)
        self.name = name
        self.strPower = strPower
        self.dexPower = dexPower
        self.cunPower = cunPower
        self.tier = tier
        self.subcategory = "sword"
        self.apCost = 5


class Dagger(Weapon):
    def __init__(self, name="dagger", strPower=45, dexPower=45, cunPower=0, tier=1):
        Weapon.__init__(self, name, 45, 45, 0, 1)
        self.name = name
        self.strPower = strPower
        self.dexPower = dexPower
        self.cunPower = cunPower
        self.tier = tier
        self.subcategory = "dagger"
        self.apCost = 4


class Axe(Weapon):
    def __init__(self, name="axe", strPower=100, dexPower=0, cunPower=0, tier=1):
        Weapon.__init__(self, name, 100, 0, 0, 1)
        self.name = name
        self.strPower = strPower
        self.dexPower = dexPower
        self.cunPower = cunPower
        self.tier = tier
        self.subcategory = "axe"
        self.apCost = 6


class Mace(Weapon):
    def __init__(self, name="mace", strPower=110, dexPower=0, cunPower=0, tier=1):
        Weapon.__init__(self, name, 110, 0, 0, 1)
        self.name = name
        self.strPower = strPower
        self.dexPower = dexPower
        self.cunPower = cunPower
        self.tier = tier
        self.subcategory = "mace"
        self.apCost = 7


# Actor class and subclasses
class Actor:
    def __init__(self, name="John Doe", baseStr=10, baseDex=10, baseCon=10, baseCun=10, baseWil=10, baseCha=10, baseLck=1):
        # Base stats init
        global numberOfActors
        numberOfActors = numberOfActors + 1
        self.id = numberOfActors
        self.name = name
        self.baseStr = baseStr
        self.baseDex = baseDex
        self.baseCon = baseCon
        self.baseCun = baseCun
        self.baseWil = baseWil
        self.baseCha = baseCha
        self.baseLck = baseLck
        self.baseSpd = 100
        self.abilities = []
        self.isAlive = True
        self.target = None
        self.attacker = None
        self.turnPriority = 0
        # Gear init
        self.gear = [None, None, None, None, None, None, None, None, None, None, None, None]
        self.gearSlotLabel = ["Head", "Face", "Neck", "Back", "Torso", "Main-hand", "Off-hand", "Hands", "Right ring", "Left ring", "Belt", "Feet"]
        # Gear: 0-head, 1-face, 2-neck, 3-back, 4-torso, 5-mainhand, 6-offhand, 7-hands, 8-right ring, 9-left ring, 10-belt, 11-feet
        # Current stats init
        self.currentStr = self.baseStr + self.getGearStat("strMod")
        self.currentDex = self.baseDex + self.getGearStat("dexMod")
        self.currentCon = self.baseCon + self.getGearStat("conMod")
        self.currentCun = self.baseCun + self.getGearStat("cunMod")
        self.currentWil = self.baseWil + self.getGearStat("wilMod")
        self.currentCha = self.baseCha + self.getGearStat("chaMod")
        self.currentLck = self.baseLck + self.getGearStat("lckMod")
        self.currentSpd = self.baseSpd + self.getGearStat("spdMod")
        # Derived stats
        self.maxAp = math.floor(self.currentSpd/20 + self.currentDex/10 + self.currentCun/10 + self.getGearStat("apMod"))
        self.ap = self.maxAp
        self.maxHp = self.currentCon*10 + self.currentWil*2
        self.hp = self.maxHp
        self.attack = math.floor(self.currentDex + self.currentCun/10 + self.currentLck + self.getGearStat("attackMod"))
        self.defense = math.floor(self.currentDex + self.currentCun/10 + self.currentLck + self.getGearStat("defenseMod"))
        self.damage = math.ceil(self.calculatePowerDamage() + self.getGearStat("damageMod"))
        self.armor = self.getGearStat("armorMod")
        self.initiative = ((self.currentCun*5 + self.currentDex*10 + self.currentLck + self.getGearStat("initiativeMod")) * self.currentSpd)/100

    def printInfo(self):
        print(self.id, self.name, self.baseStr, self.baseDex, self.baseCon, self.baseCun, self.baseWil, self.baseCha, self.baseLck, self.baseSpd, str(self.hp) + "/" + str(self.maxHp), str(self.ap) + "/" + str(self.maxAp), self.attack, self.defense, self.damage, self.armor)

    def printGearInfo(self):
        print(self.name + "'s Equipment")
        for i in range(0, len(self.gear)):
            if self.gear[i] != None:
                print "%-12s %s" % (self.gearSlotLabel[i] + ": ", self.gear[i].name)
            else:
                print "%-12s %s" % (self.gearSlotLabel[i] + ": ", "Empty")

    def calculatePowerDamage(self):
        if self.gear[5] != None:
            dmg = (self.currentStr*self.gear[5].strPower)/100 + (self.currentDex*self.gear[5].dexPower)/100 + (self.currentCun*self.gear[5].cunPower)/100
        else:
            dmg = self.currentStr/5
        return dmg

    def getGearStats(self, stat):
        rStat = 0
        if stat == "armor":
            for item in self.gear:
                if hasattr(item, armor):
                    rStat = rStat + item.armor
                else:
                    rStat = rStat
        else:
            rStat = 0
        return rStat

    def getGearStat(self, stat):
        rStat = 0
        for item in self.gear:
            if item != None:
                rStat = rStat + getattr(item, stat, 0)
            else:
                rStat = rStat
        return rStat

    def equip(self, item):
        if isinstance(item, Weapon):
            self.gear[5] = item
            print(self.name + " equiped " +  item.name)
        else:
            print("Can't equip this!")

    def unequip(self, slot):
        if slot == "mainhand" or slot == "weapon":
            if self.gear[5] != None:
                print(self.name + " unequiped " + gear[5].name)
                gear[5] = None

    def punish(self, damage):
        self.hp = self.hp - damage
        self.update()
        print "%s %s %s %s" % (self.name, "has been punished for", damage, "damage")
        print "%s %s %s %s %s" % (self.name, "has", self.hp, "hp left. Is alive?", self.isAlive)

    def attack(self, target):
        self.target = target
        if self.target != None:
            self.target.attacker = self
            print("")
            attackRoll, ir1 = roll2d6o()
            defenseRoll, ir2 = roll2d6o()
            self.ap = self.ap - self.gear[5].apCost
            if self.ap > self.gear[5].apCost:
                if (self.attack + attackRoll) >= (self.target.defense + defenseRoll):
                    self.target.hp = self.target.hp - self.damage
                    print "%s %s %s %s %s" % ("You hit", self.target.name, "for", self.damage, "damage!")
                else:
                    print "%s %s %s" % ("You missed", self.target, "...")

    def update(self):
        # Primary stats
        self.currentStr = self.baseStr + self.getGearStat("strMod")
        self.currentDex = self.baseDex + self.getGearStat("dexMod")
        self.currentCon = self.baseCon + self.getGearStat("conMod")
        self.currentCun = self.baseCun + self.getGearStat("cunMod")
        self.currentWil = self.baseWil + self.getGearStat("wilMod")
        self.currentCha = self.baseCha + self.getGearStat("chaMod")
        self.currentLck = self.baseLck + self.getGearStat("lckMod")
        self.currentSpd = self.baseSpd + self.getGearStat("spdMod")
        # Derived stats
        self.maxAp = math.floor(self.currentSpd/20 + self.currentDex/10 + self.currentCun/10 + self.getGearStat("apMod"))
        self.ap = self.ap
        self.maxHp = self.currentCon*10 + self.currentWil*2
        self.hp = self.hp
        self.attack = math.floor(self.currentDex + self.currentCun/10 + self.currentLck + self.getGearStat("attackMod"))
        self.defense = math.floor(self.currentDex + self.currentCun/10 + self.currentLck + self.getGearStat("defenseMod"))
        self.damage = math.ceil(self.calculatePowerDamage() + self.getGearStat("damageMod"))
        self.armor = self.getGearStat("armorMod")
        self.isAlive = self.hp > 0
        self.initiative = ((self.currentCun*5 + self.currentDex*10 + self.currentLck + self.getGearStat("initiativeMod")) * self.currentSpd)/100

def roll1d6(show = False):
    r = random.randint(1, 6)
    if show:
        print "%s %s" % ("Rolled", r)
    return r

def roll2d6(show = False, testing = False):
    if show:
        print("***Dice roll (open 2d6)***")
    i = 0 # Keep track of the number of rolls
    r1 = roll1d6() # Roll 1 on 2
    r2 = roll1d6() # Roll 2 on 2
    i = i + 1 # First roll
    if show:
        print "%s %s %s %s" % (str(i) + ")", "Rolled", r1, r2)
    rf = 0 # Final roll
    rr = 0 # Reroll
    rrBoolean = False
    if r1 == 6 or r2 == 6:
        rrBoolean = True
        rf = r1 + r2
        if show:
            print("Rolled a 6 => addition rolls => substract 1 => reroll")
            print "%s %s %s %s %s" % (r1, "+", r2, "=", rf)
        rf = rf - 1
        if show:
            print "%s %s %s %s %s" % (rf + 1, "-", 1, "=", rf)
            print("Rerolling...")
    else:
        rf = r1 + r2
    while (rrBoolean):
        i = i + 1 # Reroll
        rr = roll1d6()
        if show:
            print "%s %s %s" % (str(i) + ")", "Rolled", rr)
        if rr == 6:
            rrBoolean = True
            rf = rf + rr
            if show:
                print("Rolled a 6 => addition rolls => substract 1 => reroll")
                print "%s %s %s %s %s" % (rf - rr, "+", rr, "=", rf)
            rf = rf - 1
            if show:
                print "%s %s %s %s %s" % (rf + 1, "-", 1, "=", rf)
                print("Rerolling...")
        else:
            rrBoolean = False
            rf = rf + rr
            if show:
                print "%s %s %s %s %s" % (rf - rr, "+", rr, "=", rf)
    if show:
        print "%s %s" % ("***Final result:", str(rf) + "***")
    if testing:
        roll2d6.maxRerolls = i
    return rf

def roll2d6o():
    ir = 0 # Individual rolls count
    #r1 == roll1d6() # Original roll, dice 1 # roll1d6() doesn't work here for some reason
    #r2 == roll1d6() # Original roll, dice 2 # roll1d6() doesn't work here for some reason
    r1 = random.randint(1, 6)
    r2 = random.randint(1, 6)
    print("***Rolling open-ended 2d6***")
    print "%s %s %s" % (ir, "Original roll, dice 1:", r1)
    print "%s %s %s" % (ir+1, "Original roll, dice 2:", r2)
    ir = ir + 2 # Adding both individual rolls (dice 1 and dice 2)
    rr = 0
    rr1 = 0
    rr2 = 0
    rr1Boolean = False
    rr2Boolean = False
    rrBoolean = False
    rf = r1 + r2
    print "%s %s %s %s %s" % (r1, "+", r2, "=", rf)
    if r1 == 6 or r2 == 6:
        if r1 == 6:
            rr1Boolean = True
            print("Rerolling dice 1")
        if r2 == 6:
            rr2Boolean = True
            print("Rerolling dice 2")
        if rr1Boolean or rr2Boolean:
            rrBoolean = True
        rf = rf - 1
        print "%s %s %s %s %s" % (rf+1, "-", 1, "=", rf)
    else:
        rf = rf
    while rrBoolean:
        if rr1Boolean:
            rr1 = roll1d6()
            print "%s %s" % ("Reroll dice 1:", rr1)
            ir = ir + 1
        else:
            rr1 = 0
        if rr2Boolean:
            rr2 = roll1d6()
            print "%s %s" % ("Reroll dice 2:", rr2)
            ir = ir + 1
        else:
            rr2 = 0
        rr = rr1 + rr2
        print "%s %s %s %s %s %s" % ("Reroll total", rr1, "+", rr2, "=", rr)
        if rr1 == 6:
            rr1Boolean = True
            print("Rerolling dice 1 again!")
        else:
            rr1Boolean = False
        if rr2 == 6:
            rr2Boolean = True
            print("Rerolling dice 2 again!")
        else:
            rr2Boolean = False
        if rr1Boolean or rr2Boolean:
            rrBoolean = True
        else:
            rrBoolean = False
        rf = rf + rr
        print "%s %s %s %s %s" % (rf-rr, "+", rr, "=", rf)
        if rrBoolean:
            rf = rf - 1
            print "%s %s %s %s %s" % (rf+1, "-", 1, "=", rf)
        else:
            rf = rf
            print(rf)
        rr1 = 0
        rr2 = 0
        rr = 0
    print "%s %s" % ("Final result:", rf)
    print "%s %s" % ("Number of individual dice rolls:", ir)
    return rf, ir

def rerollsTest(numberOfRolls = 10, show = False):
    numberOfRolls = numberOfRolls
    maxRerolls = 0
    maxResult = 0
    for i in range(0, numberOfRolls, 1):
        funcMaxResult = roll2d6(show = True, testing = True)
        funcMaxRerolls = roll2d6.maxRerolls
        if funcMaxRerolls > maxRerolls:
            maxRerolls = funcMaxRerolls
        if funcMaxResult > maxResult:
            maxResult = funcMaxResult
    del roll2d6.maxRerolls
    if show:
        print("***2d6 test***")
        print "%s %s" % ("Max number of (re)rolls:", maxRerolls)
        print "%s %s" % ("Max result:", maxResult)
    return maxRerolls, maxResult

def fightTest(personA, personB):
    battle = Battle(persons = [personA, personB])
    battle.setTurnOrder()

# Game updates and main loop
print("***BattleSim***")
def executeCommand(playerInput):
    i = 0
    if playerInput == "exit":
        print("Exiting...")
        isRunning = False
        raise SystemExit
    elif playerInput == "flush":
        sys.stdout.flush() # Doesn't work for some reason...
        #turnIncrement = 0
        i = 0
    elif playerInput == "rolltest":
        rollsParameter = raw_input("How many 2d6 rolls do you want to make? ")
        maxRerolls, maxResult = rerollsTest(int(rollsParameter), True)
        print(maxRerolls, maxResult)
    elif "roll" in playerInput:
        if "2d6" in playerInput:
            if "true" in playerInput or "True" in playerInput:
                print(roll2d6(True))
            else:
                print(roll2d6())
        else:
            if "true" in playerInput or "True" in playerInput:
                print(roll1d6(True))
            else:
                print(roll1d6())
        i = 1
    else:
        #turnIncrement = 0
        #print(turnIncrement)
        print("Unknown command")
        i = 0
    return i

sword = Sword("iron sword")
dagger = Dagger("iron dagger")
axe = Axe("iron axe")
mace = Mace("iron mace")
clothes = Clothes("clothes")
lightArmor = LightArmor("light armor")
mediumArmor = MediumArmor("medium armor")
heavyArmor = HeavyArmor("heavy armor")
sword.printInfo()
player = Actor("John", 18, 14, 16, 12, 16, 11, 1)
player.equip(sword)
npc = Actor("Brute", 20, 12, 18, 10, 15, 10, 1)
npc.equip(axe)
actors = [player, npc]
for actor in actors:
    actor.update()
#player.update()
#npc.update()
player.printInfo()
npc.printInfo()
player.printGearInfo()
player.punish(500)
sword.printInfo()
a, b = roll2d6o()
print(a, b)
print(a, b)
c = roll1d6()
roll1d6(True)
print(c)
d = roll2d6o()
print(d)
print(sword.id)
print(dagger.id)
print(mediumArmor.id)
fightTest(player, npc)
print(battles[0].persons)


while isRunning:
    print"%s %s %s" % (turn, "+", turnIncrement)
    for actor in actors: # Update actors
        actor.update()
    print "%s %s" % ("Program is still running (Turn", str(turn) + ")")
    command = raw_input("> ")
    #executeCommand(command)
    turn = turn + executeCommand(command) # Executes command and add return value to the turn variable
