from crypt import methods
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/youtube'

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100))

    def to_json(self):
        return {"id": self.id, "nome": self.nome, "email": self.email}

# db.create_all()

# Selecionar tudo
@app.route("/usuarios", methods=["GET"])
def seleciona_usuarios():
    usuarios_objeto = Usuario.query.all()
    usuarios_json = [usuario.to_json() for usuario in usuarios_objeto]
    print(usuarios_json)
    return gera_response(200, "usuarios", usuarios_json, "sucesso!")

# Selecionar um
@app.route("/usuario/<id>", methods=["GET"])
def seleciona_usuario(id):
    usuario_obj = Usuario.query.filter_by(id=id).first()
    usuario_json = usuario_obj.to_json()
    return gera_response(200, "usuario", usuario_json, "sucesso!")

# Cadastrar
@app.route("/usuario", methods=["POST"])
def cadastra_usuario():
    body = request.get_json()

    try:
        usuario = Usuario(nome=body["nome"], email= body["email"])
        db.session.add(usuario)
        db.session.commit()
        return gera_response(201, "usuario", usuario.to_json(), "criado com sucesso!")
    except Exception as e:
        print(e)
        gera_response(400, "usuario", {}, "Falha ao cadastrar")

# Atualizar
@app.route("/usuario/<id>", methods=["PUT"])
def atualiza_usuario(id):
    usuario_obj = Usuario.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('nome' in body):
            usuario_obj.nome = body["nome"]
        if('email' in body):
            usuario_obj.email = body["email"]

        db.session.add(usuario_obj)
        db.session.commit()
        return gera_response(201, "usuario", usuario_obj.to_json(), "Atualizado com sucesso!")
                
    except Exception as e:
        print(e)
        gera_response(400, "usuario", {}, "Falha ao atualizar")

# Deletar
@app.route("/usuario/<id>", methods=["DELETE"])
def deleta_usuario(id):
    usuario_obj = Usuario.query.filter_by(id=id).first()

    try:
        db.session.delete(usuario_obj)
        db.session.commit()
        return gera_response(201, "usuario", usuario_obj.to_json(), "Deletado com sucesso!")
                
    except Exception as e:
        print(e)
        gera_response(400, "usuario", {}, "Falha ao detelar")

def gera_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")

app.run()
