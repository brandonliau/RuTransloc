import sys, os
sys.path.insert(0, '/Users/bliau/Documents/VS Code/Python/RuTransloc/configuration')
sys.path.insert(0, '/Users/bliau/Documents/VS Code/Python/RuTransloc/src/tools')
import routeInfo as ri
import getData as gd

def feedData(route: str = 'all', bus: str = None) -> list:  
    if route == 'all':
        for route in ri.routeMap.keys():
            return gd.combineData(route)
    elif route in ri.routeMap:
        return gd.combineData(route)
    else:
        return ('Invalid route')
    
    if bus != None:
        for route in ri.routeMap.keys():
            data = gd.combineData(route)
            if bus == data['Call_name']:
                return data
        else:
            return ('Invalid bus')