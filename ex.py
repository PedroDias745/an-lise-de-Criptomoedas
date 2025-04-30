import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

def dados_historicos_binance(symbol='BTCUSDT', interval='1d', limit=30):
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
    
    df['data'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['preco'] = df['close'].astype(float)
    df = df[['data', 'preco']]
    return df

st.set_page_config(page_title="📊 Dashboard Cripto", layout="wide")

st.sidebar.markdown("## ⚙️ Configurações")
coin = st.sidebar.selectbox("Escolha uma criptomoeda:", 
    ['bitcoin', 'ethereum', 'ripple', 'dogecoin', 'litecoin', 'cardano', 
     'polkadot', 'binancecoin', 'solana', 'avalanche', 'chainlink', 
     'shiba-inu', 'uniswap', 'matic', 'terra-luna', 'cosmos', 'vechain', 
     'algorand', 'stellar', 'bitcoin-cash'], key="coin_select")
days = st.sidebar.slider("Dias de histórico:", 1, 365, 30, key="days_slider")

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

symbol = coin_symbol_map.get(coin, 'BTCUSDT')

st.markdown(f"## 📈 {coin.capitalize()} ({symbol}) - Últimos {days} dias")

data = dados_historicos_binance(symbol, '1d', days)

preco_recente = data['preco'].iloc[-1]
primeiro_preco = data['preco'].iloc[0]
variacao_percentual = ((preco_recente - primeiro_preco) / primeiro_preco) * 100

col1, col2 = st.columns(2)
col1.metric(label="💰 Preço Atual (USD)", value=f"${preco_recente:,.2f}")
col2.metric(label="📊 Variação %", value=f"{variacao_percentual:.2f}%", delta=f"{variacao_percentual:.2f}%")

st.markdown("### 📉 Evolução de Preço")
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=data['data'], y=data['preco'],
    mode='lines',
    name=coin.capitalize(),
    line=dict(color='#00bfff', width=3)
))
fig.update_layout(
    template='plotly_dark',
    xaxis_title='Data',
    yaxis_title='Preço em USD',
    hovermode='x unified',
    height=500
)
st.plotly_chart(fig, use_container_width=True)

with st.expander("📋 Ver tabela de dados"):
    st.dataframe(data.style.format({'preco': '${:,.4f}'}), use_container_width=True)

st.markdown("""
<style>
    .stMetric {
        background-color: #2c2f33;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: #ffffff;
    }
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    .css-1v0mbdj {
        font-size: 2rem;
        color: #00bfff !important;
    }
</style>
""", unsafe_allow_html=True)
