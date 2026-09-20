# search.py


"""
In search.py, you will implement generic search algorithms (A* and Dijkstra)
that operate on any problem implementing the SearchProblem interface below.

For this assignment you will formulate TWO problems against this interface:
    1. Robot Navigation with Obstacles 
    2. Courier Delivery Route Planning 

You will implement a SearchProblem subclass for each (in separate files,
e.g. robotNavigation.py and courierDelivery.py), then write generic
aStarSearch and dijkstraSearch functions here that work on either subclass
purely through this interface.
"""

#hello areebs, yaar wu for coherence, mae sure this stuff remains contant, read before coding
#
#1. aStarSearch and dijkstraSearch both give back 3 things:
#   (actions, cost, nodesExpanded)
#   actions = list of moves from start to goal
#   cost = total cost of that route
#   nodesExpanded = how many nodes the search opened up
#   if there is no route they give back ([], float('inf'), nodesExpanded)
#
#2. the search functions only get the problem, nothing else. so start and
#   goal must live inside the problem. CourierDelivery should take
#   (start, goal) when we make it, like CourierDelivery(start, goal), and
#   getHeuristic should use that stored goal.
#   for stopovers just make a new CourierDelivery(a, b) for each leg
#   (hub -> stop1, stop1 -> stop2 ... last stop -> hub) and run
#   aStarSearch on each one
#
#3. for courier, let the action be the name of the area we go to next.
#   getCostOfActions needs the start area so keep it saved in the object
#
#4. states have to be hashable. grid state = (row, col), courier state =
#   the area name as a string
#
#5. step costs must be positive. for road types keep every multiplier at
#   1 or more (M = 1, S >= 1, N >= 1) so the distances in heuristics.csv
#   never go over the real cost. then A* still gives the best route
#
#6. a node counts as expanded when it is taken out of the queue and we
#   look at its neighbours, not when it is just added. same rule for A*
#   and Dijkstra so the comparison is fair
#
#7. searchWithStopovers (bottom of this file) is yours, Q1d

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't
    implement any of the methods (in object-oriented terminology: an
    abstract class).

    You do not need to change anything in this class, ever. Instead, you
    will write problem-specific subclasses (for Robot Navigation and for
    Courier Delivery) that implement each of these methods.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a successor to
        the current state, 'action' is the action required to get there,
        and 'stepCost' is the incremental cost of expanding to that
        successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of
        actions. The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

    def getHeuristic(self, state):
        """
         state: the current state of the agent

        This function returns the heuristic value of the current state,
        i.e. the estimated remaining cost/distance to the goal. Used by
        A* Search. Should return 0 for Dijkstra-equivalent behaviour.
        """
        util.raiseNotDefined()


def aStarSearch(problem):
    """
    Search the node that has the lowest combined cost (g) and heuristic (h)
    first, i.e. lowest f = g + h.

    This must work generically on ANY SearchProblem passed in - it should
    not know anything about grids, CSV files, robots, or couriers. All of
    that logic belongs inside the SearchProblem subclasses.

    Should return the list of actions from start to goal. Consider also
    tracking/returning the total cost and number of nodes expanded, since
    the assignment asks you to report these for the comparative analysis.
    """
    #A* is the same search as Dijkstra, just with the heuristic switched on
    return runSearch(problem, True)


def dijkstraSearch(problem):
    """
    Uniform-cost search: expand the node with the lowest cumulative path
    cost (g) first, ignoring the heuristic entirely (equivalent to A* with
    h(state) = 0 for every state).

    Like aStarSearch, this must work generically on any SearchProblem.
    You may reuse/adapt your CS 102 - DSA implementation here.
    """
    #same search, heuristic switched off so only the cost so far matters
    return runSearch(problem, False)


def searchWithStopovers(problem, stopovers):
    """
    Part (d): Route with Stopovers.

    Adapts A* Search so that the resulting route starts at the hub, visits
    every location in `stopovers` (in some order you determine), and
    returns to the hub - using A* Search to find the route between each
    consecutive pair of locations.

    This is the function you should pseudocode/implement for Question 1(d).
    stopovers: a list of states/locations that must all be visited before
               returning to the start state.

    Should return the complete route, its total cost, and the order in
    which stopovers were visited (see assignment spec for exact output
    requirements).
    """
    #yaar so claude suggested this approach, dekhlena:
    #1. for every pair of stops make a CourierDelivery(a, b), run
    #   aStarSearch on it and save the cost in a small table
    #2. there are only 17 areas so just try every order of the stops and
    #   keep the cheapest one (hub at the start and at the end)
    #3. stick the legs together into one full route
    "*** YOUR STOPOVER-ROUTING CODE HERE ***"
    util.raiseNotDefined()


#everything below is the extra stuff we added to make A* and Dijkstra work

def runSearch(problem, withHeuristic):
    #does the actual searching for both A* and Dijkstra
    #withHeuristic True = A*, False = Dijkstra
    #it only uses the SearchProblem functions so it works for the robot
    #grid and the courier map without any changes
    start = problem.getStartState()

    #cheapest cost we have found so far for each state
    costSoFar = {start: 0}

    #for each state, the state we came from and the move we made to get there
    cameFrom = {start: None}

    queue = util.PriorityQueue()
    if withHeuristic:
        queue.push((start, 0), problem.getHeuristic(start))
    else:
        queue.push((start, 0), 0)

    expanded = 0

    while not queue.isEmpty():
        state, g = queue.pop()

        #skip old entries, we found a cheaper way to this state after adding it
        if g > costSoFar[state]:
            continue

        expanded += 1

        if problem.isGoalState(state):
            return getActions(cameFrom, state), g, expanded

        for nextState, action, stepCost in problem.getSuccessors(state):
            newG = g + stepCost

            #only keep it if this is a cheaper way to get there
            if nextState in costSoFar and newG >= costSoFar[nextState]:
                continue

            costSoFar[nextState] = newG
            cameFrom[nextState] = (state, action)

            priority = newG
            if withHeuristic:
                priority += problem.getHeuristic(nextState)
            queue.push((nextState, newG), priority)

    #queue ran out without reaching the goal, so there is no route
    return [], float('inf'), expanded


def getActions(cameFrom, goalState):
    #walk backwards from the goal to the start collecting the moves,
    #then flip the list so it reads start to goal
    actions = []
    state = goalState
    while cameFrom[state] is not None:
        state, action = cameFrom[state]
        actions.append(action)
    actions.reverse()
    return actions