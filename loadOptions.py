import pandas as pd
import numpy as np
import datetime

# Function: loadOptions

# Author: Matthew Galarneau

# Purpose: Reads in the option data for the options in the portfolio

# Inputs: List of tickers, option types, and maturities output from the loadOptionsInputs function.
#         Risk free rate from loadInputs function

# Returns: Historical option price data, implied volatility and corresponding dates for each stock


def loadOptions(options):
    dates = [None] * len(options)
    implied_vol = [None] * len(options)
    for i in range(len(options)):
        info = pd.read_csv("Stock_Data/" + options[i] + "_OPTION.csv",
                           usecols=["Date", "12MO_PUT_IMP_VOL"], skiprows=1)
        dates[i] = np.array(pd.Series.tolist(info["Date"]))
        dates[i] = [datetime.datetime.strptime(date, '%m/%d/%Y').date() for date in dates[i]]
        dates[i] = [date.strftime('%Y-%m-%d') for date in dates[i]]
        dates[i] = np.array(dates[i])
        implied_vol[i] = np.array(pd.Series.tolist(info["12MO_PUT_IMP_VOL"]))
        dates[i] = dates[i][::-1]  # reverse the order so that the list in reverse chronological order
        implied_vol[i] = implied_vol[i][::-1] / 100  # convert implied vol to decimal

    return np.array(implied_vol), np.array(dates)
