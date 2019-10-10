import numpy as np
from scipy.stats import norm

# Function: bs_call, bs_put

# Author: Matthew Galarneau

# Purpose: Calculates call and put option price based on Black-Scholes

# Inputs: Underlying stock price: S
#         Strike price: K
#         Risk free rate: r
#         Implied volatility: sig
#         Time to maturity: t (default at 1)
#         Dividend rate: d (default at 0)

# Returns: Price of call/put


def bs_call(S, K, r, sig, t=1, d=0):
    d1 = (np.log(S / K) + (r - d + sig * sig * 0.5) * t) / (sig * np.sqrt(t))
    d2 = d1 - sig * np.sqrt(t)
    return S * np.exp(-d * t) * norm.cdf(d1) - K * np.exp(-r * t) * norm.cdf(d2)


def bs_put(S, K, r, sig, t=1, d=0):
    d1 = (np.log(S / K) + (r - d + sig * sig * 0.5) * t) / (sig * np.sqrt(t))
    d2 = d1 - sig * np.sqrt(t)
    return K * np.exp(-r * t) * norm.cdf(-d2) - S * np.exp(-d * t) * norm.cdf(-d1)


def delta_call(S, K, r, sig, t=1, d=0):
    d1 = (np.log(S / K) + (r - d + sig * sig * 0.5) * t) / (sig * np.sqrt(t))
    return norm.cdf(d1)


def delta_put(S, K, r, sig, t=1, d=0):
    d1 = (np.log(S / K) + (r - d + sig * sig * 0.5) * t) / (sig * np.sqrt(t))
    return norm.cdf(d1) - 1
