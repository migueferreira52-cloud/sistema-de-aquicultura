import sqlite3
from pathlib import Path
from models import Especie, Tanque, Fornecedor, Funcionario, Cliente, Equipamento, Lote, Alimentacao, RegistroAlimentacao, QualidadeAgua, Tratamento, Mortalidade, Manutencao, Venda, ItemVenda

BANCO = Path(__file__).resolve().parent.parent / "banco" / "aquicultura.db"

CADASTROS = {
    "especies": (Especie, ['nome_comum', 'nome_cientifico', 'tipo', 'temperatura', 'ph', 'observacoes']),
    "tanques": (Tanque, ['identificacao', 'tipo', 'volume', 'profundidade', 'status', 'localizacao']),
    "fornecedores": (Fornecedor, ['razao_social', 'tipo_documento', 'documento', 'tipo_contato', 'contato', 'tipo_insumo', 'endereco', 'observacoes']),
    "funcionarios": (Funcionario, ['nome', 'cpf', 'cargo', 'telefone', 'email', 'situacao', 'observacoes']),
    "clientes": (Cliente, ['nome']),
    "equipamentos": (Equipamento, ['nome', 'tanque_id']),
    "lotes": (Lote, ['codigo', 'especie_id', 'tanque_id', 'data_alojamento', 'quantidade', 'peso_medio', 'origem', 'observacoes', 'fornecedor_id']),
    "alimentacao": (Alimentacao, ['lote_id', 'racao', 'percentual_biomassa', 'frequencia', 'observacoes']),
    "registro_alimentacao": (RegistroAlimentacao, ['data', 'alimentacao_id', 'quantidade', 'horario', 'observacoes', 'funcionario_id']),
    "qualidade_agua": (QualidadeAgua, ['datahora', 'tanque_id', 'temperatura', 'ph', 'oxigenio', 'amonia', 'nitrito', 'nitrato', 'observacoes', 'funcionario_id']),
    "tratamentos": (Tratamento, ['data', 'lote_id', 'diagnostico', 'medicamento', 'dosagem', 'duracao', 'carencia', 'funcionario_id', 'observacoes']),
    "mortalidade": (Mortalidade, ['data', 'lote_id', 'quantidade', 'suspeita', 'destinacao', 'observacoes', 'funcionario_id']),
    "manutencoes": (Manutencao, ['data', 'tanque_id', 'tipo', 'descricao', 'custo', 'funcionario_id', 'proxima_manutencao', 'equipamento_id']),
    "vendas": (Venda, ['data', 'cliente_id', 'documento', 'observacoes']),
    "itens_venda": (ItemVenda, ['venda_id', 'lote_id', 'quantidade', 'unidade', 'preco']),
}

# Um DAO compartilhado evita repetir o mesmo CRUD 15 vezes.
class CadastroDAO:
    def __init__(self, tabela):
        self.tabela = tabela
        self.classe, self.campos = CADASTROS[tabela]

    def buscar_todos(self):
        with sqlite3.connect(BANCO) as conexao:
            cursor = conexao.cursor()
            cursor.execute(f"SELECT id, {', '.join(self.campos)} FROM {self.tabela} ORDER BY id")
            return [self.classe(*linha) for linha in cursor.fetchall()]

    def inserir(self, objeto):
        dados = objeto.to_dict()
        valores = [dados[campo] for campo in self.campos]
        marcadores = ', '.join(['?'] * len(self.campos))
        with sqlite3.connect(BANCO) as conexao:
            cursor = conexao.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute(f"INSERT INTO {self.tabela} ({', '.join(self.campos)}) VALUES ({marcadores})", valores)
            conexao.commit()
            return cursor.lastrowid

    def atualizar(self, id_registro, objeto):
        dados = objeto.to_dict()
        valores = [dados[campo] for campo in self.campos] + [id_registro]
        colunas = ', '.join([campo + '=?' for campo in self.campos])
        with sqlite3.connect(BANCO) as conexao:
            cursor = conexao.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute(f"UPDATE {self.tabela} SET {colunas} WHERE id=?", valores)
            conexao.commit()
            return cursor.rowcount

    def remover(self, id_registro):
        with sqlite3.connect(BANCO) as conexao:
            cursor = conexao.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute(f"DELETE FROM {self.tabela} WHERE id=?", (id_registro,))
            conexao.commit()
            return cursor.rowcount


def criar_banco():
    with sqlite3.connect(BANCO) as conexao:
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        with open(BANCO.parent / "modelo_fisico.sql", encoding="utf-8") as arquivo:
            cursor.executescript(arquivo.read())
        conexao.commit()
