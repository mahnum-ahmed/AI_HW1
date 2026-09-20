#comparison.py needed for Q 1(c)
#IGNORE THIS THE LATEX DOC HAS THE ACTUAL RESULTS FROM THIS, THIS WAS JUST AN INTERMEDIATE STEP TO GET THE NUMBERS

import matplotlib.pyplot as plt
import search
import robotNavigation
import courierDelivery


#bar graph: A* and Dijkstra side by side for every test
def drawGraph(labels, aCounts, dCounts, title, fileName):
    x = range(len(labels))
    plt.figure(figsize=(10, 5))
    plt.bar([i - 0.2 for i in x], aCounts, width=0.4, label='A*')
    plt.bar([i + 0.2 for i in x], dCounts, width=0.4, label='Dijkstra')
    plt.xticks(x, labels, rotation=60, ha='right')
    plt.ylabel('nodes expanded')
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(fileName)
    plt.close()


#---------- robot navigation ----------

exampleGrid = robotNavigation.readGrid(robotNavigation.exampleGrid)

#10x10 with no walls
openGrid = robotNavigation.readGrid("\n".join([". . . . . . . . . ."] * 10))

#a long wall in the middle, gaps only at the top and bottom
wallGrid = robotNavigation.readGrid("""
. . . . . # . . . .
. . . . . # . . . .
. . . . . # . . . .
. . . . . # . . . .
. . . . . # . . . .
. . . . . # . . . .
. . . . . . . . . .
""")

#(name, grid, start, goal)
robotTests = [
    ('example', exampleGrid, (0, 0), (4, 6)),
    ('example', exampleGrid, (0, 0), (4, 0)),
    ('example', exampleGrid, (0, 0), (2, 4)),
    ('example', exampleGrid, (4, 0), (0, 6)),
    ('open', openGrid, (0, 0), (9, 9)),
    ('open', openGrid, (0, 0), (0, 5)),
    ('open', openGrid, (2, 3), (8, 7)),
    ('wall', wallGrid, (3, 1), (3, 7)),
    ('wall', wallGrid, (0, 0), (0, 9)),
    ('wall', wallGrid, (2, 2), (2, 4)),
]

print('ROBOT NAVIGATION')
print('grid     start    goal     cost  A*   Dijkstra  route (A*)')
labels = []
aCounts = []
dCounts = []

for name, grid, start, goal in robotTests:
    aActions, aCost, aExpanded = search.aStarSearch(robotNavigation.RobotNavigation(grid, start, goal))
    dActions, dCost, dExpanded = search.dijkstraSearch(robotNavigation.RobotNavigation(grid, start, goal))
    print(f'{name:<8} {str(start):<8} {str(goal):<8} {aCost:<5} {aExpanded:<4} {dExpanded:<9} {"".join(aActions)}')
    labels.append(name + ' ' + str(start) + '>' + str(goal))
    aCounts.append(aExpanded)
    dCounts.append(dExpanded)

drawGraph(labels, aCounts, dCounts, 'Robot navigation: nodes expanded', 'robotGraph.png')


#---------- courier delivery ----------

data = courierDelivery.loadCourierData()
hub = courierDelivery.HUB

#(start, goal)
courierTests = [
    (hub, 'Clifton'),
    (hub, 'DHA'),
    (hub, 'PECHS'),
    (hub, 'Gulshan-e-Iqbal'),
    (hub, 'Nazimabad'),
    (hub, 'Baldia Town'),
    (hub, 'Lyari'),
    (hub, 'Korangi'),
    ('Clifton', 'Korangi'),
    ('Malir', 'Baldia Town'),
    ('Orangi Town', 'DHA'),
]

print()
print('COURIER DELIVERY')
print('start > goal                        cost    A*  Dijkstra  route (A*)')
labels = []
aCounts = []
dCounts = []

for start, goal in courierTests:
    aActions, aCost, aExpanded = search.aStarSearch(courierDelivery.CourierDelivery(start, goal, data))
    dActions, dCost, dExpanded = search.dijkstraSearch(courierDelivery.CourierDelivery(start, goal, data))
    trip = start.replace(' (Hub)', '') + ' > ' + goal
    print(f'{trip:<35} {aCost:<7} {aExpanded:<3} {dExpanded:<9} {" > ".join([start] + aActions)}')
    labels.append(trip)
    aCounts.append(aExpanded)
    dCounts.append(dExpanded)

drawGraph(labels, aCounts, dCounts, 'Courier delivery: nodes expanded', 'courierGraph.png')


#---------- effect of road types ----------
#same trips with every road costing just its km, then with our road type costs

print()
print('ROAD TYPE EFFECT (A*, from the hub)')
ourCosts = dict(courierDelivery.ROAD_COST)

for goal in ['Baldia Town', 'Orangi Town', 'Korangi']:
    courierDelivery.ROAD_COST.update({'M': 1, 'S': 1, 'N': 1})
    plain = search.aStarSearch(courierDelivery.CourierDelivery(hub, goal, data))

    courierDelivery.ROAD_COST.update(ourCosts)
    weighted = search.aStarSearch(courierDelivery.CourierDelivery(hub, goal, data))

    print(goal)
    print('  plain km    :', plain[1], ' ', ' > '.join([hub] + plain[0]))
    print('  road types  :', weighted[1], ' ', ' > '.join([hub] + weighted[0]))

print()
print('graphs saved as robotGraph.png and courierGraph.png')