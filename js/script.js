// Envia e recebe os dados das rotas Flask usando Fetch.
async function api(tabela, opcoes = {}) {
    const resposta = await fetch('/api/' + tabela, opcoes);
    const dados = await resposta.json();
    if (!resposta.ok) throw new Error(dados.erro || 'Erro na operação.');
    return dados;
}

function mensagem(modulo, texto, erro = false) {
    const elemento = modulo.querySelector('.mensagem');
    elemento.textContent = texto;
    elemento.classList.toggle('erro', erro);
}

// Busca os cadastros reais para os campos de espécie, tanque e lote.
async function carregarOpcoes(modulo) {
    for (const select of modulo.querySelectorAll('select[data-origem]')) {
        const registros = await api(select.dataset.origem);
        const selecionado = select.value;
        select.replaceChildren(new Option(registros.length ? 'Selecione' : 'Cadastre os registros primeiro', ''));
        for (const registro of registros) {
            select.add(new Option(registro[select.dataset.rotulo], registro.id));
        }
        select.value = selecionado;
    }
}

function formatarValor(modulo, campo, valor) {
    if (valor === null || valor === undefined) return '-';
    const select = modulo.querySelector('select[name="' + campo + '"][data-origem]');
    if (select) {
        const opcao = Array.from(select.options).find(o => o.value === String(valor));
        return opcao ? opcao.text : valor;
    }
    return valor;
}

function moeda(valor) {
    return Number(valor).toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'});
}

// Monta a tabela com os dados retornados pelo banco.
async function listar(modulo) {
    const registros = await api(modulo.dataset.tabela);
    const corpo = modulo.querySelector('tbody');
    const campos = Array.from(modulo.querySelectorAll('th[data-campo]'), th => th.dataset.campo);
    corpo.replaceChildren();
    if (registros.length === 0) {
        const linha = corpo.insertRow();
        const celula = linha.insertCell();
        celula.colSpan = campos.length + 1;
        celula.textContent = 'Nenhum registro cadastrado.';
        return;
    }
    for (const registro of registros) {
        const linha = corpo.insertRow();
        linha.insertCell().textContent = registro.id;
        for (const campo of campos) {
            const valor = campo === 'total' ? moeda(Number(registro.quantidade) * Number(registro.preco)) : formatarValor(modulo, campo, registro[campo]);
            linha.insertCell().textContent = valor;
        }
    }
}

async function atualizar(modulo) {
    await carregarOpcoes(modulo);
    await listar(modulo);
}

async function iniciarModulo(modulo) {
    const form = modulo.querySelector('form');
    const botao = form.querySelector('button[type="submit"]');
    const atualizarBotao = modulo.querySelector('.atualizar');
    botao.disabled = true;
    try {
        await atualizar(modulo);
    } catch (erro) {
        mensagem(modulo, erro.message, true);
    } finally {
        botao.disabled = false;
    }
    atualizarBotao.addEventListener('click', async () => {
        try {
            await atualizar(modulo);
            mensagem(modulo, 'Consulta atualizada.');
        } catch (erro) {
            mensagem(modulo, erro.message, true);
        }
    });
    form.addEventListener('submit', async evento => {
        evento.preventDefault();
        const dados = Object.fromEntries(new FormData(form));
        botao.disabled = true;
        try {
            await api(modulo.dataset.tabela, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(dados)
            });
            form.reset();
            mensagem(modulo, 'Cadastro realizado com sucesso!');
            try {
                await atualizar(modulo);
                for (const outro of document.querySelectorAll('.modulo')) {
                    if (outro !== modulo) await carregarOpcoes(outro);
                }
            } catch (erro) {
                mensagem(modulo, 'Cadastro salvo, mas não foi possível atualizar a consulta.', true);
            }
        } catch (erro) {
            mensagem(modulo, erro.message, true);
        } finally {
            botao.disabled = false;
        }
    });
}

document.querySelectorAll('.modulo').forEach(iniciarModulo);

// Mantém o valor total de vendas que existia no projeto original.
const venda = document.querySelector('[data-tabela="itens_venda"] form');
if (venda) {
    const total = venda.querySelector('.total-venda');
    venda.addEventListener('input', () => {
        total.textContent = moeda(Number(venda.elements.quantidade.value) * Number(venda.elements.preco.value));
    });
    venda.addEventListener('reset', () => { total.textContent = moeda(0); });
}

// Marca a página atual no menu.
for (const link of document.querySelectorAll('nav a')) {
    if (link.getAttribute('href') === location.pathname || (location.pathname === '/index.html' && link.getAttribute('href') === '/')) {
        link.setAttribute('aria-current', 'page');
    }
}
