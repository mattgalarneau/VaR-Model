import numpy as np
from optionCalculator import delta_call, delta_put


def HistVaR(stocks, options, implied_vol, option_type, option_wgt, r, prices, weights, s0, horizon, windowlen, daterange, VaRp):
    horizon = int(horizon * 252)
    daterange = daterange * 252
    prices = prices
    VaR_port = [None] * daterange

    for i in range(daterange):
        n = np.ceil((1 - VaRp) * (windowlen - horizon))
        loss_port = 0

        for j in range(len(prices)):
            relativechange_port = (prices[j][:-horizon] / prices[j][horizon:])
            relativechange_port = relativechange_port[i:(i + windowlen - horizon)]
            loss_port += (s0 * weights[j]) * (1 - relativechange_port)
            if len(options) > 0:
                if stocks[j] in options:
                    option_index = np.where(options == stocks[j])[0][0]
                    if option_type[option_index] == "Call":
                        option_delta = delta_call(prices[j][i], prices[j][i], r, implied_vol[option_index][i])
                        loss_port += (s0 * option_wgt[option_index] * option_delta) * (1 - relativechange_port)
                    else:
                        option_delta = delta_put(prices[j][i], prices[j][i], r, implied_vol[option_index][i])
                        loss_port += (s0 * option_wgt[option_index] * option_delta) * (1 - relativechange_port)

        loss_port = sorted(loss_port)

        VaR_port[i] = loss_port[-int(n)]

    return VaR_port
