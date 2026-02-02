import streamlit as st
import google.generativeai as genai
import os

# 1. Configuración de la página y Seguridad Simple
st.set_page_config(page_title="Virtual Engineer AI", layout="centered")

def check_password():
    """Retorna True si el usuario introdujo la contraseña correcta."""
    def password_entered():
        if st.session_state["password"] == "Ingeniero2024": # CAMBIA TU CONTRASEÑA AQUÍ
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if check_password():
    # 2. Configuración de Gemini
    # La API Key se guarda de forma segura en los Secrets de Streamlit
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

    st.title("🏗️ Virtual Engineer Assistant")
    
    # Selector de idioma
    lang = st.sidebar.selectbox("Language / Idioma", ["English", "Español"])
    st.sidebar.info("Knowledge base: Technical Documentation Folder")

    # Instrucciones de sistema según idioma
    sys_prompt = (
        "You are a professional engineer. Answer queries based ONLY on the provided files. "
        f"Always respond in {lang}."
    )

    # Inicializar el modelo con File Search
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=sys_prompt
    )

    # 3. Interfaz de Chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me about technical specs..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Aquí Gemini busca automáticamente en tus archivos subidos
            # Importante: Debes haber subido los archivos previamente a tu cuenta de Gemini
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})