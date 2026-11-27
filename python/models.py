# Cada classe representa uma entidade do banco.

class Especie:
    def __init__(self, id, nome_comum, nome_cientifico, tipo, temperatura, ph, observacoes):
        self.id = id
        self.nome_comum = nome_comum
        self.nome_cientifico = nome_cientifico
        self.tipo = tipo
        self.temperatura = temperatura
        self.ph = ph
        self.observacoes = observacoes

    def to_dict(self):
        return {
            "id": self.id,
            "nome_comum": self.nome_comum,
            "nome_cientifico": self.nome_cientifico,
            "tipo": self.tipo,
            "temperatura": self.temperatura,
            "ph": self.ph,
            "observacoes": self.observacoes,
        }


class Tanque:
    def __init__(self, id, identificacao, tipo, volume, profundidade, status, localizacao):
        self.id = id
        self.identificacao = identificacao
        self.tipo = tipo
        self.volume = volume
        self.profundidade = profundidade
        self.status = status
        self.localizacao = localizacao

    def to_dict(self):
        return {
            "id": self.id,
            "identificacao": self.identificacao,
            "tipo": self.tipo,
            "volume": self.volume,
            "profundidade": self.profundidade,
            "status": self.status,
            "localizacao": self.localizacao,
        }


class Fornecedor:
    def __init__(self, id, razao_social, tipo_documento, documento, tipo_contato, contato, tipo_insumo, endereco, observacoes):
        self.id = id
        self.razao_social = razao_social
        self.tipo_documento = tipo_documento
        self.documento = documento
        self.tipo_contato = tipo_contato
        self.contato = contato
        self.tipo_insumo = tipo_insumo
        self.endereco = endereco
        self.observacoes = observacoes

    def to_dict(self):
        return {
            "id": self.id,
            "razao_social": self.razao_social,
            "tipo_documento": self.tipo_documento,
            "documento": self.documento,
            "tipo_contato": self.tipo_contato,
            "contato": self.contato,
            "tipo_insumo": self.tipo_insumo,
            "endereco": self.endereco,
            "observacoes": self.observacoes,
        }


class Funcionario:
    def __init__(self, id, nome, cpf, cargo, telefone, email, situacao, observacoes):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.cargo = cargo
        self.telefone = telefone
        self.email = email
        self.situacao = situacao
        self.observacoes = observacoes

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "cargo": self.cargo,
            "telefone": self.telefone,
            "email": self.email,
            "situacao": self.situacao,
            "observacoes": self.observacoes,
        }


class Cliente:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
        }


class Equipamento:
    def __init__(self, id, nome, tanque_id):
        self.id = id
        self.nome = nome
        self.tanque_id = tanque_id

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "tanque_id": self.tanque_id,
        }


class Lote:
    def __init__(self, id, codigo, especie_id, tanque_id, data_alojamento, quantidade, peso_medio, origem, observacoes, fornecedor_id):
        self.id = id
        self.codigo = codigo
        self.especie_id = especie_id
        self.tanque_id = tanque_id
        self.data_alojamento = data_alojamento
        self.quantidade = quantidade
        self.peso_medio = peso_medio
        self.origem = origem
        self.observacoes = observacoes
        self.fornecedor_id = fornecedor_id

    def to_dict(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "especie_id": self.especie_id,
            "tanque_id": self.tanque_id,
            "data_alojamento": self.data_alojamento,
            "quantidade": self.quantidade,
            "peso_medio": self.peso_medio,
            "origem": self.origem,
            "observacoes": self.observacoes,
            "fornecedor_id": self.fornecedor_id,
        }


class Alimentacao:
    def __init__(self, id, lote_id, racao, percentual_biomassa, frequencia, observacoes):
        self.id = id
        self.lote_id = lote_id
        self.racao = racao
        self.percentual_biomassa = percentual_biomassa
        self.frequencia = frequencia
        self.observacoes = observacoes

    def to_dict(self):
        return {
            "id": self.id,
            "lote_id": self.lote_id,
            "racao": self.racao,
            "percentual_biomassa": self.percentual_biomassa,
            "frequencia": self.frequencia,
            "observacoes": self.observacoes,
        }


class RegistroAlimentacao:
    def __init__(self, id, data, alimentacao_id, quantidade, horario, observacoes, funcionario_id):
        self.id = id
        self.data = data
        self.alimentacao_id = alimentacao_id
        self.quantidade = quantidade
        self.horario = horario
        self.observacoes = observacoes
        self.funcionario_id = funcionario_id

    def to_dict(self):
        return {
            "id": self.id,
            "data": self.data,
            "alimentacao_id": self.alimentacao_id,
            "quantidade": self.quantidade,
            "horario": self.horario,
            "observacoes": self.observacoes,
            "funcionario_id": self.funcionario_id,
        }


