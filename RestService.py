from flask import Flask,jsonify,render_template
from flask_cors import CORS
import json
import pyrebase
import requests
def calc(valor,tipo):
     valor = int(valor)
     tipo = int(tipo)
     if tipo == 0:
          return valor*1.05
     elif tipo == 1:
          return valor*1.1
     elif tipo == 2:
          return valor*1.2

config = {

    "apiKey": "AIzaSyCEkejICo7JdPuQUfMJ0HjFnD5MdOlTDYc",
    "authDomain": "mypython-61b1b.firebaseapp.com",
    "databaseURL": "https://mypython-61b1b-default-rtdb.firebaseio.com",
    "projectId": "mypython-61b1b",
    "storageBucket": "mypython-61b1b.appspot.com",
    "messagingSenderId": "480867784563",
    "appId": "1:480867784563:web:929d8071290c400681d706",
    "measurementId": "G-FSYTV6ZCQ5"

}
firebase = pyrebase.initialize_app(config)
db  = firebase.database()

app = Flask(__name__)
CORS(app)


@app.route("/", methods=['GET'])
def index():
    return "Backend test"

@app.route("/insert/", methods=['POST','GET'])
def insert():
     #r = requests.get('https://localhost:5000/give/')
     #pega informações em formato json do front e adiciona no database 
     #
     r = {"02": {
    "Fim": "23/04/2013", 
    "Inicio": "15/03/2012", 
    "Nome_Proj": "Mar", 
    "Participantes": {
      "01": {
        "Email": "algo@gmail", 
        "Idade": 18, 
        "Nome": "Marianne"
      }, 
      "02": {
        "Email": "algo2@gmail", 
        "Idade": 41, 
        "Nome": "Rodrigo"
      }
     },
     "Risco": 2, 
     "Valor": 50000
     }}
     db.child("Projects").update(r)
     return "enviado"

@app.route("/modify/", methods=['POST','GET'])
def modify():
     #front envia json modificado e dou update com o json
     json = {"01": {
    "Fim": "26/04/2013", 
    "Inicio": "15/03/2012", 
    "Nome_Proj": "Maruka", 
    "Participantes": {
      "01": {
        "Email": "algo@gmail", 
        "Idade": 18, 
        "Nome": "Marianne"
      }, 
      "02": {
        "Email": "algo2@gmail", 
        "Idade": 41, 
        "Nome": "Rodrigo"
      }
     },
     "Risco": 2, 
     "Valor": 50000
     }}
     db.child("Projects").update(json)

@app.route("/give/", methods=['GET'])
def give():
     users = {}
     users = db.child("Projects").get()
     return users.val()

@app.route("/exclude/", methods=['GET','POST'])
def exclude():
     #front passa o número do projeto a ser excluido("Listagem mostrando tudo, selecionado só me envia número")
     #ex
     numero_proj = "02"
     db.child("Projects").child(numero_proj).remove()
@app.route("/calculate/", methods = ['GET','POST'])
def calculate():
     #front passa o número do projeto para se fazer o cálculo
     num_proj = "01"
     valor = db.child("Projects").child(num_proj).child("Valor").get()
     tipo = db.child("Projects").child(num_proj).child("Risco").get()
     
     
     valor = calc(valor.val(),tipo.val())
     i = {"renda":valor}
     return i
if __name__ == '__main__':
    app.run(debug=True)
