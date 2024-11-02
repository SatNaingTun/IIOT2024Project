import json

def data2Json(myDict):
    return json.dumps(myDict)

def json2Dict(myJson):
    return json.load(myJson)
