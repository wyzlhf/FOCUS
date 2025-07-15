import datetime
import os.path
import backtrader as bt
class SmaCross(bt.Strategy):
    params=dict(pfast=5,pslow=10)
    def __init__(self):
        sma1=bt.ind.SMA(period=self.p.pfast)
        sma2=bt.ind.SMA(period=self.p.pslow)
        self.crossover=bt.ind.CrossOver(sma1,sma2)
    def next(self):
        if not self.position:
            if self.crossover>0:
                self.buy(size=5000)
        elif self.crossover<0:
            self.close()
    def stop(self):
        print(f'(Fast Period {self.p.pfast}, Slow Period {self.p.pslow}, Ending Value {self.broker.getvalue()})')
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
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)
    strats=cerebro.optstrategy(SmaCross,pfast=[5,10,15],pslow=[20,30,60])
    cerebro.run(maxcpus=1,optdatas=True)