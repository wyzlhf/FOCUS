import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import warnings
from sklearn import linear_model
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
import datetime
import pyfolio as pf
import backtrader as bt
from backtrader.feeds import PandasData
import joblib
import akshare as ak
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Permanently changes the pandas settings
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', -1)

stock = ak.stock_zh_a_daily('sh600000', start_date='20100101', end_date='20100731', adjust='hfq')
stock.set_index(['date'], inplace=True)
prices = stock
prices.drop(['outstanding_share', 'turnover'], axis=1, inplace=True)
stock = stock['close'].to_frame()
stock['returns'] = np.log(stock / stock.shift(1))
stock.dropna(inplace=True)
stock['direction'] = np.sign(stock['returns']).astype(int)
stock.dropna(inplace=True)
stock['next_direction'] = stock['direction'].shift(-1)
lags = [1, 2, 3, 4, 5]
features_cols = ['direction']
for lag in lags:
    col = f'direction_lag{lag}'
    stock[col] = stock['direction'].shift(lag)
    features_cols.append(col)
stock.dropna(inplace=True)
# print(stock)
X_train, X_test, y_train, y_test = train_test_split(stock[features_cols], stock['next_direction'], test_size=0.2,
                                                    shuffle=False)
clf = SVC()
clf.fit(X_train, y_train)
y_predicted = clf.predict(X_test)
# print(accuracy_score(y_test,y_predicted))
# print(classification_report(y_test,y_predicted))
# print(confusion_matrix(y_test,y_predicted))
prices = prices.loc[y_test.index]
prices['predicted'] = y_predicted


class MLStrategy(bt.Strategy):
    params = dict(

    )

    def __init__(self):
        self.data_open = self.datas[0].open
        self.data_close = self.datas[0].close

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0).isoformat()
        print(f'{dt}: {txt}')

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f'买单执行，价格： {order.executed.price:.2f}，价值： {order.executed.value:.2f}，佣金： {order.executed.comm:.2f}')
            else:
                self.log(
                    f'卖单执行，价格： {order.executed.price:.2f}，价值： {order.executed.value:.2f}，佣金： {order.executed.comm:.2f}')
        if order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log(f'订单失败')
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(f'OPERATION RESULT --- Gross: {trade.pnl:.2f}, Net: {trade.pnlcomm:.2f}')
    def next(self):
        if not self.position:
            if self.data.predicted[0]>0:
                size=int(self.broker.getcash()*0.95/self.data.close[0])
                self.log(f'BUY CREATE --- Size:{size},Cash: {self.broker.getcash():.2f},Open: {self.data_open[0]}, Close: {self.data_close[0]}')
                self.buy(size=size)
        else:
            if self.data.predicted[0]<0:
                self.log(f'SELL CREATED --- Size: {self.position.size}')
                self.close()
class PandasData_ext(PandasData):
    lines=('predicted',)
    params=(('predicted',5),)
data=PandasData_ext(
    dataname=prices,
    datetime=None,
    open=0,
    high=1,
    low=2,
    close=3,
    volume=4,
    predicted=5,
    openinterest=-1,
)
cerebro = bt.Cerebro()
cerebro.addstrategy(MLStrategy)
cerebro.adddata(data,name='sh600000')
cerebro.broker.setcash(100000.0)
cerebro.broker.setcommission(commission=0.001)
cerebro.addanalyzer(bt.analyzers.PyFolio,_name='pyfolio')
print(f'Starting Portfolio Value: {cerebro.broker.getvalue()}')
backtest_results = cerebro.run()
print(f'Final Portfolio Value: {cerebro.broker.getvalue()}')

strat=backtest_results[0]
pyfoliozer=strat.analyzers.getbyname('pyfolio')
returns,positions,transactions,gross_lev=pyfoliozer.get_pf_items()
returns.name='Strategy'
X_test['returns']=stock['returns']
benchmark_rets=X_test['returns']
benchmark_rets.inde=benchmark_rets.index.tz_localize('UTC')
benchmark_rets=benchmark_rets.filter(returns.index)
benchmark_rets.name='benchmark'
pf.create_full_tear_sheet(
    returns,
    positions=positions,
    benchmark_rets=benchmark_rets,
    round_trips=True,
)