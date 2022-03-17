from cgi import test
from hashlib import new
import imp
from objects import Card, Hand,Dealer, Agent 
from random import *
import copy
import concurrent.futures as threading
import ea
import time

options = ["H", "D", "S"]   # for hand without doubles
doublesOptions = ["H", "D", "S", "SP"]  # for hand with doubles 


def testSplit():
    hand = Hand()
    for i in range (1,14):        # loops over each card type
        secondCard = Card(i)
        if i ==1: secondCard.switchValueForAce()
        hand.cards = [ Card(i), secondCard]
        newHand = hand.split()
        print(f'Hand 1 : {hand.toString()} sum: {hand.sum()} can double down: {hand.canDoubleDown}')
        print(f'Hand 2 : {newHand.toString()} sum: {newHand.sum()}   can double down: {hand.canDoubleDown}\n')

def testDoubleDown():
    hand = Hand()
    for i in range (1,14):
        secondCard = Card(i)
        if i ==1: secondCard.switchValueForAce()
        hand.cards = [ Card(i), secondCard]
        res = hand.doubleDown()
        print(f'Hand 1 : {hand.toString()} sum: {hand.sum()} can double down: {hand.canDoubleDown}')

        # print(f'Trying to hit : {newHand.toString()} sum: {newHand.sum()}   can double down: {hand.canDoubleDown}\n')


def testHit():
    hand = Hand()
    for i in range (1,14):
        secondCard = Card(i)
        if i ==1: secondCard.switchValueForAce()
        hand.cards = [ Card(), secondCard]
        res = hand.hit()
        print(f'can double: {hand.doubleDown()}    Hand: {hand.toString()} sum: {hand.sum()}   res: {res}')


def doubleAfterSplit():
    hand = Hand()
    hand.cards = [Card(3),Card(3)]
    # print(hand.toString())
    print(f'can double: {hand.canDoubleDown}    Hand: {hand.toString()} sum: {hand.sum()}')
    newHand = hand.split()
    print(f'can double: {hand.canDoubleDown}    Hand: {hand.toString()} sum: {hand.sum()}')
    print(f'can double: {newHand.canDoubleDown}    Hand: {newHand.toString()} sum: {newHand.sum()}')
    

def doubleAfterHit():
    hand = Hand()
    hand.cards = [Card(),Card()]


def testTakeAction():
    agent = Agent()
    dealer = Dealer()
    print(str(agent))
    print(agent.takeAction(agent.hands[0], dealer.getFaceUpCard()))
    print(str(agent))


def playHandTest():
    agent = Agent()
    dealer = Dealer()
    dealer.play()
    print(str(agent))
    print("----Playing--------")
    print(agent.playHand(agent.hands[0], dealer.getFaceUpCard()))
    print("----Done--------")
    print(str(agent))
    print("----Result--------")
    agent.processResult(agent.hands[0], dealer.sum())
    print(f'agent:{str(agent)}     dealer: {str(dealer)}')


def playHandsTest():
    agent = Agent()
    dealer = Dealer()
    dealer.play()
    print(str(agent))
    print("----Playing--------")
    agent.playHands(dealer)
    print("----Done--------")
    print(str(agent))
    print("----Result--------")
    print({str(dealer)})


def playMulitpleRounds():
    dealer = Dealer()
    agent = Agent()
    for i in range(0,50):
        dealer.play()
        agent.playHands(dealer)
        dealer.reDeal()
        agent.reDeal()
    print(str(agent))

def testLogicUpdating():
    agents = []
    for i in range(0,100):
       agents.append(Agent())
    dealer =Dealer()
    start = time.process_time_ns()
    roundsStart = time.process_time_ns()
    ea.playRounds(agents,dealer,100)
    print("time for rounds: %f" % (time.process_time_ns()-roundsStart))
    logicStart = time.process_time_ns()
    ea.updateLogic(agents)
    print("time for logic updating: %f" % (time.process_time_ns()-logicStart))
    revStart = time.process_time_ns()
    for agent in agents:
        agent.revenue = 0
    print("time for rev: %f" % (time.process_time_ns()-revStart))
    print("time for total: %f" % (time.process_time_ns()-start))

def eaPlayRoundsTest():
    start = time.process_time()
    agents = []
    dealer = Dealer()
    for i in range(0,500):
        agents.append(Agent())
    ea.playRounds(agents,dealer,200)
    print("time: %f" % (time.process_time()-start))


if __name__ == '__main__':   
    eaPlayRoundsTest()
    # testLogicUpdating()
    # testSplit()
    # testDoubleDown()
    # testHit()
    # doubleAfterSplit()
    # testTakeAction()
    # playHandTest()
    # playHandsTest()
    # playMulitpleRounds()
    # testLogicUpdating(89)


# agent = Agent()
# agent.printLogic()

