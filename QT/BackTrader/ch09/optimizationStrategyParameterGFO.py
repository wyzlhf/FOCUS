import datetime
import os.path
import backtrader as bt
import gradient_free_optimizers as gfo
import numpy as np


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


def runstrat(para):
    print(f'I am called, {datetime.datetime.now().strftime("%H:%M:%S")}')
    if para['sma1'] >= para['sma2']:
        return np.nan
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmaCross, sma1=para['sma1'], sma2=para['sma2'])
    cerebro.adddata(data)
    cerebro.broker.setcash(10000.0)
    cerebro.run()
    score = cerebro.broker.getvalue()
    return score

if __name__ == '__main__':
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
    search_space = {
        'sma1': np.arange(2, 55, 1),
        'sma2': np.arange(2, 55, 1),
    }
    iterations = 5
    opt = gfo.EvolutionStrategyOptimizer(search_space)
    opt.search(runstrat, n_iter=iterations)
    best_param_fast = opt.best_para['sma1']
    best_param_slow = opt.best_para['sma2']
    print(f'Best param fast: {best_param_fast}')
    print(f'Best param slow: {best_param_slow}')
    print(f'Best score: {opt.best_score}')
    print(opt.n_iter)
