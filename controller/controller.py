import requests

from flask import Flask, request, render_template, make_response
from flask_restful import Api, Resource
from flask_restful import fields, marshal
import json

SENSORS = {}
ids = []

class Sensor:
    def __init__(self, sensor_id, sensor_name, address):
        self.sensor_id = sensor_id
        self.sensor_name = sensor_name
        self.address = address
        self.status = 'active' 

    def get(self):
        r = requests.get(self.address)
        return r.json()

    def update(self, config):
        r = requests.post(self.address, json=config)
        return r.json()

#
# SENSORS = { 'sensor_1': 'obiekt Sensor() odp sensor_1' , 'sensor_2': 'ob. Sensor() odp sensor_2'}
#

def abort_if_sensor_doesnt_exist(sensor_id):
    if sensor_id not in SENSORS:
        abort(404, message="Sensor {} doesn't exist".format(sensor_id))


class Controller(Resource):
    def get(self, sensor_id=None):
        if sensor_id is None:
            lista = []
            for ob in SENSORS.values():
                lista.append({ 'sensor_name': ob.sensor_name, 'url': f"/sensor/{ob.sensor_id}"})

            print(SENSORS)
            ids = SENSORS.keys()
            return make_response(render_template("Control.html", content=lista, ids = ids), 200)

        else:
            good_keys = ['file', 'cols', 'protocol', 'T', 'pause']
            ob = SENSORS[sensor_id]
            return make_response(render_template("Change_config.html", conf = ob.get(), keys = good_keys, s_id = sensor_id ), 200)

        abort_if_sensor_doesnt_exist(sensor_id)

    def post(self, sensor_id = None):
        #{"Sensor ID": X, 'Sensor name': X, "Adres": X}
        if sensor_id is None:
            sensor_info = request.json
            object_s = Sensor(sensor_info["Sensor ID"], sensor_info["Sensor name"], sensor_info["Adres"])
            id = sensor_info["Sensor ID"]
            SENSORS[id] = object_s
            return "Registered new sensor"
        else:
            retrieved_data = request.form.to_dict()
            retrieved_data['cols'] = json.loads(retrieved_data['cols'])

            requests.put(f'http://127.0.0.1:2200/sensor/{sensor_id}', json=retrieved_data)

            return retrieved_data
    
    def put(self, sensor_id):

        data = request.json
        change = {}
        if data["file"] != "":
            new_file = data["file"]
            change["file"] = new_file
        if data["cols"] != "":
            new_cols = data["cols"]
            change["cols"] = new_cols
        if data["protocol"] != "":
            new_protocol = data["protocol"]
            change["protocol"] = new_protocol
        if data["T"] != "":
            new_t = int(data["T"])
            change["T"] = new_t
        if data["pause"] != "":
            new_pause = int(data["pause"])
            change["pause"] = new_pause

        ob = SENSORS[sensor_id]
        ob.update(change)
        return

app = Flask(__name__)
api = Api(app)

api.add_resource(Controller, '/', '/sensor', '/sensor/<int:sensor_id>')

if __name__ == '__main__':
    app.run(debug=True, port=2200)



