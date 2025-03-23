import numpy as np
from collections import deque
import heapq
from typing import List, Tuple, Set, Dict
"""
Do not import any other package unless allowed by te TAs in charge of the lab.
Do not change the name of any of the functions below.
"""

def getNextStates(x):
    i = 0
    j = 0
    for I in range(3):
        for J in range(3):
            if x[I][J] == 0:
                i = I
                j = J
                break
    next_states = []
    
    if i-1 >= 0:  
        y = list(map(list,x))
        y[i][j] = y[i-1][j]
        y[i-1][j] = 0  
        z = tuple(map(tuple,y))
        temp = (z,"U")
        next_states.append(temp)
    
    if i+1 < 3:  
        y = list(map(list,x))
        y[i][j] = y[i+1][j]
        y[i+1][j] = 0  
        z = tuple(map(tuple,y))
        temp = (z,"D")
        next_states.append(temp)
    
    if j-1 >= 0: 
        y = list(map(list,x))
        y[i][j] = y[i][j-1]
        y[i][j-1] = 0 
        z = tuple(map(tuple,y))
        temp = (z,"L")
        next_states.append(temp)
    
    if j+1 < 3:  
        y = list(map(list,x))
        y[i][j] = y[i][j+1]
        y[i][j+1] = 0
        z = tuple(map(tuple,y))
        temp = (z,"R")
        next_states.append(temp)
    
    return next_states

def h1(state):
    count = 0
    for i in range(3):
        for j in range(3):
            if i==2 and j==2 and state[i][j] != 0:
                count += 1
            elif state[i][j] != 3*i + j+1:
                count += 1
    return count

