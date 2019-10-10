import numpy as np
from parameterGBM import parameterGBM
from optionCalculator import bs_call, bs_put, delta_call, delta_put


def MonteCarloVaR(stocks, options, option_type, option_wgt, implied_vol, r, prices, weights, s0, horizon, windowlen, daterange, VaRp, method, simulations):
    rtn = [None] * len(prices)
    mu = [None] * len(prices)
    sigma = [None] * len(prices)
    shares = [None] * len(prices)
    newprices = [None] * len(prices)
    VaR = [None] * (252 * daterange)
    nVaR = int(np.ceil((1 - VaRp) * simulations))

    for j in range(252 * daterange):
        V = 0

        for i in range(len(prices)):
            rtn[i], mu[i], sigma[i] = parameterGBM(method, windowlen, prices[i])
            if sum(weights) == -1:
                shares[i] = -1 * weights[i] * s0 / prices[i]
            else:
                shares[i] = weights[i] * s0 / prices[i]
                if len(options) > 0:
                    if stocks[i] in options:
                        option_index = np.where(options == stocks[i])[0][0]
                        if option_type[option_index] == "Call":
                            option_price = bs_call(prices[i], prices[i], r, implied_vol[option_index])
                            option_delta = delta_call(prices[i], prices[i], r, implied_vol[option_index])
                            option_shares = s0 * option_wgt[option_index] / option_price * option_delta
                            shares[i] += option_shares
                        else:
                            option_price = bs_put(prices[i], prices[i], r, implied_vol[option_index])
                            option_delta = delta_put(prices[i], prices[i], r, implied_vol[option_index])
                            option_shares = s0 * option_wgt[option_index] / option_price * option_delta
                            shares[i] += option_shares

            rtn[i] = rtn[i][j:(j + windowlen)]
            mu[i] = mu[i][j:(j + windowlen)]
            sigma[i] = sigma[i][j:(j + windowlen)]
            shares[i] = shares[i][j:(j + windowlen)]
            newprices[i] = prices[i][j:(j + windowlen)]

        corr_vec = np.vstack([rtn])
        corr_mat = np.corrcoef(corr_vec) * horizon

        W = np.random.multivariate_normal([0] * len(newprices), corr_mat, simulations)

        for k in range(len(prices)):
            V += shares[k][0] * newprices[k][0] * np.exp(
                (mu[k][0] - np.power(sigma[k][0], 2) / 2) * horizon + sigma[k][0] * W[:, k])

        V = sorted(V)
        if sum(weights) == -1:
            VaR[j] = V[len(V) - nVaR] - s0
        else:
            VaR[j] = s0 - V[nVaR - 1]

    return VaR
