from __future__ import division
from __future__ import print_function

import sys
import math
import time
import resource
import queue as Q
from collections import deque
import heapq


#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []
        self.depth = 0

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def move_up(self):
        if self.blank_index >= self.n:
            new_config = self.config[:]
            swap_index = self.blank_index - self.n
            new_config[self.blank_index], new_config[swap_index] = new_config[swap_index], new_config[self.blank_index]
            return PuzzleState(new_config,self.n, parent = self, action ="Up", cost=self.cost+1)
        """
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """

      
    def move_down(self):
        if self.blank_index < (self.n * (self.n - 1)):
            new_config = self.config[:]
            swap_index = self.blank_index + self.n
            new_config[self.blank_index], new_config[swap_index] = new_config[swap_index], new_config[self.blank_index]
            return PuzzleState(new_config,self.n, parent = self, action = "Down", cost = self.cost + 1 )

        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        
      
    def move_left(self):
        if (self.blank_index % self.n) > 0:
            new_config = self.config[:]
            swap_index = self.blank_index - 1
            new_config[self.blank_index], new_config[swap_index] = new_config[swap_index], new_config[self.blank_index]
            return PuzzleState(new_config, self.n, parent = self, action = "Left", cost = self.cost + 1)

        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        pass

    def move_right(self):
        if (self.blank_index % self.n) < (self.n - 1):
            new_config = self.config[:]
            swap_index = self.blank_index + 1
            new_config[self.blank_index], new_config[swap_index] = new_config[swap_index], new_config[self.blank_index]
            return PuzzleState(new_config, self.n, parent = self, action = "Right", cost = self.cost + 1)

        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        pass
      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(text, mode):
    
    
    if mode == "w":
        with open("output.txt", "w") as f:
            f.write(str(text) +"\n")

    if mode == "a":
        with open("output.txt", "a") as f:
            f.write(str(text) + "\n")
    
    pass
        
    

def bfs_search(initial_state):
    """BFS search"""
    frontier = Q.Queue()
    frontier.put((initial_state, 0))
    explored = set([tuple(initial_state.config)])
    nodes_expanded = 0
    max_depth = 0

    while not frontier.empty():
        state, depth = frontier.get()
        max_depth = max(max_depth, depth)

        if test_goal(state):
            path_to_goal = []
            states = []
           
            current = state
            
            
            while current is not None:
                states.append(current)
                path_to_goal.append(current.action)
                current = current.parent
            states.reverse()
            path_to_goal.reverse()
            
            solution_path = [action for action in path_to_goal if action != "Initial"]

            writeOutput("path_to_goal: " + repr(solution_path), "w")
            writeOutput("cost_of_path: " + str(len(solution_path)), "a")
            writeOutput("nodes_expanded: " + str(nodes_expanded), "a")
            writeOutput("search_depth: " + str(len(solution_path)), "a")
            if len(solution_path) == 0:
                writeOutput("max_search_depth: " + str(max_depth), "a")
            else:
                writeOutput("max_search_depth: " + str(max_depth + 1), "a")
            return
        
        nodes_expanded += 1
        for child in state.expand():
            child_tuple = tuple(child.config)
            if child_tuple not in explored:
                frontier.put((child, depth + 1))
                explored.add(child_tuple)
        
    return

def dfs_search(initial_state):
    """DFS search"""
    frontier  = [(initial_state, 0)]
    explored = set([tuple(initial_state.config)])

    nodes_expanded = 0
    max_depth = 0
   
    while frontier:
        state, depth = frontier.pop()
        max_depth = max(max_depth, depth)

        if test_goal(state):
            path_to_goal = []
            states = []
            current = state
            
            
            while current is not None:
                path_to_goal.append(current.action if current.action else "Initial")
                current = current.parent
                    
            path_to_goal.reverse()
            
            
            
            

            solution_path = [action for action in path_to_goal if action != "Initial"]

            
            
            writeOutput("path_to_goal: " + repr(solution_path), "w")

            writeOutput("cost_of_path: " + str(len(solution_path)), "a")

            writeOutput("nodes_expanded: " + str(nodes_expanded), "a")
            writeOutput("search_depth: " + str(len(solution_path)), "a")
            writeOutput("max_search_depth: " + str((max_depth)), "a")
                
            
            
            return
       
        nodes_expanded += 1
        for child in reversed(state.expand()):
            

            child_tuple = tuple(child.config)
            if child_tuple not in explored:
                frontier.append((child, depth+1))
                explored.add(child_tuple)
        
    
    return

def A_star_search(initial_state):
    """A* search"""
    frontier = []
    explored = set()
    nodes_expanded = 0
    max_depth = 0
    counter = 0
    
    heapq.heappush(frontier, (calculate_total_cost(initial_state), counter, initial_state))
    counter += 1
    
    while frontier:
        priority,x, state = heapq.heappop(frontier)
        states = tuple(state.config)

        if states in explored:
            continue
        explored.add(states)
        

        
        if test_goal(state):
            

            path_to_goal = []
            current = state
            
            while current is not None:
                path_to_goal.append(current.action if current.action else "Initial")
                current = current.parent
                    
            

            path_to_goal.reverse()
            solution_path = [action for action in path_to_goal if action != "Initial"]

            
        

            writeOutput("path_to_goal: " + repr(solution_path), "w")
            writeOutput("cost_of_path: " + str(len(solution_path)), "a")

            writeOutput("nodes_expanded: " + str(nodes_expanded), "a")
            writeOutput("search_depth: " + str(len(solution_path)), "a")
            writeOutput("max_search_depth: " + str(max_depth), "a")
            
            
            return
       
        nodes_expanded += 1
        for child in state.expand():
            child.depth = state.depth + 1
            child_tuple = tuple(child.config)
            if child_tuple not in explored:
                counter += 1
                cost = calculate_total_cost(child)
                heapq.heappush(frontier, (cost, counter, child))
                max_depth = max(child.depth, max_depth)
                
            
        
    
    return


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    h = 0
    n = int(len(state.config) ** 0.5)
    for idx,val in enumerate(state.config):
        h += calculate_manhattan_dist(idx, val, n)
    
    return state.depth + h

    ### STUDENT CODE GOES HERE ###
    pass

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    if value == 0:
        return 0
    
    horizontal = abs((idx % n) - (value % n))
    vertical = abs((idx // n) - (value // n))

    return horizontal + vertical
    pass

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    for i in range(((puzzle_state.n * puzzle_state.n))):
        if puzzle_state.config[i] != i:
            return False
    return True

 


# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    
    if len(sys.argv) < 3:
        return
    
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    
    
    
    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        return
        
    end_time = time.time()
    writeOutput("running_time_: %.8f" % (end_time-start_time), "a")

    
    ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - start_ram)
    
   
    
    writeOutput("max_ram_usage: %.8f" % ram, "a")



if __name__ == '__main__':
    main()

