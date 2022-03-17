import tkinter as tk
import ea 
from objects import *
from time import process_time




def getColorElement(agents, i, j ): ## gets the matrix[i][j] element
    hitCount = 0
    stayCount = 0
    doubleCount = 0
    for k in range (0,10):
        agent = agents[k]
        action = agent.logic[i][j]
        if action == 'H': hitCount +=1
        elif action == 'S': stayCount +=1
        elif action == 'D': doubleCount += 1
    hitWeight = hitCount/10
    stayWeight = stayCount/10
    doubleWeight = doubleCount/10
    if hitWeight > stayWeight and hitWeight > doubleWeight:
        return '#%02x%02x%02x' % (194, 24, 7)
    elif stayWeight > doubleWeight:
        return '#%02x%02x%02x' % (100, 136, 234) 
    else:
        return '#%02x%02x%02x' % (255, 153, 51)

def getSplitColorElement(agents, i, j ): ## gets the matrix[i][j] element
    hitCount = 0
    stayCount = 0
    doubleCount = 0
    splitCount = 0
    for k in range (0,10):
        agent = agents[k]
        action = agent.splitLogic[i][j]
        if action == 'H': hitCount +=1
        elif action == 'S': stayCount +=1
        elif action == 'D': doubleCount += 1
        elif action == 'SP': splitCount += 1
    hitWeight = hitCount/10
    stayWeight = stayCount/10
    doubleWeight = doubleCount/10
    splitWeight = splitCount/10
    if hitWeight > stayWeight and hitWeight > doubleWeight and hitWeight > splitWeight:
        return '#%02x%02x%02x' % (194, 24, 7)
    elif stayWeight > doubleWeight and stayWeight > splitWeight:
        return '#%02x%02x%02x' % (100, 136, 234) 
    elif splitWeight > doubleWeight:
        return '#%02x%02x%02x' % (191, 227, 180)
    else:
        return '#%02x%02x%02x' % (255, 153, 51)

def getSplitColorMatrix(agents):
    splitColorMatrix = []
    for i in range (0, 10):  # 17 rows for 5-21 possible hand totals, 
        row =[]
        for j in range(0,10):  # 13 columsn for 2-A possible face up cards
            row.append((getSplitColorElement(agents,i,j)))
        splitColorMatrix.append(row)
    return splitColorMatrix


def getColorMatrix(agents):
    colorMatrix = []   #where arr [x][y] gives the xth row and yth column, retrieve action using arr[hand sum][dealer card num]
    for i in range (0, 17):  # 17 rows for 5-21 possible hand totals, 
        row =[]
        for j in range(0,10):  # 13 columsn for 2-A possible face up cards
            row.append((getColorElement(agents,i,j)))
        colorMatrix.append(row)
    return colorMatrix

def updateSplitColors(colorMatrix,labels):
    height = 10
    width = 10
    for i in range(height): #Rows
        for j in range(width): #Columns 
            mycolor = colorMatrix[i][j]
            labels[i][j].config(bg=mycolor)

def updateColors(colorMatrix,labels):
    height = 17
    width = 10
    for i in range(height): #Rows
        for j in range(width): #Columns 
            mycolor = colorMatrix[i][j]
            labels[i][j].config(bg=mycolor)

def runEa(hands, rounds, agentCount, root):
    agents = [Agent() for i in range(0,agentCount)]
    dealer = Dealer()
    for i in range(0,rounds):
        root.update()
        for agent in agents: agent.revenue = 0.0  
        agents = ea.playRounds(agents,dealer,hands)
        ea.updateLogic(agents)
        if i % 10 == 0 :
            print(i)
            updateColors(getColorMatrix(agents), regHand)
            updateSplitColors(getSplitColorMatrix(agents), splitHand)
            handsPlayedLabel2.config(text="%f" % (int(i * agentCount * hands)))
            generationLabel2.config(text="%f" % (int(i)))
            preformanceLabel2.config(text="%f" % (ea.getAverageLoss(agents,int(agentCount/10))))
            print(ea.getAverageLoss(agents,int(agentCount/10)))
    updateColors(getColorMatrix(agents), regHand)
    updateSplitColors(getSplitColorMatrix(agents), splitHand)


root = tk.Tk()
root.geometry('1000x500')
root.title("Blackjack EA")
root.iconbitmap('C:\\Users\\jobo9\\Desktop\\class\\black-jack-ea\\icon.ico')

