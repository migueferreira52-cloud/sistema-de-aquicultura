CREATE DATABASE IF NOT EXISTS aquicultura_escolar;
USE aquicultura_escolar;

CREATE TABLE IF NOT EXISTS especies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome_comum VARCHAR(150) NOT NULL,
    nome_cientifico VARCHAR(150),
    tipo VARCHAR(100),
    temperatura DECIMAL(12,3) CHECK (temperatura >= 0),
    ph DECIMAL(12,3) CHECK (ph >= 0 AND ph <= 14),
    observacoes TEXT
);

CREATE TABLE IF NOT EXISTS tanques (
    id INT PRIMARY KEY AUTO_INCREMENT,
    identificacao VARCHAR(150) NOT NULL UNIQUE,
    tipo VARCHAR(100),
    volume DECIMAL(12,3) CHECK (volume >= 0),
    profundidade DECIMAL(12,3) CHECK (profundidade >= 0),
    status VARCHAR(100),
    localizacao TEXT
);

CREATE TABLE IF NOT EXISTS fornecedores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    razao_social VARCHAR(150) NOT NULL,
    tipo_documento VARCHAR(100) NOT NULL,
    documento VARCHAR(150) NOT NULL UNIQUE,
    tipo_contato VARCHAR(100) NOT NULL,
    contato VARCHAR(150) NOT NULL,
    tipo_insumo VARCHAR(100),
    endereco VARCHAR(150),
    observacoes TEXT
);

CREATE TABLE IF NOT EXISTS funcionarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    cpf VARCHAR(150) NOT NULL UNIQUE,
    cargo VARCHAR(100),
    telefone VARCHAR(150),
    email VARCHAR(150),
    situacao VARCHAR(100) NOT NULL,
    observacoes TEXT
);

CREATE TABLE IF NOT EXISTS clientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL
);

CREATE TABLE IF NOT EXISTS equipamentos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    tanque_id INT,
    FOREIGN KEY (tanque_id) REFERENCES tanques(id)
);

CREATE TABLE IF NOT EXISTS lotes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(150) NOT NULL UNIQUE,
    especie_id INT NOT NULL,
    tanque_id INT NOT NULL,
    data_alojamento DATE NOT NULL,
    quantidade INT NOT NULL CHECK (quantidade >= 1),
    peso_medio DECIMAL(12,3) CHECK (peso_medio >= 0),
    origem VARCHAR(100),
    observacoes TEXT,
    fornecedor_id INT,
    FOREIGN KEY (especie_id) REFERENCES especies(id),
    FOREIGN KEY (tanque_id) REFERENCES tanques(id),
    FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id)
);

CREATE TABLE IF NOT EXISTS alimentacao (
    id INT PRIMARY KEY AUTO_INCREMENT,
    lote_id INT NOT NULL,
    racao VARCHAR(150) NOT NULL,
    percentual_biomassa DECIMAL(12,3) NOT NULL CHECK (percentual_biomassa >= 0.1 AND percentual_biomassa <= 10),
    frequencia INT NOT NULL CHECK (frequencia >= 1),
    observacoes TEXT,
    FOREIGN KEY (lote_id) REFERENCES lotes(id)
);

CREATE TABLE IF NOT EXISTS registro_alimentacao (
    id INT PRIMARY KEY AUTO_INCREMENT,
    data DATE NOT NULL,
    alimentacao_id INT NOT NULL,
    quantidade DECIMAL(12,3) NOT NULL CHECK (quantidade >= 0.01),
    horario TIME,
    observacoes TEXT,
    funcionario_id INT,
    FOREIGN KEY (alimentacao_id) REFERENCES alimentacao(id),
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
);

CREATE TABLE IF NOT EXISTS qualidade_agua (
    id INT PRIMARY KEY AUTO_INCREMENT,
    datahora DATETIME NOT NULL,
    tanque_id INT NOT NULL,
    temperatura DECIMAL(12,3) CHECK (temperatura >= 0 AND temperatura <= 40),
    ph DECIMAL(12,3) CHECK (ph >= 0 AND ph <= 14),
    oxigenio DECIMAL(12,3) CHECK (oxigenio >= 0),
    amonia DECIMAL(12,3) CHECK (amonia >= 0),
    nitrito DECIMAL(12,3) CHECK (nitrito >= 0),
    nitrato DECIMAL(12,3) CHECK (nitrato >= 0),
    observacoes TEXT,
    funcionario_id INT,
    FOREIGN KEY (tanque_id) REFERENCES tanques(id),
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
);

CREATE TABLE IF NOT EXISTS tratamentos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    data DATE NOT NULL,
    lote_id INT NOT NULL,
    diagnostico TEXT,
    medicamento VARCHAR(150),
    dosagem VARCHAR(150),
    duracao INT CHECK (duracao >= 1),
    carencia INT CHECK (carencia >= 0),
    funcionario_id INT,
    observacoes TEXT,
    FOREIGN KEY (lote_id) REFERENCES lotes(id),
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
);

CREATE TABLE IF NOT EXISTS mortalidade (
    id INT PRIMARY KEY AUTO_INCREMENT,
    data DATE NOT NULL,
    lote_id INT NOT NULL,
    quantidade INT NOT NULL CHECK (quantidade >= 1),
    suspeita VARCHAR(150),
    destinacao VARCHAR(100),
    observacoes TEXT,
    funcionario_id INT,
    FOREIGN KEY (lote_id) REFERENCES lotes(id),
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
);

CREATE TABLE IF NOT EXISTS manutencoes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    data DATE NOT NULL,
    tanque_id INT,
    tipo VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    custo DECIMAL(12,3) CHECK (custo >= 0),
    funcionario_id INT,
    proxima_manutencao DATE,
    equipamento_id INT,
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id),
    FOREIGN KEY (tanque_id) REFERENCES tanques(id),
    FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id),
    CHECK ((tanque_id IS NOT NULL AND equipamento_id IS NULL)
        OR (tanque_id IS NULL AND equipamento_id IS NOT NULL))
);

CREATE TABLE IF NOT EXISTS vendas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    data DATE NOT NULL,
    cliente_id INT NOT NULL,
    documento VARCHAR(100) NOT NULL,
    observacoes TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE IF NOT EXISTS itens_venda (
    id INT PRIMARY KEY AUTO_INCREMENT,
    venda_id INT NOT NULL,
    lote_id INT NOT NULL,
    quantidade DECIMAL(12,3) NOT NULL CHECK (quantidade >= 0.01),
    unidade VARCHAR(100) NOT NULL,
    preco DECIMAL(12,3) NOT NULL CHECK (preco >= 0),
    FOREIGN KEY (venda_id) REFERENCES vendas(id),
    FOREIGN KEY (lote_id) REFERENCES lotes(id)
);
