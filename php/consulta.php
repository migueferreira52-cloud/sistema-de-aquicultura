<?php
// Consulta complementar: usa o mesmo banco de dados do Flask.
// No htdocs, preserve as pastas php e css. Inicie Apache e MySQL.
$host = '127.0.0.1';
$porta = 3306;
$banco = 'aquicultura_escolar';
$usuario = 'root';
$senha = '';
$registros = [];
$erro = '';
try {
    $pdo = new PDO("mysql:host=$host;port=$porta;dbname=$banco;charset=utf8mb4", $usuario, $senha);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $sql = 'SELECT l.codigo, e.nome_comum, t.identificacao, l.quantidade, l.data_alojamento
            FROM lotes l JOIN especies e ON l.especie_id = e.id
            JOIN tanques t ON l.tanque_id = t.id ORDER BY l.id DESC';
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $registros = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    $erro = 'Não foi possível consultar o banco. Confira o MySQL e a configuração.';
}
?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Aquicultura | Consulta PHP</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
<header><div class="container"><h1 style="color:white">Aquicultura</h1><p>Consulta complementar em PHP</p></div></header>
<main class="container">
    <section class="painel">
        <h2>Consulta de lotes</h2>
        <p><a href="http://127.0.0.1:5000/">Voltar ao sistema Flask</a></p>
        <?php if ($erro): ?>
            <p class="mensagem erro"><?= htmlspecialchars($erro) ?></p>
        <?php else: ?>
            <div class="tabela"><table>
                <thead><tr><th>Código</th><th>Espécie</th><th>Tanque</th><th>Quantidade inicial</th><th>Data</th></tr></thead>
                <tbody>
                <?php foreach ($registros as $registro): ?>
                    <tr><?php foreach ($registro as $valor): ?>
                        <td><?= htmlspecialchars((string)$valor, ENT_QUOTES, 'UTF-8') ?></td>
                    <?php endforeach; ?></tr>
                <?php endforeach; ?>
                <?php if (!$registros): ?><tr><td colspan="5">Nenhum lote cadastrado.</td></tr><?php endif; ?>
                </tbody>
            </table></div>
        <?php endif; ?>
    </section>
</main>
<footer>Sistema de Gestão de Aquicultura</footer>
</body>
</html>
