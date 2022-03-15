# Opens file in read mode and stores in variable
data_orig = open("./facebook_combined.txt","r")

# Finds the total amount of friends
# In: file
def friendsTotal(file):
    
    # Lines is set to the read in lines of file
    lines = file.readlines()

    #Output array is initialised empty
    output = []
    
    #Previous is set to -1
    previous = -1

    # Variables for Kai's progress indicator
    percentage_step = 4039/100
    count = 1
    
    #For every line in lines
    for line in lines:
        
        #tokensOuter is set to the split result of line
        tokensOuter = line.split()
        
        # If tokensOuter[0] is equal to previous then continue
        if(tokensOuter[0] == previous):
            continue

        # Kai's percentage counter to show an indicator of progress
        if(int(tokensOuter[0]) > count*percentage_step):
            print(str(count) + "%")
            count +=1
        
        # Friends is set to 0
        friends = 0
        # Previous is set to whatever is in position 0 of tokensOuter
        previous = tokensOuter[0]

        # For every line in lines
        for line in lines:
            #tokensInner is set to the result of line.split()
            tokensInner = line.split()
            
            #If tokensOuter[0] matches tokenInner[0] or [1] then increment friends
            if(tokensOuter[0] == tokensInner[0] or tokensOuter[0] == tokensInner[1]):
                friends += 1

        # tokensOuter[0] and friends are appended to output
        output.append([tokensOuter[0],str(friends)])

        #Opens or creates new output file
        file_output = open("./nodeFriends.txt","w")
        
        # For every tuple in output
        for tuple in output:
            # tuple[0] & tuple[1] are written to file
            file_output.write(tuple[0] + " " + tuple[1] + "\n")

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


#Top Level
# friendsTotal(data_orig)
edgesWithSharedFriends(data_orig)