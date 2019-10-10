import pandas as pd
import numpy as np

# Function: loadStockInputs

# Author: Matthew Galarneau

# Purpose: Reads in the Stock_Inputs file from the Inputs folder. Reads in inputs such as the tickers of stocks
#   in the portfolio, the positions (long or short) and its weights in the portfolio.
#   Weights are positive for long positions, negative for short positions

# Inputs: No direct inputs. file "Stock_Inputs.csv" needed in the Inputs folder with appropriate parameters filled in

# Returns: Inputs to be used in other modules


def loadStockInputs():
    stock_inputs = pd.read_csv("Inputs/Stock_Inputs.csv")

    stocks = np.array(pd.Series.tolist(stock_inputs["Ticker"]))
    weights = np.array(pd.Series.tolist(stock_inputs["Weights"]))

    return np.array(stocks), np.array(weights)