class QualidadeAgua:
    def __init__(self, id, datahora, tanque_id, temperatura, ph, oxigenio, amonia, nitrito, nitrato, observacoes, funcionario_id):
        self.id = id
        self.datahora = datahora
        self.tanque_id = tanque_id
        self.temperatura = temperatura
        self.ph = ph
        self.oxigenio = oxigenio
        self.amonia = amonia
        self.nitrito = nitrito
        self.nitrato = nitrato
        self.observacoes = observacoes
        self.funcionario_id = funcionario_id

    def to_dict(self):
        return {
            "id": self.id,
            "datahora": self.datahora,
            "tanque_id": self.tanque_id,
            "temperatura": self.temperatura,
            "ph": self.ph,
            "oxigenio": self.oxigenio,
            "amonia": self.amonia,
            "nitrito": self.nitrito,
            "nitrato": self.nitrato,
            "observacoes": self.observacoes,
            "funcionario_id": self.funcionario_id,
        }


class Tratamento:
    def __init__(self, id, data, lote_id, diagnostico, medicamento, dosagem, duracao, carencia, funcionario_id, observacoes):
        self.id = id
        self.data = data
        self.lote_id = lote_id
        self.diagnostico = diagnostico
        self.medicamento = medicamento
        self.dosagem = dosagem
        self.duracao = duracao
        self.carencia = carencia
        self.funcionario_id = funcionario_id
        self.observacoes = observacoes

    def to_dict(self):
        return {
            "id": self.id,
            "data": self.data,
            "lote_id": self.lote_id,
            "diagnostico": self.diagnostico,
            "medicamento": self.medicamento,
            "dosagem": self.dosagem,
            "duracao": self.duracao,
            "carencia": self.carencia,
            "funcionario_id": self.funcionario_id,
            "observacoes": self.observacoes,
        }


class Mortalidade:
    def __init__(self, id, data, lote_id, quantidade, suspeita, destinacao, observacoes, funcionario_id):
        self.id = id
        self.data = data
        self.lote_id = lote_id
        self.quantidade = quantidade
        self.suspeita = suspeita
        self.destinacao = destinacao
        self.observacoes = observacoes
        self.funcionario_id = funcionario_id

    def to_dict(self):
        return {
            "id": self.id,
            "data": self.data,
            "lote_id": self.lote_id,
            "quantidade": self.quantidade,
            "suspeita": self.suspeita,
            "destinacao": self.destinacao,
            "observacoes": self.observacoes,
            "funcionario_id": self.funcionario_id,
        }


class Manutencao:
    def __init__(self, id, data, tanque_id, tipo, descricao, custo, funcionario_id, proxima_manutencao, equipamento_id):
        self.id = id
        self.data = data
        self.tanque_id = tanque_id
        self.tipo = tipo
        self.descricao = descricao
        self.custo = custo
        self.funcionario_id = funcionario_id
        self.proxima_manutencao = proxima_manutencao
        self.equipamento_id = equipamento_id

    def to_dict(self):
        return {
            "id": self.id,
            "data": self.data,
            "tanque_id": self.tanque_id,
            "tipo": self.tipo,
            "descricao": self.descricao,
            "custo": self.custo,
            "funcionario_id": self.funcionario_id,
            "proxima_manutencao": self.proxima_manutencao,
            "equipamento_id": self.equipamento_id,
        }


class Venda:
    def __init__(self, id, data, cliente_id, documento, observacoes):
        self.id = id
        self.data = data
        self.cliente_id = cliente_id
        self.documento = documento
        self.observacoes = observacoes

    def to_dict(self):
        return {
            "id": self.id,
            "data": self.data,
            "cliente_id": self.cliente_id,
            "documento": self.documento,
            "observacoes": self.observacoes,
        }


class ItemVenda:
    def __init__(self, id, venda_id, lote_id, quantidade, unidade, preco):
        self.id = id
        self.venda_id = venda_id
        self.lote_id = lote_id
        self.quantidade = quantidade
        self.unidade = unidade
        self.preco = preco

    def to_dict(self):
        return {
            "id": self.id,
            "venda_id": self.venda_id,
            "lote_id": self.lote_id,
            "quantidade": self.quantidade,
            "unidade": self.unidade,
            "preco": self.preco,
        }

