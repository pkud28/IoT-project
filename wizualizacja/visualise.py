
from doctest import REPORTING_FLAGS
from math import ulp
from os import umask
import requests
from flask import Flask, request, send_file, make_response, render_template
from flask_restful import Resource, Api
import matplotlib.pyplot as plt
import io

app = Flask(__name__)
api = Api(app)

REPORTS = []
D1_x = []
D1_y = []
D2_x = []
D2_y = []
D3_x = []
D3_y = []
D4_x = []
D4_y = []
D5_x = []
D5_y = []

ID_ = 0

'''
def do_plot():
    global D1, D2, D3, D4, D5
    ids = []

    for data in REPORTS:
        id = data["sensor"]
        if id == 1:
            x = data["report"]["Otwarcie"] 
            y = data["report"]["Data"] 
            d = {"x": x, "y": y} 
            D1_x.append(x)
            D1_y.append(y)
            if ids.count(id) == 0:
                ids.append(id)
        if id == 2:
            x = data["report"]["urodzenia_ogolem"]
            y = data["report"]["Rok"]
            d = {"x": x, "y": y} 
            D2_x.append(x)
            D2_y.append(y)
            if ids.count(id) == 0:
                ids.append(id)
        if id == 3:
            x = data["report"]["Podatek od gier (tys zl)"]
            y = data["report"]["data"]
            d = {"x": x, "y": y} 
            D3_x.append(x)
            D3_y.append(y)
            if ids.count(id) == 0:
                ids.append(id)
        if id == 4:
            x = data["report"]["pojazdystring"]
            y = data["report"]["stringczas"]
            d = {"x": x, "y": y} 
            D4_x.append(x)
            D4_y.append(y)
            if ids.count(id) == 0:
                ids.append(id)
        if id == 5:
            x = data["report"]["pm"]
            y = data["report"]["czas"]
            d = {"x": x, "y": y} 
            D5_x.append(x)
            D5_y.append(y)
            if ids.count(id) == 0:
                ids.append(id)
    
    if len(ids) == 0:
        return False
    else:
        fig, axis = plt.subplots(len(ids), 1, squeeze=False)

        for i in range(0, len(ids)):
            if ids[i] == 1:
                D = {"x": D1_x, "y": D1_y}
            if ids[i] == 2:
                D = {"x": D2_x, "y": D2_y}
            if ids[i] == 3:
                D = {"x": D3_x, "y": D3_y}
            if ids[i] == 4:
                D = {"x": D4_x, "y": D4_y}
            if ids[i] == 5:
                D = {"x": D5_x, "y": D5_y}

            axis[i, 0] = plt.plot(D["y"], D["x"])
            axis[i, 0] = plt.title(ids[i])


    print("------------", ids)
    print()

    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return bytes_image
'''  

def change_comma(string):
    for i, letter in enumerate(string):
        if letter == ',':
            pre = string[:i]
            pos = string[i+1:]
            new = pre + "." + pos
            return float(new)

    return float(string)

class Visualize(Resource):
    def get(self):
        #bytes_obj = do_plot()
        #if bytes_obj == False:
        #    return "NIE"
        global ID_, REPORTS
        x = []
        y = []
        print("IIIIIIIIIIIIIIII", ID_, ",", type(ID_))
     
        u = ""
        for data in REPORTS:
            if data:
                id = data["sensor"]
                if id == ID_:
                    if id == 1:
                        x.append( change_comma(data["report"]["Otwarcie"]))
                        y.append(data["report"]["Data"])
                        print(data["sensor"], ",", type(data["sensor"]))
                        u = "Otwarcie - KURS EURO"
                        
                    if id == 2:
                        x.append(data["report"]["urodzenia_ogolem"])
                        y.append(data["report"]["Rok"])
                        print(data["sensor"], ",", type(data["sensor"]))
                        u = "Urodzenia ogolem"
                    if id == 3:
                        x.append(data["report"]["Podatek od gier (tys zl)"])
                        y.append(data["report"]["data"])
                        print(data["sensor"], ",", type(data["sensor"]))
                        u = "Podatek od gier hazardowych"
                    if id == 4:
                        x.append(data["report"]["pojazdystring"])
                        y.append(data["report"]["stringczas"])
                        print(data["sensor"], ",", type(data["sensor"]))
                        u = "PARKING - wolne miejsca"
                    if id == 5:
                        x.append(data["report"]["pm"])
                        y.append(data["report"]["czas"])
                        print(data["sensor"], ",", type(data["sensor"]))
                        u = "Jakosc powietrza"
        

        #l = ["01-01-2020", "02-01-2020", "03-01-2020"] 
        #v = [1, 2, 3]
        #return make_response(render_template("vis2.html", labels = l, values = v), 200)

        if len(x) == 0 and len(y) == 0:
            return "BRAK DANYCH"
        '''
        return send_file(bytes_obj,
                     attachment_filename='plot.png',
                     mimetype='image/png')
        '''
        #return f"(X: {x}, Y: {y})"

        return make_response(render_template("vis.html", l = y, v = x, topic = u ), 200)

    def post(self):
        global REPORTS, ID_
        #i = request.form["vis"]
        i = request.form.to_dict()
        data = request.json

        print("DODANO:", i, "Y", type(i))
        if i:
            if "vis" in i.keys():
                print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
                ID_ = int(i["vis"])
                print("----", i)
                return i
        if data:
            if data not in REPORTS:
                REPORTS.append(data)
            return REPORTS[-1], 200

        #data = request.json
        return
            
        
        


api.add_resource(Visualize, '/')

if __name__ == '__main__':
    app.run(debug=True, port = 2600)
