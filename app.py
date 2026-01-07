import streamlit as st
from groq import Groq
import base64

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Polar IA - Oficial", page_icon="❄️")

# 2. SISTEMA DE SENHA
def login():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.markdown("<h2 style='text-align: center;'>Acesso Restrito ❄️</h2>", unsafe_allow_html=True)
        senha_mestra = "polo123"
        entrada = st.text_input("Digite a senha para liberar a Polar:", type="password")
        
        if st.button("Entrar"):
            if entrada == senha_mestra:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Senha incorreta, fale com o dono!")
        st.stop()

# Executa o login
login()

# 3. CONFIGURAÇÃO DA API
CHAVE_GROQ = "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"
client = Groq(api_key=CHAVE_GROQ)

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# 4. INTERFACE LATERAL
with st.sidebar:
    st.title("❄️ Painel da Polar")
    arquivo_foto = st.file_uploader("Mande uma foto para eu ver", type=["jpg", "jpeg", "png"])
    if st.button("Limpar Conversa"):
        st.session_state.messages = []
        st.rerun()

st.title("❄️ POLAR IA")

# 5. MEMÓRIA DO CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar = "❄️" if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 6. LÓGICA DE INTERAÇÃO
if prompt := st.chat_input("Pergunte algo..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="❄️"):
        try:
            if arquivo_foto:
                # MODELO DE VISÃO ATUALIZADO (Llama 3.2 11B Vision)
                base64_image = encode_image(arquivo_foto)
                arquivo_foto.seek(0)
                
                completion = client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview", 
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"Responda em Português como Polar: {prompt}"},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                                }
                            ]
                        }
                    ],
                )
            else:
                # MODELO DE TEXTO (Llama 3.3 70B)
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Seu nome é Polar. Use emojis de gelo e seja prestativa."},
                        {"role": "user", "content": prompt}
                    ],
                )
            
            resposta = completion.choices[0].message.content
            st.markdown(resposta)
            st.session_state.messages.append({"role": "assistant", "content": resposta})
            
        except Exception as e:
            # Se o 11b falhar, tentamos o modelo 90b automaticamente como plano B
            st.warning("Tentando modelo alternativo...")
            try:
                completion = client.chat.completions.create(
                    model="llama-3.2-90b-vision-preview",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.markdown(completion.choices[0].message.content)
            except:
                st.error(f"Erro persistente na Groq: {e}")

