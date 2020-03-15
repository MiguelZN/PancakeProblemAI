import math,copy

class Pancake:

    def __init__(self, id, position=-1):
        self.position = position
        self.id = id

    def __str__(self):
        return "Pancake" + str(self.id)
        #return "POS:"+str(self.position)+";Pancake"+str(self.id)

class PancakeStack:
    def __init__(self):
        self.stack = []
        self.__contained = {}



    def addPancake(self, pancake:Pancake, duplicates=False):

        if(duplicates==False):
            if(self.__contained.__contains__(pancake.id)==False):
                self.__contained[pancake.id] = 1
                self.stack = self.stack + [pancake]
                #print(self.__contained)
            else:
                print('Did not add duplicate pancake')


        else:
            self.stack = self.__stack+[pancake]

        self.stack=PancakeStack.getSortedStackBottomToTop(self.stack)
        self.stack=PancakeStack.SimReassignPositions(self.stack)

    def pancakeDFS(self):
        # AI:----------------
        pancakeFringe = []
        pancakeClosedSet = set([])

        pancakeFringe = self.stack #should first set options starting at the bottom

        PancakeStack.printGivenStack(pancakeFringe)

        while(self.hasReachedGoal()==False):
            ''

    def getStack(self):
        return self.stack

    def printGivenStack(listofpancakes, topDownView=False, asStr=False):
        returnstr = ""

        #if(asStr):


        if(topDownView):
            returnstr = "Top---\n"
            for x in range(len(listofpancakes)-1,-1,-1):
                returnstr += listofpancakes.__getitem__(x).__str__() + '\n'

            returnstr+="Bottom---"
        else:
            returnstr = "|BOTTOM|["
            for x in listofpancakes:
                returnstr += x.__str__()+','

            returnstr = returnstr[0:len(returnstr)-1]+"]|TOP|"


        print(returnstr)



    def printStack(self, topDownView=False):
        returnstr = ""

        if(topDownView):
            returnstr = "Top---\n"
            for x in range(len(self.stack)-1,-1,-1):
                returnstr += self.stack.__getitem__(x).__str__() + '\n'

            returnstr+="Bottom---"
        else:
            returnstr = "|BOTTOM|["
            for x in self.stack:
                returnstr += x.__str__()+','

            returnstr = returnstr[0:len(returnstr)-1]+"]|TOP|"


        print(returnstr)

    def drawStack(self):

        print("TOP")
        spaceadd = len(self.stack)
        for i in range(len(self.stack)-1,-1,-1):
            pancake = self.stack.__getitem__(i)
            drawline = "-"
            drawlineMulti=2


            print(str(pancake.position)+"|Pancake"+str(pancake.id)+":"+(" "*spaceadd)+((pancake.id*drawlineMulti)*drawline))
            spaceadd-=1

        print("BOTTOM")

    def hasReachedGoal(self):
        goalstack = PancakeStack.getSortedStackBottomToTop(self.stack)
        #print(goalstack)
        #self.printGivenStack(goalstack)

        # default is true unless found one pancake that does not match
        hasreachedgoal = True


        for i in range(0,len(goalstack)):
            goalpancake = goalstack.__getitem__(i)
            currpancake = self.__stack.__getitem__(i)

            if(goalpancake.id!=currpancake.id):
                hasreachedgoal = False

        return hasreachedgoal

    def reassignPositions(self):
        position = len(self.stack)
        for i in range(0,len(self.stack),1):
            currpancake = self.stack.__getitem__(i)
            currpancake.position = position
            #print("NEW POSITION:"+str(currpancake.position))
            position-=1

        self.stack= PancakeStack.getSortedStackBottomToTop(self.stack)

    def SimReassignPositions(listOfPancakes):
        #PancakeStack.printGivenStack(listOfPancakes)
        position = len(listOfPancakes)
        newlist = listOfPancakes
        for i in range(0,len(newlist),1):
            currpancake = newlist.__getitem__(i)
            currpancake.position = position
            #print("NEW POSITION:"+str(currpancake.position))
            position-=1

        newlist=PancakeStack.getSortedStackBottomToTop(newlist)

        return newlist

    #Successor function:
    #Flips the by the position of the pancake
    def flipPancakes(self, posnumber:int):

        splitindex = 0
        foundid = False
        for i in range(0,len(self.stack)):
            if(self.stack.__getitem__(i).position==posnumber):
                splitindex = i
                foundid = True

        if(foundid==False):
            print("DID NOT FIND PANCAKE ID, enter valid pancake id...")
            return



        bottomlist = self.stack[0:splitindex]
        toplist = self.stack[splitindex:len(self.stack)]
        toplist.reverse()

        self.stack = bottomlist+toplist
        self.reassignPositions()

    def returnPancakeListAsStr(listOfPancakes):
        returnStr = ""
        for pancake in listOfPancakes:
            returnStr += str(pancake.id)
        return returnStr


    # Successor function:
    # Flips the by the position of the pancake
    def SimFlipPancakes(listOfPancakes, posnumber: int, ReturnAsString=False):
        listcopy = copy.deepcopy(listOfPancakes)
        splitindex = 0
        foundid = False
        for i in range(0, len(listcopy)):
            if (listcopy.__getitem__(i).position == posnumber):
                splitindex = i
                #print("FOUND POS TO FLIP")
                foundid = True

        if (foundid == False):
            print("DID NOT FIND PANCAKE ID, enter valid pancake id...")
            return

        bottomlist = listcopy[0:splitindex]
        toplist = listcopy[splitindex:len(listcopy)]
        toplist.reverse()

        pretendlist= bottomlist + toplist
        pretendlist=PancakeStack.SimReassignPositions(pretendlist)
        #PancakeStack.printGivenStack(pretendlist)


        if(ReturnAsString):
            pancakeliststr = PancakeStack.returnPancakeListAsStr(pretendlist)
            print(pancakeliststr)
            return pancakeliststr
        else:
            return pretendlist


    def getSortedStackBottomToTop(listOfPancakes):
        #self.printStack()
        sortedstackASC = sorted(listOfPancakes,key=lambda x: x.position)
        #self.printGivenStack(sortedstackASC)
        sortedstackDEC = sorted(sortedstackASC,key=lambda x:x.position, reverse=True)
        #PancakeStack.printGivenStack(sortedstackDEC)
        return sortedstackDEC



    def __str__(self):
        return self.printStack(True)




