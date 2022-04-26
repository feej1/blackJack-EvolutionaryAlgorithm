from objects import Card, Hand,Dealer, Agent 
from quickSort import *
from random import Random
import concurrent.futures as threading
import threading

ROUNDS = 50
P = .05
options = ["H", "D", "S"]   # for hand without doubles
doublesOptions = ["H", "D", "S", "SP"]  # for hand with doubles 



class Evolution:
    def __init__(self, agentCount) -> None:
        self.agents = [Agent() for i in range(agentCount)]
        self.agentCount = agentCount
        self.dealer = Dealer()
        self.generationCount = 0
        self.stop_thread = False

    
    def evolve(self, uiCallback, handsPer, generations):
        for i in range(generations):
            for agent in self.agents: agent.revenue = 0.0  ## change to map
            self.runGeneration(handsPer)
            self.updateLogic()
            if self.stop_thread: break
            if i % 5 == 0:
                # print(i)
                # print(self.getAverageLoss(10))
                uiCallback(self.agents, self.generationCount, handsPer, self.getAverageLoss(10))

    def runGeneration(self, handsPer):
        for i in range(handsPer):
            # print(i)
            self.dealer.play()
            for agent in self.agents:
                agent.playHands(self.dealer)
                agent.reDeal()
            self.dealer.reDeal()
        self.generationCount += 1

    def updateLogic(self):
        generator = Random()
        quick_sort(0, self.agentCount-1, self.agents)   ### best preformers are at end of array, sorting acts as the fitness funciton judgin preformance by revenue      
        for i in range(int(2*self.agentCount/3),self.agentCount, 2):  # looping over all agents stepping by two, i and i-1 are used 
            logic1, splitLogic1 = self.agents[i].actionHandler.regLogic, self.agents[i].actionHandler.doublesLogic
            logic2, splitLogic2 = self.agents[i-1].actionHandler.regLogic, self.agents[i-1].actionHandler.doublesLogic
            newlogic = []
            newSplitLogic = []
            for iteration, row in enumerate(splitLogic1):   # looping over rows
                newRow = []
                for j in range(0, len(row)):     # looping over elements
                    if generator.uniform(0,1) < P : newRow.append(splitLogic1[generator.randint(0,9)][generator.randint(0,9)])
                    elif j % 2 == 0: newRow.append(splitLogic1[iteration][j])
                    else: newRow.append(splitLogic2[iteration][j])
                newSplitLogic.append(newRow)
            self.agents[i-int(self.agentCount/3)].actionHandler.doublesLogic = newSplitLogic
            for iteration, row in enumerate(logic1):   # looping over rows
                newRow = []
                for j in range(0, len(row)):     # looping over elements
                    if generator.uniform(0,1) < P : newRow.append(logic1[generator.randint(0,16)][generator.randint(0,9)])
                    elif iteration % 2 == 0: newRow.append(logic1[iteration][j])
                    else: newRow.append(logic2[iteration][j])
                newlogic.append(newRow)
            self.agents[i-int(self.agentCount/3)].actionHandler.regLogic = newlogic
            # return self.agents

    def getAverageLoss(self, num):
        sum = 0 
        if num > self.agentCount: return False
        for i in range (num):
            sum += self.agents[self.agentCount-i-1].revenue  
            ## [count- i -1] because the agent array should be sorted. Averaging only the top number of agents rev
        return sum/num





def getAverageLoss(agents, num):
    sum = 0 
    if num > len(agents): return False
    for i in range (0,num):
        sum += agents[len(agents)-i-1].revenue
    return sum/num


def updateLogic(agents):
    generator = Random()
    quick_sort(0, len(agents)-1, agents)   ### best preformers are at end of array       
    for i in range(int(2*len(agents)/3),len(agents), 2):  # looping over all agents
        logic1, splitLogic1 = agents[i].actionHandler.regLogic, agents[i].actionHandler.doublesLogic
        logic2, splitLogic2 = agents[i-1].actionHandler.regLogic, agents[i-1].actionHandler.doublesLogic
        newlogic = []
        newSplitLogic = []
        for iteration, row in enumerate(splitLogic1):   # looping over rows
            newRow = []
            for j in range(0, len(row)):     # looping over elements
                if generator.uniform(0,1) < P : newRow.append(splitLogic1[generator.randint(0,9)][generator.randint(0,9)])
                elif j % 2 == 0: newRow.append(splitLogic1[iteration][j])
                else: newRow.append(splitLogic2[iteration][j])
            newSplitLogic.append(newRow)
        agents[i-int(len(agents)/3)].actionHandler.doublesLogic = newSplitLogic
        for iteration, row in enumerate(logic1):   # looping over rows
            newRow = []
            for j in range(0, len(row)):     # looping over elements
                if generator.uniform(0,1) < P : newRow.append(logic1[generator.randint(0,16)][generator.randint(0,9)])
                elif iteration % 2 == 0: newRow.append(logic1[iteration][j])
                else: newRow.append(logic2[iteration][j])
            newlogic.append(newRow)
        agents[i-int(len(agents)/3)].actionHandler.regLogic = newlogic

# def playRounds(agents, dealer, rounds):
#     for i in range(0,rounds):
#         print(i)
#         dealer.play()
#         with threading.ThreadPoolExecutor(max_workers=10) as worker:
#             # for agent in agents: worker.submit(agent.playHands, dealer)
#             worker.map(lambda agent: agent.playHands(dealer), agents)
#         # for agent in agents:
#         #     executor.submit(agent.playHands, dealer)
#         # with threading.ThreadPoolExecutor(max_workers=20) as worker:
#         #     for agent in agents: worker.submit(agent.reDeal)
#         for agent in agents:
#             agent.reDeal()
#         dealer.reDeal()
#     return agents



