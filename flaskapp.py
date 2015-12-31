#!flask/bin/python
import smmbapi
from flask import Flask
import json

app = Flask(__name__)

@app.route('/')
@app.route('/api/course/<path:ID>', methods=['GET'])
def nietindex(ID):
	
	return("{data}".format(data=json.dumps(smmbapi.smmbapi(ID))))

if __name__ == '__main__':
	app.run(host="0.0.0.0")