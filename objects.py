from asyncio.windows_events import NULL
from random import Random
        
#https://m.media-amazon.com/images/I/71BA2ZSWd-L._AC_SY679_.jpg

class Card:   
    def __init__(self, num=-1):
        if num < 1: 
            generator = Random()
            self.number = generator.randint(1,13)
        else: self.number = num
        if self.number >10: 
            self.value = 10
            self.isAce = False
        elif (self.number ==1 ):
            self.isAce = True
            self.value = 11
        else:
            self.isAce = False
            self.value = self.number
    

    def switchValueForAce(self):       
        if self.isAce: 
            if self.value == 1 : self.value = 11
            if self.value == 11: self.value = 1
            return True
        else : return False

    def toString(self):
        if self.number == 13: return "K"
        elif self.number == 12: return "Q"
        elif self.number == 11: return "J"
        elif self.number == 1: return "A"
        else: return str(self.number)



class Hand:
    def __init__(self):
        self.cards = []                ## create two cards with random prob and then add them
        self.cards.append(Card())     
        secondCard = Card()
        if self.cards[0].isAce and secondCard.isAce: secondCard.switchValueForAce()  # if second card is ace then switch the value to 1
        self.cards.append(secondCard)
        self.canDoubleDown = True   ## bool indicating the ability ot double down, and the hit 
        self.stake = 1           ## amount bet on hand, added because double down hands pay double stake

    ## actions

    def doubleDown(self):
        if self.canDoubleDown:
            self.hit()
            self.stake = self.stake * 2
            return True
        return False

    def split(self):
        if self.canSplit():
            card = self.cards.pop()
            newHand = Hand()
            if card.isAce:
                newHand.cards = [Card(1)]
            else:
                newHand.cards = [card]
            newHand.hit()
            newHand.canDoubleDown =True
            self.hit()
            self.canDoubleDown =True
            return newHand
        return NULL
        

    def hit(self):
        if not self.isBust() or self.canDoubleDown:
            newCard = Card()
             ##consider options A X , hit bust, A to 1 ---> AX hit no bust keep 11,  AX hit A second ace 1
            if (self.containsAce() and newCard.isAce) or (newCard.isAce and self.sum() + 11 > 21 ): newCard.switchValueForAce()
            if self.containsAce() and self.sum() + newCard.value > 21: self.cards[self.getFirstAceIndex()].switchValueForAce()
            self.cards.append(newCard)
            self.canDoubleDown = False 
            if self.sum() < 21: return True
        return False

    ## states

    def isBust(self):
        if self.sum() > 21: 
            return True
        return False 

    def isBlackJack(self):
        if self.sum() == 21: return True
        return False

    ## helpers / general 

    def canSplit(self):
        if len(self.cards)>2: return False
        if self.cards[0].number != self.cards[1].number: return False
        return True

    def containsAce(self):
        for card in self.cards:
            if card.isAce: return True 
        return False

    def getFirstAceIndex(self):
        for i in range(0,len(self.cards)):
            if self.cards[i].isAce: return i

    def sum(self):
        sum = int()
        for card in self.cards: sum += card.value
        return sum

    def toString(self):
        handStr = str()
        for card in self.cards:
            handStr += f'{card.toString()} '
        return handStr

    def addCard(self,card):
        self.cards.append(card)
    

class Dealer:
    def __init__(self):
        self.hand = Hand()
    
    def getFaceUpCard(self):
        return self.hand.cards[0]

    def play(self):
        while self.hand.sum() < 17: self.hand.hit()
        if self.hand.isBlackJack(): return 1
        elif self.hand.isBust(): return 0
        else: return self.hand.sum()
    
    def sum(self):
        return self.hand.sum()

    def reDeal(self):
        self.hand = Hand()

    def __str__(self) -> str:
        return f'dealer hand: {self.hand.toString()}   sum:  {self.hand.sum()}'




## 100 agents each iteration top 20 make new agents, by passing its logic matrix and generatic mutations with p = .05


class Agent:
    def __init__(self):
        self.logic, self.splitLogic  = self.createLogicMatrix() # returns both arrays
        self.hands = [Hand()]
        self.revenue = 0.0

    def resetRevenue(self):
        self.revenue = 0

    def printLogic(self):
        print("-----------Logic Matrix----------")
        print("    2  3  4  5  6  7  8  9  10 A", end="")
        for j in range(0, len(self.logic)):   # looping over rows'
            if j+5 <= 9: print(f'\n{j+5} : ', end="")
            else: print(f'\n{j+5}: ', end="")
            for i in range(0, len(self.logic[j])):     # looping over elements
                print(f'{self.logic[j][i]}  ',end="") 
        print("")


    def createLogicMatrix(self):
        options = ["H", "D", "S"]   # for hand without doubles
        doublesOptions = ["H", "D", "S", "SP"]  # for hand with doubles
        generator = Random()
        logicMatrix = [ [options[generator.randint(0,2)] for i in range(2,12)] for i in range (1,18)]
        doublesLogicMatrix = [ [doublesOptions[generator.randint(0,3)] for i in range(2,12)] for i in range(2,12)]   #where arr [x][y] gives the xth row and yth column, retrieve action using arr[hand sum][dealer card num]

        return logicMatrix, doublesLogicMatrix  # return the both randomly decided newly created matricies

    def getAction(self, hand, dealerCard):
        if hand.canSplit(): 
            return self.splitLogic[11 - hand.cards[0].value][dealerCard.value-2]  
        else: 
            return self.logic[21-hand.sum()][dealerCard.value-2] ## 21-sum accounts for smallest sum being 2+3 = 5 to get the first index. thats not a able to split

    def takeAction(self,hand, dealerCard):  ## once a hand stays, BJ's, or busts its finished
        action = self.getAction(hand, dealerCard)   # gets a list of actions to take for each hand
        handFinished = False
        if action =='H': 
            if not hand.hit():    ## hit returns false when busted or DD, if case then hand is fininshed playing, take off of active hands append to fininshed for results
                handFinished = True
        elif action == 'D': 
            if hand.doubleDown(): 
                handFinished = True
            elif not hand.hit(): 
                ## hits when it can't double
                handFinished = True
        elif action == 'SP': 
            self.hands.append(hand.split()) # adds a new hand and hits the old
            handFinished = False
        else:  
            handFinished = True
        return handFinished

    def playHand(self, hand, dealerCard):  ## once a hand stays, BJ's, or busts its finished
        handFinished = False
        while not handFinished:
            handFinished = self.takeAction(hand,dealerCard)
        
    def playHands(self, dealer):  ## pass in dealer that has played, play each hand assess results
        for hand in self.hands:
            self.playHand(hand, dealer.getFaceUpCard())
            self.processResult(hand, dealer.sum())

    def processResult(self,hand, dealerRes):
            if hand.sum() >21: self.revenue -= hand.stake
            elif dealerRes > 21: self.revenue += hand.stake
            elif dealerRes > hand.sum() : self.revenue -= hand.stake
            elif dealerRes < hand.sum(): self.revenue += hand.stake

    def reDeal(self):
        self.hands = [Hand()]

    def __str__(self) -> str:
        printStr = "Current hands: "
        for hand in self.hands: printStr += f'{hand.toString()}  sum: {hand.sum()} stake: {hand.stake} ---> '
        printStr += f'\n reveue: {self.revenue}'
        return printStr

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Agent): return False
        logic = __o.logic
        for iteration, row in enumerate(logic):   # looping over rows
            for j in range(0, len(row)-1):     # looping over elements
                if not self.logic[iteration][j] == logic[iteration][j]: return False
        return True



