from loadPrices import loadPrices
from calibratePortfolio import calibratePortfolio
from loadOptions import loadOptions
from loadStockInputs import loadStockInputs
from loadOptionInputs import loadOptionInputs
from loadInputs import loadInputs
from gbmVaR import gbmVaR
from ParVaR import ParVaR
from HistVaR import HistVaR
from MCVaR import MonteCarloVaR
from MCVaR_GBM import MonteCarloVaR_GBM
from backtest import backtest
from graphResults import graphResults

# Read Inputs
s0, r, var_type, method, window_length, VaR_Horizon, VaRp, evaluation, simulations = loadInputs()
stocks, stock_weights = loadStockInputs()
options, option_type, option_wgt = loadOptionInputs()

stock_prices, stock_dates = loadPrices(stocks)

implied_vol, option_dates = loadOptions(options)


# Calibrate Portfolio
stock_prices, portVal, portDt = calibratePortfolio(stocks, options, option_type, option_wgt, r, stock_prices, stock_dates, option_dates, stock_weights, implied_vol, s0)

# Calculate VaR, Loss and Backtest
if var_type == 'Par GBM':
    var = gbmVaR(stock_weights, method, window_length, portVal, s0, VaRp, VaR_Horizon)
    bt, loss = backtest(stocks, options, implied_vol, option_type, option_wgt, r, stock_prices, var, stock_weights, VaR_Horizon, evaluation, s0)
elif var_type == 'Par BM':
    var = ParVaR(stocks, options, option_type, option_wgt, implied_vol, r, stock_prices, stock_weights, s0, VaR_Horizon, window_length, evaluation, VaRp, method)
    bt, loss = backtest(stocks, options, implied_vol, option_type, option_wgt, r, stock_prices, var, stock_weights, VaR_Horizon, evaluation, s0)
elif var_type == 'Hist':
    var = HistVaR(stocks, options, implied_vol, option_type, option_wgt, r, stock_prices, stock_weights, s0, VaR_Horizon, window_length, evaluation, VaRp)
    bt, loss = backtest(stocks, options, implied_vol, option_type, option_wgt, r, stock_prices, var, stock_weights, VaR_Horizon, evaluation, s0)
elif var_type == 'MC GBM':
    var = MonteCarloVaR_GBM(portVal, method, window_length, VaR_Horizon, evaluation, VaRp, s0, simulations)
    bt, loss = backtest(stocks, options, implied_vol, option_type, option_wgt, r, stock_prices, var, stock_weights, VaR_Horizon, evaluation, s0)
elif var_type == 'MC BM':
    var = MonteCarloVaR(stocks, options, option_type, option_wgt, implied_vol, r, stock_prices, stock_weights, s0, VaR_Horizon, window_length, evaluation, VaRp, method, simulations)
    bt, loss = backtest(stocks, options, implied_vol, option_type, option_wgt, r, stock_prices, var, stock_weights, VaR_Horizon, evaluation, s0)
else:
    print('Incorrect VaR Type. Check Inputs')

#Graph Results
graphResults(portDt, var, loss, bt)
