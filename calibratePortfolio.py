import numpy as np
from optionCalculator import bs_call, bs_put, delta_call, delta_put

# Function: calibratePortfolio

# Author: Matthew Galarneau

# Purpose: Calibrate the portfolio by aligning each constituent's stock_dates with each other.
#   Calculate the portfolio value according to the weights of each constituent.
#   Only dealing with the equity part of the portfolio

# Inputs: Historical stock prices and stock_dates from the loadPrices function.
#       Stock positions, weights and the starting portfolio value

# Returns: The value of the portfolio and its corresponding date


def calibratePortfolio(stocks, options, option_type, option_wgt, r, prices, stock_dates, option_dates, weights, implied_vol, starting_val):
    min_stock_dates = [None] * (len(stock_dates) + len(option_dates))
    shares = [None] * len(prices)
    new_prices = [None] * len(prices)
    new_iv = [None] * len(implied_vol)
    new_stock_dates = [None] * len(stock_dates)

    # determine what is the first date for each stock
    for i in range(len(stock_dates)):
        min_stock_dates[i] = min(stock_dates[i])

    for i in range(len(option_dates)):
        min_stock_dates[i + len(stock_dates)] = min(option_dates[i])

    # pick the latest of the min stock_dates as the starting date
    startDate = max(min_stock_dates)

    # remove any price/date info that is earlier than the start date
    for j in range(len(prices)):
        new_prices[j] = prices[j][np.where(stock_dates[j] >= startDate)]
        new_stock_dates[j] = stock_dates[j][np.where(stock_dates[j] >= startDate)]

    if len(options) > 0:
        for j in range(len(implied_vol)):
            new_iv[j] = implied_vol[j][np.where(option_dates[j] >= startDate)]

    # calculate the number of shares needed in the portfolio based on the weights
    # based on the prices 3 years after the start date
    # the shares will be positive or negative depending on the position
    for k in range(len(new_prices)):
        if sum(weights) == -1:
            shares[k] = -1 * weights[k] * starting_val / new_prices[k][-(252 * 3)]
        else:
            shares[k] = weights[k] * starting_val / new_prices[k][-(252 * 3)]
        if len(options) > 0:
            if stocks[k] in options:
                option_index = np.where(options == stocks[k])[0][0]
                if option_type[option_index] == "Call":
                    option_price = bs_call(new_prices[k], new_prices[k], r, new_iv[option_index])
                    option_delta = delta_call(new_prices[k], new_prices[k], r, new_iv[option_index])
                    option_shares = starting_val * option_wgt[option_index] / option_price * option_delta
                    shares[k] += option_shares[-(252 * 3)]
                else:
                    option_price = bs_put(new_prices[k], new_prices[k], r, new_iv[option_index])
                    option_delta = delta_put(new_prices[k], new_prices[k], r, new_iv[option_index])
                    option_shares = starting_val * option_wgt[option_index] / option_price * option_delta
                    shares[k] += option_shares[-(252 * 3)]

    # calculate the portfolio value
    # set the portfolio stock_dates
    portDt = new_stock_dates[0]
    portVal = np.array([0] * len(portDt))

    for i in range(len(prices)):
        for j in range(len(portDt)):
            portVal[j] += shares[i] * new_prices[i][j]
    return new_prices, portVal, portDt




