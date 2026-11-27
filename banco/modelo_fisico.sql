-- Estrutura SQLite do projeto Aquicultura.
CREATE TABLE IF NOT EXISTS especies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_comum TEXT NOT NULL,
    nome_cientifico TEXT,
    tipo TEXT,
    temperatura REAL CHECK (temperatura >= 0),
    ph REAL CHECK (ph >= 0 AND ph <= 14),
    observacoes TEXT
);

CREATE TABLE IF NOT EXISTS tanques (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    identificacao TEXT NOT NULL UNIQUE,
    tipo TEXT,
    volume REAL CHECK (volume >= 0),
    profundidade REAL CHECK (profundidade >= 0),
    status TEXT,
    localizacao TEXT
);

CREATE TABLE IF NOT EXISTS fornecedores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    razao_social TEXT NOT NULL,
    tipo_documento TEXT NOT NULL,
    documento TEXT NOT NULL UNIQUE,
    tipo_contato TEXT NOT NULL,
    contato TEXT NOT NULL,
    tipo_insumo TEXT,
    endereco TEXT,
    observacoes TEXT
);

CREATE TABLE IF NOT EXISTS funcionarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL UNIQUE,
    cargo TEXT,
    telefone TEXT,
    email TEXT,
    situacao TEXT NOT NULL,
    observacoes TEXT
);

CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS equipamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    tanque_id INTEGER,
    FOREIGN KEY (tanque_id) REFERENCES tanques(id)
);

CREATE TABLE IF NOT EXISTS lotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    especie_id INTEGER NOT NULL,
    tanque_id INTEGER NOT NULL,
    data_alojamento TEXT NOT NULL,
    quantidade INTEGER NOT NULL CHECK (quantidade >= 1),
    peso_medio REAL CHECK (peso_medio >= 0),
    origem TEXT,
    observacoes TEXT,
    fornecedor_id INTEGER,
    FOREIGN KEY (especie_id) REFERENCES especies(id),
    FOREIGN KEY (tanque_id) REFERENCES tanques(id),
    FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id)
);

CREATE TABLE IF NOT EXISTS alimentacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lote_id INTEGER NOT NULL,
    racao TEXT NOT NULL,
    percentual_biomassa REAL NOT NULL CHECK (percentual_biomassa >= 0.1 AND percentual_biomassa <= 10),
    frequencia INTEGER NOT NULL CHECK (frequencia >= 1),
    observacoes TEXT,
    FOREIGN KEY (lote_id) REFERENCES lotes(id)
);

CREATE TABLE IF NOT EXISTS registro_alimentacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    alimentacao_id INTEGER NOT NULL,
    quantidade REAL NOT NULL CHECK (quantidade >= 0.01),
    horario TEXT,
    observacoes TEXT,
    funcionario_id INTEGER,
    FOREIGN KEY (alimentacao_id) REFERENCES alimentacao(id),
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
);

CREATE TABLE IF NOT EXISTS qualidade_agua (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datahora TEXT NOT NULL,
    tanque_id INTEGER NOT NULL,
    temperatura REAL CHECK (temperatura >= 0 AND temperatura <= 40),
    ph REAL CHECK (ph >= 0 AND ph <= 14),
    oxigenio REAL CHECK (oxigenio >= 0),
    amonia REAL CHECK (amonia >= 0),
    nitrito REAL CHECK (nitrito >= 0),
    nitrato REAL CHECK (nitrato >= 0),
    observacoes TEXT,
    funcionario_id INTEGER,
    FOREIGN KEY (tanque_id) REFERENCES tanques(id),
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
);

CREATE TABLE IF NOT EXISTS tratamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    lote_id INTEGER NOT NULL,
    diagnostico TEXT,
    medicamento TEXT,
    dosagem TEXT,
    duracao INTEGER CHECK (duracao >= 1),
    carencia INTEGER CHECK (carencia >= 0),
    funcionario_id INTEGER,
    observacoes TEXT,
    FOREIGN KEY (lote_id) REFERENCES lotes(id),
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
);

