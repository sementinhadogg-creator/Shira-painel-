document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const senha = document.getElementById('senha').value;

    const response = await fetch('/auth', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ senha: senha })
    });

    const data = await response.json();

    if (data.status === 'ok') {
        window.location.href = '/painel';
    } else {
        const erro = document.getElementById('erro');
        erro.textContent = '❌ Acesso negado. Senha inválida.';
        erro.style.display = 'block';
        document.getElementById('senha').value = '';
    }
});
