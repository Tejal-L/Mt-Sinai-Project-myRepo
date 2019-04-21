from flask import json
import requests


class RasaNLUHttpApi:
    def __init__(self, nluEndpoint, app):
        self.app = app
        self.endpoint = nluEndpoint
        self.baseURI = str(nluEndpoint) + "/"

    def getStatus(self):
        return requests.get(self.endpoint + "nlu/status")

    def getVersion(self):
        return requests.get(self.endpoint + "nlu")

    def parse(self, text):
        json_data = {
            "project": "nlu",
            "q": text
        }

        headers = {'content-type': 'application/json'}

        results = requests.post(self.baseURI + "parse",
                                headers=headers,
                                data=json.dumps(json_data))

        return results.json()
