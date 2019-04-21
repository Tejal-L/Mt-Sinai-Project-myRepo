from src.BaseBot import BaseBot
from flask import json, jsonify
import requests
import os


class SlackBot(BaseBot):
    def __init__(self, token, app):
        BaseBot.__init__(self, app)
        self.slackWebhookSecret = str(os.environ.get('SLACK_WEBHOOK_SECRET'))
        self.slackBearerToken = str(os.environ.get('SLACK_BEARER_TOKEN'))

        if (token != self.slackWebhookSecret):
            raise Exception("Invalid Token")

        self.message_queue = dict()
        self.channel = None
        self.app = app

    def parseAndRespond(self, payload, isInteractive):
        try:

            if payload['type'] != 'event_callback':
                return False

            event = payload['event']
            event_id = payload['event_id']
            event_type = event['type']
            channel = event['channel']

            if event_id not in self.message_queue and 'client_msg_id' in event:
                sender_id = event['user']
                message = event['text']
                self.message_queue[event_id] = True

                if (isInteractive):
                    return self.getInteractiveResponse(sender_id, message)
                else:
                    botResponse = self.getResponse(sender_id, message)
                    self.reply(channel, botResponse)

                return True
        except Exception as e:
            raise e

        return False

    def getResponse(self, senderId, message):
        tracker = self.core.getTrackerBySenderId(senderId)
        parseData = self.nlu.parse(message)
        tracker = self.core.addMessageToTracker(senderId, message, parseData)
        scores = self.core.getScores(senderId)

        max = -1
        nextAction = ''
        for entry in scores:
            if entry['score'] > max:
                max = entry['score']
                nextAction = entry['action']

        return self.core.execute(senderId, nextAction)

    def getInteractiveResponse(self, senderId, message):
        tracker = self.core.getTrackerBySenderId(senderId)
        parseData = self.nlu.parse(message)
        tracker = self.core.addMessageToTracker(senderId, message, parseData)

        return tracker

    # TODO: THis should be refactored based on the SlackClient API library
    def reply(self, channel, message):
        json_data = {
            "channel": channel,
            "text": message
        }

        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + self.slackBearerToken
        }

        return requests.post('https://slack.com/api/chat.postMessage',
                             headers=headers,
                             data=json.dumps(json_data))
