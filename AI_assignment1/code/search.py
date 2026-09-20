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

import copy
import itertools
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
    #A* is the same search as Dijkstra but the h has a non-zero value
    return runSearch(problem, True)


def dijkstraSearch(problem):
    """
    Uniform-cost search: expand the node with the lowest cumulative path
    cost (g) first, ignoring the heuristic entirely (equivalent to A* with
    h(state) = 0 for every state).

    Like aStarSearch, this must work generically on any SearchProblem.
    You may reuse/adapt your CS 102 - DSA implementation here.
    """
    #just set h=0, so f=g
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
    hub = problem.getStartState()
    #take out the hub and repeats from the stopovers, we are already at the hub
    stopovers = [stop for stop in dict.fromkeys(stopovers) if stop != hub]
    points = [hub] + stopovers
    #run A* once for every pair of places and save the route and cost
    #(the same place to itself costs 0 and needs no moves)
    legRoute = {}
    legCost = {}
    for a in points:
        for b in points:
            if a == b:
                legRoute[(a, b)] = []
                legCost[(a, b)] = 0
                continue
            #same problem but with a different start and goal
            leg = copy.copy(problem)
            leg.start = a
            leg.goal = b
            actions, cost, expanded = aStarSearch(leg)
            legRoute[(a, b)] = actions
            legCost[(a, b)] = cost
    #try every order of the stopovers and keep the cheapest trip
    #every trip starts at the hub and ends at the hub
    bestCost = float('inf')
    bestOrder = None
    for order in itertools.permutations(stopovers):
        stops = [hub] + list(order) + [hub]
        total = 0
        for i in range(len(stops) - 1):
            total += legCost[(stops[i], stops[i + 1])]
        if total < bestCost:
            bestCost = total
            bestOrder = list(order)
    #no order works (some stopover cannot be reached)
    if bestOrder is None:
        return [], float('inf'), []
    #stick the legs of the best order together
    #for courier the actions are area names, so the route is a list of areas
    stops = [hub] + bestOrder + [hub]
    route = [hub]
    for i in range(len(stops) - 1):
        route += legRoute[(stops[i], stops[i + 1])]

    return route, bestCost, bestOrder


#everything below is the extra stuff we added to make A* and Dijkstra work

def runSearch(problem, withHeuristic):
    #does the actual searching for both A* and Dijkstra withHeuristic True = A*, False = Dijkstra
    #it only uses the SearchProblem functions so it works for the robot grid and the courier map without any changes
    start = problem.getStartState()

    #cheapest cost we have found so far for each state
    costSoFar = {start: 0}

    #for each state the state we came from(i.e prev state) and the move we made to get there
    cameFrom = {start: None}
    queue = util.PriorityQueue()
    if withHeuristic:
        queue.push((start, 0), problem.getHeuristic(start))
    else:
        queue.push((start, 0), 0)

    expanded = 0

    while not queue.isEmpty():
        state, g = queue.pop()

        #skip old (stale) entries if a better way has been found(i also mention this in my rough work)
        if g > costSoFar[state]:
            continue
        expanded += 1 # one more node visited/expanded
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

    # if queue is empty and goal not reached, that means no route exists.
    return [], float('inf'), expanded


def getActions(cameFrom, goalState):
    #backtrack from the goal to hub-> then reverse it to show path
    actions = []
    state = goalState
    while cameFrom[state] is not None:
        state, action = cameFrom[state]
        actions.append(action)
    actions.reverse()
    return actions