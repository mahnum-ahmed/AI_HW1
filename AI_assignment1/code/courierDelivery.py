
#Q1a Problem II: courier delivery route planning in Karachi
#Formulation: how we set this up as a search problem(also written in rough work so tally that if any confusion)

#1.state: the area the courier is in right now, as its name (a string)
#2.initial state: the starting area, given when the problem is made(the hub is "Saddar (Hub)")
#3.goal state: the delivery area, given when the problem is made
#4.actions: drive to a neighbouring area. the action is just the name of the area we go to next
#5.successors: every area that has a direct road from the current area in Connections.csv (a -1 means no road)
#6. cost: road distance in km times a road type number from TrackType.csv
#      M (main road)   x 1.0   best, no extra cost
#      S (standard)    x 1.25  a bit slower
#      N (narrow lane) x 3.0   van has to wait for a bike courier handoff
#so the search prefers main roads and avoids narrow lanes when it can
#7.heuristic (for A*): straight line distance from the current area to the goal area, taken from heuristics.csv. it never overestimates because a road is never shorter than the straight line, and our road type numbers are never below 1 (so the cost can only go up)

import csv
import os
import search

HUB = 'Saddar (Hub)'

#change these to try different road type costs (keep all of them at 1 or more
#or the heuristic can overestimate and A* may stop giving the best route)
ROAD_COST = {'M': 1.0, 'S': 1.25, 'N': 3.0}

#the csv folder
CSV_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'csv')


#reads one csv file. gives back the area names and a table you can use
#like table['Clifton']['DHA']. the values are left as text
def readTable(fileName):
    path = os.path.join(CSV_FOLDER, fileName)
    with open(path, newline='') as file:
        rows = list(csv.reader(file))
    names = rows[0][1:]
    table = {}
    for row in rows[1:]:
        table[row[0]] = dict(zip(names, row[1:]))
    return names, table

#loads all 3 files once... we make the problem many times (every part of a trip with stops, every test in Q1c) so we load once and pass this around
def loadCourierData():
    names, distances = readTable('Connections.csv')
    names, roadTypes = readTable('TrackType.csv')
    names, straightLine = readTable('heuristics.csv')
    return {'names': names, 'distances': distances,
            'roadTypes': roadTypes, 'straightLine': straightLine}


class CourierDelivery(search.SearchProblem):
    #start and goal are area names. we leave it out the csv files are read here
    def __init__(self, start, goal, data=None):
        if data is None:
            data = loadCourierData()
        self.names = data['names']
        self.distances = data['distances']
        self.roadTypes = data['roadTypes']
        self.straightLine = data['straightLine']

        for area in (start, goal):
            if area not in self.names:
                raise ValueError('unknown area: ' + area + ', pick from ' + str(self.names))

        self.start = start
        self.goal = goal

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state == self.goal

    #true if there is a direct road between the two areas
    def hasRoad(self, fromArea, toArea):
        if fromArea == toArea:
            return False
        return self.distances[fromArea][toArea] != '-1'

    #shown in ROUGH NOTES:cost of driving on the direct road between two areas:km * road type number

    def stepCost(self, fromArea, toArea):
        km = float(self.distances[fromArea][toArea])
        roadType = self.roadTypes[fromArea][toArea]
        return km * ROAD_COST[roadType]
    #gives back (nextState, action, stepCost) for every area with a direct road
    def getSuccessors(self, state):
        successors = []
        for area in self.names:
            if self.hasRoad(state, area):
                successors.append((area, area, self.stepCost(state, area)))
        return successors
    #adds up the cost of the trip. if any step has no road the cost is infinite
    def getCostOfActions(self, actions):
        current = self.start
        total = 0
        for area in actions:
            if not self.hasRoad(current, area):
                return float('inf')
            total += self.stepCost(current, area)
            current = area
        return total
    #straight line distance to the goal
    def getHeuristic(self, state):
        return float(self.straightLine[state][self.goal])


#prints the route one road at a time with the road type, km and cost and gives back total and how many narrow lanes use
def showRoute(problem, actions):
    current = problem.start
    totalKm = 0
    narrowCount = 0
    print('  ' + current)
    for area in actions:
        km = float(problem.distances[current][area])
        roadType = problem.roadTypes[current][area]
        cost = problem.stepCost(current, area)
        print('  -> ' + area + '  [' + roadType + ', ' + str(km) + ' km, cost ' + str(cost) + ']')
        totalKm += km
        if roadType == 'N':
            narrowCount += 1
        current = area
    print('  total km: ' + str(totalKm) + ', narrow lanes used: ' + str(narrowCount))
    return totalKm, narrowCount

#hub to all locations
if __name__ == "__main__":
    data = loadCourierData()
    print('goal, cost, A* expanded, Dijkstra expanded')
    for goal in data['names']:
        if goal == HUB:
            continue
        aStar = search.aStarSearch(CourierDelivery(HUB, goal, data))
        dijkstra = search.dijkstraSearch(CourierDelivery(HUB, goal, data))
        print(goal, aStar[1], aStar[2], dijkstra[2])

    print()
    problem = CourierDelivery(HUB, 'Gulshan-e-Iqbal', data)
    actions, cost, expanded = search.aStarSearch(problem)
    print('Saddar (Hub) to Gulshan-e-Iqbal with A*, cost', cost, 'expanded', expanded)
    showRoute(problem, actions)