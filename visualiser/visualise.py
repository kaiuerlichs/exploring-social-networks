import networkx as nx
import matplotlib.pyplot as plt

path_edges = [(6,0),(0,302)]

def on_path(a, b):
    return ((a,b) in path_edges or (b,a) in path_edges)

min = 0
max = 302 

G = nx.Graph()

G.add_nodes_from(range(min,max+1))

lines = open("../data/edges.txt").readlines()
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