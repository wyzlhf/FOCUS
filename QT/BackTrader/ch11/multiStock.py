import datetime
import glob
import os.path
import backtrader as bt


# class SmaCross(bt.Strategy):
#     params = dict(
#         fast_period=2,
#         slow_period=5,
#     )
#
#     def __init__(self):
#         fastMA = {stock: bt.ind.MovingAverageSimple(stock, period=self.params.fast_period) for stock in self.datas}
#         slowMA = {stock: bt.ind.MovingAverageSimple(stock, period=self.params.slow_period) for stock in self.datas}
#         self.crossover = {stock: bt.ind.CrossOver(fastMA[stock], slowMA[stock]) for stock in self.datas}
#         self.orderlist = []
#
#     def next(self):
#         for o in self.orderlist:
#             self.cancel(o)
#             self.orderlist = []
#         for stock in self.datas:
#             if not self.getposition(stock):
#                 if self.crossover[stock] > 0:
#                     order = self.buy(data=stock, size=100)
#                     self.orderlist.append(order)
#             elif self.crossover[stock] < 0:
#                 order = self.close(data=stock, size=100)
#                 self.orderlist.append(order)
#
#
# if __name__ == '__main__':
#     cerebro = bt.Cerebro()
#     datadir = './data1'
#     datafilelist = glob.glob(os.path.join(datadir, '*'))
#     print(datafilelist)
#     maxstocknum = 10
#     datafilelist = datafilelist[0:maxstocknum]
#     for fname in datafilelist:
#         data = bt.feeds.GenericCSVData(
#             dataname=fname,
#             datetime=1,
#             open=3,
#             high=5,
#             low=6,
#             close=4,
#             volume=7,
#             openinterest=-1,
#             dtformat=('%Y-%m-%d'),
#             timeframe=bt.TimeFrame.Months,
#             fromdate=datetime.datetime(2010, 1, 1),
#             todate=datetime.datetime(2020, 7, 8),
#         )
#         cerebro.adddata(data)
#     cerebro.addstrategy(SmaCross)
#     startcash = 1000000
#     cerebro.broker.setcash(startcash)
#     cerebro.broker.setcommission(commission=0.001)
#     cerebro.run()
#     pnl = cerebro.broker.get_value() - startcash
#     print(f'Profit...or Loss: {pnl:.2f}')
class SmaCross(bt.Strategy):
    params = dict(
        fast_period=2,
        slow_period=5,
    )

    def __init__(self):
        fastMA = {
            stock: bt.ind.MovingAverageSimple(stock, period=self.params.fast_period) for stock in self.datas
        }
        slowMA = {
            stock: bt.ind.MovingAverageSimple(stock, period=self.params.slow_period) for stock in self.datas
        }
        self.crossover = {
            stock: bt.ind.CrossOver(fastMA[stock], slowMA[stock]) for stock in self.datas
        }
        self.orderlist = []

    def next(self):
        for o in self.orderlist:
            self.cancel(o)
            self.orderlist = []
        for stock in self.datas:
            if not self.getposition(stock):
                if self.crossover[stock] > 0:
                    order = self.buy(data=stock, size=100)
                    self.orderlist.append(order)
            elif self.crossover[stock] < 0:
                order = self.close(data=stock, size=100)
                self.orderlist.append(order)
if __name__ == '__main__':
    cerebro = bt.Cerebro()
    datadir='./data1'
    datafilelist=glob.glob(os.path.join(datadir,'*'))
    maxstocknum=10
    datafilelist=datafilelist[0:maxstocknum]
    for fname in datafilelist:
        data=bt.feeds.GenericCSVData(
            dataname=fname,
            datetime=1,
            open=3,
            high=5,
            low=6,
            volume=7,
            openinterest=-1,
            dtformat=('%Y-%m-%d'),
            fromdate=datetime.datetime(2010,1,1),
            todate=datetime.datetime(2020,12,31),
            timeframe=bt.TimeFrame.Months
        )
        cerebro.adddata(data)
    cerebro.addstrategy(SmaCross)
    startcash=1000000
    cerebro.broker.setcash(startcash)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.run()
    pnl=cerebro.broker.get_value()-startcash
    print(f'Profit ... or Loss: {pnl}')
