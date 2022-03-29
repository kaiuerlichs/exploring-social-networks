# Introduction

## Project information
**Title**: Exploring Social Networks

**Participants**: Ross Coombs (2410466), Caitlin Ridge-Sykes (2423179), Kamil Krauze (2414951), Kai Uerlichs (2421101), Heather Currie (2411616) 


# Problem

## Problem description
- Akin to the "Six Degrees of Separation" principle, we aim to explore connections between people in social networks
- Create an AI system able to discover the shortest connecting path between two people in a social network
- Produce a list of friendships to traverse to reach one person from another
- Verify the "Six Degrees of Separation" hypothesis
- Analyse different strategies, such as varying search algorithms, to solve the problem

## Formal problem definition
- **States**: Each state is a person in the social network
- **Initial state**: The person to start the path from
- **Goal state**: The person to end the path on
- **Actions**: Go to any person that the current person is friends with
- **Transition model**: The state resulting from the action of going to another person will be the person travelled to
- **Goal test**: Check if the current person is the person the path shall end on
- **Path cost**: The path-cost specifies how friendships were traversed before the goal state was reached.

## Problem relevance
- We live in a globalised world
    - Digital communication can bridge any distance
    - Allows for people all around the world to stay in touch
- There is increased online communication as a result of the Covid-19 pandemic
    - In-person interaction is limited
    - Relying on online communication to stay in touch with family and friends
    - People are keen to meet new people through social media
- Public figures often have an elaborate online presence
    - This allows for insights into their social circles
    - Important in case of politicians, researchers, ...
- The solution to our problem above can help
    - Rekindling of lost friendships
    - Explaining why someone shows up on the recommended friends list
    - Understand the social connections of public figures

# Data

## Source data
- The data is from the Stanford Large Network Dataset Collection
- Anonymised subset of the Facebook network
- Contains 4039 nodes (users) and over 88000 edges (friendships)
- Data can be accessed as text files

## Suitability of the data
- Data is suitable for the search strategies theorised in the course, as they can generate a finite state-space graph which can be traversed using search algorithms
- Suitability for heuristic searches and other AI applications is limited, more on that later

## Data preparation
- Data processed with Python
- Dataset only contained the graph edges in a text file
- Generated more usable text files
    - List of all nodes containing the node ID and total friends
    - List of all nodes followed by all their friend nodes
    - List of all edges and the number of shared friends
- Data stored in text files
    - Dataset is not large enough to justify the complexity of a sophisticated database system
    - Lookup speeds are still very fast


# Approach analysis

## Search strategies
- Search strategies selected for analysis and implementation
    - Unidirectional Breadth-first Search
    - Bidirectional Breadth-first Search
    - Depth-first Search
    - Depth-limited Search
    - Iterative Deepening Depth-first Search

## Preliminary definitions
- Branching factor is widely variable in this dataset (between 1 and 1045), which makes a precise complexity calculation hard
- Maximum branching factor is 1045
- Average branching factor is 43.69
- Complexity analysis shall use average branching factor, as larger branching factors are outliers
<!-- -->
- Due to the Six Degrees of Separation hypothesis, we can assume the depth of the shallowest solution to be roughly 6
- Maximum depth on a tree search is infinite
- Step cost for all steps is 1
<!-- -->
- We also note that the state space, as well as the branching factor are finite

## Complexity analysis
### Unidirectional Breadth-first Search (Graph-based)
    - Complete? 
        - Yes - BFS is complete on a finite state-space graph
    - Optimal?
        - Yes - BFS is optimal if the step cost is uniform
    - Time complexity?
        - O(b^d) = O(43.69^6)
    - Space complexity?
        - O(b^d) = O(43.69^6)
    - Complexities are bounded by the state space size, which is 4039 nodes
### Bidirectional Breadth-first Search (Graph-based)
    - Complete? 
        - Yes - BiBFS is complete on a finite state-space graph
    - Optimal?
        - Yes - BiBFS is optimal if the step cost is uniform and both searches use BFS
    - Time complexity?
        - O(b^d/2) = O(43.69^3)
    - Space complexity?
        - O(b^d/2) = O(43.69^3)
    - Complexities are bounded by the state space size, which is 4039 nodes
### Depth-first Search (Graph-based)
    - Complete?
        - Yes - DFS is complete on for finite state spaces in graph-based searches
    - Optimal
        - No - DFS will return the first path it encounters, which may be significantly deeper than the optimal solution
    - Time complexity?
        - O(b^m) = O(Infinity)
    - Space complexity?
        - O(bm) = O(Infinity)
    - Complexities are bounded by the state space size, which is 4039 nodes
        - In a tree-based search, we would have the unbounded above infinite complexities
### Depth-limited Search with limit l (Tree-based)
    - Complete?
        No - If there only is a solution deeper than the limit, it will not be found
    - Optimal?
        No - DLS will return the first solution encountered, which may be deeper than the optimal solution
    - Time complexity?
        - O(b^l) = O(43.69^l)
    - Space complexity?
        - O(bl) = O(43.69*l)
