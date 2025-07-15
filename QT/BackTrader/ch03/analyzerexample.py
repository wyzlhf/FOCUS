from datetime import datetime
import backtrader as bt
import os.path
import sys


class SmaCross(bt.Strategy):
    params = (('period', 2),)

    def log(self, txt, dt=None):
        dt = dt or self.datetime.date(0)
        print(f'{dt}: {txt}')

    def __init__(self):
        self.move_average = bt.ind.MovingAverageSimple(self.datas[0].close, period=self.params.period)
        self.crossover = bt.ind.CrossOver(self.data, self.move_average)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy(size=100)
        elif self.crossover < 0:
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
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, riskfreerate=0.01, annualize=True, _name='sharp_ratio')
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='annual_return')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade_analyzer')
    print(f'初始市值：{cerebro.broker.getvalue()}')
    # cerebro.run()
    thestrats = cerebro.run()
    print(f'最终市值：{cerebro.broker.getvalue()}')
    thestrat = thestrats[0]
    # print(f'Sharpe Ratio: {thestrat.analyzers.sharp_ratio.get_analysis()}')
    # print(f'Annual Return: {thestrat.analyzers.annual_return.get_analysis()}')
    # print(f'Drawdown: {thestrat.analyzers.drawdown.get_analysis()}')
    # print(f'Trade: {thestrat.analyzers.trade.get_analysis()}')
    # print('Sharpe Ratio: ', thestrat.analyzers.sharp_ratio.get_analysis()['sharperatio'])
    # print('Max DrawDown: ', thestrat.analyzers.drawdown.get_analysis()['max']['drawdown'])
    for a in thestrat.analyzers:
        a.print()
        a.pprint()
