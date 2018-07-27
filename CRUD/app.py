#!/usr/bin/python
# *-* coding: UTF-8 *-*

from flask import Flask, render_template, request, url_for, redirect, jsonify

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

db = SQLAlchemy(app)


class Banco(db.Model):
    __tablename__ = "estoque"

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    marca = db.Column(db.String)
    quantidade = db.Column(db.String)
    dataEntrada = db.Column(db.String)
    dataSaida = db.Column(db.String)
    observacao = db.Column(db.String)

    def __init__(self, nome, marca, quantidade, dataEntrada, dataSaida, observacao):
        self.nome = nome.upper()
        self.marca = marca.upper()
        self.quantidade = quantidade
        self.dataEntrada = dataEntrada
        self.dataSaida = dataSaida
        self.observacao = observacao


db.create_all()


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        marca = request.form.get("marca")
        quantidade = request.form.get("quantidade")
        dataEntrada = request.form.get("dataEntrada")
        dataSaida = request.form.get("dataSaida")
        observacao = request.form.get("observacao")

        if nome and marca and quantidade and dataEntrada and dataSaida and observacao:
            p = Banco(nome, marca, quantidade, dataEntrada, dataSaida, observacao)
            db.session.add(p)
            db.session.commit()

    return redirect(url_for("index"))


@app.route("/lista")
def lista():
    equip = Banco.query.all()
    return render_template("lista.html", equip=equip)

'''
@app.route("/busca")
def buscar():
    #pessoa = Banco.query.filter_by(id=id).first()
    pessoas = Banco.query.limit(1).all()
    return render_template('busca.html', pessoas=pessoas)
'''


@app.route("/busca")
def buscar():
    equip = Banco.query.all()

    return render_template('busca.html', equip=equip)


@app.route("/excluir/<int:id>")
def excluir(id):
    tab = Banco.query.filter_by(_id=id).first()

    db.session.delete(tab)
    db.session.commit()

    equip = Banco.query.all()
    return render_template("lista.html", equip=equip)


@app.route("/atualizar/<int:id>", methods=["GET", "POST"])
def atualizar(id):
    pessoa = Banco.query.filter_by(_id=id).first()

    if request.method == "POST":
        nome = request.form.get("nome")
        marca = request.form.get("marca")
        quantidade = request.form.get("quantidade")
        dataEntrada = request.form.get("dataEntrada")
        dataSaida = request.form.get("dataSaida")
        observacao = request.form.get("observacao")

        if nome and marca and quantidade and dataEntrada and dataSaida and observacao:
            pessoa.nome = nome
            pessoa.marca = marca
            pessoa.quantidade = quantidade
            pessoa.dataEntrada = dataEntrada
            pessoa.dataSaida = dataSaida
            pessoa.observacao = observacao

            db.session.commit()
        return redirect(url_for("lista"))

    return render_template("atualizar.html", pessoa=pessoa)


if __name__ == "__main__":
    app.run(debug=True)
