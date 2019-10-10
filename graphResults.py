import datetime
from matplotlib import pyplot as plt


def graphResults(dates, var, loss, backtest):

    a = dates
    b = []
    l = min(len(var), len(loss), 252 * 20)

    for i in range(l):
        b.append(datetime.datetime.strptime(a[i], "%Y-%m-%d"))

    plt.figure(1)
    plt.plot(b, var[0:l], label="VaR")
    plt.plot(b, loss[0:l], label="Loss")
    plt.legend(bbox_to_anchor=(0.7, 1.0), loc=2, borderaxespad=0, prop={'size': 6})
    plt.title("Portfolio VaR and Loss")
    plt.show()

    b = []
    l = min(len(backtest), 252 * 20)

    for i in range(l):
        b.append(datetime.datetime.strptime(a[i], "%Y-%m-%d"))

    plt.figure(2)
    plt.plot(b, backtest[0:l], label='Exceptions')
    plt.legend(bbox_to_anchor=(0.7, 1.0), loc=2, borderaxespad=0, prop={'size': 6})
    plt.title("Backtest Exceptions")
    plt.show()
