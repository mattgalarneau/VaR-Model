import pandas as pd
import numpy as np
import datetime

# Function: loadPrices

# Author: Matthew Galarneau

# Purpose: Reads in the historical stock prices for each stock in the portfolio

# Inputs: List of tickers output from the loadStockInputs function

# Returns: Historical stock price data and corresponding dates for each stock


def loadPrices(stocks):
    dates = [None] * len(stocks)
    price = [None] * len(stocks)

    for i in range(len(stocks)):
        info = pd.read_csv("Stock_Data/" + stocks[i] + ".csv", usecols=["Date", "Adj Close"])
        dates[i] = np.array(pd.Series.tolist(info["Date"]))
        dates[i] = [datetime.datetime.strptime(date, '%m/%d/%Y').date() for date in dates[i]]
        dates[i] = [date.strftime('%Y-%m-%d') for date in dates[i]]
        dates[i] = np.array(dates[i])
        price[i] = np.array(pd.Series.tolist(info["Adj Close"]))

        dates[i] = dates[i][::-1]  # reverse the order so that the list in reverse chronological order
        price[i] = price[i][::-1]

    return np.array(price), np.array(dates)
