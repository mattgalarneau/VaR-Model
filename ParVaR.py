import numpy as np
from scipy.stats import norm
from parameterGBM import parameterGBM
from optionCalculator import bs_call, bs_put, delta_put, delta_call


def ParVaR(stocks, options, option_type, option_wgt, implied_vol, r, prices, weights, s0, horizon, windowlen, daterange, VaRp, method):
    rtn = [None] * len(prices)
    mu = [None] * len(prices)
    sigma = [None] * len(prices)
    shares = [None] * len(prices)
    newprices = [None] * len(prices)
    VaR = [None] * (252 * daterange)

    for j in range(252 * daterange):
        EVt = 0
        EVt_sq = 0

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
        corr_mat = np.corrcoef(corr_vec)

        for k in range(len(prices)):
            EVt += shares[k][0] * newprices[k][0] * np.exp(mu[k][0] * horizon)
            EVt_sq += np.power(shares[k][0], 2) * np.power(newprices[k][0], 2) * np.exp \
                ((2 * mu[k][0] + np.power(sigma[k][0], 2)) * horizon)

        for a in range(len(prices) - 1):
            for b in range(a + 1, len(prices)):
                EVt_sq += 2 * shares[a][0] * shares[b][0] * newprices[a][0] * newprices[b][0] * \
                          np.exp((mu[a][0] + mu[b][0] + corr_mat[a][b] * sigma[a][0] * sigma[b][0]) * horizon)

        varV = EVt_sq - np.power(EVt, 2)
        sdV = np.sqrt(varV)
        if sum(weights) == -1:
            VaR[j] = (EVt - norm.ppf(1 - VaRp) * sdV) - s0
        else:
            VaR[j] = s0 - (EVt - norm.ppf(VaRp) * sdV)

    return VaR
