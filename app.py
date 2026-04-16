# C1 — Interface web Streamlit pour l'agent LangChain
# Lancer avec : streamlit run app.py

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

from agent import creer_agent, tools

# ---- Configuration de la page -------------------------------------------------------------------
st.set_page_config(page_title="Agent LangChain", layout="wide")
st.title("Agent LangChain — Assistant Financier")

# ---- Sidebar : liste des outils disponibles ---------------------------------------
with st.sidebar:
    st.header("Outils disponibles")
    for tool in tools:
        st.markdown(f"**{tool.name}**")
        st.caption(tool.description)
        st.divider()
    if st.button("Réinitialiser la conversation"):
        st.session_state.messages = []
        st.session_state.agent = creer_agent()
        st.rerun()

# ---- Initialisation de l'agent et de l'historique ---------------------------------------
if "agent" not in st.session_state:
    st.session_state.agent = creer_agent()
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---- Affichage de l'historique des messages ---------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- Champ de saisie ----------------------------------------------------------------------------------
if prompt := st.chat_input("Posez votre question à l'agent..."):
    # Afficher la question de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Obtenir la réponse de l'agent
    with st.chat_message("assistant"):
        with st.spinner("L'agent réfléchit..."):
            try:
                result = st.session_state.agent.invoke({"input": prompt})
                response = result["output"]
            except Exception as e:
                response = f"Erreur : {e}"
        st.markdown(response)

    # Sauvegarder la réponse dans l'historique
    st.session_state.messages.append({"role": "assistant", "content": response})
