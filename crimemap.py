# -*- coding: utf-8 -*-
from dbhelper import DBHelper
from flask import Flask
from flask import render_template
from flask import request
from flask import Response
import json
import datetime
import dateparser
import string

app = Flask(__name__)
DB = DBHelper()
categories = ['break-in','mugging']

@app.route("/submitcrime",methods=['POST'])
def submitcrime():
  category = request.form.get('category')
  if category not in categories:
    return home()
  date = format_date(request.form.get('date'))
  if not date:
    return home("Invalid date. Please use yyyy-mm-dd format")
  try:
    latitude = float(request.form.get('latitude'))
    longitude = float(request.form.get('longitude'))
  except ValueError:
    return home()
  description = sanitize_string(request.form.get('description'))
  DB.add_crime(category,date,latitude,longitude,description)
  return home()

@app.route("/")
def home(error_message=None):
  crimes=DB.get_all_crimes()
  distance=DB.get_distance()
  crimes = json.dumps(crimes, encoding='latin1')
  distance = json.dumps(distance)

  return render_template("home.html",crimes=crimes,
            categories=categories, error_message=error_message, distance=distance
                        )
 
@app.route("/dist/<int(min=0,max=9):point>/<int(min=0,max=9):ide>")
def get_distancia_entre(point,ide,error_message=None):
  crimes=DB.get_all_crimes()
  distancia=DB.get_distancia(point,ide)
  crimes = json.dumps(crimes, encoding='latin1')
  distancia = json.dumps(distancia)
  return render_template("home.html",crimes=crimes,
       categories=categories, error_message=error_message, distance=distancia
   )

@app.route("/all")
def get_todos():
  crimes=DB.get_all_crimenes()
  crimes = json.dumps(crimes, encoding='latin1')
  return Response(crimes, mimetype='application/json')

@app.route("/add", methods=["POST"])
def add():
  try:
    data=request.form.get('userinput')
    DB.add_input(data)
  except Exception as e:
    print e
  return home()

@app.route("/clear")
def clear():
  try:
    DB.clear_all()
  except Exception as e:
    print e
  return home()

def format_date(userdate):
  date = dateparser.parse(userdate)
  try:
    return datetime.datetime.strftime(date,"%Y-%m-%d")
  except TypeError:
    return None

def sanitize_string(userinput):
  whitelist = string.letters + string.digits + " !?$.,;:-'()&"
  return filter(lambda x: x in whitelist, userinput)

if __name__ == '__main__':
  app.run(port=5300, debug=True)
