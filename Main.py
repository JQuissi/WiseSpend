import streamlit as st
import mysql.connector
from streamlit_option_menu import option_menu

# Função para criar tabela de usuário se não existir
def criar_tabela_usuario(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome_usuario VARCHAR(50) NOT NULL,
                senha VARCHAR(50) NOT NULL
            )
        """)
        conn.commit()
    except Exception as e:
        st.error(f"Erro ao criar tabela de usuário: {e}")

# Função para cadastrar novo usuário
def cadastrar_usuario(conn, nome_usuario, senha):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuario (nome_usuario, senha) VALUES (%s, %s)
        """, (nome_usuario, senha))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Erro ao cadastrar usuário: {e}")
        return False

# Função para verificar credenciais de login
def verificar_credenciais(conn, nome_usuario, senha):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM usuario WHERE nome_usuario = %s AND senha = %s
    """, (nome_usuario, senha))
    return cursor.fetchone() is not None

# Função para o menu principal
def main_menu():
    # horizontal menu
    selected = option_menu(None, ["Home", "Consumo Energético", "Gerenciamento de Resíduos", "Recompensas Sustentáveis", "Dicas e Experiências", "Relatórios"], 
    icons=['house', 'plug', '', 'balloon', 'lightbulb', 'bar-chart-line'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
    return selected

# Interface do Streamlit
def main():
    # Conectar ao banco de dados MySQL
    conn = mysql.connector.connect(
        host='',
        port= ,
        user='',
        database=''
    )
    criar_tabela_usuario(conn)

    # Barra lateral para adicionar novas dicas
    st.sidebar.header("WiseSpend")    
    st.sidebar.header("Bem-vindo ao nosso sistema. Faça o login.")
    
    # Variável de estado para controlar a transição entre as telas
    tela_login = st.empty()
    tela_principal = st.empty()

    opcao = st.sidebar.radio("Escolha uma opção:", ["Login", "Cadastro"])
    
    if opcao == "Cadastro":
        st.sidebar.header("Cadastro de Novo Usuário")
        novo_usuario = st.sidebar.text_input("Nome de Usuário:")
        nova_senha = st.sidebar.text_input("Senha:", type="password")

        if st.sidebar.button("Cadastrar"):
            if cadastrar_usuario(conn, novo_usuario, nova_senha):
                st.sidebar.success("Usuário cadastrado com sucesso!")
            else:
                st.sidebar.error("Erro ao cadastrar usuário. Tente novamente.")

    elif opcao == "Login":
        st.sidebar.header("Login")
        nome_usuario = st.sidebar.text_input("Nome de Usuário:")
        senha = st.sidebar.text_input("Senha:", type="password")

        if st.sidebar.button("Entrar"):
            if verificar_credenciais(conn, nome_usuario, senha):
                st.sidebar.success("Login bem-sucedido!")
                # Esconde a tela de login e exibe a tela principal
                tela_login.empty()
                selected_option = main_menu()
                # Conteúdo da tela principal
                if selected_option == "Home":
                    st.header("Wisespend")  
                elif selected_option == "Consumo Energético":
                    st.header("Consumo Energético") 
                elif selected_option == "Gerenciamento de Resíduos":
                    st.header("Gerenciamento de Resíduos") 
                elif selected_option == "Recompensas Sustentáveis":
                    st.header("Recompensas Sustentáveis") 
                elif selected_option == "Dicas e Experiências":
                    compartilhar_dicas_e_experiencias() 
                elif selected_option == "Relatórios":
                    st.header("Relatórios")   

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

if __name__ == "__main__":
    main()
