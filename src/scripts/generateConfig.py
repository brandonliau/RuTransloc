# Standard library imports
import sys, os
sys.path.append(os.path.abspath('../tools'))
# Local imports
import getData as gd

gd.getAgency()
index = input('Select agent: ')
os.system('cls' if os.name == 'nt' else 'clear')
agencyID = gd.getAgency(index)
input('Copy agency ID into config.py (agencyID) and enter when ready to continue: ')
os.system('cls' if os.name == 'nt' else 'clear')

gd.getRoutes(agencyID)
index = input('Select desired routes (seperate values using a comma): ')
index = list(map(int, index.split(',')))
routes = gd.getRoutes(agencyID, index)
input('Copy selected routes into routeInfo.py (allRoutes) and enter when ready to continue: ')
os.system('cls' if os.name == 'nt' else 'clear')

gd.getStops(agencyID, routes)
input('Copy selected routes into routeInfo.py (routeMap) and enter when ready to continue: ')
os.system('cls' if os.name == 'nt' else 'clear')
input('You have reached the end of setup. \nEnter to exit: ')
exit