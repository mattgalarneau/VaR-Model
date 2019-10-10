import numpy as np
from scipy.stats import norm
from parameterGBM import parameterGBM


def gbmVaR(weights, method, window_length, prices, v0, p, t):
    rtn, mu, sigma = parameterGBM(method, window_length, prices)

    if sum(weights) == -1:
        return v0 * np.exp(sigma * np.sqrt(t) * norm.ppf(p) + (mu - pow(sigma, 2) * 0.5) * t) - v0

    else:
        return v0 - v0 * np.exp(sigma * np.sqrt(t) * norm.ppf(1 - p) + (mu - pow(sigma, 2) * 0.5) * t)

