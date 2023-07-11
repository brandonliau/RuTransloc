# RuTransloc
Machine learning pipeline used predict the ETA for buses at Rutgers University. This project was originally configured for Rutgers but can easily be changed to accomadate any transportation network that relies on [TransLoc](https://transloc.com/). This project also contains the code required for deployement as an API.

## Installation
- Clone this Repository
```
git clone https://github.com/brandonliau/RuTransloc.git
```
- Install requirements
```
cd RuTransloc
pip install -r requirements.txt
```

## Configure Project
- Create a configuration folder with the neccessary files
```
$ mkdir configuration
$ cd configuration
$ touch config.py routeInfo.py validKeys.py
```
- Copy format for configuration files from the example folder
- Run the configuration generator
```
python src/scripts/generateConfig.py
```
- Choose routes to collect data from in config.py

## Get API Keys
- **TransLoc PublicAPI** - https://rapidapi.com/transloc/api/openapi-1-2/
- **TomTom Traffic API** - https://developer.tomtom.com/

## Collecting Data
- Run the data collection script
```
python src/scripts/collectData.py
```

## Training Machine Learning Models
- Train models by running the Jupyter NoteBook
- Before running, change the filepath variable
- Currently supported models:
    - Random Forest Regression
    - Support Vector Regression

## Deployment
🚧 In progress 🚧