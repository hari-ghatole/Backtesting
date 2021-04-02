from __future__ import (absolute_import, division, print_function, unicode_literals)
from datetime import datetime
import backtrader as bt
import csv

class FirstStrategy(bt.Strategy):

    #params = (

    #)
        

    def log(self, txt):
        print(txt)

    def __init__(self):
        self.datalow = self.datas[0].open
        self.datalow = self.datas[0].low
        self.datahigh = self.datas[0].high
        self.dataclose = self.datas[0].close
        self.tme = self.datas[0].datetime

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

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order canceled/Margin not sufficient" )


    def next(self):


        self.current_date_string = self.datas[0].datetime.date(-3).strftime("%Y %m %d")
        self.current_time_string = self.datas[0].datetime.time(-3).strftime("%H:%M")

        '''
        #HH
        if self.datahigh[-6] < self.datahigh[-5] and self.datahigh[-5] < self.datahigh[-4] and self.datahigh[-4] < self.datahigh[-3] and self.datahigh[-2] < self.datahigh[-3] and self.datahigh[-1] < self.datahigh[-2] and  self.datahigh[0] < self.datahigh[-1] or self.datahigh[-6] < self.datahigh[-3] and self.datahigh[-5] < self.datahigh[-3] and self.datahigh[-4] < self.datahigh[-3] and  self.datahigh[-2] < self.datahigh[-3] and self.datahigh[-1] < self.datahigh[-3] and  self.datahigh[0] < self.datahigh[-3]:
                self.log("<<< H >>> " + str(self.datahigh[-3]) + ", " + self.current_date_string + " " + self.current_time_string)
        
        #LL
        if self.datalow[-6] > self.datahigh[-5] and self.datahigh[-5] > self.datahigh[-4] and self.datahigh[-4] > self.datahigh[-3] and self.datahigh[-2] > self.datahigh[-3] and self.datahigh[-1] > self.datahigh[-2] and self.datahigh[0] > self.datahigh[-1] or self.datahigh[-6] > self.datahigh[-3] and self.datahigh[-5] > self.datahigh[-3] and self.datahigh[-4] > self.datahigh[-3] and  self.datahigh[-2] > self.datahigh[-3] and self.datahigh[-1] > self.datahigh[-3] and  self.datahigh[0] > self.datahigh[-3]:
                self.log("<<< L >>>" + str(self.datalow[-3]) + ", " + self.current_date_string + " " + self.current_time_string)
        '''

        #HH/LH
        if self.datahigh[-6] < self.datahigh[-3] and self.datahigh[-5] < self.datahigh[-3] and self.datahigh[-4] < self.datahigh[-3] and  self.datahigh[-2] < self.datahigh[-3] and self.datahigh[-1] < self.datahigh[-3] and  self.datahigh[0] < self.datahigh[-3]:
            self.log("H-H " + str(self.datahigh[-3]) + ", " + self.current_date_string + " " + self.current_time_string)
            
        #LL/HL
        if self.datalow[-6] > self.datalow[-3] and self.datalow[-5] > self.datalow[-3] and self.datalow[-4] > self.datalow[-3] and self.datalow[-2] > self.datalow[-3] and self.datalow[-1] > self.datalow[-3] and self.datalow[0] > self.datalow[-3]:
            self.log("L-L " + str(self.datalow[-3]) + ", " + self.current_date_string + " " + self.current_time_string)
        

            

if __name__ == "__main__":

    cerebro = bt.Cerebro()
    cerebro.addstrategy(FirstStrategy)
    #cerebro.optstrategy(FirstStrategy,period_short=range(5, 30,2),period_medium=range(30, 50, 2),period_long=range(70, 120, 5))

        
    datapath = "Data Files/NSE_NIFTY_30min.csv"

    data = bt.feeds.GenericCSVData(
        dataname = datapath,
        fromdate = datetime(2021,1,1),
        todate = datetime(2021,3,1),
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


    #Remove the comment below to export results in a csv file.
    # cerebro.addwriter(bt.WriterFile, csv = True, out = "Data Files"+ datetime.now().strftime("%H:%M")+".csv")
    
    starting_port = cerebro.broker.getvalue()

    print("Starting porfolio value is :", cerebro.broker.getvalue())

    cerebro.run()

    ending_port = cerebro.broker.getvalue()
    print("Final porfolio value is :", cerebro.broker.getvalue())
    print("FINAL PROFIT/LOSS : ", str(ending_port-starting_port))
    
    #To plot the trades on a chart. 

    #cerebro.plot(volume=False)