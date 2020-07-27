import requests
import json

def get_disasters():
    response = json.loads(requests.get("https://api.reliefweb.int/v1/disasters?appname=togetherly&profile=list&preset=latest&slim=1").text)
    disaster = []
    for i in range(len(response["data"])):
        print(response["data"][i]["fields"]["name"])
        disaster.append(response["data"][i]["fields"]["name"])

    return disaster