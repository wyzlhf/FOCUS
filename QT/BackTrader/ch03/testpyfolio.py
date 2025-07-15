import datetime
import glob
import os.path
import backtrader as bt
import pyfolio as pf
import pandas as pd
from analyzerexample import SmaCross

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    datadir = './dataswind'
    datafilelist = glob.glob(os.path.join(datadir, '*'))
    # print(datafilelist)
    maxstocknum=5
    datafilelist=datafilelist[0:maxstocknum]
    # print(datafilelist)
    startdate=datetime.datetime(2003,1,1)
    enddate=datetime.datetime(2010,12,10)
    for fname in datafilelist:
        print('fname:',fname)
        data=bt.feeds.GenericCSVData(
            dataname=fname,
            datetime=1,
            open=3,
            high=5,
            low=6,
            close=4,
            volume=7,
            openinterest=-1,
            dtformat=('%Y/%m/%d'),
            fromdate=startdate,
            todate=enddate
        )
        cerebro.adddata(data)
    cerebro.addstrategy(SmaCross)
    startcash=1000000/2
    cerebro.broker.setcash(startcash)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addanalyzer(bt.analyzers.PyFolio,_name='pyfolio')
    results = cerebro.run()
    strat=results[0]
    pyfoliozer=strat.analyzers.getbyname('pyfolio')
    returns,positions,transactions,gross_lev=pyfoliozer.get_pf_items()
    transactions.index=transactions.index.map(lambda t:t.replace(hour=00, minute=00, second=00, microsecond=0))
    benchmark_rets=pd.read_csv(datafilelist[0])
    benchmark_rets['date']=pd.to_datetime(benchmark_rets['date'])
    benchmark_rets['return']=benchmark_rets['close'].pct_change()
    benchmark_rets.set_index(['date'],inplace=True)
    benchmark_rets=benchmark_rets['return'].tz_localize('UTC').loc[startdate:enddate]
    pf.create_full_tear_sheet(
        returns,
        positions=positions,
        transactions=transactions,
        benchmark_rets=benchmark_rets,
        round_trips=True
    )
