import numpy as np
from parameterGBM import parameterGBM


def MonteCarloVaR_GBM(portVal, method, windowLen, horizon, evaluation, VaRp, s0, number_reps):
    rtn, mu, sigma = parameterGBM(method, windowLen, portVal)

    VaR = [None] * 252 * evaluation

    W = np.random.normal(0, np.sqrt(horizon), number_reps)

    nVaR = int(np.ceil((1 - VaRp) * number_reps))

    for i in range(252 * evaluation):
        V = s0 * np.exp((mu[i] - sigma[i] * sigma[i] / 2) * horizon + sigma[i] * W)
        V = sorted(V)
        VaR[i] = s0 - V[nVaR - 1]

    return VaR
