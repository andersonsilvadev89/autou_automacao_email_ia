---
title: Classificador Emails Autou
emoji: 🦀
colorFrom: red
colorTo: purple
sdk: gradio
sdk_version: 5.44.1
app_file: app.py
pinned: false
license: mit
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# autou_automacao_email_ia

Este projeto é um desafio para a vaga na empresa AutoU, com o objetivo de criar uma aplicação web que automatiza a classificação de e-mails usando inteligência artificial. A solução categoriza e-mails como Produtivos ou Improdutivos e sugere respostas automáticas, liberando tempo da equipe para tarefas mais estratégicas.

A aplicação é dividida em duas partes: um **backend** em Python (Flask) para o processamento de IA e um **frontend** em React para a interface do usuário.

## Tecnologias Utilizadas

- **Frontend:** React, Vite
- **Backend:** Python, Flask, Hugging Face Transformers, Gradio
- **Hospedagem:** Hugging Face Spaces

## Como Rodar Localmente

Certifique-se de que você tem Python (versão 3.8 ou superior) e Node.js instalados em sua máquina.

### 1. Configurar e Executar o Backend

1.  Navegue até a pasta `backend`:
    ```bash
    cd backend
    ```
2.  Crie e ative o ambiente virtual:
    ```bash
    python -m venv venv
    # No Windows
    .\venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate
    ```
3.  Instale as bibliotecas necessárias:
    ```bash
    pip install -r requirements.txt
    ```
4.  Execute a API Flask:
    ```bash
    python app.py
    ```

O servidor do backend estará rodando em `http://127.0.0.1:5000`.

### 2. Configurar e Executar o Frontend

Em um **novo terminal**, navegue até a pasta `frontend`:

1.  Instale as dependências do Node.js:
    ```bash
    npm install
    ```
2.  Inicie a aplicação React:
    ```bash
    npm run dev
    ```

A aplicação estará disponível em `http://localhost:5173`. Para testar, certifique-se de que ambos os servidores (backend e frontend) estejam rodando simultaneamente.
