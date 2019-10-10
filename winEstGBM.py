import numpy as np
from scipy.signal import lfilter


def winEstGBM(prices, windowLength):
    rtn = -np.diff(np.log(prices), 1)
    rtnsq = rtn * rtn

    w = 1.0 / windowLength * np.ones(windowLength)

    mubar = lfilter(w, 1, np.flip(rtn, 0))
    mubar = mubar[-1:windowLength:-1]

    x2bar = lfilter(w, 1, np.flip(rtnsq, 0))
    x2bar = x2bar[-1:windowLength:-1]

    var = x2bar - mubar * mubar
    sigmabar = np.sqrt(var)  # figure out?

    sigma = sigmabar * np.sqrt(252)
    mu = mubar * 252 + sigma * sigma * 0.5

    return rtn, mu, sigma
