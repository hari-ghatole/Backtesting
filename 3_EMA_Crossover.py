from __future__ import (absolute_import, division, print_function, unicode_literals)
from datetime import datetime
import backtrader as bt
import csv

class FirstStrategy(bt.Strategy):

    params = (
    ('period_short', 25 ),('period_medium', 50),('period_long',110 ),
    
    )
        

    def log(self, txt):
        print(txt)

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.ema_short = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.period_short)
        self.ema_medium = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.period_medium)
        self.ema_long = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.period_long)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        
        if order.status in [order.Completed]:
            if order.isbuy():
                pass
                #self.log("Buy executed" + str(order.executed.price))
            elif order.issell():
                pass
                #self.log("Sell executed" + str(order.executed.price))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order canceled/Margin not sufficient" )


    def next(self):


        self.current_date_string = self.datas[0].datetime.date(0).strftime("%Y %m %d")
        self.current_time_string = self.datas[0].datetime.time(0).strftime("%H:%M")


        #self.log("Close: "+str(self.dataclose[0]))
        if not self.position:      
            if self.ema_short[0] > self.ema_medium[0] and self.dataclose[0] > self.ema_long[0]:
                self.order = self.buy()
                self.log("=== LONG ORDER INITIATED ===: " + str(self.dataclose[0]) + ", " + self.current_date_string + " " + self.current_time_string)
            if self.ema_short[0] < self.ema_medium[0] and self.dataclose[0] < self.ema_long[0]:
                self.order = self.sell()
                self.log("=== SHORT ORDER INITIATED ===:" + str(self.dataclose[0]) + ", " + self.current_date_string + " " + self.current_time_string)
        else:
            if self.order.isbuy():
                if self.ema_short[0] < self.ema_medium[0]:
                    self.close()
                    self.log("Long exited" + ", " + self.current_date_string + " " + self.current_time_string)
                    self.log(" ")
            if self.order.issell():
                if self.ema_short[0] > self.ema_medium[0] :
                    self.close()
                    self.log("Short exited" + ", " + self.current_date_string + " " + self.current_time_string)
                    self.log(" ")

    '''
    def stop(self):
        print(("EMA_S,"+ str(self.params.period_short)+ ",EMA_M,"+ str(self.params.period_medium)+",EMA_L,"+ str(self.params.period_long)+",Profit/Loss," + str(int(self.broker.getvalue()-10000000.00))))
        #print(self.mylog)
    '''

if __name__ == "__main__":

    cerebro = bt.Cerebro()
    cerebro.addstrategy(FirstStrategy)
    #cerebro.optstrategy(FirstStrategy,period_short=range(5, 30,2),period_medium=range(30, 50, 2),period_long=range(70, 120, 5))

        
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
    # cerebro.addwriter(bt.WriterFile, csv = True, out = "Data Files"+ datetime.now().strftime("%H:%M")+".csv")
    
    starting_port = cerebro.broker.getvalue()

    print("Starting porfolio value is :", cerebro.broker.getvalue())

    cerebro.run()

    ending_port = cerebro.broker.getvalue()
    print("Final porfolio value is :", cerebro.broker.getvalue())
    print("FINAL PROFIT/LOSS : ", str(ending_port-starting_port))
    
    #To plot the trades on a chart. 

    cerebro.plot(volume=False)