#returns the largest pancake id not in order (COST)
def heuristicFunction(listOfPancakes):
    #self.printStack(False)
    #sortedstack = sorted(self.__stack,key=lambda x: x.id, reverse = True)
    #self.printStack(False)
    sortedstack = PancakeStack.getSortedStackBottomToTop(listOfPancakes)
    largestnoninorder_pancake = None

    for i in range(0,len(listOfPancakes)):
        sortedpancake = sortedstack.__getitem__(i)
        currpancake = listOfPancakes.__getitem__(i)

        if(largestnoninorder_pancake==None):
            largestnoninorder_pancake = currpancake

        if(sortedpancake.id==currpancake.id):
            print("Good")
        elif(sortedpancake.id!=currpancake.id and currpancake.id>largestnoninorder_pancake.id):
            largestnoninorder_pancake = currpancake

    return largestnoninorder_pancake.id

#Takes in two Pancake lists and returns the higher valued Pancake sequence
def tiebreakingFunction(pancakeseq1, pancakeseq2):
    # pancakeseq1 = PancakeStack()
    # pancakeseq1.addPancake(Pancake(4))
    # pancakeseq1.addPancake(Pancake(3))
    # pancakeseq1.addPancake(Pancake(2))
    # pancakeseq1.addPancake(Pancake(1))
    #
    # pancakeseq2 = PancakeStack()
    # pancakeseq2.addPancake(Pancake(3))
    # pancakeseq2.addPancake(Pancake(4))
    # pancakeseq2.addPancake(Pancake(2))
    # pancakeseq2.addPancake(Pancake(1))

    fourdigitstr1 = ""
    fourdigitstr2 = ""

    for x in pancakeseq1.__stack:
        fourdigitstr1+=str(x.id)

    for x in pancakeseq2.__stack:
        fourdigitstr2+=str(x.id)

    fourdigitnum1 = int(fourdigitstr1)
    #print(fourdigitnum1)
    fourdigitnum2 = int(fourdigitstr2)
    #print(fourdigitnum2)

    if(fourdigitnum1>=fourdigitnum2):
        #print("STACK 1")
        #pancakeseq1.printStack()
        return pancakeseq1
    else:
        #print("STACK 2")
        #pancakeseq2.printStack()
        return pancakeseq2

    return None


