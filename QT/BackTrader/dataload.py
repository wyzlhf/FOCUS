from typing import List

import akshare as ak
import numpy as np
import pandas as pd


# stock_zh_a_hist_df_d = ak.stock_zh_a_hist(symbol="600000", period="daily", end_date='20250711', adjust="qfq")
# stock_zh_a_hist_df_d.columns = ['date', 'code', 'open', 'close', 'high', 'low', 'volume', 'amount', 'amplitude',
#                                 'change', 'changemount', 'turn']
# stock_zh_a_hist_df_d.to_csv('600000d.csv')
# stock_zh_a_hist_df_w = ak.stock_zh_a_hist(symbol="600000", period="weekly", end_date='20250711', adjust="qfq")
# stock_zh_a_hist_df_w.columns = ['date', 'code', 'open', 'close', 'high', 'low', 'volume', 'amount', 'amplitude',
#                                 'change', 'changemount', 'turn']
# stock_zh_a_hist_df_w.to_csv('600000w.csv')
# stock_zh_a_hist_df_m = ak.stock_zh_a_hist(symbol="600000", period="monthly", end_date='20250711', adjust="qfq")
# stock_zh_a_hist_df_m.columns = ['date', 'code', 'open', 'close', 'high', 'low', 'volume', 'amount', 'amplitude',
#                                 'change', 'changemount', 'turn']
# stock_zh_a_hist_df_m.to_csv('600000m.csv')


# stock_zh_a_hist_min_em_df_1 = ak.stock_zh_a_hist_min_em(symbol="600000", start_date="2000-03-20 09:30:00",
#                                                         end_date="2025-07-11 15:00:00", period="1", adjust="qfq")
# stock_zh_a_hist_min_em_df_1.columns = ['date', 'open', 'close', 'high', 'low', 'volume', 'amount', 'average']
# stock_zh_a_hist_min_em_df_1.to_csv("600000_1.csv")
#
# stock_zh_a_hist_min_em_df_5 = ak.stock_zh_a_hist_min_em(symbol="600000", start_date="2000-03-20 09:30:00",
#                                                         end_date="2025-07-11 15:00:00", period="5", adjust="qfq")
# stock_zh_a_hist_min_em_df_5.columns = ['date', 'open', 'close', 'high', 'low', 'zhangdiefu', 'zhangdiee', 'volume',
#                                        'amount', 'zhenfu', 'huanshoulv']
# stock_zh_a_hist_min_em_df_5.to_csv("600000_5.csv")
def get_daily_datas_from_ak(symbols: List[str]):
    for symbol in symbols:
        stock_zh_a_hist_df_d = ak.stock_zh_a_daily(symbol=symbol, start_date="19910403", end_date="20251027",
                                                   adjust="qfq")
        # stock_zh_a_hist_df_d.columns = ['date', 'code', 'open', 'close', 'high', 'low', 'volume', 'amount', 'amplitude',
        #                                 'change', 'changemount', 'turn']
        stock_zh_a_hist_df_d.to_csv(f'./ch11/data/{symbol}.csv')


def get_daily_datas_from_em(symbols: List[str]):
    for symbol in symbols:
        stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=symbol, period="monthly", start_date="19910403", end_date='20251027',
                                                adjust="qfq")
        stock_zh_a_hist_df.columns = ['date', 'code', 'open', 'close', 'high', 'low', 'volume', 'amount', 'amplitude',
                                        'change', 'changemount', 'turn']
        stock_zh_a_hist_df.to_csv(f'./ch11/data1/{symbol}.csv')
        print(f'{symbol}保存完成')


# print(list(ak.stock_zh_a_spot().tail(20).loc[:,'代码']))
print(list(ak.stock_zh_a_spot_em().tail(50).loc[:, '代码']))
if __name__ == '__main__':
    # Permanently changes the pandas settings
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)
    # symbols = ['sz301607', 'sz301608', 'sz301611', 'sz301613', 'sz301616', 'sz301617', 'sz301618', 'sz301622',
    #            'sz301626', 'sz301628', 'sz301629', 'sz301630', 'sz301631', 'sz301633', 'sz301636', 'sz301658',
    #            'sz301662', 'sz301665', 'sz301678', 'sz302132']
    # symbols_em = ['000502', '000418', '000416', '000413', '000412', '000406', '000405', '000150', '000047', '000046',
    #               '000040', '000038', '000033', '000024', '000023', '000018', '000015', '000013', '000005', '000003']
    #
    # # get_daily_datas_from_ak(symbols)
    # get_daily_datas_from_em(symbols_em)
    # symbol_list=list(ak.stock_zh_a_spot_em().tail(300).loc[:, '代码'])




