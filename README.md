# VaR-Model

## Introduction

Value at Risk is a metric that attempts to describe the risk of a portfolio. In this repository, the purpose was to design a risk calculation system that could take several options and stocks with different positions, and compute Value at risk for such a portfolio using different VaR calculation methodology.

This risk calculation system makes good estimates about the risk of a portfolio. It covers three types of VaR: parametric VaR, historical VaR and Monte Carlo VaR. The system could take any amount in long or short position in stocks and options to calculate all three types of VaRs.

The data is taken from Bloomberg saved in the form of excel files.


## Background

### Parametric VaR

Parametric VaR is an approximation methodology that makes simplifying assumptions so as to yield a formula for the VaR based on approximate mean and variance calculations. First, we yield the corresponding estimated mean and variance of the portfolio. The mean and variance are based on either an equal weighting over a given window length or weighted exponentially where the weights decay at a given rate or “weight”.  Then we calculated VaR using formulas as follows. The limitation of parametric VaR is that it is only accurate when positions and payoffs are linear.

When calculating Parametric VaR, we consider two different approaches. One is assuming the portfolio follows Geometric Brownian Motion (GBM). The other is assuming each underlying stock or option follows GBM. In the case, we further assume the value of a portfolio that includes these underlying assets following GBM at time t is normally distributed. These assumptions allow us to estimate it by computing its mean and variance.

### Monte Carlo VaR

Monte Carlo VaR simulates the risk factors and use the prices to directly compute the VaR. It is not really a model or type, but a numerical method applied to the problem. It is rather straightforward to compute, and it is correct for nonlinear payoffs. If positions and payoffs are linear and normally distributed, then the VaR calculated by Monte Carlo simulation could be almost the same as parametric VaR.

In this risk calculation system, the Monte Carlo method could calculate VaR both assuming the portfolio following GBM and each asset following GBM.

### Historical VaR

Historical VaR assumes risk factors follow actual historical distributions. The simplicity of this model is that it doesn’t make any assumptions about distribution of historical changes. The assumption is that today's distribution of market changes is the same as historical distribution of market changes. For each day of history, we simply apply that day's change to today.

The difference here to consider is whether we are going to use absolute change or relative change. If the historical value is low and current value is high, absolute would yield little changes, but relative would yield huge changes. Conversely, if the historical value is high and current value is low, absolute causes huge changes, but relative would yield little changes.

For this model particularly, it is very important to have sufficient amount of data. We would definitely like to have more data so that we could be able to observe the rare events. At the same time, we should be very careful with how long the history we plan to look at -- we do not want to build our current risk estimates over some market that is too old.

### Delta Approximation

Another thing done with the data set is to consider the relationship between stocks and options. Intuitively, we think they may not be comparable, so it would be better if we could convert the options somehow so that it would be comparable with the stock prices. The method adapted is using a delta approximation. 

The adjustment was achieved by using formulas from Black Scholes. Delta, which is given by dV/dS represents the change in the value of an option, denoted as dV, with respect to a change in the stock price, denoted as dS. When we calculating the VaRs and taking options into considerations, the ultimate goal here is to get the changes in the options values. A common way to do it is to multiply the shares of an option to the change in the option’s price. So, in order to get the change in the value of the option dV, we’ll just look at Delta*dV. The Black Scholes formula for a 75-strike ATM call option gives a price of $6.15 and a delta of 0.55. If we want to invest $1,000 into these options, we can purchase 162.65 call options. Alternatively, we could purchase 162.6 * 0.55 = 89.43 shares of the underlying stock. If in 5 days, the price of the stock goes up to $76, the value of the option then goes to $6.685 and the profit on the 162.65 call options is about $87.31, compared to the profit on 89.43 shares of the stock which would be $89.43. As you can see, they are not equal, however it is close and the accuracy of this approximation will depend on parameters such as the stock price, risk free rate and volatility of the underlying stock.

## File Structure

### Inputs

#### Inputs.csv

All parameters that would be used in the model, including the VaR type, starting position, risk free rate, a switch to choose from windowing or exponential weighting to calculate μ and σ, window length/weight, VaR horizon, VaR percentile, Evaluation Horizon, and also number of simulation used when calculating Monte Carlo VaR.

#### Stock_Inputs.csv

This datafile contains necessary data of stocks that needed to be assigned for backtesting. Data includes Ticker (stocks), Position (Long or Short), and weights in the portfolio (number from 0 to 1, negative for short positions). Note that the combined weights of the stocks and options must sum up to 1

