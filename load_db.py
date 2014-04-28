#!/usr/bin/env python

from __future__ import print_function

import requests
import json

headers = {'content-type': 'application/json'}

# List of users
def state():
	print('list of users')
	r = requests.get('http://localhost:5000/api')
	print(r.text)

	print('models for monte')
	r = requests.get('http://localhost:5000/api/monte')
	print(r.text)

	print('models for thomas')
	r = requests.get('http://localhost:5000/api/thomas')
	print(r.text)


def add_users():
	url = 'http://localhost:5000/api/'
	users = []

	users.append({'name': 'thomas', 
				  'email': 'thomas.hauser@colorado.edu'})

	users.append({'name': 'monte', 
				  'email': 'monte.lunacek@colorado.edu'})

	for user in users:
		r = requests.post(url, data=json.dumps(user), headers=headers)


def add_models():
	urls = ['http://localhost:5000/api/thomas',
			'http://localhost:5000/api/monte']

	models = []
	models.append({'name': 'rengers', 'cmd': '$HOME/projects/rengers/webapi_wrapper/execute.py'})
	models.append({'name': 'showq', 'cmd': 'showq'})

	for url in urls:
		for model in models:
			r = requests.post(url, data=json.dumps(model), headers=headers)
			

state()
add_users()
add_models()
state()




