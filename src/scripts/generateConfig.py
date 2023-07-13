# Standard library imports
import sys, os
sys.path.append(os.path.abspath('../tools'))
# Local imports
import configSupport as cs

cs.getAgency()
index = input('Select agent: ')
os.system('cls' if os.name == 'nt' else 'clear')
agencyID = cs.getAgency(index)
input('Copy agency ID into config.py (agencyID) and enter when ready to continue: ')
os.system('cls' if os.name == 'nt' else 'clear')

cs.getRoutes(agencyID)
index = input('Select desired routes (seperate values using a comma): ')
index = list(map(int, index.split(',')))
os.system('cls' if os.name == 'nt' else 'clear')
routes = cs.getRoutes(agencyID, index)
input('Copy selected routes into routeInfo.py (allRoutes) and enter when ready to continue: ')
os.system('cls' if os.name == 'nt' else 'clear')

cs.getStops(agencyID, routes)
input('Copy selected routes into routeInfo.py (routeMap) and enter when ready to continue: ')
os.system('cls' if os.name == 'nt' else 'clear')
input('You have reached the end of setup. \nEnter to exit: ')
exit