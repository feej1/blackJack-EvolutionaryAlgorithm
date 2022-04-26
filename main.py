import threading
import tkinter as tk
import ea
from objects import *
import sys


class UI:

    def __init__(self) -> None:

        self.root = tk.Tk()
        self.root.geometry('1000x500')
        self.root.title("Blackjack EA")
        base_path = getattr(sys, '_MEIPASS','.')+'/'
        path = base_path + "icon.ico"
        self.root.iconbitmap(path)

        ## spacer labels
        tableSpacer = tk.Label(self.root, text=" ", padx=10).grid(row=16, column=11)
        tableSpacer = tk.Label(self.root, text=" ", padx=10).grid(row=1, column=23)

        self.regHandDealerLabels, self.doublesHandLabels, self.regHandTotalsLabels, self.doublesHandLabels = self.createGridLabels(self.root)
        self.regGrid, self.splitGrid = self.createGrid(self.root)
        self.createControls(self.root)
        self.creatGridKey(self.root)
        self.handsPlayed, self.generationsCount, self.preformance = self.createStatLabels(self.root)

        self.root.mainloop()

    def updateUI(self, agents, generationCount, handsPer, averageLoss):
        colorUpdater = ColorUpdater()
        colorUpdater.updateColors(colorMatrix=colorUpdater.getColorMatrix(agents), labels=self.regGrid)
        colorUpdater.updateSplitColors(colorMatrix=colorUpdater.getSplitColorMatrix(agents), labels=self.splitGrid )
        self.handsPlayed.config(text="%i" % (int(len(agents) * generationCount * handsPer)))
        self.generationsCount.config(text="%i" % (int(generationCount)))
        self.preformance.config(text="%.2f" % (float(averageLoss)))
        self.root.update()
        
        

    def createGridLabels(self, root):
        ############## dealer card labels ##############
        ## regular hands
        regHandDealerLabels = []
        regHandDealerLabels.append(tk.Label(root, text="2 ", border=5).grid(row=0, column=1))
        regHandDealerLabels.append(tk.Label(root, text="3 ", border=5).grid(row=0, column=2))
        regHandDealerLabels.append(tk.Label(root, text="4 ", border=5).grid(row=0, column=3))
        regHandDealerLabels.append(tk.Label(root, text="5 ", border=5).grid(row=0, column=4))
        regHandDealerLabels.append(tk.Label(root, text="6 ", border=5).grid(row=0, column=5))
        regHandDealerLabels.append(tk.Label(root, text="7 ", border=5).grid(row=0, column=6))
        regHandDealerLabels.append(tk.Label(root, text="8 ", border=5).grid(row=0, column=7))
        regHandDealerLabels.append(tk.Label(root, text="9 ", border=5).grid(row=0, column=8))
        regHandDealerLabels.append(tk.Label(root, text="10 ", border=5).grid(row=0, column=9))
        regHandDealerLabels.append(tk.Label(root, text="A", border=5).grid(row=0, column=10))
        # ## doubles
        doublesDealerLabels = []
        doublesDealerLabels.append(tk.Label(root, text="2 ", border=5).grid(row=0, column=13))
        doublesDealerLabels.append(tk.Label(root, text="3 ", border=5).grid(row=0, column=14))
        doublesDealerLabels.append(tk.Label(root, text="4 ", border=5).grid(row=0, column=15))
        doublesDealerLabels.append(tk.Label(root, text="5 ", border=5).grid(row=0, column=16))
        doublesDealerLabels.append(tk.Label(root, text="6 ", border=5).grid(row=0, column=17))
        doublesDealerLabels.append(tk.Label(root, text="7 ", border=5).grid(row=0, column=18))
        doublesDealerLabels.append(tk.Label(root, text="8 ", border=5).grid(row=0, column=19))
        doublesDealerLabels.append(tk.Label(root, text="9 ", border=5).grid(row=0, column=20))
        doublesDealerLabels.append(tk.Label(root, text="10", border=5).grid(row=0, column=21))
        doublesDealerLabels.append(tk.Label(root, text="A", border=5).grid(row=0, column=22))



        # ########### player card total #############
        # ##regular
        regHandTotalsLabels = []
        regHandTotalsLabels.append(tk.Label(root, text="5 ", border=5).grid(row=17, column=0))
        regHandTotalsLabels.append(tk.Label(root, text="6 ", border=5).grid(row=16, column=0))
        regHandTotalsLabels.append(tk.Label(root, text="7 ", border=5).grid(row=15, column=0))
        regHandTotalsLabels.append(tk.Label(root, text="8 ", border=5).grid(row=14, column=0))
        regHandTotalsLabels.append(tk.Label(root, text="9 ", border=5).grid(row=13, column=0))
        regHandTotalsLabels.append(tk.Label(root, text="10", border=5).grid(row=12, column=0))
        regHandTotalsLabels.append(tk.Label(root, text="11", border=5).grid(row=11, column=0))
        regHandTotalsLabels.append(tk.Label(root, text="12", border=5).grid(row=10, column=0))
        regHandTotalsLabels.append(tk.Label(root, text="13", border=5).grid(row=9, column=0))
        regHandTotalsLabels.append(tk.Label(root, text="14", border=5).grid(row=8, column=0))
        regHandTotalsLabels.append(tk.Label(root, text="15", border=5).grid(row=7, column=0))
        regHandTotalsLabels.append(tk.Label(root, text="16", border=5).grid(row=6, column=0))
        regHandTotalsLabels.append(tk.Label(root, text="17", border=5).grid(row=5, column=0))
        regHandTotalsLabels.append(tk.Label(root, text="18", border=5).grid(row=4, column=0))
        regHandTotalsLabels.append(tk.Label(root, text="19", border=5).grid(row=3, column=0))
        regHandTotalsLabels.append(tk.Label(root, text="20", border=5).grid(row=2, column=0))
        regHandTotalsLabels.append(tk.Label(root, text="21", border=5).grid(row=1, column=0))

        # ##doubles
        doublesHandLabels = []
        doublesHandLabels.append(tk.Label(root, text="2's  ", border=5).grid(row=10, column=12))
        doublesHandLabels.append(tk.Label(root, text="3's  ", border=5).grid(row=9, column=12))
        doublesHandLabels.append(tk.Label(root, text="4's  ", border=5).grid(row=8, column=12))
        doublesHandLabels.append(tk.Label(root, text="5's  ", border=5).grid(row=7, column=12))
        doublesHandLabels.append(tk.Label(root, text="6's  ", border=5).grid(row=6, column=12))
        doublesHandLabels.append(tk.Label(root, text="7's  ", border=5).grid(row=5, column=12))
        doublesHandLabels.append(tk.Label(root, text="8's  ", border=5).grid(row=4, column=12))
        doublesHandLabels.append(tk.Label(root, text="9's  ", border=5).grid(row=3, column=12))
        doublesHandLabels.append(tk.Label(root, text="10's ", border=5).grid(row=2, column=12))
        doublesHandLabels.append(tk.Label(root, text="A's", border=5).grid(row=1, column=12))

        return regHandDealerLabels, doublesHandLabels, regHandTotalsLabels, doublesHandLabels
    
    def createGrid(self, root):
        height = 17
        width = 10
        regGrid =[]
        for i in range(height): #Rows
            row = []
            for j in range(width): #Columns
                mycolor =  '#%02x%02x%02x' % (255,255,255 )
                label = tk.Label(root, text="     ", background=mycolor, border=5 )      
                label.grid(row=i+1, column=j+1)
                row.append(label)
            regGrid.append(row)

        height = 10
        width = 10
        splitGrid = []
        for i in range(height): #Rows
            row = []
            for j in range(width): #Columns
                mycolor  = '#%02x%02x%02x' % (255,255,255 )
                label = tk.Label(root, text="     ", background=mycolor, border=5 )      
                label.grid(row=i+1, column=j+13)
                row.append(label)
            splitGrid.append(row)
        return regGrid, splitGrid
    

    def runThread(self):
        self.th = threading.Thread(target=self.runEa, args=(int(self.agentsVal.get()),))
        self.th.start()

    def reset(self):
        self.pop.stop_thread = True
        colorUpdater = ColorUpdater()
        col1 = [['#%02x%02x%02x' % (255,255,255 ) for i in range(10) ] for j in range(17)]
        col2 = [['#%02x%02x%02x' % (255,255,255 ) for i in range(10) ] for j in range(10)]
        colorUpdater.updateColors(colorMatrix=col1, labels=self.regGrid)
        colorUpdater.updateSplitColors(colorMatrix=col2, labels=self.splitGrid )
        self.handsPlayed.config(text="%i" % 0)
        self.generationsCount.config(text="%i" % 0)
        self.preformance.config(text="%.2f" % 0)


    def runEa(self, agents):
        self.pop = ea.Evolution(agents)
        self.pop.evolve(self.updateUI , int(self.handsVal.get()), int(self.roundsVal.get()))

    def createControls(self, root):
        ## run button
        runButton = tk.Button(root, text="Run", padx=10, pady=1, command= lambda: self.runThread()).grid(row=9,column=24)

        ## reset button
        resetButton = tk.Button(root, text="Reset", padx=10, pady=1, command= lambda: self.reset()).grid(row=9,column=25)

        ## hands per round control and label
        self.handsVal = tk.StringVar(value=100)
        handSpinner = tk.Spinbox(root,from_=20, to=200, textvariable=self.handsVal , wrap=False).grid(row=3,column=25)
        handsControlLabel = tk.Label(root, text="Hands Per Round:", padx=5).grid(row=3, column=24, sticky=tk.W)

        ## rounds control and label
        self.roundsVal = tk.StringVar(value=200)
        roundSpinner = tk.Spinbox(root,from_=10, to=2000, textvariable=self.roundsVal, wrap=False).grid(row=5,column=25)
        roundsControlLabel = tk.Label(root, text="Iterations:", padx=5 ).grid(row=5, column=24, sticky=tk.W)

        ## agents control and label
        self.agentsVal = tk.StringVar(value=160)
        agentSpinner = tk.Spinbox(root,from_=10, to=200, textvariable=self.agentsVal, wrap=False).grid(row=7,column=25)
        agentsControlLabel = tk.Label(root, text="Number of Agents:", padx=5 ).grid(row=7, column=24, sticky=tk.W)

    def creatGridKey(self, root):
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

    def createStatLabels(self, root):
        handsPlayedLabel = tk.Label(root, text="Number of Hands Played:", padx=5 ).grid(row=13, column=24, sticky=tk.W)
        generationLabel = tk.Label(root, text="Generations:", padx=5 ).grid(row=14, column=24, sticky=tk.W)
        preformanceLabel = tk.Label(root, text="Top 10% Ave Preformance", padx=5 ).grid(row=15, column=24, sticky=tk.W)
        handsPlayedLabel2 = tk.Label(root, text="0", padx=5 )
        handsPlayedLabel2.grid(row=13, column=25, sticky=tk.W)
        generationLabel2 = tk.Label(root, text="0", padx=5 )
        generationLabel2.grid(row=14, column=25, sticky=tk.W)
        preformanceLabel2 = tk.Label(root, text="0", padx=5 )
        preformanceLabel2.grid(row=15, column=25, sticky=tk.W)

        return handsPlayedLabel2, generationLabel2, preformanceLabel2



