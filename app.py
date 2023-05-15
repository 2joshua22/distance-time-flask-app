from flask import Flask,render_template,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
import requests
import confidential

app=Flask(__name__)
app.config["SECRET_KEY"]=confidential.SECRET_KEY

class DmForm(FlaskForm):
    destination=StringField("Destination: ",validators=[DataRequired()])
    origin=StringField("Origin: ",validators=[DataRequired()])
    submit=SubmitField("Go")

@app.route('/',methods=["GET","POST"])
def index():
    form=DmForm()
    data=[]
    if form.validate_on_submit():
        destination=form.destination.data
        origin=form.origin.data
        url="https://maps.googleapis.com/maps/api/distancematrix/json?destinations={}&origins={}&key={}".format(destination,origin,confidential.key)
        response=requests.get(url)
        distance=response.json()["rows"][0]["elements"][0]["distance"]["text"]
        duration=response.json()["rows"][0]["elements"][0]["duration"]["text"]
        destination_addresses=str(response.json()["destination_addresses"])
        origin_addresses=str(response.json()["origin_addresses"])
        data=[distance,duration,destination_addresses,origin_addresses]
    return render_template('home.html',Data=data,Form=form)

if __name__=="__main__":
    app.run(debug=True)


