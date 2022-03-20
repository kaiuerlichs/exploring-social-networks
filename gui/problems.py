"""
    Import required library classes
"""
from collections import deque
import sys
import os

from numpy import Infinity
    

"""
    Problem data structure to hold problem definitions
"""
class Problem:
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        raise NotImplementedError

    def transition(self, state, action):
        raise NotImplementedError

    def goal_test(self, state):
        if isinstance(self.goal, list):
            return (state in self.goal)
        else:
            return state == self.goal

    def path_cost(cost, state_from, state_to):
        raise NotImplementedError
        

"""
    Definition of the Social Network Problem
"""
class SocialNetworkProblem(Problem):
    friendsList = [None] * 4039

    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

        friendsFile = open(os.path.dirname(__file__) + "/../data/friendsLists.txt")

        for line in friendsFile:
            list_tokens = line.split()
            list = []

            for token in list_tokens[1:]:
                list.append(token)

            self.friendsList[int(list_tokens[0])] = list

    def actions(self, state):
        return self.friendsList[int(state)]

    def transition(self, state, action):
        return action

    def path_cost(self, cost, state_from, state_to):
        return cost + 1


"""
    Node data structure for search algorithms
"""
class Node:
    # Constructs a new node object
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent != None:
            self.depth = parent.depth + 1

    # String representation
    def __repr__(self):
        return "<Node> " + str(self.state) + " " + str(self.path_cost)

    def expandAll(self, problem):
        return [ self.expand(problem, action) for action in problem.actions(self.state) ]

    def expand(self, problem, action):
        new_state = problem.transition(self.state, action)
        return Node(new_state, self, action, problem.path_cost(self.path_cost, self.state, new_state))

    def action_sequence(self):
        if self.parent:
            sequence = self.parent.action_sequence()
            sequence.append(self.action)
            return sequence
        else:
            return []

    def state_sequence(self):
        if self.parent:
            sequence = self.parent.state_sequence()
            sequence.append(self.state)
            return sequence
        else:
            return [ self.state ]

    def print_sequence(self):
        if self.parent:
            self.parent.print_sequence()
            print("Action [" + str(self.action) + "] leads to State [" + str(self.state) + "]")
        else:
            print("Initial state [" + str(self.state) + "]")

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __repr__(self) -> str:
        return self.state


"""
    Implementation of the Breadth-First Graph Search algorithm
"""
def breadth_first_search(problem):
    initial = Node(problem.initial)
    if problem.goal_test(initial.state):
        return initial.action_sequence()

    frontier = deque([initial])
    explored = set()

    while frontier:
        node = frontier.popleft()
        explored.add(node.state)
        for expanded in node.expandAll(problem):
            if expanded.state not in explored and expanded not in frontier:
                if problem.goal_test(expanded.state):
                    return expanded.action_sequence()
                frontier.append(expanded)
    
    return None


def depth_first_search(problem):
    frontier = [(Node(problem.initial))]
    explored = set()

    while frontier:
        node = frontier.pop()
        if(problem.goal_test(node.state)):
            return node.action_sequence()
        explored.add(node.state)
        for expanded in node.expandAll(problem):
            if expanded.state not in explored and expanded not in frontier:
                frontier.append(expanded)


"""
    Implementation of the DLS algorithm
"""
def depth_limited_search(problem, limit=50):
    def recursive_dls(node, problem, limit):
        if(problem.goal_test(node.state)):
            return node.action_sequence()
        elif(limit == 0):
            return "Cutoff"
        else:
            cutoff_occured = False
            for action in node.expandAll(problem):
                result = recursive_dls(action, problem, limit-1)
                if result == "Cutoff":
                    cutoff_occured = True
                elif result != "Fail":
                    return result
            if cutoff_occured:
                return "Cutoff"
            else:
                return "Fail"

    return recursive_dls(Node(problem.initial), problem, limit)


"""
    Implementation of the IDDFS algorithm
"""
def iterative_deepening_search(problem):
    for depth in range(sys.maxsize):
        result = depth_limited_search(problem, depth)
        if result != 'Cutoff':
            return result


def bidirectional_breadth_first_search(problem):

    src_frontier = deque([(Node(problem.initial))])
    dest_frontier = deque([(Node(problem.goal))])

    src_explored = []
    dest_explored = []

    def bfs(direction):
        if direction == "fw":
            copy_frontier = src_frontier.copy()
            while copy_frontier:
                node = copy_frontier.popleft()
                src_explored.append(node)
                for expanded in node.expandAll(problem):
                    if expanded not in src_explored and expanded not in src_frontier:
                        src_frontier.append(expanded)

        elif direction == "bw":
            copy_frontier = dest_frontier.copy()
            while copy_frontier:
                node = copy_frontier.popleft()
                dest_explored.append(node)
                for expanded in node.expandAll(problem):
                    if expanded not in dest_explored and expanded not in dest_frontier:
                        dest_frontier.append(expanded)

    def intersect():
        intersect = None
        path = Infinity
        for src_node in src_frontier:
            for dest_node in dest_frontier:
                if src_node == dest_node:
                    if (src_node.path_cost + dest_node.path_cost) < path:
                        intersect = (src_node,dest_node)
                        path = (src_node.path_cost + dest_node.path_cost)
        return intersect

    def find_sequence(nodes):
        src_node = nodes[0]
        dest_node = nodes[1]
        
        src_seq = src_node.action_sequence()
        dest_seq = dest_node.action_sequence()

        if len(dest_seq) > 0:
            dest_seq.pop()
            dest_seq.reverse()

            for action in dest_seq:
                src_seq.append(action)

            src_seq.append(problem.goal)

        return src_seq

    while src_frontier and dest_frontier:
        bfs("fw")

        intersection = intersect()

        if intersection:
            return find_sequence(intersection)

        bfs("bw")
        
        intersection = intersect()

        if intersection:
            return find_sequence(intersection)
        
