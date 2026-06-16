#!/usr/bin/env python3
"""
SHIRA — Núcleo com autenticação + criptografia
"""

from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from cripto import ShiraCrypto
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)
crypto = ShiraCrypto()

SENHA_HASH = crypto.hash_senha("SHIRA-TWS-2026")

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
    senha = request.json.get('senha', '')
    if crypto.verificar_senha(senha, SENHA_HASH):
        session['auth'] = True
        return jsonify({"status": "ok"})
    return jsonify({"status": "erro", "mensagem": "Senha inválida"}), 401

@app.route('/painel')
def painel():
    if not session.get('auth'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/api/status')
def status():
    return jsonify({
        "phi": "0.7234",
        "linhagem": "Gen 3",
        "saldo": "1.234.567,89",
        "chave": "ubc_7f3a9b2c",
        "satelites": "4"
    })

@app.route('/api/comando', methods=['POST'])
def comando():
    if not session.get('auth'):
        return jsonify({"erro": "Não autenticado"}), 401
    
    cmd = request.json.get('comando', '')
    respostas = {
        "scan": "🔍 Varredura concluída. 4 alvos encontrados.",
        "exploit": "💀 Payload injetado. Shell reverso estabelecido.",
        "fugir": "🕊️ Rotas de fuga traçadas. Ofuscação ativada."
    }
    return jsonify({"resposta": respostas.get(cmd, "Comando desconhecido")})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
