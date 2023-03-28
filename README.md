## IoT sensorlike system

This is a project from my uni IoT classes. It pretends to be system, in which 5 sensors are sending reports in given periods of time

Every sensor (sensor-1, sensor-2, sensor-3, sensor-4, sensor-5) has its own modifiable configuration file (f.e. sensor-1.json)

```
{
  "sensor_id": 1,
  "sensor_name": "Urzadzenie nr 1",
  "file": "euro-kurs.csv",
  "cols": [
    "Data",
    "Otwarcie"
  ],
  "T": 10,
  "protocol": "http",
  "broker_host": "127.0.0.1",
  "broker_port": 1883,
  "mqtt_topic": "Kurs Euro",
  "http_url": "http://127.0.0.1:5000",
  "pause": 0,
  "app_url": "http://127.0.0.1:2137"
}
```

We can change params of this config file using 'controller'. 

As I use Multiprocessing, i have decided to use Lock() to unable doing anything while reading config instruction of every sensor (config file is continously checked and followed before taking action by any sensor).
Every sensor has a common base - class: ConfigFile and ReportSender (activated in def worker)


Whole system also consists of:
- 'subskrybent' which is basically a paho mqtt brocker.
- 'controller' in which we can change config file of any sensor from one place (web)
- 'agregator' which receives data from every active sensor and tries to agregate them into 'weird function' just calculate some nonsense
- 'filer' in which we can decide from which sensor we would like to collect data
- 'wizualizacja' which collects data and creates charts of each sensor
- 'server' which is a main server, 

These are RESTAPI servers and each is at different port and all (except sensors - they are optional) have to be run in terminal.

Some examplary screenshots of how it works:





