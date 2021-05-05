
import pandas as pd
import numpy as np
import pickle
from strategy.LongShort import LongShort
from exchange.Exchange import Exchange
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

def load_obj(path:str,
             name:str):
    """
    :parameter
    :param name:The name of dictionary.
    :return: The dictionary.
    """
    with open(path+ name + '.pkl', 'rb') as f:
        return pickle.load(f)


class runLongShort:
    def __init__(self,
                 factor:str,
                 num:int,
                 stock_pool:pd.DataFrame,
                 start_date:str,
                 end_date:str):
        """
        :parameter
        :param factor:The factor.
        :param num:The number of layer you want.
        :param stock_pool:A dataframe that includes the stock id.
        :param start_date:The start date of the longshort.
        :param end_date: The end date of the longshort.
        """
        self.factor=factor
        self.num=num
        self.stock_pool=stock_pool
        self.start_date=start_date
        self.end_date=end_date

    def runlongshort(self,if_store:bool=True):
        dic_neutral_factor = load_obj(r'./因子//' + self.factor + '//', 'dic_neutral_' + self.factor)
        longshort = LongShort(self.num, dic_neutral_factor, self.factor)
        path=r'../data/close_data//'
        stock_list = self.stock_pool['stock_id'].tolist()

        dic_data = {}
        for i in self.stock_pool.index:
            stock_id = self.stock_pool.loc[i, 'stock_id']
            data = pd.read_excel(path + stock_id + '.xlsx', index_col=0)
            data = data.resample('M').last()
            dic_data[stock_id] = data
        exchange = Exchange(dic_data)

        Df = pd.DataFrame()
        for date in pd.date_range(start=self.start_date, end=self.end_date, freq='M'):
            print(date)
            dic_account = exchange.get_account_info()
            close_price = exchange.get_close_price(date)
            order = longshort.get_order(dic_account, date, close_price, stock_list)
            exchange.trade(order, date)
            net_value = exchange.get_account_info()['Total_banlance']
            Df.loc[date, 'net value'] = net_value
            print('总余额', net_value)
            print('')

        fig = plt.figure(figsize=[10, 5])
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.plot(Df.index,Df['net value'],label=self.factor+'多空组合净值')
        ax1.legend()
        ax1.set_xlabel('时间')
        ax1.set_ylabel('资产净值')
        ax1.set_title(self.factor+'因子多空组合')
        plt.show()
        if if_store==True:
            Df.to_excel(r'./因子//' + self.factor + '//' + self.factor + '_longshort_' + str(self.num) + 'layer.xlsx')