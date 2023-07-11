# Standard library imports
import sys, os
sys.path.append(os.path.abspath('configuration'))
sys.path.append(os.path.abspath('src/tools'))
# Third party imports
from fastapi import FastAPI, HTTPException, status, Security
from fastapi.security import APIKeyHeader, APIKeyQuery
# Local imports
from validKeys import API_KEYS as authorized
import apiSupport as apiS

api_key_query = APIKeyQuery(name="apiKey", auto_error=False)
api_key_header = APIKeyHeader(name="x-apiKey", auto_error=False)

def getAPIKey(api_key_query: str = Security(api_key_query), api_key_header: str = Security(api_key_header)) -> str:
    if api_key_query in authorized:
        return api_key_query
    if api_key_header in authorized:
        return api_key_header
    raise HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid or missing API Key",
    )

app = FastAPI()
@app.get('/')
async def health(apiKey: str = Security(getAPIKey)):
    return {'Status': 'Operational', 'Version': 'v1'}

@app.get('/predict/')
async def predict(routes: str = None, model: str = 'RandomForest', apiKey: str = Security(getAPIKey)):
    return apiS.generatePrediction(routes, model)

@app.get('/raw/')
async def raw(routes: str = None, apiKey: str = Security(getAPIKey)):
    routes = routes.split(',')
    return apiS.returnRaw(routes)
