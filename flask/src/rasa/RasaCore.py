from src.rasa.RasaCoreHttpApi import RasaCoreHttpApi
import os


class RasaCore:
    def __init__(self, app):
        self.app = app
        endpoint = os.environ.get('RASA_CORE_ENDPOINT')
        if (endpoint is None):
            raise Exception("No Core Endpoint Found")

        self.api = RasaCoreHttpApi(str(endpoint), app)

    def status(self):
        return self.api.getStatus().text

    def getTrackerBySenderId(self, senderId):
        return self.api.getTracker(senderId)

    def addMessageToTracker(self, senderId, message, parseData):
        result = self.api.addMessageToTracker(senderId, message, parseData)
        return result
        # return result.json()

    def getScores(self, senderId):
        prediction_response = self.api.predictNextAction(senderId)

        return prediction_response['scores']

    def execute(self, senderId, action):
        self.api.addEventToTracker(senderId, action)
        newTracker = self.api.executeAction(senderId, action)
        return newTracker['messages']
