#inportando bibliotecas flask, pyrebase e request(para request do frontend) 
from flask import Flask
from flask_cors import CORS
import pyrebase
import requests

#fzndo o cálculo do retorno do dinheiro
def calc(valor,tipo):
     valor = int(valor)
     tipo = int(tipo)
     if tipo == 0:
          return valor*1.05
     elif tipo == 1:
          return valor*1.1
     elif tipo == 2:
          return valor*1.2
#configuração do Banco de dados do firebase
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
#inicializando o firebase
firebase = pyrebase.initialize_app(config)
#passando db como referência ao database di firebase
db  = firebase.database()
#criando a página web
app = Flask(__name__)
CORS(app)

#rota inicio mostrando uma página com backent test
@app.route("/", methods=['GET'])
def index():
    return "Backend test"
#rota insert para inserir dados no database
@app.route("/insert/", methods=['POST','GET'])
def insert():
     #r = requests.get('https://localhost:5000/give/')
     #pega informações em formato json do frontend e adiciona no database 
     #não consegui implementar o front, então aq tem dado 01
     r = {"01": {
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
     },"02": {
    "Fim": "23/04/2013", 
    "Inicio": "15/03/2012", 
    "Nome_Proj": "lolzinho", 
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
     #enviando o projeto para o database
     db.child("Projects").update(r)
     #retornando para a webpage confirmando q foi enviado
     return "enviado"

#rota para modificar o database
@app.route("/modify/", methods=['POST','GET'])
def modify():
     #front envia json modificado e dou update com o json
     #aqui eu modifico de acordo com o json enviado e envio pro database
     #json 'recebido' pelo frontend
     json= {"01": {
    "Fim": "29/04/2013", 
    "Inicio": "15/03/2012", 
    "Nome_Proj": "Maruka43", 
    "Participantes": {
      "01": {
        "Email": "fafaalgo@gmail", 
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
     #aqui envio a atualização
     db.child("Projects").update(json)
#aqui é uma rota que lista todos os projetos
@app.route("/give/", methods=['GET'])
def give():
     users = {}
     #um método pra requisitar os dados do local  "/project/" do firebase 
     users = db.child("Projects").get()
     #retornando para a página em formato de string
     return users.val()
#exclui o projeto solicitado
@app.route("/exclude/", methods=['GET','POST'])
def exclude():
     #front passa o número do projeto a ser excluido("Listagem mostrando tudo, selecionado só me envia número")
     #aqui eu passo o projeto numero 02
     numero_proj = "02"
     #método para retirar o projeto
     db.child("Projects").child(numero_proj).remove()
     
#envia para a página web o lucro + o dinheiro investido     
@app.route("/calculate/", methods = ['GET','POST'])
def calculate():
     #front passa o número do projeto para se fazer o cálculo
     #faço o calculo do projeto 1
     num_proj = "01"
     #pego as informações necessárias do projeto
     valor = db.child("Projects").child(num_proj).child("Valor").get()
     tipo = db.child("Projects").child(num_proj).child("Risco").get()
          
     #chamo a função calc para fzr o cálculo do valor
     valor = calc(valor.val(),tipo.val())
     #retorno um dicionário 
     i = {"renda":valor}
     return i


if __name__ == '__main__':
    app.run(debug=True)
