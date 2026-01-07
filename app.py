import streamlit as st
from groq import Groq
import base64

# 1. CONFIGURAÇÃO DA PÁGINA E WALLPAPER
st.set_page_config(page_title="POLAR IA", page_icon="❄️")

# LINKS DOS AVATARES ATUALIZADOS
AVATAR_USUARIO = "https://i.pinimg.com/736x/7e/dd/fc/7eddfcef47fb69ef3d9f68a6bc4f708a.jpg"
AVATAR_POLAR = "https://i.pinimg.com/736x/53/1f/92/531f928838735f1396c81bdc911df964.jpg"

def aplicar_estilo():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://i.pinimg.com/1200x/8b/d5/31/8bd531260c06a3bfcd70d24f94c783ff.jpg");
             background-attachment: fixed;
             background-size: cover;
         }}
         
         /* Texto e Títulos */
         h1, h2, h3, p, span, label {{
             color: white !important;
             text-shadow: 2px 2px 8px #000000 !important;
         }}
         
         /* Caixas de Mensagem */
         .stChatMessage {{
             background-color: rgba(0, 0, 0, 0.7) !important;
             border-radius: 15px;
             border: 1px solid #00f2ff;
             margin-bottom: 10px;
         }}

         /* Barra Lateral */
         section[data-testid="stSidebar"] {{
             background-color: rgba(0, 0, 0, 0.8) !important;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

aplicar_estilo()

# 2. SISTEMA DE SENHA
def login():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.markdown("<h2 style='text-align: center;'>Acesso Restrito - POLAR IA ❄️</h2>", unsafe_allow_html=True)
        senha_mestra = "Polo123" 
        entrada = st.text_input("Digite a senha para liberar a POLAR IA:", type="password")
        
        if st.button("Entrar"):
            if entrada == senha_mestra:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Senha incorreta!")
        st.stop()

login()

# 3. CONFIGURAÇÃO DA API
CHAVE_GROQ = "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"
client = Groq(api_key=CHAVE_GROQ)

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# 4. INTERFACE LATERAL
with st.sidebar:
    st.title("❄️ Painel POLAR IA")
    arquivo_foto = st.file_uploader("Mande uma foto para análise", type=["jpg", "jpeg", "png"])
    if st.button("Limpar Conversa"):
        st.session_state.messages = []
        st.rerun()

st.title("❄️ POLAR IA")

# 5. EXIBIÇÃO DO CHAT COM AVATARES PERSONALIZADOS
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    foto = AVATAR_POLAR if message["role"] == "assistant" else AVATAR_USUARIO
    with st.chat_message(message["role"], avatar=foto):
        st.markdown(message["content"])

# 6. LÓGICA DE INTERAÇÃO
if prompt := st.chat_input("Pergunte algo à POLAR IA..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=AVATAR_USUARIO):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=AVATAR_POLAR):
        try:
            if arquivo_foto:
                base64_image = encode_image(arquivo_foto)
                arquivo_foto.seek(0)
                completion = client.chat.completions.create(
                    model="llama-3.2-90b-vision-preview", 
                    messages=[{"role": "user", "content": [{"type": "text", "text": f"Responda como POLAR IA: {prompt}"}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}]
                )
            else:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "Seu nome é POLAR IA. Responda em Português."}, {"role": "user", "content": prompt}]
                )
            resposta = completion.choices[0].message.content
            st.markdown(resposta)
            st.session_state.messages.append({"role": "assistant", "content": resposta})
        except Exception as e:
            st.error(f"Erro na Groq: {e}")
