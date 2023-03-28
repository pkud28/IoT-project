import sys, os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

from my_sensor import ReportSender, ConfigFile

import json
from flask import Flask, request
from flask_restful import Resource, Api
from multiprocessing import Lock, Process
from os.path import splitext

app = Flask(__name__)
api = Api(app)

class SensorConfig(Resource):
    def get(self):
        return cf.read()

    def post(self):
        cf.update(request.json)
        return cf.read(), 200

api.add_resource(SensorConfig, '/')

def worker(cf):
    rs = ReportSender(cf)
    rs.loop_forever()

if __name__ == "__main__":
    lock = Lock()
    
    path = splitext(__file__)[0] + '.json'
    cf = ConfigFile(path, lock)

    Process(target=worker, args=(cf,)).start()
    app.run(debug=True, port=2137, use_reloader=False)
    #app.run(debug=True, port=1800, use_reloader=False)
    #app.run(debug=True, port=1900, use_reloader=False)
    #app.run(debug=True, port=2000, use_reloader=False)
    #app.run(debug=True, port=2100, use_reloader=False)


