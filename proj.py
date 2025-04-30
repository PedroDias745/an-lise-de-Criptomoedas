import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.graph_objects as go  # Gráficos interativos
import time

def get_historical_data(coin_id, days=30):
    # A API do CoinGecko retorna dados históricos
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart'
    params = {
        'vs_currency': 'usd',  # moeda para comparação, pode ser BTC, EUR, etc
        'days': days,  # últimos dias de dados (ex: '30' para 30 dias)
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    # Converte para DataFrame
    prices = data['prices']
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    
    # Converte timestamp para data legível
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df[['date', 'price']]
    
    return df

# Configuração inicial do Streamlit
st.set_page_config(page_title="Dashboard de Criptomoedas", page_icon="📊", layout="wide")

# Barra lateral para navegação
st.sidebar.header("Configurações de Exibição")
coin = st.sidebar.selectbox("Escolha uma criptomoeda:", 
    ['bitcoin', 'ethereum', 'ripple', 'dogecoin', 'litecoin', 'cardano', 
     'polkadot', 'binancecoin', 'solana', 'avalanche', 'chainlink', 
     'shiba-inu', 'uniswap', 'matic', 'terra-luna', 'cosmos', 'vechain', 
     'algorand', 'stellar', 'bitcoin-cash'], key="coin_select")
days = st.sidebar.slider("Escolha o número de dias para exibir:", min_value=1, max_value=365, value=30, key="days_slider")

# Estilo do título
st.title('📉 Dashboard de Criptomoedas')

# Obtendo os dados históricos
st.write(f"Obtendo dados para {coin} nos últimos {days} dias...")
data = get_historical_data(coin, days)

# Exibindo os dados em uma tabela
st.subheader('📊 Tabela de Preços')
st.write(data)

# Estatísticas adicionais (preço atual e variação)
st.subheader('📈 Estatísticas de Preço')
latest_price = data['price'].iloc[-1]
st.write(f"Preço atual de {coin.capitalize()}: **${latest_price:.2f} USD**")
percentage_change = ((latest_price - data['price'].iloc[0]) / data['price'].iloc[0]) * 100
st.write(f"Variação de preço nos últimos {days} dias: **{percentage_change:.2f}%**")

# Gráfico interativo de preços
st.subheader(f'📉 Gráfico Interativo de Preço de {coin.capitalize()} nos Últimos {days} Dias')

# Plotando o gráfico com Plotly (gráfico interativo)
fig = go.Figure()

# Adicionando linha de preço
fig.add_trace(go.Scatter(x=data['date'], y=data['price'], mode='lines', name=f'Preço {coin.capitalize()}',
                         line=dict(color='#007bff', width=2)))  # Azul moderno

# Melhorando o layout do gráfico
fig.update_layout(
    title=f'Preço de {coin.capitalize()} ao Longo do Tempo',
    xaxis_title='Data',
    yaxis_title='Preço em USD',
    template='plotly_dark',  # Tema escuro para melhorar a aparência
    xaxis=dict(tickangle=45),  # Inclinação dos rótulos do eixo x
    hovermode='x unified',  # Exibição de valores ao passar o mouse
    height=500,
)

# Exibindo o gráfico interativo
st.plotly_chart(fig)

# Barra de navegação de informações adicionais no rodapé
st.markdown("---")
st.sidebar.markdown("### Sobre o Dashboard")
st.sidebar.markdown("Este dashboard é alimentado pela [API do CoinGecko](https://www.coingecko.com/en/api).")
st.sidebar.markdown("Criado com 💙 por Pedro.")
st.markdown("Você pode visualizar o histórico de preços de várias criptomoedas e suas variações nas últimas 24h.")

# Estilizando a página para cores e melhorias
st.markdown("""
<style>
    .css-18e3th9 {
        background-color: #23272a;
    }
    .css-1v0mbdj {
        color: #007bff;
    }
    .css-10trblm {
        background-color: #2b2d42;
        color: #fff;
    }
    .css-12ttz1f {
        background-color: #f6f7f8;
    }
</style>
""", unsafe_allow_html=True)
