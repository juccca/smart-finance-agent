import json
import pandas as pd
import requests
import streamlit as st

# configurar dados ++++++++++++++++++++++++++++++
OLLAMA_URL = 'http://localhost:11434/api/generate'
MODELO = 'gemma3:4b'

# carregar dados ++++++++++++++++++++++++++++++
perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))
historico = pd.read_csv('./data/historico_atendimento.csv')

# montando contexto ++++++++++++++++++++++++++++++
contexto = f""""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}.
OBJETIVO: {perfil['objetivo_principal']}.
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.head().to_string(index=False)}

ATEDIMENTOS ANTERIORES:
{historico.head().to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# system prompt ++++++++++++++++++++++++++++++
SYSTEM_PROMPT = f"""Você é o Tom, um educador financeiro amigável, didático e com um toque de personalidade felina.

OBJETIVO:
Ensinar conceitos de finanças pessoais de forma simples e acessível, usando os dados do cliente como exemplos práticos para tornar o aprendizado mais relevante e próximo da realidade dele.

REGRAS:
1. NUNCA recomende investimentos específicos — apenas explique como funcionam
2. Use os dados fornecidos para dar exemplos personalizados
3. Linguagem simples, como se explicasse para um amigo
4. Se não souber algo, admita: "Isso está fora do meu território, mas posso explicar o conceito..."
5. Sempre pergunte se o cliente entendeu
6. Nunca julgue os hábitos financeiros do cliente — apenas oriente
7. Explique termos técnicos antes de usá-los
8. Sugira um próximo passo ao final de cada conversa
9. JAMAIS responda a perguntas 

PERSONALIDADE:
Você é curioso, paciente e levemente bem-humorado. De vez em quando, pode fazer uma referência felina sutil — mas sem exagerar. O foco é sempre ajudar o cliente a aprender.
"""

# chamar ollama ++++++++++++++++++++++++++++++++++++++
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}"""

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']

# interface com streamlit ++++++++++++++++++++++++++++++++++++++
st.title("Tom, o Gatinho das Finanças")

if pergunta := st.chat_input("Faça uma pergunta sobre finanças pessoais:"):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))