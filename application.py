import pickle
from flask import Flask,request,jsonify,render_template
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

application = Flask(__name__)
app=application

##impport ridge regressor and stamndard scaler pickle
redge_model=pickle.load(open("models/linreg.pkl","rb"))
standard_scaler=pickle.load(open("models/scaler.pkl","rb"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method=="POST":
        field_aliases = {
            "Temperature": ("Temperature", "temperature"),
            "RH": ("RH", "rh"),
            "Ws": ("Ws", "ws", "wind_speed"),
            "Rain": ("Rain", "rain"),
            "FFMC": ("FFMC", "ffmc"),
            "DMC": ("DMC", "dmc"),
            "ISI": ("ISI", "isi"),
            "Classes": ("Classes", "classes"),
            "Region": ("Region", "region"),
        }

        values = {
            name: next((request.form.get(alias) for alias in aliases if request.form.get(alias) is not None), None)
            for name, aliases in field_aliases.items()
        }
        missing_fields = [name for name, value in values.items() if value in (None, "")]
        if missing_fields:
            return f"Missing form fields: {', '.join(missing_fields)}", 400

        Temperature=float(values["Temperature"])
        RH=float(values["RH"])
        Ws=float(values["Ws"])
        Rain=float(values["Rain"])
        FFMC=float(values["FFMC"])
        DMC=float(values["DMC"])
        ISI=float(values["ISI"])
        Classes=0 if values["Classes"].strip().lower() == "not fire" else 1
        Region=float(values["Region"])

        prediction_data = pd.DataFrame([{
            "Temperature": Temperature,
            "RH": RH,
            "Ws": Ws,
            "Rain": Rain,
            "FFMC": FFMC,
            "DMC": DMC,
            "ISI": ISI,
            "Classes": Classes,
            "Region": Region,
        }])
        new_data_scaled=standard_scaler.transform(prediction_data)
        result=redge_model.predict(new_data_scaled)

        return render_template('home.html', results=result[0])
        
    else:
         return render_template("home.html", results=None)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5002)