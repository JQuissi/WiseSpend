import streamlit as st

# Título do aplicativo
st.title("Login")

# Campo de entrada para o nome de usuário
username = st.text_input("Nome de Usuário")

# Campo de entrada para a senha
password = st.text_input("Senha", type="password")

# Botão de login
if st.button("Login"):
    if username == "seu_nome_de_usuario" and password == "sua_senha":
        st.success("Login bem-sucedido!")
    else:
        st.error("Nome de usuário ou senha incorretos")