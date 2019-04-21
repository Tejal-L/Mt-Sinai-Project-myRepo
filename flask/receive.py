from flask import Flask, request, Response, json, jsonify
import os
import requests
import logging
from nlu import parse
from core import add_message, get_tracker, predict_next, execute, add_event
import interactive_training
# from interactive_training import make_intents_block, validate_user_text
from queueObject import QueueObject
import json
import requests
import redis
from redis import Redis



#from RedisQueue import RedisQueue


SLACK_WEBHOOK_SECRET = os.environ['SLACK_WEBHOOK_SECRET']
BEARER_TOKEN = os.environ['BEARER_TOKEN']
#message_queue = dict()



import redis

message_queue = redis.Redis(host="redis", db=0, socket_timeout=5, charset="utf-8", decode_responses=True)

# usage
#r.set('foo', 'bar')
#value = r.get('foo')
app = Flask(__name__)



@app.route('/')
def hello_world():
    return 'Flask Dockerized'


@app.route('/core')
def hello_core():
    r = requests.get('http://rasa_core:5005')
    return r.text


@app.route('/nlu')
def hello_nlu():
    r = requests.get('http://rasa_nlu:5000/version')
    return r.text


@app.route('/nlu/status')
def nlu_status():
    r = requests.get('http://rasa_nlu:5000/status')
    return r.text

# @app.route('/parse')
# def parse_query():

# 	json_data = {
# 		"project": "rasa_nlu",
# 		"q": request.args.get('query')				app.logger.info('rasa core next action %s', next_action)

# 	}

# 	headers = { 'content-type': 'application/json' }

# 	r = requests.post('http://rasa_nlu:5000/parse',
# 		headers=headers,
# 		data=json.dumps(json_data))

# 	return r.text


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
    app.logger.info("inbound")
    print("inbound print")
    # app.logger.info('json payload %s', data)

    if data['token'] == SLACK_WEBHOOK_SECRET:
        app.logger.info('SLACK Secret Matched')

        if data['type'] == 'url_verification':
            challenge = data['challenge']
            app.logger.info('challenge %s', data['challenge'])
            return jsonify({'challenge': data['challenge']}), 200

        if data['type'] == 'event_callback':
            event = data['event']
            event_id = data['event_id']
            event_type = event['type']
            if message_queue.get(event_id) == None:
            	val = True
            else:
            	val = False
            #app.logger.info("foo value =>" + r.get('foo'))

            if val == True and 'client_msg_id' in event:
                # return Response(), 200
                # simple event queue via hashmap
                #message_queue[event_id] = True
                ##creating object for redis
                #senderID, payload, queryType, botId
                app.logger.info("senderID =>" + event['channel'])
                app.logger.info("payload =>" + event['text'])
                app.logger.info("queryType =>" + "text")
                app.logger.info("botId =>" + "slack")
                object = QueueObject(event['channel'], event['text'], 'text', 'slack')  
                app.logger.info("object => "+ object.payload)
                message_queue.set(event_id, json.dumps(object, default=lambda o: o.__dict__))#"event")

                # get channel ID
                channel = event['channel']

                # get tracker for user
                sender_id = event['user']
                tracker = get_tracker(sender_id)
                app.logger.info('rasa core tracker %s', tracker)

                # parse message with nlu
                msg = event['text']
                parse_data = parse(msg)
                app.logger.info('nlu parse data %s', parse_data)
                app.logger.info('nlu parse data type %s', type(parse_data))

                # add message to dialogue tracker
                tracker_after_add_message = add_message(
                    sender_id, msg, parse_data)
                app.logger.info('rasa core response %s',
                                tracker_after_add_message)

                # create message to send to user to validate intent
                message = interactive_training.validate_user_text(
                    tracker_after_add_message)
                    
                #########redis

                                      
                # send user buttons to ratify intent
                reply_ratify_intent_block(channel, message)
                
                
                
                # test returning intent selection block
                # intent_blocks = interactive_training.make_intents_block(sender_id)
                # app.logger.info('tracker events %s', intent_blocks)
                # reply_select_intent_block(channel, intent_blocks)

                # predict next action
                # prediction_response = predict_next(sender_id)
                # app.logger.info('rasa core prediction response %s',
                #                 prediction_response['scores'])

                # scores = prediction_response['scores']

                # max = -1
                # next_action = ''
                # for entry in scores:
                #     if entry['score'] > max:
                #         max = entry['score']
                #         next_action = entry['action']

                # app.logger.info('rasa core next action %s', next_action)

                # half_new_tracker = add_event(sender_id, next_action)

                # new_tracker = execute(sender_id, next_action)
                # app.logger.info('result of execute %s', new_tracker)
                #reply(channel, str(dialogue_response['latest_message']['intent_ranking']))
                #if r.get('new') == None:
                #	app.logger.info("new value => none")
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

    return Response(), 200


def reply(channel, block):
	app.logger.info("in reply")
	json_data = {
		"channel": channel,
        "text": message
    }

	headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + BEARER_TOKEN
    }

	r = requests.post('https://slack.com/api/chat.postMessage',
                      headers=headers,
                      data=json.dumps(json_data))
	app.logger.info('reply : Sending to Slack %s', r.text)
	


def reply_ratify_intent_block(channel, message):
    block = [
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
                    "style": "danger",
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
    json_data = {
        "channel": channel,
        "text": "this is a message",
        "blocks": block
    }
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + BEARER_TOKEN
    }

    r = requests.post('https://slack.com/api/chat.postMessage',
                      headers=headers,
                      data=json.dumps(json_data))

    app.logger.info('reply_ratify_intent_block : Sending to Slack %s', r.text)


def reply_select_intent_block(channel, options):
    block = [
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
    json_data = {
        "channel": channel,
        "text": "this is a message",
        "blocks": block
    }
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + BEARER_TOKEN
    }
    r = requests.post('https://slack.com/api/chat.postMessage',
                      headers=headers,
                      data=json.dumps(json_data))

    app.logger.info('reply_select_intent_block : Sending to Slack %s', r.text)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