def pancakeProblem():
    pancakestack = PancakeStack()
    textinput = ""
    requirements = "####X" #where X is either 'a' or 'b'




    try:
        #Input should be four sequence digits, and a 'd' or 'a' character fifth place
        textinput = input("Enter input for Pancake Problem:"+ requirements[0:len(requirements)-1]+'d or '+ requirements[0:len(requirements)-1]+"a\n")
    except:
        ""

    #Error catching for incorrect input-----------------
    isGoodInput = False

    try:
        for i in range(0,len(requirements),1):
            if(i==len(requirements)-1 and textinput[i].isalpha()):
                isGoodInput = True

            if(i<len(requirements)-1 and textinput[i].isdigit()==False):
                isGoodInput = False
                break
    except:
        ""




    try:
        if(isGoodInput==False):
            raise Exception("ERROR: the input needs to be "+ requirements[0:len(requirements)-1]+'d or '+ requirements[0:len(requirements)-1]+'a')
    except Exception as error:
        print("Caught error:"+repr(error))
        return
    #---------------------------------------------------



    DFSorAStar = textinput[len(textinput)-1]
    position = len(textinput)-1
    for i in range(0,len(textinput),1):
        curr_char = textinput.__getitem__(i)

        if(curr_char.isdigit()):
            pancakestack.addPancake(Pancake(int(curr_char),position), False)
            position-=1

    print("HAS REACHED GOAL?:" + str(pancakestack.hasReachedGoal()))


    #MENU:------------
    inputoption = -1#start value
    while(inputoption!="exit"):
        #pancakestack.printStack(True)
        pancakestack.drawStack()
        pancakestack.printStack(False)
        print("")
        #pancakestack.heuristicFunction()
        print("Enter a number to flip pancakes:")
        print("(OR enter 'exit' to exit)")

        #try:
        inputoption = input("")

        if(inputoption=="exit"):
            print("Exiting...")
            break
        elif(inputoption[0].isdigit()==False):
            print("Enter a single digit number representing the id of pancake to flip...")
            continue
        else:
            inputoption = int(inputoption[0])

            print("Flipping pancake:"+str(inputoption))
            pancakestack.flipPancakes(inputoption)
            print("HAS REACHED GOAL?:" + str(pancakestack.hasReachedGoal()))

        #except:
        #    print("Error in option selection")






    print(textinput)



def main():
    print("MAIN:")
    #
    # pancakestack = PancakeStack()
    #
    # for i in range(4,0,-1):
    #     pancakestack.addPancake(Pancake(i))

    #pancakestack.addPancake(Pancake(3))
    #pancakestack.addPancake(Pancake(4))
    #pancakestack.addPancake(Pancake(1))
    #pancakestack.addPancake(Pancake(2))

    #
    # pancakestack.printStack(False)
    # print("")
    # pancakestack.printStack(True)
    #
    # print("")
    # pancakestack.drawStack()



    #pancakeProblem()

    testlist = [Pancake(4,4),Pancake(3,3),Pancake(2,2),Pancake(1,1)]
    #print(testlist.__getitem__(0).id)
    PancakeStack.printGivenStack(testlist)
    PancakeStack.SimFlipPancakes(testlist,1, True)
    PancakeStack.SimFlipPancakes(testlist, 2, True)
    PancakeStack.SimFlipPancakes(testlist, 3, True)

    print("GETTING STRING VERSION")
    PancakeStack.SimFlipPancakes(testlist, 4, True)

    ps = PancakeStack()
    ps.addPancake(Pancake(3))
    ps.addPancake(Pancake(4))
    ps.addPancake(Pancake(2))
    ps.addPancake(Pancake(1))
    ps.drawStack()
    ps.printStack()
    ps.addPancake(Pancake(8))
    ps.drawStack()
    ps.printStack()
    PancakeStack.SimFlipPancakes(ps.getStack(), 1, True)
    PancakeStack.SimFlipPancakes(ps.getStack(), 2, True)
    PancakeStack.SimFlipPancakes(ps.getStack(), 3, True)
    PancakeStack.SimFlipPancakes(ps.getStack(), 4, True)
    PancakeStack.SimFlipPancakes(ps.getStack(),5,True)







main()