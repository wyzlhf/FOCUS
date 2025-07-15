import datetime
import os.path
import time
import sys
import backtrader as bt
import backtrader.indicators as btind


class OrderExecutionStrategy(bt.Strategy):
    params = (
        ('smaperiod', 15),
        ('exectype', 'Market'),
        ('perc1', 3),
        ('perc2', 1),
        ('valid', 4),
    )

    def log(self, txt, dt=None):
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print(f'{dt.isoformat()}: {txt}')

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            self.log(f'ORDER ACCEPTED/SUBMITTED: {order.created.dt}')
            self.order = order
            return
        if order.status in [order.Expired]:
            self.log('BUY EXPIRED')
        elif order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f'BUY EXECUTED: Price: {order.executed.price:.2f},Cost: {order.executed.value:.2f},Comm {order.executed.comm:.2f}')
            else:
                self.log(
                    f'SELL EXECUTED,Price: {order.executed.price:.2f},Cost: {order.executed.value:.2f},Comm {order.executed.comm:.2f}')

    def __init__(self):
        sma = btind.SMA(period=self.p.smaperiod)
        self.buysell = btind.CrossOver(self.data.close, sma, plot=True)

    def next(self):
        if self.position:
            if self.buysell < 0:
                self.log(f'SELL CREATE,{self.data.close[0]}')
                self.sell()
        elif self.buysell > 0:
            if self.p.valid:
                valid = self.data.datetime.datetime(0) + datetime.timedelta(days=self.p.valid)
            else:
                valid = None
            if self.p.exectype == 'Market':
                self.order = self.buy(exectype=bt.Order.Market)
                self.log(f'BUY CREATE, ExecType Market, Price: {self.data.close[0]}')
            elif self.p.exectype == 'Close':
                self.order = self.buy(exectype=bt.Order.Close)
                self.log(f'BUY CREATE, ExecType Close, Price: {self.data.close[0]}')
            elif self.p.exectype == 'Limit':
                price = self.data.close * (1.0 - self.p.perc1 / 100.0)
                self.order = self.buy(exectype=bt.Order.Limit, price=price, valid=valid)
                if self.p.valid:
                    self.log(f'BUY CREATE, ExecType Limit, Price: {price}, Valid: {valid.strftime("%Y-%m-%d")}')
                else:
                    self.log(f'BUY CREATE, ExecType Limit, Price: {price}')
            elif self.p.exectype == 'Stop':
                price = self.data.close * (1.0 + self.p.perc1 / 100.0)
                self.order = self.buy(exectype=bt.Order.Stop, price=price, valid=valid)
                if self.p.valid:
                    self.log(f'BUY CREATE, ExecType Stop, Price: {price}, Valid: {valid.strftime("%Y-%m-%d")}')
                else:
                    self.log(f'BUY CREATE, ExecType Stop, Price: {price}')
            elif self.p.exectype == 'StopLimit':
                price = self.data.close * (1.0 + self.p.perc1 / 100.0)
                plimit = self.data.close * (1.0 + self.p.perc2 / 100.0)
                self.order = self.buy(exectype=bt.Order.StopLimit, price=price, plimit=plimit, valid=valid)
                if self.p.valid:
                    self.log(
                        f'BUY CREATE, execType StopLimit, Price: {price}, Valid: {valid.strftime("%Y-%m-%d")}, plimit: {plimit}')
                else:
                    self.log(f'BUY CREATE, execType StopLimit, Price: {price}, pricelimit: {plimit}')


if __name__ == '__main__':
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
    cerebro.addstrategy(
        OrderExecutionStrategy,
        exectype='Market',
        perc1=1,
        perc2=2,
        valid=2,
        smaperiod=5,
    )
    cerebro.run()
