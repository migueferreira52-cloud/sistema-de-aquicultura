USE aquicultura_escolar;

-- 1. Quais lotes pertencem a cada espécie? (INNER JOIN)
SELECT l.codigo, e.nome_comum
FROM lotes l
INNER JOIN especies e ON l.especie_id = e.id
ORDER BY l.id;

-- 2. Quais clientes compraram? Inclui clientes sem venda. (LEFT JOIN)
SELECT c.nome, v.id AS venda
FROM clientes c
LEFT JOIN vendas v ON c.id = v.cliente_id
ORDER BY c.id, v.id;

-- 3. Quais espécies e tanques estão relacionados aos lotes? (3 tabelas)
SELECT l.codigo, e.nome_comum, t.identificacao
FROM lotes l
JOIN especies e ON l.especie_id = e.id
JOIN tanques t ON l.tanque_id = t.id
ORDER BY l.id;

-- 4. Quais lotes têm quantidade acima da média? (subconsulta de valor único)
SELECT codigo, quantidade
FROM lotes
WHERE quantidade > (SELECT AVG(quantidade) FROM lotes)
ORDER BY id;

-- 5. Quais clientes possuem vendas? (subconsulta IN)
SELECT nome
FROM clientes
WHERE id IN (SELECT cliente_id FROM vendas)
ORDER BY id;

-- 6. Qual a segunda página de espécies, com duas por página? (paginação)
SELECT id, nome_comum
FROM especies
ORDER BY id
LIMIT 2 OFFSET 2;

-- 7. Quanto custa cada item e a qual venda pertence? (JOINs e cálculo)
SELECT v.id AS venda, c.nome, l.codigo, i.quantidade * i.preco AS valor_item
FROM itens_venda i
JOIN vendas v ON i.venda_id = v.id
JOIN clientes c ON v.cliente_id = c.id
JOIN lotes l ON i.lote_id = l.id
ORDER BY v.id, i.id;