class ColorUpdater:

    def getColorElement(self, agents, i, j ): ## gets the matrix[i][j] element
        hitCount = 0
        stayCount = 0
        doubleCount = 0
        for k in range (0,10):
            agent = agents[k]
            action = agent.actionHandler.regLogic[i][j]
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

    def getSplitColorElement(self, agents, i, j ): ## gets the matrix[i][j] element
        hitCount = 0
        stayCount = 0
        doubleCount = 0
        splitCount = 0
        for k in range (0,10):
            agent = agents[k]
            action = agent.actionHandler.doublesLogic[i][j]
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

    def getSplitColorMatrix(self, agents):
        splitColorMatrix = []
        for i in range (0, 10):  # 17 rows for 5-21 possible hand totals, 
            row =[]
            for j in range(0,10):  # 13 columsn for 2-A possible face up cards
                row.append((self.getSplitColorElement(agents,i,j)))
            splitColorMatrix.append(row)
        return splitColorMatrix

    def getColorMatrix(self, agents):
        colorMatrix = []   #where arr [x][y] gives the xth row and yth column, retrieve action using arr[hand sum][dealer card num]
        for i in range (0, 17):  # 17 rows for 5-21 possible hand totals, 
            row =[]
            for j in range(0,10):  # 13 columsn for 2-A possible face up cards
                row.append((self.getColorElement(agents,i,j)))
            colorMatrix.append(row)
        return colorMatrix

    def updateSplitColors(self, colorMatrix,labels):
        height = 10
        width = 10
        for i in range(height): #Rows
            for j in range(width): #Columns 
                mycolor = colorMatrix[i][j]
                labels[i][j].config(bg=mycolor)

    def updateColors(self, colorMatrix, labels):
        height = 17
        width = 10
        for i in range(height): #Rows
            for j in range(width): #Columns 
                mycolor = colorMatrix[i][j]
                labels[i][j].config(bg=mycolor)


ui = UI() 



