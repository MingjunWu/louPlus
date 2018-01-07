import os
from flask import Flask
import json

def create_app():
	app = Flask('rmon')
	file = os.environ.get("RMON_CONFIG")
	contents = ""
	try:
		with open(file) as f:
			for line in f:
				line = line.strip()
				if line.startswith('#'):
					continue
				else:
					contents += line
	except IOError:
		return app

	try:
		data = json.loads(contents)
	except:
		return app

	for key in data:
		app.config[key.upper()] = data.get(key)
	return app
