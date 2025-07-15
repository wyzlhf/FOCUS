import datetime
import os.path
import backtrader as bt
import optunity


class SmaCross(bt.Strategy):
    params = (
        ('sma1', 10),
        ('sma2', 30),
    )

    def __init__(self):
        SMA1 = bt.ind.SMA(period=int(self.params.sma1))
        SMA2 = bt.ind.SMA(period=int(self.params.sma2))
        self.crossover = bt.ind.CrossOver(SMA1, SMA2)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy(size=100)
        elif self.crossover < 0:
            self.sell(size=100)
def runstrat(sma1, sma2):
    print('I am called ',datetime.datetime.now().strftime('%H:%M:%S'))
    cerebro.addstrategy(SmaCross,sma1=sma1,sma2=sma2)
    cerebro.adddata(data)
    cerebro.broker.setcash(10000.0)
    cerebro.run()
    return cerebro.broker.getvalue()
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
    opt=optunity.maximize(runstrat,num_evals=10,solver_name='particle swarm',sma1=[2,55],sma2=[2,55])
    optimal_pars,details,_=opt
    print('Optimal Parameters:')
    print(f'sma1={optimal_pars["sma1"]}')
    print(f'sma2={optimal_pars["sma2"]}')
    # cerebro.run()
    cerebro.plot()