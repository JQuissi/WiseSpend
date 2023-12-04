import streamlit as st
import mysql.connector
from streamlit_option_menu import option_menu

# Função para criar tabela de usuário se não existir
def criar_tabela_usuario(conn):
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome_usuario VARCHAR(50) NOT NULL,
                senha VARCHAR(50) NOT NULL
            )
        """)
        conn.commit()


# Função para realizar o login
def login(conn):
    st.sidebar.header("Login")
    nome_usuario = st.sidebar.text_input("Nome de Usuário:")
    senha = st.sidebar.text_input("Senha:", type="password")

    if st.sidebar.button("Entrar"):
        if verificar_credenciais(conn, nome_usuario, senha):
            st.sidebar.success("Login bem-sucedido!")
            st.session_state['connection_established'] = True
        else:
            st.sidebar.error("Falha no login. Verifique suas credenciais.")
            st.session_state['connection_established'] = False         
            

# Função para cadastrar novo usuário
def cadastrar_usuario(conn, nome_usuario, senha):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuario (nome_usuario, senha) VALUES (%s, %s)
    """, (nome_usuario, senha))
    conn.commit()
    return True

# Função para verificar credenciais de login
def verificar_credenciais(conn, nome_usuario, senha):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM usuario WHERE nome_usuario = %s AND senha = %s
    """, (nome_usuario, senha))
    return cursor.fetchone() is not None    


# Dicas e Experiências
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

# Função para a página inicial
def inicial_page(conn):  
    # Barra lateral para adicionar novas dicas
    st.sidebar.header("WiseSpend")    
    st.sidebar.header("Bem-vindo ao nosso sistema. Faça o login.")
    
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
        login(conn)  # Chama a função de login


# Interface do Streamlit
# Interface do Streamlit
def main():
    # Conectar ao banco de dados MySQL
    conn = mysql.connector.connect(
        host='',
        port=3306,
        user='',
        database=''
    )
    criar_tabela_usuario(conn)
    
    # Página inicial
    inicial_page(conn)

    # Verifica se a conexão foi estabelecida
    if 'connection_established' not in st.session_state or not st.session_state.connection_established:
        return  # Se não houver conexão estabelecida, encerra a execução

    # Página principal
    selected_option = option_menu(None, ["Home", "Consumo Energético", "Gerenciamento de Resíduos", "Recompensas Sustentáveis", "Dicas e Experiências", "Relatórios"], 
        icons=['house', 'plug', '', 'balloon', 'lightbulb', 'bar-chart-line'], 
        menu_icon="cast", default_index=0, orientation="horizontal")
        
    # Conteúdo da tela principal
    if selected_option == "Home":
         st.header("Home")
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
    
if __name__ == "__main__":
    main()