#### Option_Inputs.csv

This datafile contains necessary data of options that needed to be assigned for backtesting. Data includes Tickers (options), Type (Call or Put), and weights in the portfolio (number from 0 to 1). Note that the combined weights of the stocks and options must sum up to 1

### Code

1. The “Interface”
* main.py: Work with all the functions below. Contain all functions that could take test data and take corresponding functions to compute the the results. To change assumptions and inputs, they can simply be changed in the excel input files mentioned above, then re-run using this file.

2. Loading Data
* loadInputs.py: Reads in the Inputs file from Inputs.csv. Reads in inputs such as the starting position of the portfolio, risk free rate for option pricing, method of parameter calculations (window length or exponential) and the window length or weight. It also loads in necessary VaR parameters such as horizon, percentile, evaluation horizon and number of simulations for Monte Carlo VaR. 
* loadOptionInputs.py: Reads in the Option_Inputs.csv file from the Inputs folder. Reads in inputs such as the tickers of the underlying options the portfolio, type of option (call or put), position in the option (long or short),option maturity and weight of the option in the portfolio. Note that the combined weights of the stocks and options must sum up to 1.
* loadStocksInputs.py: Reads in the Stock_Inputs.csv file from the Inputs folder. Reads in inputs such as the tickers of stocks in the portfolio, the positions (long or short) and its weights in the portfolio. Weights are positive for long positions, negative for short positions.
* loadOptions.py: Reads in the option data for the options in the portfolio. That includes the implied vol and dates. For option price, we calculate it using Black-Scholes formula in the optionCalculator.py function. 
* loadPrices.py: Reads in the historical stock prices for each stock in the portfolio. The input of this function is a list of tickers output from the loadStockInputs function, and the return will be the historical stock price data and corresponding dates for each stock.
* optionCalculator.py: Calculates call and put option prices and deltas based on Black-Scholes.
* calibratePortfolio.py: Calibrate the portfolio by aligning each constituent's dates with each other. So if one stock has a lot more history than another, the older dates get cut off so that everything runs over the same date range.  Calculate the portfolio value according to the weights of each constituent. It is then used for the calculations considering the portfolio following GBM. Also, in this file, the optionCalculator.py is being used to calculate the price of the option, how many options we need to buy and then calculates the delta to determine how many "shares" to buy. 

3. Estimations
* parameterGBM.py: assuming underlying stocks/options following GBM or portfolio following GBM, calculating the corresponding parameters including returns, mu and sigma using windowing or exponential weighting. The function will run the appropriate method based on the input by the user.
* winEstGBM.py: Estimating the corresponding parameters including returns, mu and sigma using windowing weighting. 
* expEstGBM.py: Estimating the corresponding parameters including returns, mu and sigma using exponential weighting.

4. VaR Calculation
* ParVaR.py: Calculate parametric VaR under underlying asset following GBM assumption. Also calculate corresponding option prices (when backtesting includes options) and adjust option shares using delta approximation.
* gbmVaR.py: Calculate parametric VaR under portfolio following GBM assumption. Taking estimates such as initial value, mu and sigma, percentile and etc as inputs. Uses the total portfolio value calculated in calibratePortfolio.py.
* HisVaR.py: Calculate Historical VaR using relative changes in each underlying stock or option in the portfolio. Also calculate corresponding option prices (when backtesting includes options) and adjust option shares using delta approximation.
* MCVaR.py: Calculate Monte Carlo VaR under underlying stocks following GBM assumption and the portfolio following GBM assumption. Also calculate corresponding option prices (when backtesting includes options) and adjust option shares using delta approximation.

5. Backtesting
* backtest.py: The exceptions function looks in a one year window to calculate how many exceptions are hit. Compares the actual loss of the portfolio in a given horizon to the input VaR. The backtest function then sums up the exceptions in each rolling 1 year window for a given evaluation range(5 years, 10 years etc.). It takes the stock prices, the calculated VaR, the weights of the portfolio, the horizon for the VaR, and the starting position. The exceptions function also takes in a start date variable in order to properly index the stock price vectors. It returns a vector of exceptions in each rolling 1 year window over a evaluation period.

6. Plot
* graphResults.py: Generate one plot for VaR compared to the actual loss, and another plot for the exceptions hit in each rolling window output from the backtesting.
