import numpy as np
from optionCalculator import bs_call, bs_put, delta_call, delta_put

# Function: exceptions, backtest

# Author: Matthew Galarneau

# Purpose: The exceptions function looks in a one year window to calculate how many exceptions are hit
#   Compares the actual loss of the portfolio in a given horizon to the input VaR

#   The backtest function then sums up the exceptions in each rolling 1 year window for a given evaluation range
#   (5 years, 10 years etc.)

# Inputs: Needed are the stock prices, the calculated VaR, the weights of the portfolio, the horizon for the VaR,
#       and the starting position. The exceptions function also takes in a startdate variable in order to properly
#       index the stock price vectors

# Returns: A vector of exceptions in each rolling 1 year window over a evaluation period


def exceptions(stocks, options, implied_vol, option_type, option_wgt, r, prices, var, weights, horizon, s0, startdate):
    days = int(horizon * 252)  # convert the days into an integer
    number_exceptions = 0
    loss = [0] * 252
    newprices = np.zeros([len(prices), (252 + days)])  # need to create a new price vector in order to re-index
    new_iv = np.zeros([len(prices), (252 + days)])

    for k in range(len(prices)):
        newprices[k] = prices[k][startdate:(startdate + 252 + days)]  # set up these new price vectors. the length
                                                                      # should be 252 plus the VaR horizon
    for k in range(len(implied_vol)):
        new_iv[k] = implied_vol[k][startdate:(startdate + 252 + days)]

    for i in range(252):
        for j in range(len(newprices)):
            shares = s0 * weights[j] / newprices[j]
            if len(options) > 0:
                if stocks[j] in options:
                    option_index = np.where(options == stocks[j])[0][0]
                    if option_type[option_index] == "Call":
                        option_price = bs_call(newprices[j], newprices[j], r, new_iv[option_index])
                        option_delta = delta_call(newprices[j], newprices[j], r, new_iv[option_index])
                        option_shares = s0 * option_wgt[option_index] / option_price * option_delta
                        shares += option_shares
                    else:
                        option_price = bs_put(newprices[j], newprices[j], r, new_iv[option_index])
                        option_delta = delta_put(newprices[j], newprices[j], r, new_iv[option_index])
                        option_shares = s0 * option_wgt[option_index] / option_price * option_delta
                        shares += option_shares

            loss[i] += shares[i + days] * (newprices[j][i + days] - newprices[j][i])  # calculate the total loss of the portfolio
        if loss[i] > var[i + days]:
            number_exceptions += 1  # count the number of exceptions
    return number_exceptions, loss[0]


def backtest(stocks, options, implied_vol, option_type, option_wgt, r, prices, var, weights, horizon, daterange, s0):
    days = int(horizon * 252)
    total_exceptions = [None] * (252 * (daterange - 1) - days + 1)
    loss = [None] * (252 * (daterange - 1) - days + 1)
    for i in range(252 * (daterange - 1) - days + 1):
        total_exceptions[i], loss[i] = exceptions(stocks, options, implied_vol, option_type, option_wgt, r, prices, var[i:(i + 252 + days)], weights, horizon, s0, i)  # for each rolling window, count the number of exceptions
    return total_exceptions, loss
