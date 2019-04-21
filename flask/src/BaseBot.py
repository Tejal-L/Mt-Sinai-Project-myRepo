from src.rasa.RasaCore import RasaCore
from src.rasa.RasaNLU import RasaNLU


class BaseBot:
    def __init__(self, app):
        self.core = RasaCore(app)
        self.nlu = RasaNLU(app)

    def parseAndRespond(self, payload):
        pass

    def getBotResponse(self, senderId, message):
        pass

    def reply(self, channel, message):
        pass
