from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__) #decorators

@app.route('/', methods = ["POST", "GET"])

def render():
   return render_template("main.html")

def submit():
   if request.method == "GET":
      return render_template("submit.html")
   else:   
      message = request.form["message"]
      name = request.form["name"]

def get_message_db():
  # write some helpful comments here
  try:
     return g.message_db
  except:
     g.message_db = sqlite3.connect("messages_db.sqlite")
     cmd = '' # replace this with your SQL query
     cursor = g.message_db.cursor()
     cursor.execute(cmd)
     return g.message_db