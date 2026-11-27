-- Dados fictícios para demonstração. Execute uma vez, em um banco vazio.
INSERT INTO especies (id, nome_comum, tipo, temperatura, ph) VALUES
(1, 'Tilapia', 'Peixe', 27.0, 7.0), (2, 'Camarao', 'Camarão', 28.0, 7.5),
(3, 'Carpa', 'Peixe', 24.0, 7.0);
INSERT INTO tanques (id, identificacao, tipo, volume, status) VALUES
(1, 'T01', 'Escavado', 100, 'Ativo'), (2, 'T02', 'Alvenaria', 80, 'Ativo'),
(3, 'T03', 'Rede', 60, 'Ativo');
INSERT INTO fornecedores (id, razao_social, tipo_documento, documento, tipo_contato, contato, tipo_insumo) VALUES
(1, 'Fornecedor teste A', 'CNPJ', 'TESTE-01', 'E-mail', 'fornecedor@example.com', 'Outro');
INSERT INTO funcionarios (id, nome, cpf, cargo, situacao) VALUES
(1, 'Funcionario teste A', 'TESTE-01', 'Técnico em aquicultura', 'Ativo');
INSERT INTO clientes (id, nome) VALUES (1, 'Cliente teste A'), (2, 'Cliente teste B'), (3, 'Cliente teste C');
INSERT INTO equipamentos (id, nome, tanque_id) VALUES (1, 'Bomba A', 1), (2, 'Filtro B', 2);
INSERT INTO lotes (id, codigo, especie_id, tanque_id, data_alojamento, quantidade, peso_medio, origem, fornecedor_id) VALUES
(1, 'L01', 1, 1, '2026-10-01', 100, 50, 'Aquisição externa', 1),
(2, 'L02', 2, 2, '2026-10-02', 200, 10, 'Produção própria', NULL);
INSERT INTO alimentacao (id, lote_id, racao, percentual_biomassa, frequencia) VALUES
(1, 1, 'Racao A', 3, 2), (2, 2, 'Racao B', 4, 3);
INSERT INTO registro_alimentacao (id, data, alimentacao_id, quantidade, horario, funcionario_id) VALUES
(1, '2026-10-03', 1, 2.5, '08:00:00', 1);
INSERT INTO qualidade_agua (id, datahora, tanque_id, temperatura, ph, funcionario_id) VALUES
(1, '2026-10-03 09:00:00', 1, 27, 7, 1);
INSERT INTO tratamentos (id, data, lote_id, diagnostico, funcionario_id) VALUES
(1, '2026-10-04', 1, 'Registro de teste', 1);
INSERT INTO mortalidade (id, data, lote_id, quantidade, funcionario_id) VALUES
(1, '2026-10-04', 1, 2, 1);
INSERT INTO manutencoes (id, data, tanque_id, tipo, descricao, funcionario_id) VALUES
(1, '2026-10-05', 1, 'Preventiva', 'Limpeza de teste', 1);
INSERT INTO manutencoes (id, data, equipamento_id, tipo, descricao, funcionario_id) VALUES
(2, '2026-10-06', 1, 'Corretiva', 'Inspecao de teste', 1);
INSERT INTO vendas (id, data, cliente_id, documento) VALUES
(1, '2026-10-07', 1, 'Recibo'), (2, '2026-10-08', 2, 'NF-e');
INSERT INTO itens_venda (id, venda_id, lote_id, quantidade, unidade, preco) VALUES
(1, 1, 1, 10, 'kg', 15), (2, 1, 2, 5, 'kg', 25), (3, 2, 1, 4, 'kg', 15);
