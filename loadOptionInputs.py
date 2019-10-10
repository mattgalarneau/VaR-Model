import pandas as pd
import numpy as np

# Function: loadOptionInputs

# Author: Matthew Galarneau

# Purpose: Reads in the Option_Inputs file from the Inputs folder. Reads in inputs such as the tickers
#   of the underlying options the portfolio, type of option (call or put), position in the option (long or short),
#   option maturity and weight of the option in the portfolio. Note that the combined weights of the stocks and options
#   must sum up to 1

# Inputs: No direct inputs. file "Option_Inputs.csv" needed in the Inputs folder with appropriate parameters filled in

# Returns: Inputs to be used in other modules


def loadOptionInputs():
    option_inputs = pd.read_csv("Inputs/Option_Inputs.csv")

    option = np.array(pd.Series.tolist(option_inputs["Ticker"]))
    option_type = np.array(pd.Series.tolist(option_inputs["Type"]))
    option_wgt = np.array(pd.Series.tolist(option_inputs["Weight"]))

    return option, option_type, option_wgt
