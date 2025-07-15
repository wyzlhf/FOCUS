from __future__ import (absolute_import,division,print_function,unicode_literals)
import datetime
import os.path
import sys
from backtrader.observers.orderobserver import OrderObserver
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind



class MyStrategy(bt.Strategy):
    params = (
        ('smaperiod', 15),
        ('limitperc', 1.0),
        ('valid', 7),
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print(f'{dt.isoformat()}: {txt}')

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            self.log('ORDER ACCEPTED/SUBMITTED', dt=order.created.dt)
            self.order = order
            return
        if order.status in [order.Expired]:
            self.log('BUY EXPIRED')
        elif order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f'BUY EXECUTED,PRICE:{order.executed.price},COST:{order.executed.value},COMM {order.executed.comm}')
            else:
                self.log(
                    f'SELL EXECUTED, PRICE:{order.executed.price},PRICE:{order.executed.value},COMM {order.executed.comm}')
        self.order = None

    def __init__(self):
        sma = btind.SMA(period=self.p.smaperiod)
        self.crossover = btind.CrossOver(self.data.close, sma, plot=True)
        self.order = None

    def next(self):
        if self.order:
            return
        if self.position:
            if self.crossover < 0:
                self.log(f'SELL CREATE,{self.data.close[0]}')
                self.order = self.sell()
        elif self.crossover > 0:
            plimit = self.data.close[0] * (1.0 - self.p.limitperc / 100.0)
            valid = self.data.datetime.datetime(0) + datetime.timedelta(days=self.p.valid)
            self.log(f'BUY CREATE,{plimit}')
            self.order = self.buy(
                exectype=bt.Order.Limit, price=plimit, valid=valid
            )


def runstrat():
    cerebro = bt.Cerebro()
    modpath = os.path.dirname(os.path.abspath(__file__))
    datapath = os.path.join(modpath, './600000qfq.csv')
    data = bt.feeds.GenericCSVData(
        dataname=datapath,
        datetime=1,
        open=3,
        high=5,
        low=6,
        close=4,
        volume=7,
        openinterest=-1,
        dtformat=('%Y/%m/%d'),
        fromdate=datetime.datetime(2019, 1, 1),
        todate=datetime.datetime(2020, 7, 8),
    )
    cerebro.adddata(data)
    cerebro.addobserver(OrderObserver)
    cerebro.addstrategy(MyStrategy)
    cerebro.run()
    cerebro.plot()


if __name__ == '__main__':
    runstrat()
