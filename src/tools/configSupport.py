# Standard imports
from pprint import pprint
# Local imports
import utils as util

def getAgency(index: str = None) -> int:
    """
    :param: index
    :return: Agency ID of selected agent
    :usage: Lists all avaliable agents
	"""
    response = util.agencyAPI()
    i = 0
    if not index:
        for item in response['data']:
            print(f"{i} - {item['long_name']}")
            i += 1
    elif index and int(index) < len(response['data']):
        agencyID = response['data'][int(index)]['agency_id']
        print(f'Agency ID: {agencyID}')
        return agencyID
    else:
        print('Unable to retrieve agency ID for provided number')

def getRoutes(agencyID: str, index: list = None) -> list:
    """
    :param: agencyID, index
    :return: List of selected routes
    :usage: Prints avaliable routes for given agency ID
	"""
    agencyID = str(agencyID)
    response = util.routesAPI(agencyID)
    routeDict, routes, i = {} , [], 0
    if not index:
        for item in response['data'][agencyID]:
            print(f"{i} - {item['long_name']}")
            i += 1
    elif index:
        if all(x < len(response['data'][agencyID]) for x in index):
            for x in index:
                name = response['data'][agencyID][x]['long_name'].replace(' ', '_')
                route = response['data'][agencyID][x]['route_id']
                routeDict[route] = name
                routes.append(route)
            pprint(routeDict, width = 40)
            return routes
    else:
        print('Unable to retrieve selected routes')

def getStops(agencyID: str, routes: list) -> None:
    """
    :param: agencyID, routes (generated by getRoutes)
    :return: None
    :usage: Prints all stops for the selected routes 
	"""
    response = util.stopsAPI(agencyID)
    agencyID = str(agencyID)
    stopDict = {}
    for route in routes:
        tempDict = {}
        for stop in response['data']:
            if route in stop['routes']:
                stopID = int(stop['stop_id'])
                name = stop['name']
                lat = stop['location']['lat']
                lng = stop['location']['lng']
                tempDict[stopID] = {'name': name, 'lat': lat, 'lng': lng}
        stopDict[route] = tempDict
    pprint(stopDict, width = 300)
