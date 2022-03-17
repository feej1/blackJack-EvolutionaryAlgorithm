from objects import Card, Hand,Dealer, Agent 
from quickSort import *
from random import Random
import concurrent.futures as threading

ROUNDS = 50
P = .05
options = ["H", "D", "S"]   # for hand without doubles
doublesOptions = ["H", "D", "S", "SP"]  # for hand with doubles 




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
        logic1, splitLogic1 = agents[i].logic, agents[i].splitLogic
        logic2, splitLogic2 = agents[i-1].logic, agents[i-1].splitLogic
        newlogic = []
        newSplitLogic = []
        for iteration, row in enumerate(splitLogic1):   # looping over rows
            newRow = []
            for j in range(0, len(row)):     # looping over elements
                if generator.uniform(0,1) < P : newRow.append(splitLogic1[generator.randint(0,9)][generator.randint(0,9)])
                elif j % 2 == 0: newRow.append(splitLogic1[iteration][j])
                else: newRow.append(splitLogic2[iteration][j])
            newSplitLogic.append(newRow)
        agents[i-int(len(agents)/3)].splitLogic = newSplitLogic
        for iteration, row in enumerate(logic1):   # looping over rows
            newRow = []
            for j in range(0, len(row)):     # looping over elements
                if generator.uniform(0,1) < P : newRow.append(logic1[generator.randint(0,16)][generator.randint(0,9)])
                elif iteration % 2 == 0: newRow.append(logic1[iteration][j])
                else: newRow.append(logic2[iteration][j])
            newlogic.append(newRow)
        agents[i-int(len(agents)/3)].logic = newlogic


def runEvolution(iterations):
    agents = []
    for i in range(0,100):
        agents.append(Agent())
    for i in range(0,iterations):
        for agent in agents: agent.revenue = 0.0  
        agents = playRounds(agents,Dealer())
        updateLogic(agents)
        print(i)
        if i % 10 == 0 :
            print(getAverageLoss(agents,10))
    return agents

def playRounds(agents, dealer, rounds):
    for i in range(0,rounds):
        # print(i)
        dealer.play()
        for agent in agents:
            agent.playHands(dealer)
            agent.reDeal()
        dealer.reDeal()
    return agents

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