CREATE TABLE IF NOT EXISTS mortalidade (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    lote_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL CHECK (quantidade >= 1),
    suspeita TEXT,
    destinacao TEXT,
    observacoes TEXT,
    funcionario_id INTEGER,
    FOREIGN KEY (lote_id) REFERENCES lotes(id),
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
);

CREATE TABLE IF NOT EXISTS manutencoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    tanque_id INTEGER,
    tipo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    custo REAL CHECK (custo >= 0),
    funcionario_id INTEGER,
    proxima_manutencao TEXT,
    equipamento_id INTEGER,
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id),
    FOREIGN KEY (tanque_id) REFERENCES tanques(id),
    FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id),
    CHECK ((tanque_id IS NOT NULL AND equipamento_id IS NULL)
        OR (tanque_id IS NULL AND equipamento_id IS NOT NULL))
);

CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    cliente_id INTEGER NOT NULL,
    documento TEXT NOT NULL,
    observacoes TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE IF NOT EXISTS itens_venda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venda_id INTEGER NOT NULL,
    lote_id INTEGER NOT NULL,
    quantidade REAL NOT NULL CHECK (quantidade >= 0.01),
    unidade TEXT NOT NULL,
    preco REAL NOT NULL CHECK (preco >= 0),
    FOREIGN KEY (venda_id) REFERENCES vendas(id),
    FOREIGN KEY (lote_id) REFERENCES lotes(id)
);


-- CONSULTAS PARA A DISCIPLINA DE BANCO DE DADOS
-- Exemplos comentados para não executar ao iniciar o site.
-- Para praticar, copie uma consulta sem os marcadores de comentário.
-- -- 1. Quais lotes pertencem a cada espécie? (INNER JOIN)
-- SELECT l.codigo, e.nome_comum
-- FROM lotes l
-- INNER JOIN especies e ON l.especie_id = e.id
-- ORDER BY l.id;
--
-- -- 2. Quais clientes compraram? Inclui clientes sem venda. (LEFT JOIN)
-- SELECT c.nome, v.id AS venda
-- FROM clientes c
-- LEFT JOIN vendas v ON c.id = v.cliente_id
-- ORDER BY c.id, v.id;
--
-- -- 3. Quais espécies e tanques estão relacionados aos lotes? (3 tabelas)
-- SELECT l.codigo, e.nome_comum, t.identificacao
-- FROM lotes l
-- JOIN especies e ON l.especie_id = e.id
-- JOIN tanques t ON l.tanque_id = t.id
-- ORDER BY l.id;
--
-- -- 4. Quais lotes têm quantidade acima da média? (subconsulta de valor único)
-- SELECT codigo, quantidade
-- FROM lotes
-- WHERE quantidade > (SELECT AVG(quantidade) FROM lotes)
-- ORDER BY id;
--
-- -- 5. Quais clientes possuem vendas? (subconsulta IN)
-- SELECT nome
-- FROM clientes
-- WHERE id IN (SELECT cliente_id FROM vendas)
-- ORDER BY id;
--
-- -- 6. Qual a segunda página de espécies, com duas por página? (paginação)
-- SELECT id, nome_comum
-- FROM especies
-- ORDER BY id
-- LIMIT 2 OFFSET 2;
--
-- -- 7. Quanto custa cada item e a qual venda pertence? (JOINs e cálculo)
-- SELECT v.id AS venda, c.nome, l.codigo, i.quantidade * i.preco AS valor_item
-- FROM itens_venda i
-- JOIN vendas v ON i.venda_id = v.id
-- JOIN clientes c ON v.cliente_id = c.id
-- JOIN lotes l ON i.lote_id = l.id
-- ORDER BY v.id, i.id;
--
-- -- 8. Consulta de lotes que antes estava na página PHP.
-- SELECT l.codigo, e.nome_comum, t.identificacao, l.quantidade, l.data_alojamento
-- FROM lotes l
-- JOIN especies e ON l.especie_id = e.id
-- JOIN tanques t ON l.tanque_id = t.id
-- ORDER BY l.id DESC;
