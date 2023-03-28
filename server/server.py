
import requests
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

REPORTS = []

class ReportAggregator(Resource):
    def get(self):
        return REPORTS

    def post(self):
        data = request.json
        REPORTS.append(data)

        url = 'http://127.0.0.1:2222'
        r = requests.post(url, json = data )
        
        return REPORTS[-1], 200


api.add_resource(ReportAggregator, '/')

if __name__ == '__main__':
    app.run(debug=True)


