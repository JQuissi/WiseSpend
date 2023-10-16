import streamlit as st

st.set_page_config(
     page_title="WiseSpend",
     page_icon="🌎",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://developers.snowflake.com',
         'About': "This is an *extremely* cool app powered by Snowpark for Python, Streamlit, and Snowflake Data Marketplace"
     }
)

# Seção para exibir dicas e experiências compartilhadas por outros usuários
st.title("Dicas e Experiências Compartilhadas por Outros Usuários")
# Aqui você pode carregar e exibir dicas e experiências compartilhadas por outros usuários a partir do seu local de armazenamento




# Título da página
st.header("Compartilhamento de Dicas e Experiências Sustentáveis")

# Campo de entrada para o nome do usuário
username = st.text_input("Nome de Usuário", key="username")

# Campo de texto para compartilhar dicas e experiências
user_input = st.text_area("Compartilhe sua dica ou experiência sustentável", key="user_input")

# Botão para enviar
if st.button("Enviar"):
    if user_input:
        # Salvar a entrada do usuário em algum local, como um arquivo ou banco de dados
        # Neste exemplo, exibimos a entrada do usuário na tela
        st.success(f"O usuário '{username}' compartilhou a seguinte dica ou experiência sustentável:\n\n{user_input}")
    else:
        st.warning("Por favor, insira uma dica ou experiência antes de enviar.")
