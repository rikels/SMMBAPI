#!flask/bin/python
import smmbapi
from flask import Flask
import json

app = Flask(__name__)

@app.route('/api/course/<path:ID>', methods=['GET'])
def GetCourseByID(ID):
        return("{data}".format(data=json.dumps(smmbapi.GetCourseByID(ID))))

@app.route('/api/course/recommended', methods=['GET'])
def GetRecommendedCourses():
        return("{data}".format(data=json.dumps(smmbapi.GetRecommendedCourses())))

@app.route('/api/course/ranked', methods=['GET'])
def GetRankedCourses():
        PageNum = int(request.args['pagenum'])
        Type = request.args['type']
        return("{data}".format(data=json.dumps(smmbapi.GetRankedCourses(PageNum=PageNum,Type=Type))))

@app.route('/api/maker/ranked', methods=['GET'])
def GetRankedMakers():
        PageNum = int(request.args['pagenum'])
        Type = request.args['type']
        return("{data}".format(data=json.dumps(smmbapi.GetRankedMakers(PageNum=PageNum,Type=Type))))

if __name__ == '__main__':
	app.run(host="0.0.0.0")
