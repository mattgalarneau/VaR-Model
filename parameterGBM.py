from winEstGBM import winEstGBM
from expEstGBM import expEstGBM


def parameterGBM(method, window, prices):
    if method == 'Windows':
        rtn, mu, sigma = winEstGBM(prices, window)
    else:
        rtn, mu, sigma = expEstGBM(prices, window)

    return rtn, mu, sigma
