from datetime import datetime
import backtrader as bt
import os.path
import pandas as pd
import backtrader.analyzers as btanalyzers


class MaCrossStrategy(bt.Strategy):
    params = (
        ('fast_length', 10),
        ('slow_length', 50),
    )

    def __init__(self):
        ma_fast = bt.ind.SMA(period=self.params.fast_length)
        ma_slow = bt.ind.SMA(period=self.params.slow_length)
        self.crossover = bt.ind.CrossOver(ma_fast, ma_slow)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        elif self.crossover < 0:
            self.close()


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
    cerebro.optstrategy(
        MaCrossStrategy,
        fast_length=range(1, 11, 5),
        slow_length=range(25, 35, 5),
    )
    cerebro.broker.setcash(1000000.0)
    cerebro.addsizer(bt.sizers.PercentSizer,percents=10)
    cerebro.addanalyzer(btanalyzers.SharpeRatio,_name='sharpe')
    cerebro.addanalyzer(btanalyzers.DrawDown,_name='drawdown')
    cerebro.addanalyzer(btanalyzers.Returns,_name='returns')
    back=cerebro.run()
    par_list=[
        [X[0].params.fast_length,
         X[0].params.slow_length,
         X[0].analyzers.returns.get_analysis()['rnorm100'],
         X[0].analyzers.drawdown.get_analysis()['max']['drawdown'],
         X[0].analyzers.sharpe.get_analysis()['sharperatio']] for X in back
    ]
    par_df=pd.DataFrame(par_list,columns=['length_fast','length_slow','return','dd','sharpe'])
    print(par_df)
    par_df.to_csv('result.csv')
