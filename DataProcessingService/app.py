from fastapi import FastAPI, Request
import json
import uvicorn
import requests
import logging
import argparse

app = FastAPI()

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--color', type=str, required=False)
arg_parser.add_argument('-port', type=str, required=False)
arg_parser.add_argument('--datastore', type=str, required=False)
args = arg_parser.parse_args()

DEFAULT_ENV = 'local'
DEFAULT_COLOR = 'blue'
DEFAULT_DATASTORE_URL = 'http://verylargedatastore:8080'
DEFAULT_PORT = 3000

# Configure app cia command line params
if args.color:
    color = args.color
else:
    color = DEFAULT_COLOR
if args.port:
    port = args.port
else:
    port = DEFAULT_PORT
if args.datastore:
    datastoreURL = args.datastore
else:
    datastoreURL = DEFAULT_DATASTORE_URL

environment = DEFAULT_ENV
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)
log.setLevel(logging.INFO)


# Root
@app.get('/')
async def root(request: Request):
    log.info(request.url)
    return 'root endpoint entry (DataProcessingService)'


# Color
@app.get('/color')
def get_color():
    log.info('color endpoint entry')
    return color


# Environment
@app.get('/environment')
def get_environment():
    log.info('environment endpoint entry')
    return environment


# recordCount (get the number or records via a call to the datastore service)
@app.get('/recordCount')
def record_count():
    log.info('recordCount endpoint entry')
    try:
        response = requests.get(datastoreURL + '/recordCount')
        log.info(response.text)
        return response.text
    except requests.exceptions.RequestException as error:
        log.error(error)


# findMerch (find EdgeyCorp merchandise matching search params via datastore service)
@app.get('/findMerch')
def find_merchandise(country: str = "", season: str = ""):
    log.info('findMerch endpoint retry')
    log.info(country)
    log.info(season)
    payload = {'country': country, 'season': season}
    try:
        search_response = requests.get(datastoreURL + '/findMerch', params=payload)
        log.info(search_response.text)
        return json.loads(search_response.text)
    except requests.exceptions.RequestException as error:
        log.error(error)


if __name__ == '__main__':
    log.info('Welcome to the DataServiceProcessingPythonService!')
    uvicorn.run("app:app", host='0.0.0.0', port=3000, reload=True)
