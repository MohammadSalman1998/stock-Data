import yfinance as yf
from django.shortcuts import render, redirect
from .forms import StockForm
import json
import plotly.graph_objs as go
import pandas as pd


def fetch_stock_data(ticker, start_date, end_date):
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        if not stock_data.empty:
            return stock_data
    except Exception:
        pass

    return None



def stock_data_form(request):
    if request.method == "POST":
        ticker = request.POST["ticker"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]

        resChart = plotChartLines(ticker,start_date,end_date)

        stock_data = fetch_stock_data(ticker, start_date, end_date)
        if stock_data is not None and end_date > start_date:
            return render(request, "stockapp/form.html", {"stock_data": stock_data,
                                                          "ticker":ticker,
                                                          "startDate":start_date,
                                                          "endDate":end_date,
                                                          "resChart":resChart
                                                          })
        elif end_date < start_date:
            return render(request, "stockapp/form.html", {"errorInput": "ERROR -End date should be after the start date."})
        else:
            return render(request, "stockapp/form.html", {"errorInput": "ERROR - Verify the input"})
    else:
        form = StockForm()

    return render(request, "stockapp/form.html", {"form": form})



def plotChartLines(ticker, start_date, end_date, interval='1d'):
    data = yf.download(ticker, start=start_date, end=end_date)
    df = pd.DataFrame(data)
    df.reset_index(inplace=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'],y=df['Close'],mode='lines',name='RollingStock'))
    fig.update_xaxes(type='date')
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=7, label='1w', step='day',stepmode='backward'),
                    dict(count=1, label='1m', step='month',stepmode='backward'),
                    dict(count=6, label='6m', step='month',stepmode='backward'),
                    dict(count=1, label='YTD', step='year',stepmode='todate'),
                    dict(count=1, label='1y', step='year',stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider = dict(visible=True),
            type = 'date'
        )
    )
    fig.update_layout(title=ticker)
    json_string = json.dumps(fig.to_json())

    return json_string
