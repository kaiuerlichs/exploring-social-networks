# Opens file in read mode and stores in variable
data_orig = open("./facebook_combined.txt","r")

# Finds the total amount of friends
# In: file
def friendsTotal(file):
    # Lines is set to the read in lines of file
    lines = file.readlines()

    #Output array is initialised empty
    output = []

    for i in range(0,4039):
        output.append(str(i) + " 0\n")

    # Variables for Kai's progress indicator
    percentage_step = 88234/100
    count = 1
    lineNo = 0
    
    #For every line in lines
    for line in lines:
        tokens = line.split()
        lineNo += 1

        # Kai's percentage counter to show an indicator of progress
        if(lineNo > count*percentage_step):
            print(str(count) + "%")
            count +=1

        for token in tokens:
            entry = output[int(token)]
            entry_tokens = entry.split()
            output[int(token)] = token + " " + str(int(entry_tokens[1])+1) + "\n"

    #Opens or creates new output file
    file_output = open("./nodeFriends.txt","w")
    
    # For every tuple in output
    for line in output:
        file_output.write(line)

# Method to find the edges with shared friends
# In: file
def edgesWithSharedFriends(file):
    
    # Lines is set to the read in lines of file
    lines = file.readlines()

    #Output array is initialised empty
    output = []

    #Variables for Kai's progress indicator
    percentage_step = 88234/100
    count = 1

    currentLine = 0
    
    # For every line in lines
    for line in lines:
        currentLine += 1

        if(currentLine > count*percentage_step):
            count += 1
            print(str(count) + "%")

        #tokensOuter is set to the result of line.split()
        tokensOuter = line.split()
        
        #friendsA & friendsB are initialised as set()
        friendsA = set()
        friendsB = set()

        # maxLines is set to tokensOuter[0] if tokensOuter[0] is over tokensOuter[1], otherwise it is set to tokensOuter[1]
        maxLines = int(tokensOuter[0]) if int(tokensOuter[0]) > int(tokensOuter[1]) else int(tokensOuter[1])
        
        #For every line in lines
        for line in lines:
            
            #tokenInner is set to line.split()
            tokensInner = line.split()
            
            #if tokensInner[0] is over tokensOuter[0] then break 
            if(int(tokensInner[0]) > maxLines):
                break
            
            #if tokensInner[0] is equal to tokensOuter[0] then tokensInner[1] is added to friendsA 
            if(tokensInner[0] == tokensOuter[0]):
                friendsA.add(tokensInner[1])
            #if tokensInner[1] is equal to tokensOuter[0] then tokensInner[0] is added to friendsA 
            elif(tokensInner[1] == tokensOuter[0]):
                friendsA.add(tokensInner[0])

            #if tokensInner[0] is equal to tokensOuter[1] then tokensInner[1] is added to friendsB
            if(tokensInner[0] == tokensOuter[1]):
                friendsB.add(tokensInner[1])
            #if tokensInner[1] is equal to tokensOuter[1] then tokensInner[0] is added to friendsB
            elif(tokensInner[1] == tokensOuter[1]):
                friendsB.add(tokensInner[0])
        
        sharedFriends = friendsA.intersection(friendsB)
        output.append([tokensOuter[0],tokensOuter[1],str(len(sharedFriends))])
    
    out_file = open("./edges.txt","w")
    for tuple in output:
        out_file.write(tuple[0] + " " + tuple[1] + " " + tuple[2] + "/n")

    print("100%")

def friendsLists(data):
    lines = data.readlines()

    output = [None] * 4039

    for i in range(0,4039):
        output[i] = str(i)

    for line in lines:
        tuple = line.split()
        if(int(tuple[1]) > 4030):
            print(tuple)
        output[int(tuple[0])] += (" " + tuple[1])
        output[int(tuple[1])] += (" " + tuple[0])

    outfile = open("./friendsLists.txt","w")

    for o in output:
        outfile.write(o + "\n")

#Top Level
# friendsTotal(data_orig)
# edgesWithSharedFriends(data_orig)
friendsLists(data_orig)