import interactive_training
import os
import requests
import logging
from core import predict_next
from dotenv import load_dotenv
from src.SlackBot import SlackBot
from flask import Flask, request, Response, json, jsonify
load_dotenv()

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Flask Dockerized'


@app.route('/core')
def hello_core():
    return core.status()


@app.route('/nlu')
def hello_nlu():
    return nlu.version()


@app.route('/nlu/status')
def nlu_status():
    return nlu.status()


@app.route('/evaluate')
def evaluate():

    json_data = {
        "project": "rasa_nlu",
        "model": "rasa_nlu"
    }

    headers = {'content-type': 'application/json'}

    r = requests.post('http://rasa_nlu:5000/evaluate',
                      headers=headers,
                      data=json.dumps(json_data))

    return r.text


@app.route('/slack', methods=['POST'])
def inbound():
    data = request.get_json()
    try:

        if data['type'] == 'url_verification':
            challenge = data['challenge']
            return jsonify({'challenge': data['challenge']}), 200

        bot = SlackBot(data["token"], app)

        # TODO: Refactor this to not hard code the boolean for isInteractive.
        #       Maybe move this to a different endpoint?
        #       I'm thinking we should have an interactive endpoint
        #       And a endpoint that will just respond
        botResponse = bot.parseAndRespond(data, True)
        channel = data['event']['channel']

        # create message to send to user to validate intent
        message = interactive_training.validate_user_text(
            botResponse)

        # send user buttons to ratify intent
        reply_ratify_intent_block(channel, message)

    except Exception as e:
        app.logger.info('Exception caught %s', str(e))
        return(str(e))

    return Response(), 200


@app.route('/slack/interactive', methods=['POST'])
def interactive_response():
    payload = json.loads(request.values.get("payload"))
    # app.logger.info('interactive reponse payload %s', type(payload))
    channel = payload.get("channel").get("id")
    trigger_id = payload.get("trigger_id")
    sender_id = payload.get("user").get("id")
    actions = payload.get("actions", [])
    app.logger.info('channel: %s, sender_id: %s, actions: %s',
                    channel, sender_id, actions)

    first_action = actions[0]
    if first_action['type'] == 'button':
        if first_action['value'] == 'true':
            prediction_response = predict_next(sender_id)
            app.logger.info(
                'intent correct! predicted reponses: %s', prediction_response['scores'])
        else:
            intent_options_block = interactive_training.make_intents_block(
                sender_id)
            app.logger.info('intent selection block: %s', intent_options_block)
            reply_select_intent_block(channel, intent_options_block)

    elif first_action['type'] == 'static_select':
		# get tracker before update
        initial_tracker = get_tracker(channel)
        app.logger.info('initial tracker %s', initial_tracker)
		# get correct intent label from message
        corrected_intent = first_action['selected_option']['value']

		# construct NLU json with correct intent
        corrected_nlu = interactive_training.make_corrected_nlu(
            corrected_intent, channel, initial_tracker)
		
		# update tracker by correctly previous intent
        updated_tracker = interactive_training.correct_wrong_nlu(corrected_nlu, channel, initial_tracker)
        app.logger.info('updated tracker %s', updated_tracker)
    return Response(), 200


def reply_ratify_intent_block(channel, message):
    block=[
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": message
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Yes",
                        "emoji": False
                    },
                    "value": "true"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "No",
                        "emoji": False
                    },
                    "value": "false"
                }
            ]
        }
    ]
    json_data={
        "channel": channel,
        "text": "this is a message",
        "blocks": block
    }
    headers={
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + str(os.environ.get('SLACK_BEARER_TOKEN'))
    }

    r=requests.post('https://slack.com/api/chat.postMessage',
                      headers=headers,
                      data=json.dumps(json_data))

    app.logger.info('Sending to Slack %s', r.text)


def reply_select_intent_block(channel, options):
    block=[
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Please select the correct Intent your message."
            },
            "accessory": {
                "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Intents",
                            "emoji": False
                        },
                "options": options
            }
        }
    ]
    json_data={
        "channel": channel,
        "text": "this is a message",
        "blocks": block
    }
    headers={
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + str(os.environ.get('SLACK_BEARER_TOKEN'))
    }
    r=requests.post('https://slack.com/api/chat.postMessage',
                      headers=headers,
                      data=json.dumps(json_data))

    app.logger.info('Sending to Slack %s', r.text)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
