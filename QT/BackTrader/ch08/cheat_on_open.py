import datetime
import os.path
import backtrader as bt


class St(bt.Strategy):
    params = dict(
        periods=[10, 30],
        matype=bt.ind.SMA,
    )

    def __init__(self):
        self.cheating = self.cerebro.p.cheat_on_open
        print(f'self.cheating {self.cheating}')
        mas = [self.p.matype(period=x) for x in self.p.periods]
        self.signal = bt.ind.CrossOver(*mas)
        self.order = None

    def notify_order(self, order):
        if order.status != order.Completed:
            return
        self.order = None
        print(
            f'{bt.num2date(order.executed.dt).date()} {"Buy" * order.isbuy() or "Sell"} Executed at price {order.executed.price}, size {order.executed.size}')

    def operate(self, fromopen):
        if self.order is not None:
            return
        if self.position:
            if self.signal < 0:
                self.order = self.close()
        elif self.signal > 0:
            print(f'{self.data.datetime.date()} Send Buy, fromopen {fromopen}, Close {self.data.close[0]}')
            self.order = self.buy()

    def next(self):
        if self.cheating:
            return
        print(f'{self.data.datetime.date()} next, open {self.data.open[0]} close {self.data.close[0]}')
        self.operate(fromopen=False)

    def next_open(self):
        if not self.cheating:
            return
        print(f'{self.data.datetime.date()} next_open, open {self.data.open[0]} close {self.data.close[0]}')
        self.operate(fromopen=True)
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
    cerebro.addstrategy(St)
    cerebro.broker.setcash(10000.0)
    cerebro.broker.setcommission(0.001)
    cerebro.broker.set_slippage_fixed(0.05)
    print(f'初始市值：{cerebro.broker.getvalue()}')
    cerebro.run()
    print(f'最终市值：{cerebro.broker.getvalue()}')