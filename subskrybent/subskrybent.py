import paho.mqtt.client as mqtt_client
import requests
import json


#Postowanie

url = "http://127.0.0.1:5000"

def post(report):
    r = requests.post(url, json=report)
    #print(r.text)

#broker:

broker = "127.0.0.1"
port = 1883
topics = [("Kurs Euro", 0), ("Urodzenia", 0), ("Podatek", 0), ("Parking", 0), ("Powietrze jakosc", 0)]
client_id = "Aplikacja"

#Subskrybent

def connect_to_MQTT():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker")
        else:
            print("Failed to connect")

    client = mqtt_client.Client(client_id)
    client.connect(broker, port)
    client.on_connect = on_connect    
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        data = str(msg.payload.decode('utf-8'))
        print(f"Received {data}")
        print(type(data))
        data = json.loads(data)
        print("=========")
        print(type(data))
        #data = json.dumps(data)
        #print("__________")
        #print(type(data))
        post(data)

    client.subscribe(topics)
    client.on_message = on_message


if __name__ == "__main__":
    client = connect_to_MQTT()
    subscribe(client)
    client.loop_forever()