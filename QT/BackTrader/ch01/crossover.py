from datetime import datetime, timedelta
import backtrader as bt
import os.path


class SmaCross(bt.Strategy):
    params = dict(period=5)

    def log(self, txt, dt=None):
        dt = dt or self.datetime.date(0)
        print(f'{dt}: {txt}')

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        elif order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'买单执行，{order.executed.price:.2f}')
            if order.issell():
                self.log(f'卖单执行，{order.executed.price:.2f}')
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log(f'订单 Canceled/Margin/Rejected')
            self.order = None

    def notify_trade(self, trade):
        print('交易执行')
        if trade.isclosed:
            print(f'毛收益 {trade.pnl:.2f}，扣佣后收益 {trade.pnlcomm:.2f}，佣金 {trade.commission:.2f}')

    def __init__(self):
        self.move_average = bt.ind.MovingAverageSimple(self.data, period=self.params.period)
        self.crossover = bt.ind.CrossOver(self.data, self.move_average)

    def next(self):
        if not self.position:
            if self.crossover > 0:  # 上穿
                self.log('创建买单')
                self.buy(size=100)
        elif self.crossover < 0:  # 下破
            self.log('创建卖单')
            self.sell(size=100)


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
