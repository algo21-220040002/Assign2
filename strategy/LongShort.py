
import numpy as np
import pandas as pd
import math

class LongShort:
    """LongShort
    根据某一个因子进行回测，并计算多空净值
    """
    def __init__(self,
                 num:int,
                 dic_factor:dict,
                 factor:str):
        """
        :parameter
        :param num: The num of the layer.
        :param dic_factor:A dictionary whose key is timestamp and value is dataframe whose index is stock id and columns are factor.
        :param factor:The factor you want use to do a long short strategy.
        """
        self.num=num
        self.dic_factor=dic_factor
        self.factor=factor

    def get_order(self,
                  dic_account:dict,
                  date:pd.Timestamp,
                  close_price:dict,
                  stock_list:list)->dict:
        """
        :parameter
        :param dic_account:The dic_account of the exchange.
        :param date:
        :param close_price:The close price of the exchange.
        :return:
        """
        data = self.dic_factor[date][[self.factor]]
        data=data.T[stock_list].T
        df_long = data[data[self.factor] >= data[self.factor].quantile(1 - 1 / self.num)]  #找到多头组合
        df_short = data[data[self.factor] <= data[self.factor].quantile(1 / self.num)]     #找到空头组合
        order = {}

        Total_banlance=dic_account['Total_banlance']
        total_stock_num=len(df_long)+len(df_short)  #多空组合股票总数量
        for stock_id in data.index:
            order[stock_id]={}
            if stock_id in df_long.index:
                value=Total_banlance/total_stock_num-dic_account[stock_id+'_value']  #找到目标价值
            elif stock_id in df_short.index:
                value = -Total_banlance/total_stock_num-dic_account[stock_id + '_value']
            else:
                value= -dic_account[stock_id + '_value']

            if value>0:
                if not math.isnan(close_price[stock_id]):  #此时价格信息不为空，保证此时股票确实已经上市
                    order[stock_id]['type']='buy'
                    order[stock_id]['shares']=value/close_price[stock_id]
                else:
                    order[stock_id]['type'] = 'hold' #如何此时价格信息为空，表明此时股票并未上市，所以就选择hold不做任何操作
            elif value==0:
                order[stock_id]['type'] = 'hold'
            elif value<0:
                if not math.isnan(close_price[stock_id]):
                    order[stock_id]['type'] = 'sell'
                    order[stock_id]['shares'] =-1*value/close_price[stock_id]
                else:
                    order[stock_id]['type'] = 'hold'
        return order









