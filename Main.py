import math,copy

class Pancake:

    def __init__(self, id, position=-1):
        self.position = position
        self.id = id

    def __str__(self):
        #return "Pancake" + str(self.id)
        return "POS:"+str(self.position)+";Pancake"+str(self.id)

class PancakeSeq:
    def __init__(self, seq:str, parent = None, children = None, isRoot=False):
        self.seq = seq
        self.parent = parent
        self.children = None
        self.isRoot=isRoot

        self.parentFlipPosition = -1 #This is the position that was flipped from Parent pancake sequence to get to this sequence (self)
        self.parentToSelfCost = 0
        self.rootToSelfCost = 0 #G(x)
        self.heuristicCost = self.heuristicFunction() #H(x)
        self.fNCost = 0 #this will not be changed until we get the rootToSelfCost F(x)

        self.largestPancake = -1
        self.smallestPancake = -1
        self.findSmallestLargestPancakes()

    def __repr__(self):
        return self.seq

    # returns the largest pancake id not in order (COST)
    def heuristicFunction(self):
        listOfPancakes = PancakeStack.convertPancakeSeqStrToList(self.seq)
        # self.printStack(False)
        # sortedstack = sorted(self.__stack,key=lambda x: x.id, reverse = True)
        # self.printStack(False)
        sortedstack = PancakeStack.getSortedStackBottomToTop(listOfPancakes)
        largestnoninorder_pancake = None

        for i in range(0, len(listOfPancakes)):
            sortedpancake = sortedstack.__getitem__(i)
            currpancake = listOfPancakes.__getitem__(i)


            if (sortedpancake.id == currpancake.id):
                ''
                # print("Good")
            elif(largestnoninorder_pancake==None and sortedpancake.id!=currpancake.id):
                largestnoninorder_pancake = currpancake
            elif (sortedpancake.id != currpancake.id and currpancake.id > largestnoninorder_pancake.id):
                largestnoninorder_pancake = currpancake

        if(largestnoninorder_pancake==None):
            return 0
        else:
            return largestnoninorder_pancake.id

    #Finds the smallest and largest pancakes in the sequence
    def findSmallestLargestPancakes(self):
        self.smallestPancake = int(self.seq[0])
        self.largestPancake = int(self.seq[0])
        for c in self.seq:
            curr_num = int(c)
            if(curr_num<self.smallestPancake):
                self.smallestPancake = curr_num

            if(curr_num>self.largestPancake):
                self.largestPancake=curr_num

    def drawStackOfPancakes(self, multiplier=2, includeID=True):
        foundationlen = self.largestPancake*multiplier

        for i in range(len(self.seq)-1,-1,-1):
            currDigit = int(self.seq[i])
            currLen = currDigit*multiplier
            numSpaces= int((foundationlen-currLen)/2)*multiplier

            currPancakeDrawStr = ""

            if (includeID):
                currPancakeDrawStr = "ID:" + str(currDigit) + "|" + (
                            ' ' * numSpaces) + ('-' * multiplier * currLen)
            else:
                currPancakeDrawStr = (' ' * numSpaces) + ('-' * multiplier * currLen)
            print(currPancakeDrawStr)

    def getDrawStackOfPancakesStr(self, multiplier=2, includeID=True):
        pancakeStackStr = ""
        foundationlen = self.largestPancake*multiplier

        for i in range(len(self.seq)-1,-1,-1):
            currDigit = int(self.seq[i])
            currLen = currDigit*multiplier
            numSpaces= int((foundationlen-currLen)/2)*multiplier
            currPancakeDrawStr =""

            if(includeID):
                currPancakeDrawStr = "ID:"+str(currDigit)+"|"+(' ' * numSpaces) + ('-' * multiplier * currLen)
            else:
                currPancakeDrawStr = (' '*numSpaces)+('-'*multiplier*currLen)
            pancakeStackStr+=currPancakeDrawStr+'\n'

        return pancakeStackStr

    def __eq__(self, other):
        if(isinstance(other, PancakeSeq)):
            return self.seq==other.seq
        elif(isinstance(other,str)):
            return self.seq==other
        else:
            return False

    #This gets the ID of the pancake that was flipped to get this current sequence using the position (int)
    def getIntPancakeIDFromParentFlipPosition(self):
        parentSeqStr = self.parent.seq
        ID = int(parentSeqStr[len(parentSeqStr)-self.parentFlipPosition])
        return ID

    def getSeqStr(self):
        return self.seq
    def getParent(self):
        return self.parent

    def __str__(self):
        return self.seq

    # ACTUAL COST for specified flip position
    # Returns the amount of pancakes being flipped (Cost) from the parent sequence to this sequence
    # self.parentFlipPosition is the position of the pancake that was flipped to get this sequence
    # EX: Parent sequence4213, pancake(ID:4) is position 4, pancake(ID:3) is position 1, this is the COST
    def getParentToSelfFlipCost(self):
        if(self.parentFlipPosition>0):
            return self.parentFlipPosition
        else:
            return 0

    def getFlipCostGivenPosition(self, flipPosition:int):
        if(flipPosition>0 and flipPosition<=len(self.seq)):
            return flipPosition
        else:
            return 0



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
            self.stack = self.stack+[pancake]

        self.stack=PancakeStack.getSortedStackBottomToTop(self.stack)
        PancakeStack.SimReassignPositions(self.stack)



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

    def drawGivenStack(listOfPancakes):

        print("TOP")
        spaceadd = len(listOfPancakes)
        for i in range(len(listOfPancakes)-1,-1,-1):
            pancake = listOfPancakes.__getitem__(i)
            drawline = "-"
            drawlineMulti=2


            print(str(pancake.position)+"|Pancake"+str(pancake.id)+":"+(" "*spaceadd)+((pancake.id*drawlineMulti)*drawline))
            spaceadd-=1

        print("BOTTOM")

    def SimHasReachedGoal(PancakeSeqStr:str):
        stack = PancakeStack.convertPancakeSeqStrToList(PancakeSeqStr)

        PancakeStack.printGivenStack(stack)
        goalstack = PancakeStack.getSortedStackBottomToTop(stack)
        PancakeStack.printGivenStack(goalstack)
        #print(goalstack)
        #self.printGivenStack(goalstack)

        # default is true unless found one pancake that does not match
        hasreachedgoal = True


        for i in range(0,len(goalstack)):
            goalpancake = goalstack.__getitem__(i)
            currpancake = stack.__getitem__(i)

            if(goalpancake.id!=currpancake.id):
                hasreachedgoal = False

        if(hasreachedgoal):
            print("The seq:"+PancakeSeqStr+" has reached GOAL")
        else:
            print("The seq:" + PancakeSeqStr + " has NOT reached GOAL")

        return hasreachedgoal

    def hasReachedGoal(self):
        hasreachedgoal= PancakeStack.SimHasReachedGoal(PancakeStack.returnPancakeListAsStr(self.stack))

        return hasreachedgoal

    def reassignPositions(self):
        PancakeStack.SimReassignPositions(self.stack)

    def SimReassignPositions(listOfPancakes):
        #PancakeStack.printGivenStack(listOfPancakes)
        position = len(listOfPancakes)
        for i in range(0,len(listOfPancakes),1):
            currpancake = listOfPancakes.__getitem__(i)
            currpancake.position = position
            #print("NEW POSITION:"+str(currpancake.position))
            position-=1



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

    def convertPancakeSeqStrToList(pancakeseq:str):
        listOfPancakes = []
        print("SEQ:"+pancakeseq)
        if(pancakeseq.isnumeric()):
            position=len(pancakeseq)
            for i in range(0,len(pancakeseq),1):
                id = int(pancakeseq.__getitem__(i))
                newpancake = Pancake(id,position)
                #print(newpancake)
                listOfPancakes =listOfPancakes+ [newpancake]
                #PancakeStack.printGivenStack(listOfPancakes)
                position-=1

            return listOfPancakes
        else:
            print("ERROR-Not a sequence")



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
        PancakeStack.SimReassignPositions(pretendlist)
        #PancakeStack.printGivenStack(pretendlist)


        if(ReturnAsString):
            pancakeliststr = PancakeStack.returnPancakeListAsStr(pretendlist)
            print(pancakeliststr)
            return pancakeliststr
        else:
            return pretendlist


    def getSortedStackBottomToTop(listOfPancakes):
        #self.printStack()
        sortedstackASC = sorted(listOfPancakes,key=lambda x: x.id)
        #PancakeStack.printGivenStack(sortedstackASC)
        sortedstackDEC = sorted(sortedstackASC,key=lambda x:x.id, reverse=True)
        PancakeStack.SimReassignPositions(sortedstackDEC)
        #PancakeStack.printGivenStack(sortedstackDEC)
        return sortedstackDEC



    def __str__(self):
        return self.printStack(True)






