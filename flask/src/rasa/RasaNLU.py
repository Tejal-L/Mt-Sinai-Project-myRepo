from src.rasa.RasaNLUHttpApi import RasaNLUHttpApi
import os


class RasaNLU:
    def __init__(self, app):
        self.app = app
        app.logger.info("Getting NLU up and running")
        endpoint = os.environ.get('RASA_NLU_ENDPOINT')

        if (endpoint is None):
            raise Exception("No NLU Endpoint found")

        self.api = RasaNLUHttpApi(str(endpoint), app)
        app.logger.info("NLU Endpoint: " + str(endpoint))

    def status(self):
        return self.api.getCoreStatus().text

    def version(self):
        return self.api.getCoreStatus().text

    def parse(self, message):
        self.app.logger.info("Here's what I'm about to parse")
        self.app.logger.info("Message: " + message)
        parseData = self.api.parse(message)
        self.app.logger.info("Just finished parsing")
        self.app.logger.info(parseData)
        return parseData
