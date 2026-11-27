const API_URL = '/api/';

async function api(caminho, opcoes = {}) {
    const resposta = await fetch(API_URL + caminho, opcoes);
    const dados = await resposta.json();
    if (!resposta.ok) throw new Error(dados.erro || 'Erro na operação.');
    return dados;
}

// Preenche as chaves estrangeiras com registros já cadastrados.
async function carregarOpcoes() {
    for (const select of document.querySelectorAll('select[data-origem]')) {
        const valor = select.value;
        const registros = await api(select.dataset.origem);
        select.innerHTML = '<option value="">Selecione</option>';
        for (const registro of registros) {
            const opcao = document.createElement('option');
            opcao.value = registro.id;
            opcao.textContent = registro[select.dataset.rotulo];
            select.appendChild(opcao);
        }
        select.value = valor;
    }
}

function moeda(valor) {
    return 'R$ ' + Number(valor).toFixed(2).replace('.', ',');
}

function iniciar(modulo) {
    const tabela = modulo.dataset.tabela;
    const form = modulo.querySelector('form');
    const mensagem = modulo.querySelector('.mensagem');
    const botao = form.querySelector('button[type="submit"]');
    let idEdicao = null;

    // GET: monta a tabela com os dados da API.
    async function listar() {
        const registros = await api(tabela);
        const corpo = modulo.querySelector('tbody');
        corpo.innerHTML = '';
        for (const registro of registros) {
            const linha = document.createElement('tr');
            const id = document.createElement('td');
            id.textContent = registro.id;
            linha.appendChild(id);
            for (const th of modulo.querySelectorAll('th[data-campo]')) {
                const campo = th.dataset.campo;
                let valor = registro[campo];
                const select = form.querySelector('select[name="' + campo + '"][data-origem]');
                if (select && valor != null) {
                    for (const opcao of select.options) {
                        if (opcao.value == valor) valor = opcao.textContent;
                    }
                }
                if (campo === 'total') valor = moeda(registro.quantidade * registro.preco);
                const celula = document.createElement('td');
                celula.textContent = valor == null ? '-' : valor;
                linha.appendChild(celula);
            }
            const acoes = document.createElement('td');
            const editar = document.createElement('button');
            editar.textContent = 'Editar';
            editar.addEventListener('click', () => {
                idEdicao = registro.id;
                for (const campo of form.elements) {
                    if (campo.name) campo.value = registro[campo.name] == null ? '' : registro[campo.name];
                }
                const cep = form.querySelector('#fornecedores-cep');
                if (cep) {
                    cep.value = '';
                    form.querySelector('#mensagem-cep').textContent = '';
                }
                botao.textContent = 'Salvar edição';
                mensagem.textContent = 'Editando registro ' + registro.id;
                mostrarTotal();
            });
            const excluir = document.createElement('button');
            excluir.textContent = 'Excluir';
            excluir.addEventListener('click', async () => {
                if (!confirm('Excluir este registro?')) return;
                try {
                    await api(tabela + '/' + registro.id, {method: 'DELETE'});
                    if (idEdicao === registro.id) form.reset();
                    await carregarOpcoes();
                    await listar();
                    mensagem.textContent = 'Registro excluído!';
                } catch (erro) {
                    mensagem.textContent = erro.message;
                }
            });
            acoes.appendChild(editar);
            acoes.appendChild(excluir);
            linha.appendChild(acoes);
            corpo.appendChild(linha);
        }
    }

    function mostrarTotal() {
        const total = form.querySelector('.total-venda');
        if (total) total.textContent = moeda(form.elements.quantidade.value * form.elements.preco.value);
    }

    form.addEventListener('input', mostrarTotal);
    form.addEventListener('reset', () => {
        idEdicao = null;
        botao.textContent = 'Cadastrar';
        const total = form.querySelector('.total-venda');
        if (total) total.textContent = moeda(0);
    });

    // POST para cadastrar; PUT para editar.
    form.addEventListener('submit', async evento => {
        evento.preventDefault();
        const dados = {};
        for (const campo of form.elements) {
            if (campo.name) dados[campo.name] = campo.value;
        }
        botao.disabled = true;
        try {
            const resultado = await api(idEdicao === null ? tabela : tabela + '/' + idEdicao, {
                method: idEdicao === null ? 'POST' : 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(dados)
            });
            form.reset();
            mensagem.textContent = resultado.mensagem;
            await carregarOpcoes();
            await listar();
        } catch (erro) {
            mensagem.textContent = erro.message;
        }
        botao.disabled = false;
    });

    async function atualizar() {
        try {
            await carregarOpcoes();
            await listar();
        } catch (erro) {
            mensagem.textContent = 'Abra o site pelo endereço http://127.0.0.1:5000. ' + erro.message;
        }
    }
    modulo.querySelector('.atualizar').addEventListener('click', atualizar);
    atualizar();
}

document.querySelectorAll('.modulo').forEach(iniciar);


// API pública ViaCEP - apostila DWS, capítulo 2.
async function buscarCep() {
    const campoCep = document.querySelector('#fornecedores-cep');
    const endereco = document.querySelector('#fornecedores-endereco');
    const mensagemCep = document.querySelector('#mensagem-cep');
    const botaoCep = document.querySelector('#buscar-cep');
    const cep = campoCep.value.replace('-', '').trim();

    if (!/^[0-9]{8}$/.test(cep)) {
        mensagemCep.textContent = 'Digite um CEP com 8 números.';
        return;
    }

    const enderecoAnterior = endereco.value;
    botaoCep.disabled = true;
    mensagemCep.textContent = 'Buscando endereço...';
    try {
        const resposta = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
        const dados = await resposta.json();
        if (campoCep.value.replace('-', '').trim() !== cep || endereco.value !== enderecoAnterior) {
            mensagemCep.textContent = 'Consulta descartada: o formulário mudou.';
        } else if (!resposta.ok || dados.erro) {
            mensagemCep.textContent = 'CEP não encontrado. Informe o endereço manualmente.';
        } else {
            let texto = '';
            if (dados.logradouro) texto += dados.logradouro + ', ';
            if (dados.bairro) texto += dados.bairro + ', ';
            texto += dados.localidade + ' - ' + dados.uf;
            if (texto.length > 150) {
                mensagemCep.textContent = 'Endereço longo. Informe o endereço manualmente.';
            } else {
                endereco.value = texto;
                mensagemCep.textContent = 'Endereço encontrado! Complete com número e complemento.';
            }
        }
    } catch (erro) {
        mensagemCep.textContent = 'Não foi possível consultar o ViaCEP. Informe o endereço manualmente.';
    }
    botaoCep.disabled = false;
}

const botaoCep = document.querySelector('#buscar-cep');
if (botaoCep) {
    botaoCep.addEventListener('click', buscarCep);
    document.querySelector('.formulario').addEventListener('reset', () => {
        document.querySelector('#mensagem-cep').textContent = '';
    });
}