def h2(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            num = state[i][j]
            if num == 0:
                distance += abs(2-i)+abs(2-j)
            else:
                J = 0
                I = 0
                if num%3 == 0:
                    J = 2
                    I = int(num/3-1)
                else:
                    J = num%3-1
                    I = int(num/3)
                distance += abs(I-i)+abs(J-j)
    return distance

def h_dijkstra(state):
    return 0

def h_DFS(state):
    return 0

def h_BFS(state):
    return 0


def areEqual(x,y):
    for i in range(3):
        for j in range(3):
            if x[i][j] != y[i][j]:
                return False
    return True
            

def bfs(initial: np.ndarray, goal: np.ndarray) -> Tuple[List[str], int]:
    """
    Implement Breadth-First Search algorithm to solve 8-puzzle problem.
    
    Args:
        initial (np.ndarray): Initial state of the puzzle as a 3x3 numpy array.
                            Example: np.array([[1, 2, 3], [4, 0, 5], [6, 7, 8]])
                            where 0 represents the blank space
        goal (np.ndarray): Goal state of the puzzle as a 3x3 numpy array.
                          Example: np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    
    Returns:
        Tuple[List[str], int]: A tuple containing:
            - List of moves to reach the goal state. Each move is represented as
              'U' (up), 'D' (down), 'L' (left), or 'R' (right), indicating how
              the blank space should move
            - Number of nodes expanded during the search

    Example return value:
        (['R', 'D', 'R'], 12) # Means blank moved right, down, right; 12 nodes were expanded
              
    """
    # TODO: Implement this function
    S = tuple(map(tuple,initial))
    G = tuple(map(tuple,goal))
    g = {}
    g[S] = 0
    h = {}
    h[S] = h_dijkstra(S)
    f = {}
    f[S] = g[S]+h[S]
    Initial_conf = (f[S], S)
    OL = deque()
    OL.append(Initial_conf)
    CL = []
    move_used = {}
    parent = {}
    num = 0
    while True:
        Bekar,x = OL.popleft()
        
        # End search if x is final
        if areEqual(x,G):
            break
        num += 1
        next_states = getNextStates(x)

        # adding new states and states with shorter path
        for state,P in next_states:
            if state in CL and g[x]+1 < g[state]:
                parent[state] = x
                g[state] = g[x]+1
                f[state] = g[state]+h[state]
                new_conf = (f[state],state)
                OL.append(new_conf)
                CL.remove(state)
                move_used[state] = P
            elif state not in CL:
                parent[state] = x
                g[state] = g[x]+1
                h[state] = h_dijkstra(state)
                f[state] = g[state]+h[state]
                new_conf = (f[state],state)
                OL.append(new_conf)
                move_used[state] = P
        
        # Adding x to CL
        CL.append(x)
    
    # Backtracking path
    temp = G
    path = []
    while True:
        path.append(move_used[temp])
        temp = parent[temp]
        if areEqual(temp,S):
            break
    path.reverse()
    return (path,num)


def dfs(initial: np.ndarray, goal: np.ndarray) -> Tuple[List[str], int]:
    """
    Implement Depth-First Search algorithm to solve 8-puzzle problem.
    
    Args:
        initial (np.ndarray): Initial state of the puzzle as a 3x3 numpy array
        goal (np.ndarray): Goal state of the puzzle as a 3x3 numpy array
    
    Returns:
        Tuple[List[str], int]: A tuple containing:
            - List of moves to reach the goal state
            - Number of nodes expanded during the search
    """
    # TODO: Implement this function
    S = tuple(map(tuple,initial))
    G = tuple(map(tuple,goal))
    g = {}
    g[S] = 1e8
    h = {}
    h[S] = h_DFS(S)
    f = {}
    f[S] = g[S]+h[S]
    Initial_conf = (f[S], S)
    OL = []
    heapq.heappush(OL,Initial_conf)
    CL = []
    move_used = {}
    parent = {}
    num = 0
    while True:
        Bekar,x = heapq.heappop(OL)
        
        # End search if x is final
        if areEqual(x,G):
            break
        num += 1
        next_states = getNextStates(x)

        # adding new states and states with shorter path
        for state,P in next_states:
            if state in CL and g[x]+1 < g[state]:
                parent[state] = x
                g[state] = 1/(int(1/g[x])+1)
                f[state] = g[state]+h[state]
                new_conf = (f[state],state)
                heapq.heappush(OL,new_conf)
                CL.remove(state)
                move_used[state] = P
            elif state not in CL:
                parent[state] = x
                g[state] = 1/(int(1/g[x])+1)
                h[state] = h_DFS(state)
                f[state] = g[state]+h[state]
                new_conf = (f[state],state)
                heapq.heappush(OL,new_conf)
                move_used[state] = P
        
        # Adding x to CL
        CL.append(x)
    
    # Backtracking path
    temp = G
    path = []
    while True:
        path.append(move_used[temp])
        temp = parent[temp]
        if areEqual(temp,S):
            break
    path.reverse()
    return (path,num)

def dijkstra(initial: np.ndarray, goal: np.ndarray) -> Tuple[List[str], int, int]:
    """
    Implement Dijkstra's algorithm to solve 8-puzzle problem.
    
    Args:
        initial (np.ndarray): Initial state of the puzzle as a 3x3 numpy array
        goal (np.ndarray): Goal state of the puzzle as a 3x3 numpy array
    
    Returns:
        Tuple[List[str], int, int]: A tuple containing:
            - List of moves to reach the goal state
            - Number of nodes expanded during the search
            - Total cost of the path for transforming initial into goal configuration
            
    """
    # TODO: Implement this function
    S = tuple(map(tuple,initial))
    G = tuple(map(tuple,goal))
    g = {}
    g[S] = 0
    h = {}
    h[S] = h_dijkstra(S)
    f = {}
    f[S] = g[S]+h[S]
    Initial_conf = (f[S], S)
    OL = []
    heapq.heappush(OL,Initial_conf)
    CL = []
    move_used = {}
    parent = {}
    num = 0
    while True:
        Bekar,x = heapq.heappop(OL)
        
        # End search if x is final
        if areEqual(x,G):
            break
        num += 1
        next_states = getNextStates(x)

        # adding new states and states with shorter path
        for state,P in next_states:
            if state in CL and g[x]+1 < g[state]:
                parent[state] = x
                g[state] = g[x]+1
                f[state] = g[state]+h[state]
                new_conf = (f[state],state)
                heapq.heappush(OL,new_conf)
                CL.remove(state)
                move_used[state] = P
            elif state not in CL:
                parent[state] = x
                g[state] = g[x]+1
                h[state] = h_dijkstra(state)
                f[state] = g[state]+h[state]
                new_conf = (f[state],state)
                heapq.heappush(OL,new_conf)
                move_used[state] = P
        
        # Adding x to CL
        CL.append(x)
    
    # Backtracking path
    temp = G
    path = []
    while True:
        path.append(move_used[temp])
        temp = parent[temp]
        if areEqual(temp,S):
            break
    path.reverse()
    return (path,num,len(path))

def astar_dt(initial: np.ndarray, goal: np.ndarray) -> Tuple[List[str], int, int]:
    """
    Implement A* Search with Displaced Tiles heuristic to solve 8-puzzle problem.
    
    Args:
        initial (np.ndarray): Initial state of the puzzle as a 3x3 numpy array
        goal (np.ndarray): Goal state of the puzzle as a 3x3 numpy array
    
    Returns:
        Tuple[List[str], int, int]: A tuple containing:
            - List of moves to reach the goal state
            - Number of nodes expanded during the search
            - Total cost of the path for transforming initial into goal configuration
              
    
    """
    # TODO: Implement this function
    S = tuple(map(tuple,initial))
    G = tuple(map(tuple,goal))
    g = {}
    g[S] = 0
    h = {}
    h[S] = h1(S)
    f = {}
    f[S] = g[S]+h[S]
    Initial_conf = (f[S], S)
    OL = []
    heapq.heappush(OL,Initial_conf)
    CL = []
    move_used = {}
    parent = {}
    num = 0
    while True:
        Bekar,x = heapq.heappop(OL)
        
        # End search if x is final
        if areEqual(x,G):
            break
        num += 1
        next_states = getNextStates(x)

        # adding new states and states with shorter path
        for state,P in next_states:
            if state in CL and g[x]+1 < g[state]:
                parent[state] = x
                g[state] = g[x]+1
                f[state] = g[state]+h[state]
                new_conf = (f[state],state)
                heapq.heappush(OL,new_conf)
                CL.remove(state)
                move_used[state] = P
            elif state not in CL:
                parent[state] = x
                g[state] = g[x]+1
                h[state] = h1(state)
                f[state] = g[state]+h[state]
                new_conf = (f[state],state)
                heapq.heappush(OL,new_conf)
                move_used[state] = P
        
        # Adding x to CL
        CL.append(x)
    
    # Backtracking path
    temp = G
    path = []
    while True:
        path.append(move_used[temp])
        temp = parent[temp]
        if areEqual(temp,S):
            break
    path.reverse()
    return (path,num,len(path))

def astar_md(initial: np.ndarray, goal: np.ndarray) -> Tuple[List[str], int, int]:
    """
    Implement A* Search with Manhattan Distance heuristic to solve 8-puzzle problem.
    
    Args:
        initial (np.ndarray): Initial state of the puzzle as a 3x3 numpy array
        goal (np.ndarray): Goal state of the puzzle as a 3x3 numpy array
    
    Returns:
        Tuple[List[str], int, int]: A tuple containing:
            - List of moves to reach the goal state
            - Number of nodes expanded during the search
            - Total cost of the path for transforming initial into goal configuration
    """
    # TODO: Implement this function
    S = tuple(map(tuple,initial))
    G = tuple(map(tuple,goal))
    g = {}
    g[S] = 0
    h = {}
    h[S] = h2(S)
    f = {}
    f[S] = g[S]+h[S]
    Initial_conf = (f[S], S)
    OL = []
    heapq.heappush(OL,Initial_conf)
    CL = []
    move_used = {}
    parent = {}
    num = 0
    while True:
        Bekar,x = heapq.heappop(OL)
        
        # End search if x is final
        if areEqual(x,G):
            break
        num += 1
        next_states = getNextStates(x)

        # adding new states and states with shorter path
        for state,P in next_states:
            if state in CL and g[x]+1 < g[state]:
                parent[state] = x
                g[state] = g[x]+1
                f[state] = g[state]+h[state]
                new_conf = (f[state],state)
                heapq.heappush(OL,new_conf)
                CL.remove(state)
                move_used[state] = P
            elif state not in CL:
                parent[state] = x
                g[state] = g[x]+1
                h[state] = h2(state)
                f[state] = g[state]+h[state]
                new_conf = (f[state],state)
                heapq.heappush(OL,new_conf)
                move_used[state] = P
        
        # Adding x to CL
        CL.append(x)
    
    # Backtracking path
    temp = G
    path = []
    while True:
        path.append(move_used[temp])
        temp = parent[temp]
        if areEqual(temp,S):
            break
    path.reverse()
    return (path,num,len(path))

# Example test case to help verify your implementation
if __name__ == "__main__":
    # Example puzzle configuration
    initial_state = np.array([
        [1, 2, 3],
        [0, 4, 5],
        [6, 7, 8]
    ])
    
    goal_state = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ])
    
    # # Test each algorithm
    print("Testing BFS...")
    bfs_moves, bfs_expanded = bfs(initial_state, goal_state)
    print(f"BFS Solution: {bfs_moves}")
    print(f"Nodes expanded: {bfs_expanded}")
    
    print("\nTesting DFS...")
    dfs_moves, dfs_expanded = dfs(initial_state, goal_state)
    print(f"DFS Solution: {dfs_moves}")
    print(f"Nodes expanded: {dfs_expanded}")
    
    print("\nTesting Dijkstra...")
    dijkstra_moves, dijkstra_expanded, dijkstra_cost = dijkstra(initial_state, goal_state)
    print(f"Dijkstra Solution: {dijkstra_moves}")
    print(f"Nodes expanded: {dijkstra_expanded}")
    print(f"Total cost: {dijkstra_cost}")
    
    print("\nTesting A* with Displaced Tiles...")
    dt_moves, dt_expanded, dt_fscore = astar_dt(initial_state, goal_state)
    print(f"A* (DT) Solution: {dt_moves}")
    print(f"Nodes expanded: {dt_expanded}")
    print(f"Total cost: {dt_fscore}")
    
    print("\nTesting A* with Manhattan Distance...")
    md_moves, md_expanded, md_fscore = astar_md(initial_state, goal_state)
    print(f"A* (MD) Solution: {md_moves}")
    print(f"Nodes expanded: {md_expanded}")
    print(f"Total cost: {md_fscore}")