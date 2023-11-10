import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import calendar

# Function to authenticate and get Google Sheets data
def get_google_sheets_data():
    sheet_url = 'https://docs.google.com/spreadsheets/d/1kQ1hpvqYTJJEjAlK5IvR-I6Dv56tv_Qq/edit#gid=765041942'
    url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
    df = pd.read_csv(url_1)
    return df

def candlestick(ticker, day):
    ############################
    # === Candlestick chart == #
    ############################

    start_date = datetime.datetime(2023, 11, 9)
    end_date = start_date + datetime.timedelta(days=1)

    # Define the ticker symbol for E-mini S&P 500 (ES)
    ticker_symbol = "^SPX"

    # Download 5-minute candles data from Yahoo Finance
    data = yf.download(ticker_symbol, start=start_date, end=end_date, interval="5m")

    # Extract data within the specified time range (9:30 to 10:25)
    time_range_data = data.between_time('09:30', '10:25')

    # Find the max of high and low, and min of high and low
    max_high_low = time_range_data[['High', 'Low']].max(axis=1).max()
    min_high_low = time_range_data[['High', 'Low']].min(axis=1).min()

    # Find the max of close and open, and min of close and open
    max_close_open = time_range_data[['Close', 'Open']].max(axis=1).max()
    min_close_open = time_range_data[['Close', 'Open']].min(axis=1).min()

    # Entry point data (replace these with your actual entry point values)
    entry_time = '2023-11-09 10:50:00-05:00'
    entry_price = 4391.5

    # Example stop loss and take profit values (replace with your actual values)
    stop_loss = 4399.5
    take_profit = 4368

    fig = make_subplots(rows=1, cols=1)

    # Add candlestick trace
    fig.add_trace(go.Candlestick(x=data.index,
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close']),
                  row=1, col=1)

    # Add horizontal lines for the max of close and open and min of close and open
    fig.add_shape(go.layout.Shape(
        type="line",
        x0=data.index.min(),
        x1=data.index.max(),
        y0=max_close_open,
        y1=max_close_open,
        line=dict(color="red", dash="dot"),
    ))

    fig.add_shape(go.layout.Shape(
        type="line",
        x0=data.index.min(),
        x1=data.index.max(),
        y0=min_close_open,
        y1=min_close_open,
        line=dict(color="red", dash="dot"),
    ))

    # Add white lines for the max of high and low and min of high and low
    fig.add_shape(go.layout.Shape(
        type="line",
        x0=data.index.min(),
        x1=data.index.max(),
        y0=max_high_low,
        y1=max_high_low,
        line=dict(color="white"),
    ))

    fig.add_shape(go.layout.Shape(
        type="line",
        x0=data.index.min(),
        x1=data.index.max(),
        y0=min_high_low,
        y1=min_high_low,
        line=dict(color="white"),
    ))

    # Add marker for entry point
    fig.add_trace(go.Scatter(x=[entry_time],
                             y=[entry_price],
                             mode='markers',
                             marker=dict(color='white', size=10),
                             name='Entry Point'))

    # Add red box from entry to stop loss
    fig.add_shape(go.layout.Shape(
        type="rect",
        x0=entry_time,
        x1=data.index.max(),
        y0=entry_price,
        y1=stop_loss,
        fillcolor="red",
        opacity=0.3,
        layer="below",
        line=dict(color="red"),
    ))

    # Add green box from entry to take profit
    fig.add_shape(go.layout.Shape(
        type="rect",
        x0=entry_time,
        x1=data.index.max(),
        y0=entry_price,
        y1=take_profit,
        fillcolor="green",
        opacity=0.3,
        layer="below",
        line=dict(color="green"),
    ))

    # Add light grey box between the dotted red lines from 9:30 to 10:25
    fig.add_shape(go.layout.Shape(
        type="rect",
        x0=data.index.min(),
        x1='2023-11-09 10:25:00-05:00',
        y0=min_close_open,
        y1=max_close_open,
        fillcolor="lightgrey",
        opacity=0.3,
        layer="below",
        line=dict(color="lightgrey", dash="dot"),
    ))

    # Update layout
    fig.update_layout(title_text='Candlestick Chart', xaxis_rangeslider_visible=False)

    # Display the chart
    st.plotly_chart(fig)

# Function to create a formatted calendar for a specific month and year
def create_month_calendar(year, month):
    cal_data = calendar.monthcalendar(year, month)

    # Convert the data to a Pandas DataFrame
    df = pd.DataFrame(cal_data, columns=['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'])

    return df

def main():
    st.set_page_config('Dashboard', page_icon="🧊", layout='wide')
    st.title('Log')
    df = get_google_sheets_data()
    st.dataframe(df, hide_index=True)

    st.divider()

    with st.container():
        st.write("##### Calendar Controls")
        c1, c2, c3 = st.columns(3)
        yy = c1.selectbox("Select Year", list(range(2020, 2031)), index=3)
        mm = c2.selectbox("Select Month", list(calendar.month_name)[1:], index=10)
        dd = c3.selectbox("Select Day", list(calendar.day_abbr)[0:5])

        # Sidebar controls for month and year
    st.write(f"## Calendar for {mm} {yy}")
    # Display the calendar for the selected year and month

    st.dataframe(create_month_calendar(yy, list(calendar.month_name).index(mm)), hide_index=True,use_container_width=True)       

if __name__ == "__main__":
    main()
