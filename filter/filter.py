import requests
from flask import Flask, request, render_template, make_response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

DATA = []
FILTERED_DATA = []
CONFIGURATION = [0, 0, 0, 0, 0]

def filterdata():
    global FILTERED_DATA
    global CONFIGURATION
    global DATA

    for d in DATA:
        if "Config" in d.keys():
            CONFIGURATION = [0, 0, 0, 0, 0]
            config = []
            keys = d["Config"].keys()
            keys = [ int(x) for x in keys ]

            for i in range( max( keys) ): 
                 config.append(0)
            for k in d["Config"].keys():
                value = d["Config"][k]
                #config.insert(int(k)-1, int(value) )
                config[int(k)-1] = int(value)

            for j in range(0, len(config)):
                if config[j] == 1:
                    CONFIGURATION[j] = 1
                else:
                    CONFIGURATION[j] = 0

            FILTERED_DATA = []

        else:
            id = d["sensor"]
            if id == 1 and CONFIGURATION[0] == 1:
                FILTERED_DATA.append(d)
            if id == 2 and CONFIGURATION[1] == 1:
                FILTERED_DATA.append(d)
            if id == 3 and CONFIGURATION[2] == 1:
                FILTERED_DATA.append(d)
            if id == 4 and CONFIGURATION[3] == 1:
                FILTERED_DATA.append(d)
            if id == 5 and CONFIGURATION[4] == 1:
                FILTERED_DATA.append(d)
            
            #print("_____________________________")
            #print(CONFIGURATION)
            #print(FILTERED_DATA)
            #print("______________________________")
    return


class Filter(Resource):
    def get(self):   
        filterdata()   

        #Dalsze przesyłania ?

        #
        #url1 = "http://127.0.0.1:2600"
        #for data in FILTERED_DATA:
        #    requests.post(url1, json = data)
        #print("WYSLANO")

        return FILTERED_DATA

        #return 0
    def post(self):
        dane = request.form.to_dict()
        dane_json = request.json
        global DATA
        
        if dane_json:   
            DATA.append(dane_json)
            print(dane_json)
            print("|||||||")
        
        if bool(dane) != False:
            for key in dane.keys():
                d1 = {key: int(dane[key])}
                dane.update(d1)
            d = {"Config": dane}
            DATA.append(d)
        
        #DATA.append(dane)
        print(dane , "|", dane_json)
        print("___________________________________________")

        return DATA[-1], 200

api.add_resource(Filter, '/')

if __name__ == '__main__':
    app.run(debug=True, port = 2500)