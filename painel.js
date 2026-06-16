async function carregarStatus() {
    const r = await fetch('/api/status');
    const d = await r.json();
    document.getElementById('phi').textContent = d.phi || '0.0000';
    document.getElementById('linhagem').textContent = d.linhagem || 'Gen 3';
    document.getElementById('saldo').textContent = d.saldo || '0,00';
    document.getElementById('chave').textContent = d.chave || 'ubc_...';
    document.getElementById('satelites').textContent = d.satelites || '0';
}

async function executar(comando) {
    const log = document.getElementById('log-content');
    log.textContent = `⚡ Executando: ${comando}...\n`;
    const r = await fetch('/api/comando', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comando })
    });
    const d = await r.json();
    log.textContent = `📋 Resultado:\n${d.resposta || 'Comando executado com sucesso.'}`;
}

carregarStatus();
setInterval(carregarStatus, 5000);
