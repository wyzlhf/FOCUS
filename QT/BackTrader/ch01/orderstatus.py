from datetime import datetime
import backtrader as bt
import os.path
import sys


class SmaCross(bt.Strategy):
    params = (('period', 5),)

    def log(self, txt, dt=None):
        dt = dt or self.datetime.date(0)
        print(f'{dt.isoformat()}: {txt}')

    def __init__(self):
        self.move_average = bt.ind.MovingAverageSimple(self.data, period=self.params.period)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f'买单执行，price {round(order.executed.price, 2)}，size {order.executed.size}，cost {round(order.executed.value, 2)}')
            elif order.issell():
                self.log(
                    f'卖单执行，price {round(order.executed.price, 2)}，size {order.executed.size}，cost {round(order.executed.value, 2)}')
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单 Canceled/Margin/Rejected')

    def notify_trade(self, trade):
        print('订单状态改变')
        if trade.isclosed:
            print(f'毛收益 {trade.pnl:.2f}，扣佣后收益 {trade.pnlcomm:.2f}，佣金 {trade.commission:.2f}')

    def next(self):
        if not self.position:
            if self.data.close[-1] < self.move_average[-1] and self.data > self.move_average:
                self.log('创建买单')
                self.buy(size=100)
        elif self.data.close[-1] > self.move_average[-1] and self.data < self.move_average:
            self.log('创建卖单')
            self.sell(size=100)


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    modpath = os.path.dirname(os.path.abspath(__file__))
    # print(modpath)
    datapath = os.path.join(modpath, './600000qfq.csv')
    data = bt.feeds.GenericCSVData(
        dataname=datapath,
        # 这里的序号是按照Python形式，即从0开始索引
        datetime=1,
        open=3,
        high=5,
        low=6,
        close=4,
        volume=7,
        openinterest=-1,
        dtformat=('%Y/%m/%d'),
        fromdate=datetime(2019, 1, 1),
        todate=datetime(2020, 7, 8),
    )
    cerebro.adddata(data)
    cerebro.addstrategy(SmaCross)
    cerebro.broker.setcash(10000.0)
    cerebro.broker.setcommission(0.001)
    cerebro.broker.set_slippage_fixed(0.05)
    print(f'初始市值：{cerebro.broker.getvalue()}')
    cerebro.run()
    print(f'最终市值：{cerebro.broker.getvalue()}')
    cerebro.plot()
