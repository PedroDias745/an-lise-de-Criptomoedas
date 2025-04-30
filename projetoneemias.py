import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Função para obter dados históricos da Binance
def get_historical_data_binance(symbol='BTCUSDT', interval='1d', limit=30):
    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol.upper(),
        'interval': interval,
        'limit': limit
    }
    response = requests.get(url, params=params)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['price'] = df['close'].astype(float)
    df = df[['date', 'price']]
    return df

# Configuração da página
st.set_page_config(page_title="Dashboard de Criptomoedas", page_icon="📊", layout="wide")

# Sidebar
st.sidebar.header("Configurações de Exibição")
coin = st.sidebar.selectbox("Escolha uma criptomoeda:", 
    ['bitcoin', 'ethereum', 'ripple', 'dogecoin', 'litecoin', 'cardano', 
     'polkadot', 'binancecoin', 'solana', 'avalanche', 'chainlink', 
     'shiba-inu', 'uniswap', 'matic', 'terra-luna', 'cosmos', 'vechain', 
     'algorand', 'stellar', 'bitcoin-cash'], key="coin_select")
days = st.sidebar.slider("Escolha o número de dias para exibir:", min_value=1, max_value=365, value=30, key="days_slider")

# Mapeamento das moedas para os símbolos da Binance
coin_symbol_map = {
    'bitcoin': 'BTCUSDT',
    'ethereum': 'ETHUSDT',
    'ripple': 'XRPUSDT',
    'dogecoin': 'DOGEUSDT',
    'litecoin': 'LTCUSDT',
    'cardano': 'ADAUSDT',
    'polkadot': 'DOTUSDT',
    'binancecoin': 'BNBUSDT',
    'solana': 'SOLUSDT',
    'avalanche': 'AVAXUSDT',
    'chainlink': 'LINKUSDT',
    'shiba-inu': 'SHIBUSDT',
    'uniswap': 'UNIUSDT',
    'matic': 'MATICUSDT',
    'terra-luna': 'LUNAUSDT',
    'cosmos': 'ATOMUSDT',
    'vechain': 'VETUSDT',
    'algorand': 'ALGOUSDT',
    'stellar': 'XLMUSDT',
    'bitcoin-cash': 'BCHUSDT',
}

# Obter símbolo correto
symbol = coin_symbol_map.get(coin, 'BTCUSDT')

# Título
st.title('📉 Dashboard de Criptomoedas')

# Obtenção dos dados
st.write(f"Obtendo dados para {coin} ({symbol}) nos últimos {days} dias...")
data = get_historical_data_binance(symbol, interval='1d', limit=days)

# Tabela
st.subheader('📊 Tabela de Preços')
st.write(data)

# Estatísticas
st.subheader('📈 Estatísticas de Preço')
latest_price = data['price'].iloc[-1]
st.write(f"Preço atual de {coin.capitalize()}: **${latest_price:.2f} USD**")
percentage_change = ((latest_price - data['price'].iloc[0]) / data['price'].iloc[0]) * 100
st.write(f"Variação de preço nos últimos {days} dias: **{percentage_change:.2f}%**")

# Gráfico
st.subheader(f'📉 Gráfico Interativo de Preço de {coin.capitalize()} nos Últimos {days} Dias')
fig = go.Figure()
fig.add_trace(go.Scatter(x=data['date'], y=data['price'], mode='lines', name=f'Preço {coin.capitalize()}',
                         line=dict(color='#007bff', width=2)))
fig.update_layout(
    title=f'Preço de {coin.capitalize()} ao Longo do Tempo',
    xaxis_title='Data',
    yaxis_title='Preço em USD',
    template='plotly_dark',
    xaxis=dict(tickangle=45),
    hovermode='x unified',
    height=500,
)
st.plotly_chart(fig)

# Rodapé
st.markdown("---")
st.sidebar.markdown("### Sobre o Dashboard")
st.sidebar.markdown("Este dashboard é alimentado pela [API da Binance](https://binance-docs.github.io/apidocs/spot/en/).")
st.sidebar.markdown("Criado com 💙 por Pedro.")
st.markdown("Você pode visualizar o histórico de preços de várias criptomoedas e suas variações.")

# Estilo customizado
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
