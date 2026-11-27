from pathlib import Path
from datetime import date, datetime, time, timedelta
from decimal import Decimal, InvalidOperation
from flask import Flask, jsonify, render_template, request, abort, send_from_directory
import pymysql
from campos import CAMPOS

# Localiza a raiz do projeto, mesmo com app.py dentro da pasta python.
RAIZ = Path(__file__).resolve().parent.parent
app = Flask(__name__, template_folder=str(RAIZ), static_folder=None)

# Configuração padrão do MySQL do XAMPP. Altere se necessário.
HOST = '127.0.0.1'
PORTA = 3306
USUARIO = 'root'
SENHA = ''
BANCO = 'aquicultura_escolar'


def conectar():
    return pymysql.connect(host=HOST, port=PORTA, user=USUARIO,
                           password=SENHA, database=BANCO, charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


# DAO: contém apenas as operações de banco de dados.
class CadastroDAO:
    def __init__(self, tabela):
        if tabela not in CAMPOS:
            raise ValueError('Tabela inválida.')
        self.tabela = tabela

    def listar(self):
        conexao = conectar()
        try:
            with conexao.cursor() as cursor:
                cursor.execute(f'SELECT * FROM `{self.tabela}` ORDER BY id DESC')
                return cursor.fetchall()
        finally:
            conexao.close()

    def cadastrar(self, dados):
        campos = list(CAMPOS[self.tabela])
        colunas = ', '.join(f'`{campo}`' for campo in campos)
        marcadores = ', '.join(['%s'] * len(campos))
        sql = f'INSERT INTO `{self.tabela}` ({colunas}) VALUES ({marcadores})'
        valores = [dados[campo] for campo in campos]
        conexao = conectar()
        try:
            with conexao.cursor() as cursor:
                cursor.execute(sql, valores)
                codigo = cursor.lastrowid
            conexao.commit()
            return codigo
        finally:
            conexao.close()


def validar(tabela, dados):
    if not isinstance(dados, dict):
        raise ValueError('Envie os dados do formulário em JSON.')
    resultado = {}
    for nome, regra in CAMPOS[tabela].items():
        valor = dados.get(nome)
        if isinstance(valor, str):
            valor = valor.strip()
        rotulo = regra['label']
        if valor is None or valor == '':
            if regra['required']:
                raise ValueError(f'Preencha: {rotulo}.')
            resultado[nome] = None
            continue
        if not isinstance(valor, (str, int, float)) or isinstance(valor, bool):
            raise ValueError(f'Valor inválido: {rotulo}.')
        tipo = regra['type']
        try:
            if tipo in ('number', 'id'):
                valor = Decimal(str(valor))
                if not valor.is_finite():
                    raise ValueError()
                minimo = Decimal(regra.get('min', '1' if tipo == 'id' else '0'))
                maximo = Decimal(regra.get('max', '2147483647' if tipo == 'id' or regra.get('step') == '1' else '999999999.999'))
                if not minimo <= valor <= maximo:
                    raise ValueError()
                passo = Decimal(regra.get('step', '1'))
                if valor % passo != 0:
                    raise ValueError()
                if tipo == 'id' or passo == 1:
                    valor = int(valor)
            elif tipo == 'date':
                valor = date.fromisoformat(str(valor))
            elif tipo == 'datetime-local':
                valor = datetime.strptime(str(valor), '%Y-%m-%dT%H:%M')
            elif tipo == 'time':
                valor = time.fromisoformat(str(valor))
            else:
                if not isinstance(valor, str):
                    raise ValueError()
                if 'choices' in regra and valor not in regra['choices']:
                    raise ValueError()
                if 'length' in regra and len(valor) > regra['length']:
                    raise ValueError()
                if tipo == 'email' and ('@' not in valor or ' ' in valor):
                    raise ValueError()
        except (ValueError, InvalidOperation, OverflowError):
            raise ValueError(f'Valor inválido: {rotulo}.') from None
        resultado[nome] = valor
    if tabela == 'manutencoes':
        if resultado['tanque_id'] is None and resultado['equipamento_id'] is None:
            raise ValueError('Selecione um tanque ou um equipamento.')
        if resultado['tanque_id'] is not None and resultado['equipamento_id'] is not None:
            raise ValueError('Selecione apenas um tanque ou um equipamento.')
    return resultado


def json_registros(registros):
    # Converte datas e decimais do MySQL para valores que o JavaScript entende.
    for registro in registros:
        for campo, valor in registro.items():
            if isinstance(valor, (datetime, date, time)):
                registro[campo] = valor.isoformat()
            elif isinstance(valor, timedelta):
                registro[campo] = str(valor)
            elif isinstance(valor, Decimal):
                registro[campo] = str(valor)
    return registros


@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/<pagina>.html')
def pagina(pagina):
    permitidas = ['index'] + [t.replace('_', '-') for t in CAMPOS if t not in ('registro_alimentacao', 'itens_venda')]
    if pagina not in permitidas:
        abort(404)
    if pagina == 'index':
        return inicio()
    return render_template('paginas/' + pagina + '.html')


# Disponibiliza apenas os arquivos de estilo e JavaScript.
@app.route('/css/style.css')
def estilo():
    return send_from_directory(str(RAIZ / 'css'), 'style.css')


@app.route('/js/script.js')
def javascript():
    return send_from_directory(str(RAIZ / 'js'), 'script.js')


@app.route('/api/<tabela>', methods=['GET', 'POST'])
def api(tabela):
    if tabela not in CAMPOS:
        return jsonify(erro='Cadastro não encontrado.'), 404
    dao = CadastroDAO(tabela)
    try:
        if request.method == 'GET':
            return jsonify(json_registros(dao.listar()))
        dados = validar(tabela, request.get_json(silent=True))
        codigo = dao.cadastrar(dados)
        return jsonify(mensagem='Cadastro realizado com sucesso!', id=codigo), 201
    except ValueError as erro:
        return jsonify(erro=str(erro)), 400
    except pymysql.err.IntegrityError:
        return jsonify(erro='Registro duplicado ou referência inexistente. Confira os dados.'), 409
    except pymysql.err.DataError:
        return jsonify(erro='Algum dado excede o tamanho permitido.'), 400
    except pymysql.MySQLError:
        app.logger.exception('Erro no banco de dados')
        return jsonify(erro='Não foi possível acessar o banco. Confira o MySQL e o banco.sql.'), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
