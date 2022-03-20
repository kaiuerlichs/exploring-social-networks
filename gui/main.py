from tkinter import *
from tkinter import ttk # Combobox stuff
from tkinter.messagebox import showinfo # For pop ups


def getAllNodes():
    file = open("../data/nodeFriends.txt")
    output = []
    for line in file:
        output.append(line.split())
    return output

class Table(Frame):
    def __init__(self, master, data, headings):
        Frame.__init__(self, master)

        colwidth = 50

        column = 0

        for heading in headings:
            Label(self, text=heading, font = "Helvetica 10 bold", width=colwidth, wraplength=colwidth).grid(row=0, column=column, sticky="w")
            self.columnconfigure(column,weight=1)
            column += 1

        column = 0
        row = 1

        for entry in data:
            for value in entry:
                if row % 2 == 0:
                    bg_colour = "grey"
                else:
                    bg_colour = "blue"
                Label(self, text=value, bg=bg_colour, font = "Helvetica 10").grid(row=row, column=column, sticky="w")
                column += 1
            row += 1
            column = 0

class MainWindow(Frame):

    selectedAlgorithm = ""

    def __init__(self, master=None):
        Frame.__init__(self, master)               
        self.master = master

        self.master.title = "Exploring Social Networks"
        self.pack(fill=BOTH, expand=1)


        # Show help popup
        def help_popup():
            showinfo(
                title="Help",
                message=f'Enter a valid number between 0-4038 which are not identical in the input boxes.\n\nsThen select the search algorithm to use from the list which will find the shortest path of mutual relations the two selected nodes have.\n\nFinally press "Go" to get your results.'
            )

        # Show about popup
        def about_popup():
            showinfo(
                title="About",
                message=f'A simple desktop interface for the user to play about with the implemented search algorithms and the dataset'
            )

        # Run search
        def search_start():
            print(algosrch_cb.get())


        # Add menu bar
        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        helpMenu = Menu(menubar, tearoff="off")
        helpMenu.add_command(label="Help me!", command=help_popup)
        helpMenu.add_command(label="About", command="")
        menubar.add_cascade(label="Help", menu=helpMenu)

        # Add tabs
        tabControl = ttk.Notebook(self.master)
        tabSearch = ttk.Frame(tabControl, width=600, height=380, padding=10)
        tabData = ttk.Frame(tabControl, width=600, height=380, padding=10)
        tabAlgorithms = ttk.Frame(tabControl, width=600, height=380, padding=10)
        tabControl.add(tabSearch, text='Run a Search')
        tabControl.add(tabData, text='Data Explorer')
        tabControl.add(tabAlgorithms, text='Search Algorithms')
        tabControl.pack(fill="both", expand=True)


        # tabSearch
        nodeStart_inBox = Entry(tabSearch)
        nodeStart_inBox.place(x=25, y=50)

        nodeGoal_inBox = Entry(tabSearch)
        nodeGoal_inBox.place(x=200, y=50)
        
        submitBtn = Button(tabSearch, text = "Go", width = 8, command=search_start)
        submitBtn.place(x=265, y=100)
        
        # Combobox - Dropdown list
        algosrch_cb = ttk.Combobox(tabSearch, width=35)
        # Combobox elements - 
        algosrch_cb['values'] = ["Bi-directional Breadth-first Search",
                                "Undirectional Breadth-first Search",
                                "Depth First Search",
                                "Depth Limited Search",
                                "Iterative Deep Learning Depth First Search"]
        algosrch_cb['state'] = 'readonly' # Makes it readonly
        algosrch_cb.current(0)
        algosrch_cb.place(x=25, y=103)


        # tabData
        headingDataset = Label(tabData,
                        text="Dataset Information",
                        font = "Helvetica 16 bold").grid(row=0, pady=2, columnspan=2, sticky="w")
        lblDataset = Label(tabData,
                        text="Dataset Name: ",
                        font = "Helvetica 10 bold").grid(row=1, column=0, sticky="w")
        textDataset = Label(tabData,
                        text="Stanford Network Analysis Platform (SNAP) Social Circles - Facebook",
                        font = "Helvetica 10").grid(row=1, column=1, sticky="w")
        lblNodes = Label(tabData,
                        text="Number of nodes: ",
                        font = "Helvetica 10 bold").grid(row=2, column=0, sticky="w")
        textNodes = Label(tabData,
                        text="4039",
                        font = "Helvetica 10").grid(row=2, column=1, sticky="w")
        lblNodes = Label(tabData,
                        text="Number of edges: ",
                        font = "Helvetica 10 bold").grid(row=3, column=0, sticky="w")
        textNodes = Label(tabData,
                        text="88234",
                        font = "Helvetica 10").grid(row=3, column=1, sticky="w")
        lblDesc = Label(tabData,
                        text="Description: ",
                        font = "Helvetica 10 bold").grid(row=4, column=0, sticky="nw")
        textDesc = Label(tabData,
                        text="The dataset consists of friend circles from Facebook. The data was collected through a survey on the Facebook app, and then anonymised with ids. The network contains additional information about node feautures, however this will be ommitted here.",
                        font = "Helvetica 10",
                        wraplength=450,
                        justify=LEFT).grid(row=4, column=1, sticky="w")

        headingData = Label(tabData,
                        text="Data nodes",
                        font = "Helvetica 16 bold").grid(row=5, pady=(10,0), columnspan=2, sticky="w")
        
        table = Table(tabData, [(1,2),(2,3),(4,5)], ("A", "B")).grid(row=6, columnspan=2, sticky="w")

root = Tk()
root.geometry("600x400")
root.title("Exploring Social Networks")


app = MainWindow(root)
root.mainloop()