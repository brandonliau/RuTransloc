# Local imports
import config as con
import utils as util

allRoutes = 

routeMap = 

if 'active_routes' in con.chooseRoues:
    chosenRoutes = []
    response = util.routesAPI(con.agencyID)
    for route in response[con.agencyID]:
        chosenRoutes.append(route['route_id'])
else:
      chosenRoutes = [key for key, value in allRoutes.items() if value in con.chooseRoutes]