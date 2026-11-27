from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
from dao import CadastroDAO, CADASTROS, criar_banco
import sqlite3

app = Flask(__name__, static_folder=None)
PASTA = Path(__file__).resolve().parent.parent


@app.route("/")
@app.route("/index.html")
def inicio():
    return send_from_directory(PASTA, "index.html")


@app.route("/paginas/<arquivo>")
def pagina(arquivo):
    return send_from_directory(PASTA / "paginas", arquivo)


@app.route("/css/style.css")
def estilo():
    return send_from_directory(PASTA / "css", "style.css")


@app.route("/js/script.js")
def javascript():
    return send_from_directory(PASTA / "js", "script.js")


@app.route("/api/<tabela>", methods=["GET"])
def listar(tabela):
    if tabela not in CADASTROS:
        return jsonify({"erro": "Cadastro não encontrado."}), 404
    dao = CadastroDAO(tabela)
    return jsonify([objeto.to_dict() for objeto in dao.buscar_todos()])


def montar_objeto(dao, id_registro):
    dados = request.json
    valores = []
    for campo in dao.campos:
        valor = dados.get(campo)
        if valor == "":
            valor = None
        valores.append(valor)
    return dao.classe(id_registro, *valores)


@app.route("/api/<tabela>", methods=["POST"])
def cadastrar(tabela):
    if tabela not in CADASTROS:
        return jsonify({"erro": "Cadastro não encontrado."}), 404
    dao = CadastroDAO(tabela)
    try:
        codigo = dao.inserir(montar_objeto(dao, None))
        return jsonify({"id": codigo, "mensagem": "Cadastro realizado!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"erro": "Confira os campos obrigatórios, valores e vínculos."}), 400


@app.route("/api/<tabela>/<int:id_registro>", methods=["PUT"])
def editar(tabela, id_registro):
    if tabela not in CADASTROS:
        return jsonify({"erro": "Cadastro não encontrado."}), 404
    dao = CadastroDAO(tabela)
    try:
        if dao.atualizar(id_registro, montar_objeto(dao, id_registro)) == 0:
            return jsonify({"erro": "Registro não encontrado."}), 404
        return jsonify({"mensagem": "Registro atualizado!"})
    except sqlite3.IntegrityError:
        return jsonify({"erro": "Confira os campos obrigatórios, valores e vínculos."}), 400


@app.route("/api/<tabela>/<int:id_registro>", methods=["DELETE"])
def excluir(tabela, id_registro):
    if tabela not in CADASTROS:
        return jsonify({"erro": "Cadastro não encontrado."}), 404
    dao = CadastroDAO(tabela)
    try:
        if dao.remover(id_registro) == 0:
            return jsonify({"erro": "Registro não encontrado."}), 404
        return jsonify({"mensagem": "Registro excluído!"})
    except sqlite3.IntegrityError:
        return jsonify({"erro": "Este registro está vinculado a outro cadastro."}), 400


if __name__ == "__main__":
    criar_banco()
    app.run()
