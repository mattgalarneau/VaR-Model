import numpy as np
from scipy.signal import lfilter


def expEstGBM(prices, weight):
    rtn = -np.diff(np.log(prices), 1)
    rtnsq = rtn * rtn

    windowLength = int(np.ceil(np.log(0.01) / np.log(weight)))

    if windowLength > 5000:
        windowLength = 5000

    w = np.power(weight, range(1, windowLength))
    w = w / sum(w)

    mubar = lfilter(w, 1, np.flip(rtn, 0))
    mubar = mubar[-1:windowLength:-1]

    x2bar = lfilter(w, 1, np.flip(rtnsq, 0))
    x2bar = x2bar[-1:windowLength:-1]

    var = x2bar - mubar * mubar
    sigmabar = np.sqrt(var)  # figure out?

    sigma = sigmabar * np.sqrt(252)
    mu = mubar * 252 + sigma * sigma * 0.5

    return rtn, mu, sigma
