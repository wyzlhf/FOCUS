# import akshare as ak
# stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="600000", period="daily", start_date="20080101", end_date='20241231', adjust="qfq")
# stock_zh_a_hist_df.to_csv('600000qfq.csv',encoding='utf-8')

class A(object):
    def __init__(self):
        self.get_len()
    def __len__(self):
        return 5
    def get_len(self):
        print(f'len(): {len(self)}')
        # return len(self)

if __name__ == '__main__':
    import subprocess
    zen_of_python=subprocess.check_output(['python','-c','import this'])
    print(zen_of_python)