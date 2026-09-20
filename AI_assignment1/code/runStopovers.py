#Q1d: try the stopover route planner on a few delivery runs
import search
import courierDelivery
data = courierDelivery.loadCourierData()
hub = courierDelivery.HUB
#ok so each list is a seperate delivery run, u start at the hub then visit all nodes mentioned and return to hub.
runs = [
    ['Clifton', 'Gulshan-e-Iqbal', 'Korangi'],
    ['Lyari', 'SITE Area', 'Malir'],
    ['PECHS', 'Nazimabad', 'Liaquatabad', 'DHA'],
]

for stopovers in runs:
    #notice that the goal doesnt matter here
    problem = courierDelivery.CourierDelivery(hub, hub, data)
    route, cost, order = search.searchWithStopovers(problem, stopovers)
    print('stopovers      :', stopovers)
    print('order visited  :', order)
    print('route          :', ' > '.join(route))
    print('total cost     :', cost)
    print()