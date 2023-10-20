import streamlit as st
import json
from PIL import Image

# Inicializar a conexao
conn = st.experimental_connection('snowpark')

# st.set_page_config(
#      page_title="WiseSpend",
#      page_icon="🌎",
#      layout="wide",
#      initial_sidebar_state="expanded",
#      menu_items={
#          'Get Help': 'https://developers.snowflake.com',
#          'About': "This is an *extremely* cool app powered by Snowpark for Python, Streamlit, and Snowflake Data Marketplace"
#      }
# )

image = Image.open('Image\imagem1.jpg')
st.image(image)
# Definir estilos CSS
custom_css = """
<style>
     /* Estilos para os campos de entrada de nome de usuário e senha */
    input[type="text"], input[type="password"] {
        background-color: ##f1f5ec;
        color: black;
        padding: 10px;
        border: none;
        border-radius: 5px;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)


# Função de autenticação
def authenticate(username, password):
    with open('credentials.json') as file:
        credentials = json.load(file)

    if username in credentials:
        stored_password = credentials[username]["password"]
        if password == stored_password:
            return True  # Alterado para True se o usuário e senha estiverem corretos

    return False  # Alterado para False se o usuário e senha estiverem incorretos


def login_page():
    st.title("WiseSpend")

    with st.container():
        st.markdown("Bem-vindo ao nosso sistema. Faça o login.")

    username = st.text_input("Nome de Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Login", key="login-button"):  
        if authenticate(username, password):
            st.success("Login bem-sucedido!")  # Exibir mensagem de sucesso
            main_page()  # Redirecionar para a página principal
        else:
            st.error("Nome de usuário ou senha incorretos.")

     # Personalizar a cor do botão
    st.markdown(f'<style>div.row-widget.stButton > button {{background-color: #0e8e6b; color: white}}</style>', unsafe_allow_html=True)


def compartilhar_dicas_e_experiencias():


    # Seção para exibir dicas e experiências compartilhadas por outros usuários
    st.title("Dicas e Experiências Compartilhadas por Outros Usuários")

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

def main_page():
    compartilhar_dicas_e_experiencias()


def main():
    login_page()

if __name__ == "__main__":
    main()




