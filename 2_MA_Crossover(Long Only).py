#Strategy Name - 50EMA and 200 EMA Crossover - Long Only

from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import backtrader as bt
from datetime import datetime

class FirstStrategy(bt.Strategy):

    def log(self, txt):
        print(txt)

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.ema50 = bt.indicators.ExponentialMovingAverage(self.datas[0], period=50)
        self.ema200 = bt.indicators.ExponentialMovingAverage(self.datas[0], period=200)


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("Buy executed" + str(order.executed.price))
            elif order.issell():
                self.log("Sell executed" + str(order.executed.price))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order canceled/Margin not sufficient" )


    def next(self):
        if not self.position:
            if self.ema50[0] > self.ema200[0]:
                self.order = self.buy()
                self.log("BUY ORDER CREATED: " +str(self.dataclose[0]))
        else:
            if self.ema50[0] < self.ema200[0]:
                self.close()
                self.log("ORDER EXITED: " +str(self.dataclose[0]))
     

if __name__ == '__main__':

    cerebro = bt.Cerebro()
    cerebro.addstrategy(FirstStrategy)

    datapath = "Data Files/NSE_NIFTY_30min.csv"

    data = bt.feeds.GenericCSVData(
        dataname = datapath,
        fromdate = datetime(2019,1,1),
        todate = datetime(2021,1,1),
        datetime = 0,
        timeframe = bt.TimeFrame.Minutes,
        compression = 1,
        dtformat = ('%Y-%m-%d %H:%M:%S'),
        open = 1,
        high = 2,
        low = 3,
        close = 4,
        volume = None,
        openinterest = None,
        reverse = False,
        header = 0
        )


    cerebro.adddata(data)

    cerebro.addsizer(bt.sizers.FixedSize, stake=75)
    cerebro.broker.setcommission(commission=0.001)

    cerebro.broker.setcash(1000000.00)

    print('Starting portfolio value: ', cerebro.broker.getvalue())

    cerebro.run()

    print('Final portfolio value: ', cerebro.broker.getvalue())

    #cerebro.plot(volume=False)
