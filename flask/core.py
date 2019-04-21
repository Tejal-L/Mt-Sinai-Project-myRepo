from flask import Flask, request, Response, json, jsonify
import requests
import logging
from typing import (Any, Callable, Dict, List, Optional, Text, Tuple, Union)


def add_message(sender_id, msg, parse_data):
    payload = {'sender': 'user', 'text': msg, 'parse_data': parse_data}
    sent_msg = requests.post(
        'http://rasa_core:5005/conversations/' + sender_id + '/messages', json=payload)
    return sent_msg.json()


def get_tracker(sender_id):
    r = requests.get(
        'http://rasa_core:5005/conversations/' + sender_id + '/tracker')
    tracker = r.json()
    return tracker


def predict_next(sender_id):
    r = requests.post(
        'http://rasa_core:5005/conversations/' + sender_id + '/predict')
    payload = r.json()
    return payload


def execute(sender_id, action):
    payload = {'action': action}
    r = requests.post('http://rasa_core:5005/conversations/' +
                      sender_id + '/execute', json=payload)
    # app.logger.info("execute response %s", r)
    tracker = r.json()
    return tracker


def add_event(sender_id, action):
    payload = {'event': 'action', 'name': action}
    r = requests.post('http://rasa_core:5005/conversations/' +
                      sender_id + '/tracker/events', json=payload)
    tracker = r.json()
    return tracker


def replace_events(sender_id: Text, evts: List[Dict[Text, Any]]) -> Dict[Text, Any]:
    """Replace all the events of a conversation with the provided ones."""
    payload = evts
    r = requests.put('http://rasa_core:5005/conversations/' +
                     sender_id + '/tracker/events', json=payload)
    tracker = r.json()
    return tracker
