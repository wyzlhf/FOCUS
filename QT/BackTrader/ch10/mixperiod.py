import datetime
import os.path
import backtrader as bt


class SmaCross(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'买单执行价格： {order.executed.price}')
            elif order.issell():
                self.log(f'卖单执行价格： {order.executed.price}')
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单 Canceled/Margin/Rejected')

    def notify_trade(self, trade):
        if trade.isclosed:
            print(f'毛收益： {trade.pnl},扣佣后收益： {trade.pnlcomm},佣金： {trade.commission}')

    def __init__(self):
        self.move_average = bt.ind.MovingAverageSimple(self.data, period=5)
        self.move_average2 = bt.ind.MovingAverageSimple(self.datas[1], period=2)
        self.crossover = bt.ind.CrossOver(self.data, self.move_average)
        self.isover = self.move_average > self.move_average2

    def next(self):
        if not self.position:
            if self.crossover > 0 and self.isover == 1:
                self.log('创建买单')
                self.buy(size=100)
        elif self.crossover < 0 and not self.isover == 0:
            self.log('创建卖单')
            self.close()


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    modpath = os.path.dirname(os.path.abspath(__file__))
    datapath = os.path.join(modpath, './600000d.csv')
    datapath2 = os.path.join(modpath, './600000w.csv')
    data = bt.feeds.GenericCSVData(
        dataname=datapath,
        datetime=1,
        open=3,
        high=5,
        low=6,
        close=4,
        volume=7,
        openinterest=-1,
        dtformat=('%Y-%m-%d'),
        timeframe=bt.TimeFrame.Days,
        fromdate=datetime.datetime(2019, 1, 1),
        todate=datetime.datetime(2020, 7, 8),
    )
    data2 = bt.feeds.GenericCSVData(
        dataname=datapath2,
        datetime=1,
        open=3,
        high=5,
        low=6,
        close=4,
        volume=7,
        openinterest=-1,
        dtformat=('%Y-%m-%d'),
        timeframe=bt.TimeFrame.Weeks,
        fromdate=datetime.datetime(2019, 1, 1),
        todate=datetime.datetime(2020, 7, 8),
    )
    cerebro.adddata(data)
    cerebro.adddata(data2)
    cerebro.addstrategy(SmaCross)
    cerebro.broker.setcash(10000.0)
    cerebro.broker.setcommission(0.001)
    cerebro.broker.set_slippage_fixed(0.05)
    print(f'初始市值： {cerebro.broker.getvalue()}')
    cerebro.run(stdstats=False, runonce=False)
    print(f'最终市值： {cerebro.broker.getvalue()}')