#Takes in two Pancake lists and returns the higher valued Pancake sequence
def tiebreakingFunction(pancakeseq1:PancakeSeq, pancakeseq2:PancakeSeq):
    fourdigitnum1 = int(pancakeseq1.seq)
    #print(fourdigitnum1)
    fourdigitnum2 = int(pancakeseq2.seq)
    #print(fourdigitnum2)

    if(fourdigitnum1>=fourdigitnum2):
        #print("STACK 1")
        return pancakeseq1
    else:
        #print("STACK 2")
        return pancakeseq2

    return None


def pancakeAStar(startPancakeSeq:PancakeSeq):
    # AI:----------------
    pancakeFringe = []
    pancakeClosedSet = set([]) #contains all of the visited node states already
    PancakeStack.printGivenStack(pancakeFringe)
    actualCost = 0 #the total cost to flip/accumulation of total amount of pancakes flipped

    num_pancakestates = math.factorial(len(startPancakeSeq.seq))
    currStateSeq = startPancakeSeq
    goalStateSeq = None

    #Adding start state to fringe
    pancakeFringe.append(currStateSeq)

    #Number of total states = n! where n is the number of pancakes
    #In our case n = 4, thus 4! = 24 total possible states
    while(num_pancakestates>=len(pancakeClosedSet) or len(pancakeFringe)==0):
        # Loops through the fringe and finds the pancake sequence with smallest f(x) cost
        smallestFNCostpancake = pancakeFringe[0]
        for pancake in pancakeFringe:
            if (smallestFNCostpancake.seq != pancake.seq and smallestFNCostpancake.fNCost > pancake.fNCost):
                smallestFNCostpancake = pancake
            #Uses the tie-breaking function to determine the better sequence state
            elif(smallestFNCostpancake!=pancake.seq and smallestFNCostpancake.fNCost==pancake.fNCost):
                smallestFNCostpancake = tiebreakingFunction(smallestFNCostpancake,pancake)
        currStateSeq = smallestFNCostpancake
        print("SMALLEST F(X) COST:"+str(smallestFNCostpancake))
        pancakeFringe.remove(currStateSeq)  # Remove from fringe


        #Converting pancakeSeqString into a pancake list and get all possible flip states from it
        currStatePancakeList = PancakeStack.convertPancakeSeqStrToList(currStateSeq.seq)
        #PancakeStack.printGivenStack(currStatePancakeList)

        #Add to closed set
        if(currStateSeq.seq not in pancakeClosedSet):
            pancakeClosedSet.add(currStateSeq.seq)

            #Expanding states (Creating branch/children nodes for current node)
            expandedStates = [] #Children nodes
            for pancake in currStatePancakeList:
                childSeq = PancakeSeq(PancakeStack.SimFlipPancakes(currStatePancakeList,pancake.position,True))
                print("POS:"+str(pancake.position)+"|Seq:"+currStateSeq.seq)
                childSeq.parentFlipPosition = pancake.position
                childSeq.parentToSelfCost = pancake.position
                childSeq.parent=currStateSeq

                childSeq.rootToSelfCost=actualCost+childSeq.parentToSelfCost
                childSeq.fNCost = currStateSeq.heuristicCost+childSeq.rootToSelfCost

                if(childSeq.seq not in pancakeClosedSet):
                    expandedStates.append(childSeq)

            #Calculating Flip Cost (G(x))
            actualCost += currStateSeq.parentToSelfCost  # Gets the pancake flip cost
            currStateSeq.rootToSelfCost = actualCost

            #Getting the F(x) cost = heuristic + total Flip Cost = h(x) + g(x)
            #currStateSeq.fNCost = currStateSeq.heuristicCost+currStateSeq.rootToSelfCost


            currStateSeq.children = expandedStates

            print("EXPANDED STATES:")
            print(expandedStates)

            print("CLOSED SET:")
            print(pancakeClosedSet)
            #pancakeFringe.append("2555")
            print("FRINGE AFTER EXPANDING: ")
            #print(pancakeFringe)

            pancakeFringe = expandedStates+pancakeFringe[0:len(pancakeFringe)]
            print(pancakeFringe)

            #Checking if the current pancake sequence is sorted (GOAL State)
            if (PancakeStack.SimHasReachedGoal(currStateSeq.seq)):
                print("BROKE OUT BECAUSE FOUND GOAL\n\n")
                goalStateSeq = currStateSeq
                break




    #print("FOUND:"+goalStateSeq.seq)

    temp = goalStateSeq
    #print("PATH FROM GOAL TO ROOT")
    instructions = []

    instructions.append(temp.getDrawStackOfPancakesStr())

    #"Actual Cost:" + str(actualCost)

    if (temp.parentFlipPosition == 1):
        #print("FLIPPED " + str(temp.parentFlipPosition) + "st largest pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition(self))+")to get:" + temp.__str__()+"\nActual Cost:"+str(temp.rootToSelfCost))
        instructions.append("FLIPPED " + str(temp.parentFlipPosition) + "st pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition())+")to get:" + temp.__str__()+"\nActual Cost:"+str(temp.rootToSelfCost))

    elif (temp.parentFlipPosition == 2):
        #print("FLIPPED " + str(temp.parentFlipPosition) + "nd largest pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition(self))+")to get:" + temp.__str__()+"\nActual Cost:"+str(temp.rootToSelfCost))
        instructions.append("FLIPPED " + str(temp.parentFlipPosition) + "nd pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition())+")to get:" + temp.__str__()+"\nActual Cost:"+str(temp.rootToSelfCost))
    elif (temp.parentFlipPosition == 3):
        #print("FLIPPED " + str(temp.parentFlipPosition) + "rd largest pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition(self))+")to get:" + temp.__str__()+"\nActual Cost:"+str(temp.rootToSelfCost))
        instructions.append("FLIPPED " + str(temp.parentFlipPosition) + "rd pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition())+")to get:" + temp.__str__()+"\nActual Cost:"+str(temp.rootToSelfCost))
    elif (temp.isRoot):
        #print("Started at Root:" + temp.__str__()+"\nActual Cost:"+str(actualCost))
        instructions.append("Started at Root:" + temp.__str__()+"\nActual Cost:"+str(actualCost))
    else:
        #print("FLIPPED " + str(temp.parent.parentFlipPosition) + "th largest pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition(self))+")to get:" + temp.__str__()+"\nActual Cost:"+str(temp.rootToSelfCost))
        instructions.append("FLIPPED " + str(temp.parentFlipPosition) + "th pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition())+")to get:" + temp.__str__()+"\nActual Cost:"+str(temp.rootToSelfCost))

    while(True):
        if(temp.parent!=None):
            instructions.append(temp.parent.getDrawStackOfPancakesStr())
            if(temp.parent.parentFlipPosition==1):
                #print("FLIPPED " + str(temp.parent.parentFlipPosition) + "st largest pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition(self))+")to get:" + temp.parent.__str__()+"\Actual Cost:"+str(temp.parent.rootToSelfCost))
                instructions.append("FLIPPED " + str(temp.parent.parentFlipPosition) + "st pancake(ID:"+str(temp.parent.getIntPancakeIDFromParentFlipPosition())+")to get:" + temp.parent.__str__()+"\nActual Cost:"+str(temp.parent.rootToSelfCost))
            elif(temp.parent.parentFlipPosition==2):
                #print("FLIPPED " + str(temp.parent.parentFlipPosition) + "nd largest pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition(self))+")to get:" + temp.parent.__str__()+"\Actual Cost:"+str(temp.parent.rootToSelfCost))
                instructions.append("FLIPPED " + str(temp.parent.parentFlipPosition) + "nd pancake(ID:"+str(temp.parent.getIntPancakeIDFromParentFlipPosition())+")to get:" + temp.parent.__str__()+"\nActual Cost:"+str(temp.parent.rootToSelfCost))
            elif(temp.parent.parentFlipPosition==3):
                #print("FLIPPED " + str(temp.parent.parentFlipPosition) + "rd largest pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition(self))+")to get:" + temp.parent.__str__()+"\Actual Cost:"+str(temp.parent.rootToSelfCost))
                instructions.append("FLIPPED " + str(temp.parent.parentFlipPosition) + "rd pancake(ID:"+str(temp.parent.getIntPancakeIDFromParentFlipPosition())+")to get:" + temp.parent.__str__()+"\nActual Cost:"+str(temp.parent.rootToSelfCost))
            elif(temp.parent.isRoot):
                #print("Started with:" + temp.parent.__str__()+"\nActual Cost:"+str(actualCost))
                ''
            else:
                #print("FLIPPED " + str(temp.parent.parentFlipPosition) + "th largest pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition(self))+")to get:" + temp.parent.__str__()+"\nActual Cost:"+str(temp.parent.rootToSelfCost))
                instructions.append("FLIPPED " + str(temp.parent.parentFlipPosition) + "th pancake(ID:"+str(temp.parent.getIntPancakeIDFromParentFlipPosition())+")to get:" + temp.parent.__str__()+"\nActual Cost:"+str(temp.parent.rootToSelfCost))

        temp = temp.parent

        if(temp==None):
            #print("FOUND ROOT")
            break

        if(temp.isRoot):
            break

    instructions.reverse()
    print("Printing instructions:")
    print("Started with:" + startPancakeSeq.__str__())

    index = 0
    for i in range(0,len(instructions)):
        line=instructions[i]

        if('-' in line):
            print(line)
        else:
            index += 1
            print("Step "+str(index) + ") " + line)

    print("Finished:" + goalStateSeq.seq)
    print("Total Actual Cost:"+str(actualCost))
    print("Finished in "+str(index)+" steps using AStar.")

    goalStateSeq.drawStackOfPancakes()

