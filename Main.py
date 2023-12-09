import streamlit as st
import mysql.connector
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from io import BytesIO
from PIL import Image
import pandas as pd
from datetime import datetime, timedelta

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


def compartilhar_dicas_e_experiencias(conn):
    st.title('Dicas de Sustentabilidade')
    
    # Adicionando st.radio para a escolha do usuário
    opcao = st.radio("Escolha uma opção:", ["Consultar Dicas e Experiências", "Cadastrar Dicas e Experiências"])

    # Verificar se o usuário fez uma escolha
    if opcao:
        # Se a opção for "Consultar Dicas e Experiências"
        if opcao == "Consultar Dicas e Experiências":     
            cursor = conn.cursor()
            cursor.execute("SELECT categoria, titulo_dica, desc_dica, data FROM dicas")
            dicas = cursor.fetchall()
            cursor.close()

            st.header('Consultar Dicas e Experiêcias')

            # Converter para DataFrame do pandas
            colunas = ['Categoria', 'Titulo_Dica', 'Desc_Dica', 'Data']
            df_dicas = pd.DataFrame(dicas, columns=colunas)

            # Filtrar por categoria (multiselect)
            categorias_selecionadas = st.multiselect('Selecione as Categorias:', df_dicas['Categoria'].unique())

            # Adicionar filtro de intervalo de tempo
            intervalo_dias = st.slider('Selecione o Intervalo de Tempo (Dias):', 1, 30, 7)
            data_inicio = datetime.now() - timedelta(days=intervalo_dias)

            # Filtrar as dicas com base nas categorias selecionadas e no intervalo de tempo
            df_dicas = df_dicas[(df_dicas['Categoria'].isin(categorias_selecionadas)) & (df_dicas['Data'] >= data_inicio.date())]

            # Exibir dicas das categorias selecionadas e intervalo de tempo
            categorias_str = ', '.join(map(str, categorias_selecionadas))  # Converter lista para string
            st.subheader(f'Dicas das Categorias: {categorias_str} nos últimos {intervalo_dias} dias')

            # Filtrar por palavra-chave
            palavra_chave = st.text_input('Digite uma Palavra-chave para Filtrar:', '')
            if palavra_chave:
                df_dicas = df_dicas[df_dicas['Titulo_Dica'].str.contains(palavra_chave, case=False) | df_dicas['Desc_Dica'].str.contains(palavra_chave, case=False)]

            # Exibir as dicas em uma lista
            for _, row in df_dicas.iterrows():
                st.write(f'**{row["Categoria"]} - {row["Titulo_Dica"]}**')
                st.write(row["Desc_Dica"])
                st.write("---")
        # Se a opção for "Cadastrar Dicas e Experiências"
        elif opcao == "Cadastrar Dicas e Experiências":
            st.header('Cadastrar/Compartilhar Dicas e Experiências')

            # Adicionar campos para o cadastro de dica
            categoria = st.text_input('Categoria:')
            titulo_dica = st.text_input('Título da Dica:')
            desc_dica = st.text_area('Descrição da Dica:')
            data = datetime.now().date()  # Data atual

            # Adicionar botão para salvar a dica
            if st.button('Compartilhar Dica'):
                cursor = conn.cursor()
                cursor.execute("INSERT INTO dicas (categoria, titulo_dica, desc_dica, data) VALUES (?, ?, ?, ?)", (categoria, titulo_dica, desc_dica, data))
                conn.commit()
                cursor.close()
                st.success('Dica compartilhada com sucesso!')




def home():
    st.header("Bem-vindo ao WiseSpend!")
    st.subheader("Transformando Tecnologia em Sustentabilidade Ambiental")
    
    st.markdown("Explore o futuro sustentável, onde a tecnologia se une à preservação do meio ambiente.")
    st.markdown("Descubra como você pode fazer a diferença, adotando práticas eco-friendly no seu dia a dia.")

    st.markdown("🌿 Monitoramento de Consumo Energético")

    text1 = '''Visualize e compreenda seu consumo de energia. 
            Identifique padrões de uso, reduza o desperdício e tome o controle para uma vida mais eficiente e sustentável.'''
    st.markdown(text1)

    st.markdown("♻️ Gerenciamento de Resíduos")
    text2 = '''Acompanhe seus hábitos de geração de resíduos. 
            Receba dicas personalizadas de reciclagem e redução para minimizar seu impacto no planeta.'''
    st.markdown(text2)

    st.markdown("🎮 Módulo Recompensas Sustentáveis")
    text3 = '''Adote práticas sustentáveis e seja recompensado! 
            Participe da gameficação para reduzir seu consumo energético.'''
    st.markdown(text3)

    st.markdown("🤝 Compartilhamento de Dicas e Experiências")
    text4 = '''Conecte-se com outros usuários, compartilhe dicas e experiências sustentáveis. 
            Juntos, promovemos a colaboração e aprendizado mútuo para um futuro mais verde.'''
    st.markdown(text4)

    st.markdown("📊 Análise de Dados e Relatórios")
    text5 = '''Avalie seu progresso de maneira intuitiva. 
            Analise dados sobre sua redução de consumo e emissões para entender o impacto positivo que você está fazendo no mundo.'''
    st.markdown(text5)

    st.markdown("Faça parte da revolução verde!")
    st.markdown("Embarque na jornada rumo a um futuro mais sustentável. Cada pequena ação conta! 🌍✨")
    
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
def main():
    # Conectar ao banco de dados MySQL
    conn = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        database='wisespend'
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
        home()
    elif selected_option == "Consumo Energético":
        st.header("Consumo Energético") 
    elif selected_option == "Gerenciamento de Resíduos":
        st.header("Gerenciamento de Resíduos") 
    elif selected_option == "Recompensas Sustentáveis":
        st.header("Recompensas Sustentáveis") 
    elif selected_option == "Dicas e Experiências":
        compartilhar_dicas_e_experiencias(conn) 
    elif selected_option == "Relatórios":
        st.header("Relatórios") 
    
if __name__ == "__main__":
    main()