### Iterative Deepening Depth-first Search (Tree-based)
    - Complete?
        - Yes - IDDFS will find a solution if there is one
    - Optimal?
        - Yes - IDDFS will encounter the optimal solution before any other solution, as the search depth is iteratively increased
    - Time complexity?
        - O(b^d) = O(43.69^6)
    - Space complexity?
        - O(bd) = O(43.69*6)

## Notes on implementation
- Bidirectional Breadth-first Search implementation uses depth-based turns
    - Forwards search expands all nodes of depth x in its frontier
    - Backwards search expands all nodes of depth x in its frontier
    - Intersection is checked
    - Process is repeated for x+1 if no intersection was found
    - This ensures optimality
- All other searches were implemented following Russell and Norvig

## Analysis interpretation
- Search strategies will need to be optimal in order to verify the Six Degrees of Separation hypothesis
    - Thus, DFS and DLS are not viable solutions
- Tree-based implementation are not suitable implementations as the graph is undirected, causing algorithms to fall into infinite loops
- Bidirectional BFS and Unidirectional BFS seem like good solutions as the solution depth is presumed to be shallow and graph-implementations significantly cut down the complexities
- IDDFS may be considered too, but the complexity is not bounded and there is the the risk of tree-based algorithms on the data
<!--  -->
- Best approach is Bidirectional Breadth-first Search


# Results

## Verifying the "Six Degrees of Separation" hypothesis
- Use Bidirectional BFS to compute optimal paths for 500 random pairs of nodes and analyse their path lengths
- Results (Path length ; Occurrence)
    - 6 or below ; 490
    - 7 ; 10
- 2% failure rate
- This is likely due to the small social network, and the edge limitation
    - Only 4039 nodes, whereas the principle is assuming a global social network
    - Only 88000 edges, mostly friends and family, whereas the principle may consider other links between people

## Evaluating search algorithms in practice
- Two batches of 10 searches for random pairs of nodes
- Use Lab PC to create a (somewhat) controlled and repeatable environment

### Search batch 1
- BiBFS: 5.99it/s
- BFS: 1.02it/s
- DFS: 0.18it/s
- DLS (limit=6): 2.03it/s
- IDDFS: 12.46it/s
<!--  -->
- BiBFS outperforms BFS as expected
- DFS performs very poorly
- DLS is fast, but only since the deepest solution in this set was at d=4
- IDDFS incredibly fast due to the same reason
- DFS and DLS do not return optimal results as expected

### Search batch 2
- BiBFS: 1.40it/s
- BFS: 3.00it/s
- DFS: 0.14it/sec
- DLS (limit=6): 0.26it/s
- IDDFS: 0.09it/s
<!--  -->
- BFS outperforms BiBFS
- All other searches perform poorly
- This shows that while occasionally, IDDFS may outperform the BFS-based algorithms, it performance varies significantly
- BiBFS and BFS seem to offer acceptable speeds consistently -> confirms correct selection of search strategy
- BiBFS should perform better than BFS consistently -> likely a implementation overhead issue

## Interpreting the results
- Six Degrees of Separation principle seems to hold
- Breadth-first Search approaches seem like the best choice for path-finding in social networks due to the short path-lengths
- Finding the shortest paths between people in a social network seems like a viable and worthwhile solution to improve the social media experience by linking people based on their shared friendships


# Practical Application
- How can this problem solution be applied in the real world?

## Proof-of-concept Application
- Showcase of screenshots of the GUI provided
    - Search connection between users with various search algorithms and view their complexities and performance
    - Explore the dataset
    - Visualise the network and found paths

## Mock-up of a real implementation
- Showcase of a mock-up screenshot showing a possible integration of the functionality into Facebook


# Possible enhancements

## Heuristic searches
- Not viable on the dataset
    - The features provided do not give heuristic information on how close two people may be
    - Even with potential heuristic information, the design of an admissible and consistent heuristic may not be possible as the information is hard to express in path-lengths
    - Common heuristics such as Manhattan or Euclidean distances are not applicable as nodes do not exist in a dimensional space graph

## Constraint Satisfaction Problems
- While an implementation as a CSP would be possible, due to the atomic nature of the states (only one variable), there is no real application in this
- CSP implementations would be useful if instead of finding the path between two specified people, the system should try to find another person with features
    - Suggest new friends on a social network
    - Auto-generate local interest groups

## Classical Planning
- Again, while an implementation using PDDL and advanced solving techniques is imaginable, due to the simplicity of actions and states, this implementation would only add unnecessary overhead

## Machine and Deep Learning
- While search problems are usually more efficiently implemented in more simple AI systems, machine and deep learning techniques may be useful in other social network analyses
    - Cluster people into social groups within the network, based on features such as common interests, hometowns, schools, or employers
    - Predict interests and recommend friends to users based on their social connections and own activities