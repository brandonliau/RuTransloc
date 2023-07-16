# RuTransloc
Machine learning pipeline used to predict the ETA for buses at Rutgers University. This project was originally configured for Rutgers but can easily be changed to accomadate any transportation network that relies on [TransLoc](https://transloc.com/). This project also contains the code required for deployement as an API.

## Installation
- Clone this Repository
```
git clone https://github.com/brandonliau/RuTransloc.git
```
- Install requirements
```
cd RuTransloc
pip install -r .github/requirements.txt
```

## Configure Project
- Generate required API keys and populate corresponding variables in config.py
- Run the configuration generator
```
cd src/scripts/
python generateConfig.py
```
- Populate all variables specificied by the configuration generator
- Choose routes to track by adding items to the allRoutes list in config.py

## Get API Keys
- **TransLoc PublicAPI** - https://rapidapi.com/transloc/api/openapi-1-2/
- **TomTom Traffic API** - https://developer.tomtom.com/

## Collecting Data
- Run the data collection script
```
cd src/scripts/
python collectData.py
```

## Training Machine Learning Models
- Train models by running the Jupyter NoteBook
- Before running, change the filepath variable
- Currently supported models:
    - Random Forest Regression
    - Support Vector Regression

## Deployment
- Feel free to deploy to any service you are comfortable using
- To deploy to Google Cloud:
    - Install Docker: https://docs.docker.com/engine/install/
    - Install the gcloud CLI: https://cloud.google.com/sdk/docs/install
    - Create a new project in Google Cloud
    - Create a repository in Google Cloud Artifact Registry
    - Build image
    ```
    sudo docker build -t {image_name} .
    ```
    - Minify Docker image with slim (*optional*): https://github.com/slimtoolkit/slim
    ```
    sudo docker slim build -http-probe --include-path /app/ --preserve-path src/models/ {image_name}
    ```
    - Push image to Google Cloud Artifact Registry
    ```
    docker tag {image_name} {location}-docker.pkg.dev/{project_name}/{repo_name}/{name}
    docker push {location}.pkg.dev/{project_name}/{repo_name}/{name}
    ```
    - Create service in Cloud Run with image from Artifact Registry