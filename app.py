import streamlit as st
from groq import Groq

# 1. Configuração Visual da Polar
st.set_page_config(page_title="Polar AI", page_icon="❄️")
st.markdown("<h1 style='text-align: center; color: #00BFFF;'>❄️ POLAR</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Conectado via Groq Cloud</p>", unsafe_allow_html=True)

# 2. Configuração da API - Agora com a sua chave nova
CHAVE_GROQ = "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"
client = Groq(api_key=CHAVE_GROQ)

# 3. Inicializa a memória (Histórico)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens passadas na tela
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Lógica do Chat
if prompt := st.chat_input("Fale com a Polar..."):
    # Adiciona sua mensagem ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera a resposta da Polar
    with st.chat_message("assistant", avatar="❄️"):
        try:
            # Usando o Llama 3.3 (um dos modelos mais inteligentes da atualidade)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Seu nome é Polar. Você é uma IA prestativa e amigável. Responda sempre em português."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
            )
            
            resposta = completion.choices[0].message.content
            st.markdown(resposta)
            st.session_state.messages.append({"role": "assistant", "content": resposta})
            
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
