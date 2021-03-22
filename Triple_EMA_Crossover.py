from __future__ import (absolute_import, division, print_function, unicode_literals)
from datetime import datetime
import backtrader as bt
import csv

class FirstStrategy(bt.Strategy):

    params = (
        ('period1', 13),('period2', 55),('period3',144 )
        )

    def log(self, txt):
        print(txt)

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.ema1 = bt.indicators.EMA(self.datas[0], period = self.params.period1)
        self.ema2 = bt.indicators.EMA(self.datas[0], period = self.params.period2)
        self.ema3 = bt.indicators.EMA(self.datas[0], period = self.params.period3)
        self.bias = 0
        self.mylog = []

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
        #self.log("Close: "+str(self.dataclose[0]))
        if not self.position:
            if self.dataclose[0] > self.ema3[0]:
                if self.ema1[-1] < self.ema2[-1] and self.ema1[0] > self.ema2[0]:
                    self.order = self.buy()
                    self.log("Long ORDER INITIATED:" + str(self.dataclose[0]))
                    self.bias = 1

            if self.dataclose[0] < self.ema3[0]:
                if self.ema1[-1] > self.ema2[-1] and self.ema1[0] < self.ema2[0]:
                    self.order = self.sell()
                    self.log("\nShort ORDER INITIATED:" + str(self.dataclose[0]))
                    self.bias = -1
                 
            
        else :
            if self.bias == 1:
                if self.ema1[0] < self.ema2[0] or self.dataclose[0] < self.ema3[0]:
                    self.close()
                    self.log("LONG ORDER EXITED:" + str(self.dataclose[0]))
                    self.bias = 0

            if self.bias == -1:
                if self.ema1[0] > self.ema2[0] or self.dataclose[0] > self.ema3[0]:
                    self.close()
                    self.log("SHORT ORDER EXITED:\n" + str(self.dataclose[0]))
                    self.bias = 0

'''
    def stop(self):
        print(("EMA1 : "+ str(self.params.period1)+ ",EMA2 : "+ str(self.params.period2)+",EMA3 : "+ str(self.params.period3)+",Profit/Loss : " + str(int(self.broker.getvalue()-10000000.00))))
        #print(self.mylog)

'''

        
if __name__ == "__main__":

    cerebro = bt.Cerebro()
    cerebro.addstrategy(FirstStrategy, period1 = 13, period2 = 55, period3 = 144 )

    #cerebro.optstrategy(FirstStrategy, period1 = [], period2 = [], period3 = [])
        
    datapath = "Data Files/NSE_NIFTY_30min.csv"

    data = bt.feeds.GenericCSVData(
        dataname = datapath,
        fromdate = datetime(2015,1,1),
        todate = datetime(2021,1,1),
        datetime = 0,
        timeframe = bt.TimeFrame.Minutes,
        compression = 1,
        dtformat = ("%Y-%m-%d %H:%M:%S"),
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
    cerebro.addsizer(bt.sizers.FixedSize, stake=75 )
    cerebro.broker.setcommission(commission = 0.0001)
    cerebro.broker.setcash(1000000.00)

    cerebro.addobserver(bt.observers.Trades)
    cerebro.addobserver(bt.observers.DrawDown)
    cerebro.addobserver(bt.observers.BuySell)

    #Remove the comment below to export results in a csv file.
    #cerebro.addwriter(bt.WriterFile, csv = True, out = "Data Files"+ datetime.now().strftime("%H:%M")+".csv")
    
    starting_port = cerebro.broker.getvalue()

    print("Starting porfolio value is :", cerebro.broker.getvalue())

    cerebro.run()

    ending_port = cerebro.broker.getvalue()
    print("Final porfolio value is :", cerebro.broker.getvalue())
    print("FINAL PROFIT/LOSS : ", str(ending_port-starting_port))
    
    #To plot the trades on a chart. 

    cerebro.plot(volume=False)