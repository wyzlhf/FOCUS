import datetime
import os.path
import backtrader as bt
import backtrader.indicators as btind


class SmaCross(bt.Strategy):
    params = dict(period=5)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print(f'{dt.isoformat()}: {txt}')

    def notify_order(self, order):
        self.log(f'订单状态{order.getstatusname()}')
        if order.status in [order.Submitted, order.Accepted]:
            self.order=order
            return
        self.order=order
    def notify_trade(self, trade):
        if trade.isclosed:
            print(f'毛收益 {trade.pnl},扣佣后收益 {trade.pnlcomm},佣金 {trade.commission}')
    def __init__(self):
        self.move_average = bt.indicators.MovingAverageSimple(self.data,period=self.params.period)
        self.order=None
    def next(self):
        if self.order:
            return
        if not self.position:
            if self.data.close[-1]<self.move_average[-1] and self.data>self.move_average:
                self.log('创建买单')
                validday=self.data.datetime.datetime(1)
                print(f'validday:{validday}')
                upperprice=self.data.close[0]*1.1-0.02
                self.order=self.buy(size=100,valid=validday,exectype=bt.Order.Limit,price=upperprice)
        elif self.data.close[-1]>self.move_average[-1] and self.data<self.move_average:
            self.log('创建卖单')
            validday=self.data.datetime.datetime(1)
            print(f'validday:{validday}')
            lowerprice=self.data.close[0]*0.9+0.02
            self.order=self.sell(size=100,valid=validday,exectype=bt.Order.Limit,price=lowerprice)
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
    cerebro.addstrategy(SmaCross)
    cerebro.broker.setcash(10000.0)
    cerebro.broker.setcommission(0.001)
    print(f'初始市值：{cerebro.broker.getvalue()}')
    cerebro.run()
    print(f'最终市值：{cerebro.broker.getvalue()}')