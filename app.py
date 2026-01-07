import streamlit as st
from groq import Groq
import base64

# 1. Configuração de Página
st.set_page_config(page_title="Polar AI - Vision", page_icon="❄️")

# 2. Chave da API
CHAVE_GROQ = "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"
client = Groq(api_key=CHAVE_GROQ)

# Função para converter imagem para base64
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# 3. Interface Lateral
with st.sidebar:
    st.title("❄️ Configurações")
    arquivo_foto = st.file_uploader("Envie uma foto para a Polar analisar", type=["jpg", "jpeg", "png"])
    if st.button("Limpar Conversa"):
        st.session_state.messages = []
        st.rerun()

st.title("❄️ POLAR VISION")

# 4. Memória do Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Lógica de Chat e Visão
if prompt := st.chat_input("Pergunte algo sobre a foto ou converse..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="❄️"):
        try:
            if arquivo_foto:
                # LÓGICA PARA FOTO
                base64_image = encode_image(arquivo_foto)
                arquivo_foto.seek(0) 
                
                completion = client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview", # Modelo de visão atualizado
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"Seu nome é Polar. Responda em Português: {prompt}"},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                                }
                            ]
                        }
                    ],
                )
            else:
                # LÓGICA APENAS TEXTO
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Seu nome é Polar. Responda sempre em Português."},
                        {"role": "user", "content": prompt}
                    ],
                )
            
            resposta = completion.choices[0].message.content
            st.markdown(resposta)
            st.session_state.messages.append({"role": "assistant", "content": resposta})
            
        except Exception as e:
            st.error(f"Erro: {e}")
