import requests
from flask import Flask, request, render_template, make_response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

DATA = []
kursy = []
urodzenia = []
powietrza = []
parkingi = []
podatki = []
CONFIGURATION = [0, 0, 0, 0, 0]
weird_current = float(0.0)


def change_comma(string):
    for i, letter in enumerate(string):
        if letter == ',':
            pre = string[:i]
            pos = string[i+1:]
            new = pre + "." + pos
            return float(new)

    return float(string)

def weird_function(config):
    weird = 0
    global weird_current

    for i,c in enumerate(config):
        if int(c) == 0:
            CONFIGURATION[i] = 0
        else:
            CONFIGURATION[i] = 1

    if len(kursy) > 0 and CONFIGURATION[0] == 1:
        for kurs in kursy:
            weird += 2*kurs
            kursy.remove(kurs)
    if len(urodzenia) > 0 and CONFIGURATION[1] == 1:
        for urodzenie in urodzenia:
            weird += 1*urodzenie
            urodzenia.remove(urodzenie)
    if len(powietrza) > 0 and CONFIGURATION[2] == 1:
        for powietrze in powietrza:
            weird += 3*powietrze
            powietrza.remove(powietrze)
    if len(parkingi) > 0 and CONFIGURATION[3] == 1:
        for parking in parkingi:
            weird += 0.15*parking
            parkingi.remove(parking)
    if len(podatki) > 0 and CONFIGURATION[4] == 1:
        for podatek in podatki:
            weird += 0.07*podatek
            podatki.remove(podatek)
        
    weird_current += weird
            
    return weird
    
'''
      input {
	      padding: 1%;
	      margin-left: 10%;
	      margin-right: 10%;
	      min-width: 80%;
	      background-color: rgb(0, 253, 194);
        border: 5px solid rgb(60, 12, 172);
      }
'''
    
class Aggregator(Resource):
    def get(self):
        config = []
        for d in DATA:
            if "Config" in d.keys():
                config = []
                for k in d["Config"].keys():
                    value = d["Config"][k]
                    config.append(int(value))
 
            else:
                id = int(d["sensor"])
                #print(id)
                if id == 1:
                    kurs = d["report"]["Otwarcie"]
                    kurs = change_comma(kurs)
                    kursy.append(kurs)
                    print(kurs)
                elif id == 2:
                    urodzenie = d["report"]["urodzenia_ogolem"]
                    urodzenie = change_comma(urodzenie)
                    urodzenia.append(urodzenie)
                elif id == 3:
                    podatek = d["report"]["Podatek od gier (tys zl)"]
                    podatek = change_comma(podatek)
                    podatki.append(podatek)
                elif id == 4:
                    parking = d["report"]["pojazdystring"]
                    parking = change_comma(parking)
                    parkingi.append(parking)
                elif id == 5:
                    pm = d["report"]["pm"]
                    pm = change_comma(pm)
                    powietrza.append(pm)
            
        if config:
            weird = weird_function(config)
        else:
            config2 = [0]
            weird = weird_function(config2)
        #return weird
        
        #for d in DATA:
        #    print(d)
        print("_______________________")
        print(CONFIGURATION)
        print("_______________________")
        #weird = 0
        return make_response(render_template("agregator.html", content=weird), 200)
    
    def post(self):
        dane = request.form.to_dict()
        dane_json = request.json
        if dane_json:   
            DATA.append(dane_json)
            url = 'http://127.0.0.1:2500'
            requests.post(url, json = dane_json )
            
            url1 = "http://127.0.0.1:2600"
            requests.post(url1, json = dane_json)
            print("WYSLANO")

        
        
        if bool(dane) != False:
            d = {"Config": dane}
            DATA.append(d)
        #DATA.append(dane)
        print(dane , "|", dane_json)
        print("___________________________________________")

        return DATA[-1], 200
    


api.add_resource(Aggregator, '/')

if __name__ == '__main__':
    app.run(debug=True, port = 2222)