# basicStratImg = ImageTk.PhotoImage(Image.open("table.png"))
# imgLabel = tk.Label(image=basicStratImg).grid()

############## dealer card labels ##############
## regular hands
label = tk.Label(root, text="2 ", border=5).grid(row=0, column=1)
label = tk.Label(root, text="3 ", border=5).grid(row=0, column=2)
label = tk.Label(root, text="4 ", border=5).grid(row=0, column=3)
label = tk.Label(root, text="5 ", border=5).grid(row=0, column=4)
label = tk.Label(root, text="6 ", border=5).grid(row=0, column=5)
label = tk.Label(root, text="7 ", border=5).grid(row=0, column=6)
label = tk.Label(root, text="8 ", border=5).grid(row=0, column=7)
label = tk.Label(root, text="9 ", border=5).grid(row=0, column=8)
label = tk.Label(root, text="10 ", border=5).grid(row=0, column=9)
label = tk.Label(root, text="A", border=5).grid(row=0, column=10)
## doubles
label = tk.Label(root, text="2 ", border=5).grid(row=0, column=13)
label = tk.Label(root, text="3 ", border=5).grid(row=0, column=14)
label = tk.Label(root, text="4 ", border=5).grid(row=0, column=15)
label = tk.Label(root, text="5 ", border=5).grid(row=0, column=16)
label = tk.Label(root, text="6 ", border=5).grid(row=0, column=17)
label = tk.Label(root, text="7 ", border=5).grid(row=0, column=18)
label = tk.Label(root, text="8 ", border=5).grid(row=0, column=19)
label = tk.Label(root, text="9 ", border=5).grid(row=0, column=20)
label = tk.Label(root, text="10", border=5).grid(row=0, column=21)
label = tk.Label(root, text="A", border=5).grid(row=0, column=22)



########### player card total #############
##regular
label = tk.Label(root, text="5 ", border=5).grid(row=17, column=0)
label = tk.Label(root, text="6 ", border=5).grid(row=16, column=0)
label = tk.Label(root, text="7 ", border=5).grid(row=15, column=0)
label = tk.Label(root, text="8 ", border=5).grid(row=14, column=0)
label = tk.Label(root, text="9 ", border=5).grid(row=13, column=0)
label = tk.Label(root, text="10", border=5).grid(row=12, column=0)
label = tk.Label(root, text="11", border=5).grid(row=11, column=0)
label = tk.Label(root, text="12", border=5).grid(row=10, column=0)
label = tk.Label(root, text="13", border=5).grid(row=9, column=0)
label = tk.Label(root, text="14", border=5).grid(row=8, column=0)
label = tk.Label(root, text="15", border=5).grid(row=7, column=0)
label = tk.Label(root, text="16", border=5).grid(row=6, column=0)
label = tk.Label(root, text="17", border=5).grid(row=5, column=0)
label = tk.Label(root, text="18", border=5).grid(row=4, column=0)
label = tk.Label(root, text="19", border=5).grid(row=3, column=0)
label = tk.Label(root, text="20", border=5).grid(row=2, column=0)
label = tk.Label(root, text="21", border=5).grid(row=1, column=0)

##doubles
label = tk.Label(root, text="2's  ", border=5).grid(row=10, column=12)
label = tk.Label(root, text="3's  ", border=5).grid(row=9, column=12)
label = tk.Label(root, text="4's  ", border=5).grid(row=8, column=12)
label = tk.Label(root, text="5's  ", border=5).grid(row=7, column=12)
label = tk.Label(root, text="6's  ", border=5).grid(row=6, column=12)
label = tk.Label(root, text="7's  ", border=5).grid(row=5, column=12)
label = tk.Label(root, text="8's  ", border=5).grid(row=4, column=12)
label = tk.Label(root, text="9's  ", border=5).grid(row=3, column=12)
label = tk.Label(root, text="10's ", border=5).grid(row=2, column=12)
label = tk.Label(root, text="A's", border=5).grid(row=1, column=12)

## run button
button = tk.Button(root, text="Run", padx=10, pady=1, command= lambda: runEa(int(handsVal.get()), int(roundsVal.get()), int(agentsVal.get()), root)).grid(row=9,column=25, sticky=tk.W)

## hands per round control and label
handsVal = tk.StringVar(value=100)
handSpinner = tk.Spinbox(root,from_=20, to=200, textvariable=handsVal , wrap=False).grid(row=3,column=25)
handsControlLabel = tk.Label(root, text="Hands Per Round:", padx=5).grid(row=3, column=24, sticky=tk.W)

