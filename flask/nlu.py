from flask import Flask, request, Response, json, jsonify
import requests
import logging

def parse(text):
    json_data = {
		"project": "nlu",
		# 'model': 'default',
		"q": text
	}

    headers = { 'content-type': 'application/json' }

    r = requests.post('http://rasa_nlu:5000/parse',
		headers=headers,
		data=json.dumps(json_data))

    return r.json()