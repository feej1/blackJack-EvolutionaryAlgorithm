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
        self.actions = 0
    ## actions

    ## returns if doubled or not
    def doubleDown(self):
        if self.canDoubleDown:
            self.hit()
            self.stake = self.stake * 2
            self.canDoubleDown = False
            return True
        return False

    ## if cansplit returns new hand if it can split
    def split(self):
        if self.canSplit():
            card = self.cards.pop()  ## gets rid of second card
            newHand = Hand()
            ## if the card is an ace generate a card w/ val 11 as first card in new hand
            ## else add the card
            if card.isAce:            
                newHand.cards = [Card(1)]
            else:    
                newHand.cards = [card]
            ## gets a new card for each hand
            newHand.hit()
            newHand.canDoubleDown =True
            self.hit()
            self.canDoubleDown =True
            return newHand
        
    ## return true if hand is fininshed ie: busted this hit, or was called with busted hand
    def hit(self) -> bool:
        if not self.isBust():
            newCard = Card()
            ## handles options   
            # XX: hit ace and bust --> A goes to 1   
            # AX: hit and bust --> A goes to 1     
            # AX: hit no bust --> keep 11,  
            # AX: hit A second --> second ace goes to one
            if (self.containsAce() and newCard.isAce) or (newCard.isAce and self.sum() + 11 > 21 ): newCard.switchValueForAce()
            if self.containsAce() and self.sum() + newCard.value > 21: self.cards[self.getFirstAceIndex()].switchValueForAce()
            self.cards.append(newCard)
            self.canDoubleDown =False
            if self.sum() <= 21: return False
        return True

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


class actionHandler():
    def __init__(self) -> None:
        self.regLogic, self.doublesLogic = self.createLogicMatricies()

    def createLogicMatricies(self):
        options = ["H", "D", "S"]   # for hand without doubles H --> hit D --> double down  S--> stay
        doublesOptions = ["H", "D", "S", "SP"]  # for hand with doubles  SP --> split
        generator = Random()

        ## where arr [x][y] gives the xth row and yth column, where columns represent a dealers card and rows represent the players hand
        ## both arrays are filled with random actions, that are likley not a good choice ei hit on 20, stay on 4 etc
        logicMatrix = [ [options[generator.randint(0,2)] for i in range(2,12)] for i in range (1,18)]
        doublesLogicMatrix = [ [doublesOptions[generator.randint(0,3)] for i in range(2,12)] for i in range(2,12)]   

        return logicMatrix, doublesLogicMatrix  # return the both randomly decided newly created matricies

    def getAction(self, hand, dealerCard) -> str:
        if hand.canSplit(): 
            return self.doublesLogic[11 - hand.cards[0].value][dealerCard.value-2]  
        else: 
            return self.regLogic[21-hand.sum()][dealerCard.value-2] ## 21-sum accounts for smallest sum being 2+3 = 5 to get the first index. thats not a able to split

    def takeAction(self, hand, action) -> bool:  ## once a hand stays, BJ's, or busts its finished
        # print(action)
        handFinished = False
        if action =='H': 
            if hand.hit(): handFinished = True
        elif action == 'D': 
            hand.doubleDown()  ## decide on how to handle action resolving to double, but its not your first move -- H or S??
            handFinished = True
        elif action == 'SP': 
            newHand = hand.split() ## gets new hand for agent
            return False, newHand
        else:  
            ## else it must be stay and therfore hand is finished
            handFinished = True 
        return handFinished, None

    def __str__(self) -> str:
        printStr = "-----------Logic Matrix----------\n"
        printStr += "    2  3  4  5  6  7  8  9  10 A"
        for j in range(0, len(self.regLogic)):   # looping over rows'
            if j+5 <= 9: printStr += f'\n{j+5} : '
            else: printStr += f'\n{j+5}: '
            for i in range(0, len(self.regLogic[j])):     # looping over elements
                printStr += f'{self.regLogic[j][i]}  ' 
        printStr += "\n"
        return printStr


class Agent:
    def __init__(self):
        # self.logic, self.splitLogic  = self.createLogicMatrix() # returns both arrays
        self.hands = [Hand()]
        self.revenue = 0.0
        self.actionHandler = actionHandler()

    def resetRevenue(self):
        self.revenue = 0

    def playHand(self, hand, dealerCard): 
        handFinished = False
        while not handFinished:
            handFinished, newHand = self.actionHandler.takeAction(hand, self.actionHandler.getAction(hand, dealerCard))
            if newHand != None: self.hands.append(newHand)

    def playHands(self, dealer):  ## pass in dealer that has played, play each hand assess results
        dealerCard = dealer.getFaceUpCard()
        for hand in self.hands:
            self.playHand(hand, dealerCard)
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



