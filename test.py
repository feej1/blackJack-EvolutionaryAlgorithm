
from objects import Card, Hand,Dealer, Agent 
from random import *
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
        # print(str(agent))
        agent.playHands(dealer)
        dealer.reDeal()
        agent.reDeal()
    print(str(agent))

def testLogicUpdating():
    evo =ea.Evolution(100)
    ag = evo.agents[0]
    print(str(ag.actionHandler))
    print(ag.hands[0].sum())
    evo.runGeneration(50)
    evo.agents = evo.updateLogic()
    print(str(ag.actionHandler))
    print(ag.hands[0].sum())

def evolov():
    evo =ea.Evolution(100)
    evo.evolve(4, 100, 200)

def eaPlayRoundsTest():
    start = time.process_time()
    agents = []
    dealer = Dealer()
    for i in range(0,150):
        agents.append(Agent())
    ea.playRounds(agents,dealer,100)
    print("time: %f" % (time.process_time()-start))


if __name__ == '__main__':   
    evolov()
    # eaPlayRoundsTest()
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

