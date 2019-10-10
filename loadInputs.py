import pandas as pd
import numpy as np

# Function: loadInputs

# Author: Matthew Galarneau

# Purpose: Reads in the Inputs file from the Inputs folder. Reads in inputs such as the starting position of
#   the portfolio, risk free rate for option pricing,
#   method of parameter calculations (window lenght or exponential) and the window length or weight.
#   VaR parameters such as horizon, percentile, evaluation horizon and number of simulations for Monte Carlo VaR

# Inputs: No direct inputs. file "Inputs.csv" needed in the Inputs folder with appropriate parameters filled in

# Returns: Inputs to be used in other modules


def loadInputs():
    inputs = pd.read_csv("Inputs/Inputs.csv")
    parameters = np.array(pd.Series.tolist(inputs["Value"]))
    s0 = int(parameters[0])
    r = float(parameters[1])
    var_type = parameters[2]
    method = parameters[3]
    window_length = int(parameters[4])
    VaR_Horizon = float(parameters[5])
    VaRp = float(parameters[6])
    evaluation = int(parameters[7])
    simulations = int(parameters[8])

    return s0, r, var_type, method, window_length, VaR_Horizon, VaRp, evaluation, simulations


