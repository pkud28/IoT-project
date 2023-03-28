
import time, datetime
import json, csv
import pandas as pd
import requests
import paho.mqtt.client as mqtt_client
import os.path

###############################################################################

def http_post(data, url):
    r = requests.post(url, json=data)
    print(f"[ > ] POST to {url} | {r.text}")

###############################################################################

def mqtt_connect(client_id, broker, port):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("[ < ] Connected to MQTT Broker")
        else:
            print("[ ! ] Failed to connect")

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    
    return client

def publish(data, client, topic):
    json_data = json.dumps(data)
    result = client.publish(topic, json_data)
 
    if result[0] == 0:
        print(f"[ > ] Sent '{json_data}' to topic '{topic}'")
    else:
        print(f"[ ! ] Failed to send a message to topic '{topic}'")

###############################################################################

class ConfigFile:
    def __init__(self, path, lock):
        self.lock = lock
        self.path = path
        
    def read(self):
        self.lock.acquire()
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        finally:
            self.lock.release()

    def update(self, change):
        config = self.read()
        good_keys = ['file', 'cols', 'protocol', 'T', 'pause']
        config.update((k, v) for k, v in change.items() if k in good_keys)

        print('================================================')
        print(change)
        print('================================================')
        print(config)
        print('================================================')


        self.lock.acquire()
        try:
            with open(self.path, "w", encoding='utf8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        finally:
            self.lock.release()

###############################################################################

def report(x, cols, id, adres):

    report = {}
    for c in cols: 
        report[f"{c}"] = x[c]

    return { 'sensor': id,
             'report': report,
             'adres': adres}

###############################################################################

class ReportSender:
    def __init__(self, cf):
        self.cf = cf

        config = cf.read()
        self.id = config['sensor_id']
        self.name = config['sensor_name']

        # MQTT
        broker_host = config['broker_host']
        broker_port = config['broker_port']
        self.mqtt_topic = config['mqtt_topic']
        self.mqttc = mqtt_connect(self.name, broker_host, broker_port)
        self.mqttc.loop_start()
        
        # HTTP 
        self.http_url = config['http_url']

        # Reports
        self.file = None
        self.cols = None
        self.gen = iter([None])
        self.T = None

        #Post 'connected' status to controller
        c_data = {"Sensor ID": self.id, 'Sensor name': self.name, "Adres": config["app_url"]}
        c_url = 'http://127.0.0.1:2200'
        r = requests.post(c_url, json = c_data)
        print(f"[ > ] POST to {c_url} | {r.text}")

       
    def send(self, data):
        config = self.cf.read()
        get_abs_fpath = lambda x:  os.path.join(os.path.dirname(self.cf.path), x)

        new_file = get_abs_fpath(config['file'])
        new_cols = config['cols']
        if self.file != new_file or self.cols != new_cols:
            self.file = get_abs_fpath(new_file)
            self.cols = new_cols

            df = pd.read_csv(self.file, usecols=self.cols, dtype=str)

            self.gen = (report(x, self.cols, id=self.id, adres = config["app_url"]) for i, x in df.iterrows())


        if data is not None and config['pause'] == 0:
            if config['protocol'] == 'mqtt':
                publish(data, self.mqttc, self.mqtt_topic)
            elif config['protocol'] == 'http':
                http_post(data, self.http_url)


        self.T = config['T']

    def loop_forever(self):
        while True:
            try:
                print('[ - ] send()') 
                self.send(next(self.gen)) 
            except StopIteration:
                self.gen = iter([None])
            time.sleep(self.T)

