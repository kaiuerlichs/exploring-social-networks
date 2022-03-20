import threading
from time import thread_time
from tkinter import *
from tkinter import ttk # Combobox stuff
from tkinter.messagebox import showinfo # For pop ups
import os
import problems #Imports search methods
import networkx as nx
import matplotlib.pyplot as plt


###Gets All Nodes from File nodeFriends.txt
def getAllNodes():
    file = open(os.path.dirname(__file__) + "/../data/nodeFriends.txt")
    output = []    
    for line in file:
        output.append(line.split())
    return output

###Gets NodeInfo
###In: ID
def getNodeInfo(id):
    fileA =  open(os.path.dirname(__file__) + "/../data/nodeFriends.txt")
    totalFriends = fileA.readlines()[id].split()[1]
    
    fileB = open(os.path.dirname(__file__) + "/../data/friendsLists.txt")
    friends = fileB.readlines()[id].split()
    friends = friends[1:]

    return (totalFriends, friends)

###Handles Setting Up The GUI
class MainWindow(Frame):

    #Variable to store the selectedAlgorithm
    selectedAlgorithm = ""

    #Initialises the class
    def __init__(self, master=None):
        Frame.__init__(self, master)               
        self.master = master

        self.master.title = "Exploring Social Networks"
        self.pack(fill=BOTH, expand=1)

        # Show help popup
        def help_popup():
            showinfo(
                title="Help",
                message=f'Enter a valid number between 0-4038 into each of the input boxes.\n\nThen select the search algorithm to use from the list which will find the shortest path within the social network to connect the nodes.\n\nClick the button to start the search.'
            )

        # Show about popup
        def about_popup():
            showinfo(
                title="About",
                message=f'A sophisticated desktop GUI to interact with the SNAP Facebook data and run various search algorithms.\n\nCopyright (C) Ross Coombs, Heather Currie, Kamil Krauze, Caitlin Ridge-Skyes, Kai Uerlichs'
            )

        # Run search
        def search_start():
            
            #Stores search as blank
            search = ""
            
            #If algorch_cb.get() is not blank
            if algosrch_cb.get() != "":
                #Search is set to the result of algosrch_cb.get()
                search = algosrch_cb.get()
            
            #Start is set to the result of nodeStart_inBox.get()
            start = nodeStart_inBox.get()
            
            #Goal is set to the result of nodeGoal_inBox.get()
            goal = nodeGoal_inBox.get()
            
            #If start and goal aren't blank and start doesn't equal goal
            if start != "" and goal != "" and start != goal:
                
                #Start equals goal
                start = start
                
                #Goal equals goal
                goal = goal
                
                # print(str(search) + " " + str(start) + " " + str(goal)) - Debug line
            
            #If start is blank
            elif start == "":
                
                #calls showInfo
                showinfo(
                    title="Missing Input",
                    message="No starting node defined."
                )
                return
            
            #If start or goal has alphabetic letters then shows info
            elif start.isdigit() != True or goal.isdigit() != True:
                showinfo(
                    title="Invalid Input",
                    message="Alphabetic characters detected"
                )
                return
            
            #If goal is blank then calls show info
            elif goal == "":
                showinfo(
                    title="Missing Input",
                    message="No goal node defined."
                )
                return

            #Starts threading
            threading.Thread(target=run_search, args=(search,start,goal), daemon=True).start()
            
            #SolutionLabel is set to "searching for a solution"
            solutionBox.delete("1.0", END)
            solutionBox.insert(INSERT, "Searching for a solution...")

        #Runs searches
        #In: search, start, goal
        def run_search(search, start, goal):
            
            #Prints algorithm, start node and goal node to console.
            print("Algorithm: " + search)
            print("Start node: " + str(start))
            print("Goal node: " + str(goal))
            
            #Problem equals problems.SocialNetworkProblem(start, goal)
            problem = problems.SocialNetworkProblem(start, goal)
            
            #If search equals Bidirectional, calls that search from problems.
            if search == "Bi-directional Breadth-first Search":
                solution = problems.bidirectional_breadth_first_search(problem)
            #If search equals unidirectional, calls that search from problems.
            elif search == "Uni-directional Breadth-first Search":
                solution = problems.breadth_first_search(problem)
            #If search equals depth first, calls that search from problems.
            elif search == "Depth First Search":
                solution = problems.depth_first_search(problem)
                #If search equals depth limited, calls that search from problems.
            elif search == "Depth Limited Search with limit=6":
                solution = problems.depth_limited_search(problem, limit=6)
            #If search equals iterative deepening depth first, calls that search from problems.
            elif search == "Iterative Deepening Depth First Search":
                solution = problems.iterative_deepening_search(problem)

            #Prints thread_time
            time_elapsed = thread_time()

            totalConnections = str(len(solution))
            solution = start + " ▶ " + str(solution).replace("', '", " ▶ ").replace("['","").replace("']","")

            solutionBox.delete("1.0", END)
            solutionBox.insert(INSERT, solution + "\nTotal connections: " + totalConnections + "\n\nSolution was found in " + str(time_elapsed) + " seconds.")


        #When the node is selected
        #In: event
        def on_node_selected(event):
            
            #Item is set to table.selection()[0]
            item = table.selection()[0]
            
            #TotalFriends, friends are set to getNodeInfo from table.item[item][0]
            (totalFriends, friends) = getNodeInfo(int(table.item(item, "values")[0]))
            
            #nodeID is set to table item[0]
            nodeID = table.item(item, "values")[0]
            
            #New instance of TK
            new= Tk()
            
            #Sets windows dimensions
            new.geometry("400x300")
            
            #Title is set to node information
            new.title("Node information")
            
            #Creates new label
            Label(new, text="Node Information", font=('Helvetica 16 bold')).grid(row=0, column=0, columnspan=2, sticky="w")
            
            #lblNodeID, textNodeID, lblFriends, textFriends and lblFriends are initialised
            lblNodeID = Label(new,
                    text="Node ID: ",
                    font = "Helvetica 10 bold").grid(row=1, column=0, sticky="w")
            textNodeID = Label(new,
                            text=nodeID,
                            font = "Helvetica 10").grid(row=1, column=1, sticky="w")
            lblFriends = Label(new,
                            text="Number of friends: ",
                            font = "Helvetica 10 bold").grid(row=2, column=0, sticky="w")
            textFriends = Label(new,
                            text=totalFriends,
                            font = "Helvetica 10").grid(row=2, column=1, sticky="w")
            lblFriends = Label(new,
                            text="All friends: ",
                            font = "Helvetica 10 bold").grid(row=3, column=0, sticky="w")

            #ListboxFriends is set to new listbox
            listBoxFriends = Listbox(new, width=65)
            
            #Is added in a grid
            listBoxFriends.grid(row=4, sticky="w", columnspan=2)
            
            #For every friend in friends, inserted into listBoxFriends.
            for friend in friends:
                listBoxFriends.insert("active",friend)


        # Add menu bar
        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        helpMenu = Menu(menubar, tearoff="off")
        helpMenu.add_command(label="Help me!", command=help_popup)
        helpMenu.add_command(label="About", command=about_popup)
        menubar.add_cascade(label="Help", menu=helpMenu)

        # Add tabs
        tabControl = ttk.Notebook(self.master)
        tabSearch = ttk.Frame(tabControl, width=600, height=480, padding=10)
        tabData = ttk.Frame(tabControl, width=600, height=480, padding=10)
        tabVisualise = ttk.Frame(tabControl, width=600, height=480, padding=10)
        tabAlgorithms = ttk.Frame(tabControl, width=600, height=480, padding=10)
        tabControl.add(tabSearch, text='Run a Search')
        tabControl.add(tabData, text='Data Explorer')
        tabControl.add(tabAlgorithms, text='Search Algorithms')
        tabControl.add(tabVisualise, text="Visualisation")
        tabControl.pack(fill="both", expand=True)


        # tabAlgorithms ------------------------------------------------------------------------------------------------

        title_lbl = Label(tabAlgorithms, text="Complexities", font="Helvetica 12 bold")
        
        branchFacInfo_lbl = Label(tabAlgorithms, text="The branching factor is variable and the average is much lower than the maximum value,\nthus we will be using the average b.", font="Helvetica 9 bold", justify="left")
        maxBranchingFac_lbl = Label(tabAlgorithms, text="Max Branching Factor: 1045", font="Helvetica 10 bold")
        avgBranchingFac_lbl = Label(tabAlgorithms, text="Average Branching Factor: 43.69", font="Helvetica 10 bold")
        
        depthInfo_lbl = Label(tabAlgorithms, text="Due to the Six Degress of Separation hypothesis, we can assume the shallowest solution depth\nto be roughly six.", font="Helvetica 8 bold", justify="left")
        depth_lbl = Label(tabAlgorithms, text="Depth: 6\t\t Maximum Depth: Infinite", font="Helvetica 10 bold")

        steps_lbl = Label(tabAlgorithms, text="Step cost for all steps: 1", font="Helvetica 10 bold")

        bisearch_lbl = Label(tabAlgorithms, text="Bi-Directional Breadth-first Search (Graph-based)", font="Helvetica 10 underline")
        unisearch_lbl = Label(tabAlgorithms, text="Uni-Directional Breadth-first Search (Graph-based)", font="Helvetica 10 underline")
        dfsearch_lbl = Label(tabAlgorithms, text="Depth First Search (Graph-based)", font="Helvetica 10 underline")
        dlsearch_lbl = Label(tabAlgorithms, text="Depth Limited Search (Tree-based)", font="Helvetica 10 underline")
        iddfsearch_lbl = Label(tabAlgorithms, text="Iterative Deepening Depth First Search (Tree-based)", font="Helvetica 10 underline")

        bisearch_time_lbl = Label(tabAlgorithms, text="Complete: Yes \tOptimal: Yes \tTime Comp: O(b^d/2) = O(43.69^6/2) \tSpace Comp: O(b^d/2) = O(43.69^6/2) \nBounded? - Time and space complexities are bounded by the state space size (4039 nodes)", font="Helvetica 8", justify="left") 
        unisearch_time_lbl = Label(tabAlgorithms, text="Complete: Yes \tOptimal: Yes \tTime Comp: O(b^d) = O(43.69^6) \tSpace Comp: O(b^d) = O(43.69^6) \nBounded? - Time and space complexities are bounded by the state space size (4039 nodes)", font="Helvetica 8", justify="left")
        dfsearch_time_lbl = Label(tabAlgorithms, text="Complete: Yes \tOptimal: No \tTime Comp: O(b^m) = O(Infinite) \tSpace Comp: O(bm) = O(Infinite) \nBounded? - Time and space complexities are bounded by the state space size (4039 nodes)", font="Helvetica 8", justify="left")
        dlsearch_time_lbl = Label(tabAlgorithms, text="Complete: No \tOptimal: No \tTime Comp: O(b^l) = O(43.69^l) \tSpace Comp: O(bl) = O(43.69*l) \nBounded? - No", font="Helvetica 8", justify="left")
        iddfsearch_time_lbl = Label(tabAlgorithms, text="Complete: Yes \tOptimal: Yes \tTime Comp: O(b^d) = O(43.69^6) \tSpace Comp: O(bd) = O(43.69*6) \nBounded? - No", font="Helvetica 8", justify="left")

        #Places the labels
        title_lbl.place(x=5, y=5)
        
        branchFacInfo_lbl.place(x=10, y=25)
        maxBranchingFac_lbl.place(x=10, y=65)
        avgBranchingFac_lbl.place(x=200, y=65)

        depthInfo_lbl.place(x=10, y=90)
        depth_lbl.place(x=10, y=120)

        steps_lbl.place(x=350, y=120)

        bisearch_lbl.place(x=10, y=145)
        bisearch_time_lbl.place(x=15, y=165)
        
        unisearch_lbl.place(x=10, y=205)
        unisearch_time_lbl.place(x=15, y=225)

        dfsearch_lbl.place(x=10, y=265)
        dfsearch_time_lbl.place(x=15, y=285)

        dlsearch_lbl.place(x=10, y=325)
        dlsearch_time_lbl.place(x=15, y=345)
        
        iddfsearch_lbl.place(x=10, y=385)
        iddfsearch_time_lbl.place(x=15, y=405)

        # --------------------------------------------------------------------------------------------------------------


        # tabSearch ----------------------------------------------------------------------------------------------------
        
        startLabel = Label(tabSearch, text="Start node: ")
        startLabel.grid(row = 0, column = 0, sticky="w")
        nodeStart_inBox = Entry(tabSearch, width=75)
        nodeStart_inBox.grid(row = 0, column = 1, sticky="w")

        goalLabel = Label(tabSearch, text="Goal node: ")
        goalLabel.grid(row = 1, column = 0, sticky="w")
        nodeGoal_inBox = Entry(tabSearch, width=75)
        nodeGoal_inBox.grid(row = 1, column = 1, sticky="w")
        
        algoLabel = Label(tabSearch, text="Search Algorithm: ")
        algoLabel.grid(row = 2, column = 0, sticky="w")
        algosrch_cb = ttk.Combobox(tabSearch, width=72)
        algosrch_cb['values'] = ["Bi-directional Breadth-first Search",
                                "Uni-directional Breadth-first Search",
                                "Depth First Search",
                                "Depth Limited Search with limit=6",
                                "Iterative Deepening Depth First Search"]
        algosrch_cb['state'] = 'readonly' # Makes it readonly
        algosrch_cb.current(0)
        algosrch_cb.grid(row = 2, column = 1, sticky="w")
        
        submitBtn = Button(tabSearch, text = "Run search", width = 15, command=search_start)
        submitBtn.grid(row = 3, column = 0, columnspan=2, pady=18)

        solutionBox = Text(tabSearch, width=72, height=20)
        solutionBox.grid(row = 4, column = 0, columnspan=2, sticky="w")

        # --------------------------------------------------------------------------------------------------------------


        # tabData ------------------------------------------------------------------------------------------------------
        
        headingDataset = Label(tabData, text="Dataset Information", font = "Helvetica 16 bold")
        headingDataset.grid(row=0, pady=2, columnspan=2, sticky="w")
        lblDataset = Label(tabData, text="Dataset Name: ", font = "Helvetica 10 bold")
        lblDataset.grid(row=1, column=0, sticky="w")
        textDataset = Label(tabData, text="Stanford Network Analysis Platform (SNAP) Social Circles - Facebook", font = "Helvetica 10")
        textDataset.grid(row=1, column=1, sticky="w")
        lblNodes = Label(tabData, text="Number of nodes: ", font = "Helvetica 10 bold")
        lblNodes.grid(row=2, column=0, sticky="w")
        textNodes = Label(tabData, text="4039", font = "Helvetica 10")                
        textNodes.grid(row=2, column=1, sticky="w")
        lblNodes = Label(tabData, text="Number of edges: ", font = "Helvetica 10 bold")
        lblNodes.grid(row=3, column=0, sticky="w")
        textNodes = Label(tabData, text="88234", font = "Helvetica 10")
        textNodes.grid(row=3, column=1, sticky="w")
        lblDesc = Label(tabData, text="Description: ", font = "Helvetica 10 bold")
        lblDesc.grid(row=4, column=0, sticky="nw")
        textDesc = Label(tabData,
                        text="The dataset consists of friend circles from Facebook. The data was collected through a survey on the Facebook app, and then anonymised with ids. The network contains additional information about node feautures, however this will be ommitted here.",
                        font = "Helvetica 10", wraplength=450, justify=LEFT)
        textDesc.grid(row=4, column=1, sticky="w")

        headingData = Label(tabData,
                        text="Data nodes",
                        font = "Helvetica 16 bold")
        headingData.grid(row=5, pady=(10,0), columnspan=2, sticky="w")
        
        table = ttk.Treeview(tabData, columns=("Node ID", "Total number of friends"), show='headings', selectmode="browse")
        table.heading('Node ID', text='Node ID')
        table.heading('Total number of friends', text='Total number of friends')
        for col in table['columns']:
            table.column(col, anchor=CENTER, width=285)  # set column width

        node_friends = getAllNodes()
        for node in node_friends:
            table.insert('', END, values=node)
        table.bind("<Double-1>", on_node_selected)
        table.grid(row=6, columnspan=2, sticky="w")

        # --------------------------------------------------------------------------------------------------------------

        # tabVisualise -------------------------------------------------------------------------------------------------

        def openNetworkGraph(min, max,path_edges):

            def on_path(a, b):
                return ((a,b) in path_edges or (b,a) in path_edges)

            G = nx.Graph()
            G.add_nodes_from(range(min,max+1))

            lines = open(os.path.dirname(__file__) + "/../data/edges.txt").readlines()
            for line in lines:
                tok = line.split()
                if(int(tok[0]) < min):
                    pass
                elif(int(tok[0]) > max):
                    break
                
                if(int(tok[1]) >= min and int(tok[1]) <= max):
                    if(on_path(int(tok[0]), int(tok[1]))):
                        G.add_edge(int(tok[0]), int(tok[1]), color="red", weight=2)
                    else:
                        G.add_edge(int(tok[0]), int(tok[1]), color="grey", weight=0.1)

            colors = nx.get_edge_attributes(G,'color').values()
            weights = nx.get_edge_attributes(G,'weight').values()

            nx.draw(G, with_labels=True, edge_color=colors, node_size=15, font_size=8, node_color="skyblue", width=list(weights))
            plt.show()


        def initialiseNetworkGraph():
            min = int(min_input.get())
            max = int(max_input.get())
            path = path_input.get().split(" ▶ ")
            if(len(path) == 1):
                path = path_input.get().split(",")

            print(path)

            path_edges = []
            for i in range(0, len(path)-2):
                path_edges.append((int(path[i]),int(path[i+1])))

            print(path_edges)

            openNetworkGraph(min, max, path_edges)

        
        def copy_path():
            sol = solutionBox.get('1.0', END).splitlines()[0]
            path_input.delete(0, END)
            path_input.insert(0, sol)
    
        min_label = Label(tabVisualise, text="Lowest node in network", width=30, justify=LEFT)
        min_label.grid(row=0, column=0, sticky="w")
        min_input = Entry(tabVisualise, width=30)
        min_input.grid(row=0, column=1, sticky="w")
        max_label = Label(tabVisualise, text="Highest node in network", width=30, justify=LEFT)
        max_label.grid(row=1, column=0, sticky="w")
        max_input = Entry(tabVisualise, width=30)
        max_input.grid(row=1, column=1, sticky="w")
        path_label = Label(tabVisualise, text="Path to highlight", width=30, justify=LEFT)
        path_label.grid(row=2, column=0, sticky="w")
        path_input = Entry(tabVisualise, width=30)
        path_input.grid(row=2, column=1, sticky="w")
        copy_button = Button(tabVisualise, text="Copy Path from Search Output", command=copy_path, width=60)
        copy_button.grid(row=3, column=0, columnspan=2, sticky="w")
        vis_button = Button(tabVisualise, text="Show Network Graph", command=initialiseNetworkGraph, width=60)
        vis_button.grid(row=4, column=0, columnspan=2, sticky="w")

        # --------------------------------------------------------------------------------------------------------------


root = Tk()
root.geometry("600x500")
root.title("Exploring Social Networks")
root.resizable(False,False)

app = MainWindow(root)
root.mainloop()
exit()