#returns the largest pancake id not in order (COST)
def heuristicFunction(pancakeSeq:PancakeSeq):
    listOfPancakes=PancakeStack.convertPancakeSeqStrToList(pancakeSeq.seq)
    #self.printStack(False)
    #sortedstack = sorted(self.__stack,key=lambda x: x.id, reverse = True)
    #self.printStack(False)
    sortedstack = PancakeStack.getSortedStackBottomToTop(listOfPancakes)
    largestnoninorder_pancake = None

    for i in range(0, len(listOfPancakes)):
        sortedpancake = sortedstack.__getitem__(i)
        currpancake = listOfPancakes.__getitem__(i)

        if (sortedpancake.id == currpancake.id):
            ''
            # print("Good")
        elif (largestnoninorder_pancake == None and sortedpancake.id != currpancake.id):
            largestnoninorder_pancake = currpancake
        elif (sortedpancake.id != currpancake.id and currpancake.id > largestnoninorder_pancake.id):
            largestnoninorder_pancake = currpancake

    if (largestnoninorder_pancake == None):
        return 0
    else:
        return largestnoninorder_pancake.id


def createPancakeHeap(startPancakeSeq:str):
    ''



def pancakeDFS(startPancakeSeq:PancakeSeq):
    # AI:----------------
    pancakeFringe = []
    pancakeClosedSet = set([]) #contains all of the visited node states already
    PancakeStack.printGivenStack(pancakeFringe)
    actualCost = 0 #the total cost to flip/accumulation of total amount of pancakes flipped

    num_pancakestates = math.factorial(len(startPancakeSeq.seq))
    currStateSeq = startPancakeSeq
    goalStateSeq = None

    #Adding start state to fringe
    pancakeFringe.append(currStateSeq)

    #Number of total states = n! where n is the number of pancakes
    #In our case n = 4, thus 4! = 24 total possible states
    while(num_pancakestates>=len(pancakeClosedSet) or len(pancakeFringe)==0):
        currStateSeq = pancakeFringe.__getitem__(0)#get first pancake state in fringe
        pancakeFringe.remove(currStateSeq)#Remove from fringe

        #Converting pancakeSeqString into a pancake list and get all possible flip states from it
        currStatePancakeList = PancakeStack.convertPancakeSeqStrToList(currStateSeq.seq)
        PancakeStack.printGivenStack(currStatePancakeList)

        #Add to closed set
        if(currStateSeq.seq not in pancakeClosedSet):
            pancakeClosedSet.add(currStateSeq.seq)

            #Expanding states (Creating branch/children nodes for current node)
            expandedStates = [] #Children nodes
            for pancake in currStatePancakeList:
                childSeq = PancakeSeq(PancakeStack.SimFlipPancakes(currStatePancakeList,pancake.position,True))
                print("POS:"+str(pancake.position)+"|Seq:"+currStateSeq.seq)
                childSeq.parentFlipPosition = pancake.position
                childSeq.parentToSelfCost = pancake.position
                childSeq.parent=currStateSeq
                if (childSeq.seq not in pancakeClosedSet):
                    expandedStates.append(childSeq)

            actualCost += currStateSeq.parentToSelfCost  # Gets the pancake flip cost
            currStateSeq.rootToSelfCost = actualCost

            currStateSeq.children = expandedStates

            print("EXPANDED STATES:")
            print(expandedStates)

            print("CLOSED SET:")
            print(pancakeClosedSet)
            #pancakeFringe.append("2555")
            print("FRINGE AFTER EXPANDING: ")
            #print(pancakeFringe)

            pancakeFringe = expandedStates+pancakeFringe[0:len(pancakeFringe)]
            print(pancakeFringe)

            #Checking if the current pancake sequence is sorted (GOAL State)
            if (PancakeStack.SimHasReachedGoal(currStateSeq.seq)):
                print("BROKE OUT BECAUSE FOUND GOAL\n\n")
                goalStateSeq = currStateSeq
                break

    #print("FOUND:"+goalStateSeq.seq)

    temp = goalStateSeq
    #print("PATH FROM GOAL TO ROOT")
    instructions = []

    instructions.append(temp.getDrawStackOfPancakesStr())


    if (temp.parentFlipPosition == 1):
        #print("FLIPPED " + str(temp.parentFlipPosition) + "st largest pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition(self))+")to get:" + temp.__str__()+"\nActual Cost:"+str(temp.rootToSelfCost))
        instructions.append("FLIPPED " + str(temp.parentFlipPosition) + "st pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition())+")to get:" + temp.__str__()+"\nActual Cost:"+str(temp.rootToSelfCost))

    elif (temp.parentFlipPosition == 2):
        #print("FLIPPED " + str(temp.parentFlipPosition) + "nd largest pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition(self))+")to get:" + temp.__str__()+"\nActual Cost:"+str(temp.rootToSelfCost))
        instructions.append("FLIPPED " + str(temp.parentFlipPosition) + "nd pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition())+")to get:" + temp.__str__()+"\nActual Cost:"+str(temp.rootToSelfCost))
    elif (temp.parentFlipPosition == 3):
        #print("FLIPPED " + str(temp.parentFlipPosition) + "rd largest pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition(self))+")to get:" + temp.__str__()+"\nActual Cost:"+str(temp.rootToSelfCost))
        instructions.append("FLIPPED " + str(temp.parentFlipPosition) + "rd pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition())+")to get:" + temp.__str__()+"\nActual Cost:"+str(temp.rootToSelfCost))
    elif (temp.isRoot):
        #print("Started at Root:" + temp.__str__()+"\nActual Cost:"+str(actualCost))
        instructions.append("Started at Root:" + temp.__str__()+"\nActual Cost:"+str(actualCost))
    else:
        #print("FLIPPED " + str(temp.parent.parentFlipPosition) + "th largest pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition(self))+")to get:" + temp.__str__()+"\nActual Cost:"+str(temp.rootToSelfCost))
        instructions.append("FLIPPED " + str(temp.parentFlipPosition) + "th pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition())+")to get:" + temp.__str__()+"\nActual Cost:"+str(temp.rootToSelfCost))




    while(True):
        if(temp.parent!=None):
            instructions.append(temp.parent.getDrawStackOfPancakesStr())
            if(temp.parent.parentFlipPosition==1):
                #print("FLIPPED " + str(temp.parent.parentFlipPosition) + "st largest pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition(self))+")to get:" + temp.parent.__str__()+"\Actual Cost:"+str(temp.parent.rootToSelfCost))
                instructions.append("FLIPPED " + str(temp.parent.parentFlipPosition) + "st pancake(ID:"+str(temp.parent.getIntPancakeIDFromParentFlipPosition())+")to get:" + temp.parent.__str__()+"\nActual Cost:"+str(temp.parent.rootToSelfCost))
            elif(temp.parent.parentFlipPosition==2):
                #print("FLIPPED " + str(temp.parent.parentFlipPosition) + "nd largest pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition(self))+")to get:" + temp.parent.__str__()+"\Actual Cost:"+str(temp.parent.rootToSelfCost))
                instructions.append("FLIPPED " + str(temp.parent.parentFlipPosition) + "nd pancake(ID:"+str(temp.parent.getIntPancakeIDFromParentFlipPosition())+")to get:" + temp.parent.__str__()+"\nActual Cost:"+str(temp.parent.rootToSelfCost))
            elif(temp.parent.parentFlipPosition==3):
                #print("FLIPPED " + str(temp.parent.parentFlipPosition) + "rd largest pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition(self))+")to get:" + temp.parent.__str__()+"\Actual Cost:"+str(temp.parent.rootToSelfCost))
                instructions.append("FLIPPED " + str(temp.parent.parentFlipPosition) + "rd pancake(ID:"+str(temp.parent.getIntPancakeIDFromParentFlipPosition())+")to get:" + temp.parent.__str__()+"\nActual Cost:"+str(temp.parent.rootToSelfCost))
            elif(temp.parent.isRoot):
                #print("Started with:" + temp.parent.__str__()+"\nActual Cost:"+str(actualCost))
                ''
            else:
                #print("FLIPPED " + str(temp.parent.parentFlipPosition) + "th largest pancake(ID:"+str(temp.getIntPancakeIDFromParentFlipPosition(self))+")to get:" + temp.parent.__str__()+"\nActual Cost:"+str(temp.parent.rootToSelfCost))
                instructions.append("FLIPPED " + str(temp.parent.parentFlipPosition) + "th pancake(ID:"+str(temp.parent.getIntPancakeIDFromParentFlipPosition())+")to get:" + temp.parent.__str__()+"\nActual Cost:"+str(temp.parent.rootToSelfCost))



        temp = temp.parent

        if(temp==None):
            #print("FOUND ROOT")
            break

        if(temp.isRoot):
            break

    instructions.reverse()
    print("Printing instructions:")
    print("Started with:" + startPancakeSeq.__str__())

    index = 0
    for i in range(0,len(instructions)):
        line=instructions[i]

        if('-' in line):
            print(line)
        else:
            index += 1
            print("Step "+str(index) + ") " + line)

    print("Finished:" + goalStateSeq.seq)
    print("Total Actual Cost:"+str(actualCost))
    print("Finished in "+str(index)+" steps using DFS.")

    goalStateSeq.drawStackOfPancakes()




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

            #print("FLipping pancake:"+str(inputoption))
            pancakestack.flipPancakes(inputoption)
            print("HAS REACHED GOAL?:" + str(pancakestack.hasReachedGoal()))

        #except:
        #    print("Error in option selection")






    print(textinput)



def main():
    testseq = "874952"
    #pancakeDFS(PancakeSeq(testseq,isRoot=True))
    pancakeAStar(PancakeSeq(testseq, isRoot=True))
    #tiebreakingFunction(PancakeSeq("3421"),PancakeSeq("4321"))

    print(PancakeSeq("9835").heuristicCost)


main()