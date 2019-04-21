from flask import json
import requests


class RasaCoreHttpApi:
    def __init__(self, coreEndpoint, app):
        self.app = app
        self.endpoint = coreEndpoint
        self.baseURI = "%s/conversations/" % str(coreEndpoint)

    def getTracker(self, senderId):
        uri = self.baseURI + "%s/tracker" % senderId
        return requests.get(uri)

    def addEventToTracker(self, senderId, action):
        payload = {
            "event": "action",
            "name": action
        }

        result = requests.post(self.baseURI + "%s/tracker/events" % senderId,
                               json=payload)

        return result.json()

    def predictNextAction(self, senderId):
        uri = self.baseURI + "%s/predict" % senderId
        result = requests.post(uri)

        return result.json()

    def addMessageToTracker(self, senderId, message, parse_data):
        payload = {
            "sender": "user",
            "message": message,
            "parse_data": parse_data
        }

        uri = self.baseURI + "%s/messages" % senderId

        result = requests.post(uri, json=payload)

        return result.json()

    def executeAction(self, senderId, action):
        payload = {
            "action": action
        }

        result = requests.post(self.baseURI + "%s/execute" % senderId,
                               json=payload)

        return result.json()

    def getStory(self, senderId):
        return requests.get(self.baseURI + "%s/story" % senderId)

    def getStatus(self):
        return requests.get(self.endpoint)
