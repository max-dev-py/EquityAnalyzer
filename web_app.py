import streamlit as st
import yfinance as yf
import plotly.graph_objects as go


# --- Page Configuration ---
st.set_page_config(
    page_title="Equity Dividends!",
    # page_icon=":crypto:",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None,
)

st.text_input('Enter ticker symbol:', key="ticker", help="Equity ticker")

if st.session_state.ticker != "":
    ticker = yf.Ticker(st.session_state.ticker)
    info = ticker.info

    st.write(f"**{info['longName']}**")

    dividends = ticker.dividends
    d_last_year = dividends.loc[dividends.index.year == dividends.index.year.max()-1]
    price = info['currentPrice'] if 'currentPrice' in info else info['previousClose']
    st.write(d_last_year.sum(), '/', price, '=', d_last_year.sum() / price *100, '%')

    st.write(dividends.sort_index(ascending=False))

    # st.plotly_chart(ticker.history(period="1y"), y="Close", use_container_width=True)
    history = ticker.history(period="1y")

    fig = go.Figure(
        data=go.Scatter(x=history.index, y=history.Close, mode='lines', name='Цена закрытия')
    )

    fig.update_layout(
        title=f"{ticker.info['longName']} - Цена закрытия за последний год",
        xaxis_title="Дата",
        yaxis_title="Цена закрытия"
    )

    st.plotly_chart(fig)

    st.write(info)
