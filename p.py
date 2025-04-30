import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Função para gráfico com Matplotlib
def matplotlib_graph():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, label='Seno', color='b')
    plt.title('Gráfico de Seno com Matplotlib')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.legend()
    
    st.pyplot(plt)

# Barra lateral
st.sidebar.title('Navegação')
page = st.sidebar.radio("Escolha uma seção:", ['Home', 'Gráficos', 'Sobre'])

# Conteúdo da página
if page == 'Home':
    st.title('Meu Site Melhorado com Streamlit')
    st.write("""
        Bem-vindo ao meu site interativo! Aqui você pode explorar gráficos, interagir com dados e aprender mais sobre o Streamlit.
    """)

    # Caixa de texto
    nome = st.text_input('Qual o seu nome?')

    if nome:
        st.write(f"Olá, {nome}! Seja bem-vindo ao site.")
    
    st.subheader('Escolha uma cor:')
    cor = st.radio("Selecione uma cor favorita", ["Verde", "Azul", "Vermelho", "Preto"])

    if cor:
        st.write(f"Você escolheu a cor {cor}.")

elif page == 'Gráficos':
    st.title('Gráficos Interativos')
    st.write("""
        Aqui você pode visualizar gráficos interativos e explorar diferentes tipos de visualizações.
    """)
    
    st.subheader('Gráfico de Seno com Matplotlib')
    matplotlib_graph()

    st.subheader('Gráfico de Cosseno com Matplotlib')
    x = np.linspace(0, 10, 100)
    y = np.cos(x)

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, label='Cosseno', color='g')
    plt.title('Gráfico de Cosseno')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.legend()

    st.pyplot(plt)

elif page == 'Sobre':
    st.title('Sobre o Streamlit')
    st.write("""
        O Streamlit é uma biblioteca Python de código aberto que permite criar aplicativos web interativos de maneira rápida e fácil. 
        É especialmente útil para quem trabalha com dados e deseja criar dashboards e aplicativos com pouco código.
    """)

    st.write("""
        - Criado por: **Adrien Treuille**, **Thiago Teixeira** e **Randall Hunt**.
        - Primeira versão lançada em: **2019**.
        - A principal vantagem é que é fácil de aprender e usar.
    """)

    st.subheader('Funcionalidades do Streamlit')
    st.write("""
        - Criação de interfaces com apenas algumas linhas de código.
        - Suporte a gráficos e visualizações interativas.
        - Integração simples com bibliotecas como pandas, matplotlib, etc.
    """)

# Footer com informações de contato
st.sidebar.markdown("---")
st.sidebar.write("Feito com 💻 e Streamlit.")