## rounds control and label
roundsVal = tk.StringVar(value=200)
roundSpinner = tk.Spinbox(root,from_=10, to=2000, textvariable=roundsVal, wrap=False).grid(row=5,column=25)
roundsControlLabel = tk.Label(root, text="Iterations:", padx=5 ).grid(row=5, column=24, sticky=tk.W)

## agents control and label
agentsVal = tk.StringVar(value=160)
agentSpinner = tk.Spinbox(root,from_=10, to=200, textvariable=agentsVal, wrap=False).grid(row=7,column=25)
agentsControlLabel = tk.Label(root, text="Number of Agents:", padx=5 ).grid(row=7, column=24, sticky=tk.W)


## stats label
handsPlayedLabel = tk.Label(root, text="Number of Hands Played:", padx=5 ).grid(row=13, column=24, sticky=tk.W)
generationLabel = tk.Label(root, text="Generations:", padx=5 ).grid(row=14, column=24, sticky=tk.W)
preformanceLabel = tk.Label(root, text="Top 10% Ave Preformance", padx=5 ).grid(row=15, column=24, sticky=tk.W)
handsPlayedLabel2 = tk.Label(root, text="0", padx=5 )
handsPlayedLabel2.grid(row=13, column=25, sticky=tk.W)
generationLabel2 = tk.Label(root, text="0", padx=5 )
generationLabel2.grid(row=14, column=25, sticky=tk.W)
preformanceLabel2 = tk.Label(root, text="0", padx=5 )
preformanceLabel2.grid(row=15, column=25, sticky=tk.W)



keySpanWidth = 3
## color key labels
keyLableRedColor = tk.Label(root, text="     ", background='#%02x%02x%02x' % (194, 24, 7), border=5 ).grid(row=13, column=16, sticky=tk.W)
keyLableRedText = tk.Label(root, text="Hit", padx=5 ).grid(row=13, column=18, columnspan=keySpanWidth ,sticky=tk.W)
keyLableBlueColor = tk.Label(root, text="     ", background='#%02x%02x%02x' % (100, 136, 234) , border=5 ).grid(row=14, column=16, sticky=tk.W)
keyLableBlueText = tk.Label(root, text="Stay", padx=5 ).grid(row=14, column=18, columnspan=keySpanWidth , sticky=tk.W)
keyLableOrangeColor = tk.Label(root, text="     ", background='#%02x%02x%02x' % (255, 153, 51), border=5 ).grid(row=15, column=16, sticky=tk.W) 
keyLableOrangeText = tk.Label(root, text="Double", padx=5 ).grid(row=15, column=18, columnspan=keySpanWidth ,  sticky=tk.W)
keyLableGreenColor = tk.Label(root, text="     ", background='#%02x%02x%02x' % (191, 227, 180), border=5 ).grid(row=16, column=16, sticky=tk.W) 
keyLableGreenText = tk.Label(root, text="Split", padx=5 ).grid(row=16, column=18,columnspan=keySpanWidth , sticky=tk.W)

keyEqls1 = tk.Label(root, text="=", padx=5 ).grid(row=13, column=17)
keyEqls2 = tk.Label(root, text="=", padx=5 ).grid(row=14, column=17)
keyEqls3 = tk.Label(root, text="=", padx=5 ).grid(row=15, column=17)
keyEqls4 = tk.Label(root, text="=", padx=5 ).grid(row=16, column=17)

## spacer labels
tableSpacer = tk.Label(root, text=" ", padx=10).grid(row=16, column=11)
tableSpacer = tk.Label(root, text=" ", padx=10).grid(row=1, column=23)

height = 17
width = 10
regHand =[]
for i in range(height): #Rows
    row = []
    for j in range(width): #Columns
        mycolor = cellColor = '#%02x%02x%02x' % (255,255,255 )
        label = tk.Label(root, text="     ", background=mycolor, border=5 )      
        label.grid(row=i+1, column=j+1)
        row.append(label)
    regHand.append(row)

height = 10
width = 10
splitHand = []
for i in range(height): #Rows
    row = []
    for j in range(width): #Columns
        mycolor = cellColor = '#%02x%02x%02x' % (255,255,255 )
        label = tk.Label(root, text="     ", background=mycolor, border=5 )      
        label.grid(row=i+1, column=j+13)
        row.append(label)
    splitHand.append(row)




tk.mainloop()