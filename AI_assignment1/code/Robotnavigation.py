#robotNavigation.py
#Q1a Problem I: robot moving on a grid with walls
#
#how we set this up as a search problem
#
#1. state: where the robot is, as (row, col)
#2. initial state: the cell marked S in the grid
#3. goal state: the cell marked G in the grid
#4. actions: U, D, L, R (up, down, left, right)
#5. successors: for a state, every move that ends inside the grid on a
#   cell that is not a wall (#). moving diagonally is not allowed
#6. cost: every move costs 1, so the total cost is the number of moves
#7. heuristic (for A*): Manhattan distance to the goal, which is
#   (rows away) + (columns away). it never overestimates because the robot
#   can't go diagonal, and walls can only make the real route longer

import search
import util

#the four moves the robot can make: (row change, column change)
#this order is also the order successors are given back in
MOVES = [('U', -1, 0), ('D', 1, 0), ('L', 0, -1), ('R', 0, 1)]


class RobotNavigation(search.SearchProblem):
    #grid = list of rows, each row is a list of cells like ['S', '.', '#']
    #start and goal are optional (row, col). if we leave them out they
    #are taken from where S and G are written in the grid.
    #giving them lets us test many start/goal spots on the same grid (Q1c)
    def __init__(self, grid, start=None, goal=None):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.start = start if start is not None else findCell(grid, 'S')
        self.goal = goal if goal is not None else findCell(grid, 'G')

    #state is just where the robot is: (row, col)
    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state == self.goal

    #robot can stand on a cell if it is inside the grid and not a wall
    def isFree(self, row, col):
        if row < 0 or row >= self.rows:
            return False
        if col < 0 or col >= self.cols:
            return False
        return self.grid[row][col] != '#'

    #gives back (nextState, action, stepCost) for every move that works
    def getSuccessors(self, state):
        row, col = state
        successors = []
        for action, dRow, dCol in MOVES:
            newRow = row + dRow
            newCol = col + dCol
            if self.isFree(newRow, newCol):
                successors.append(((newRow, newCol), action, 1))
        return successors

    #every move costs 1 so the cost is the number of moves
    #if any move is not allowed we say the cost is infinite
    def getCostOfActions(self, actions):
        row, col = self.start
        for action in actions:
            for name, dRow, dCol in MOVES:
                if name == action:
                    row += dRow
                    col += dCol
            if not self.isFree(row, col):
                return float('inf')
        return len(actions)

    #Manhattan distance: rows away + columns away from the goal
    #the robot can't go diagonal or through walls so it never needs
    #fewer moves than this, it can only need more
    def getHeuristic(self, state):
        return util.manhattanDistance(state, self.goal)


#turns text like "S . #" into a grid (list of rows)
#works with spaces between cells or without
def readGrid(text):
    grid = []
    for line in text.strip().split('\n'):
        line = line.strip()
        if ' ' in line:
            grid.append(line.split())
        else:
            grid.append(list(line))
    return grid


#finds where a symbol (S or G) sits in the grid
def findCell(grid, symbol):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == symbol:
                return (row, col)
    return None


#prints the grid with the route drawn on it using *
def showPath(problem, actions):
    row, col = problem.start
    drawn = [list(line) for line in problem.grid]
    for action in actions:
        for name, dRow, dCol in MOVES:
            if name == action:
                row += dRow
                col += dCol
        if drawn[row][col] == '.':
            drawn[row][col] = '*'
    for line in drawn:
        print(' '.join(line))


exampleGrid = """
S . . # . . .
# # . # . # .
. . . . . # .
. # # # . . .
. . . . . # G
"""


#quick test on the example grid from the assignment PDF
if __name__ == "__main__":
    problem = RobotNavigation(readGrid(exampleGrid))
    for name, algorithm in [('A*', search.aStarSearch), ('Dijkstra', search.dijkstraSearch)]:
        actions, cost, expanded = algorithm(problem)
        print(name)
        print('  actions  :', ' '.join(actions))
        print('  cost     :', cost)
        print('  expanded :', expanded)
        showPath(problem, actions)
        print()