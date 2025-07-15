from datetime import datetime
import backtrader as bt
import os.path
import sys
import matplotlib.pyplot as plt


class SmaCross(bt.Strategy):
    params = dict(period=5)

    def __init__(self):
        self.move_average = bt.ind.MovingAverageSimple(self.datas[0].close, period=self.params.period)

    def next(self):
        if not self.position.size:
            if self.datas[0].close[-1] < self.move_average.sma[-1] and self.datas[0].close[0] > self.move_average.sma[
                0]:
                self.buy(size=100)
        elif self.datas[0].close[-1] > self.move_average.sma[-1] and self.datas[0].close[0] < self.move_average.sma[0]:
            self.sell(size=100)
        print(len(self))


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    print(modpath)
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
        todate=datetime(2019, 12, 31),
        # decodings='gbk'
    )
    cerebro.adddata(data)
    cerebro.addstrategy(SmaCross)
    cerebro.broker.setcash(100000.0)
    cerebro.run()
    print(f'最终市值：{cerebro.broker.getvalue()}')
    cerebro.plot(style='candle')
