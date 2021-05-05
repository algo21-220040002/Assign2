
import pandas as pd
import numpy as np
import os
import pickle
import math

def save_obj(obj:dict, name:str):
    """
    :parameter
    :param obj:The dictionary.
    :param name:The name of the dictionary you want to store.
    """
    with open(r'./'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    """
    :parameter
    :param name:The name of dictionary.
    :return: The dictionary.
    """
    with open(r'./' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


class Exchange:
    """Exchange
    It's a simulated exchange of the stocks.
    """
    def __init__(self,
                 dic_data:dict,
                 account_id:float='1314',
                 init_cash:float=1,
                 commision:float=0.00025,
                 slippage_rate:float=0):
        """
        :parameter
        :param dic_data: The dictionary whose key is the stock id and the value is the dataframe whose index is date and column is close price.
        :param account_id: The account id.
        :param init_cash: The initial cash.
        :param commision: The commision.
        :param slippage_rate: The slippage rate.
        """
        self.dic_data=dic_data
        self.account_id=account_id
        self.init_cash=init_cash
        self.commision=commision
        self.slippage_rate=slippage_rate

        if os.path.exists(str(account_id)+'.pkl')==False:
            print('You do not have an account,we will help you open the account,the initial cash is ' + str(self.init_cash))
            print('please notice that the account id is ' + str(account_id))
            dic_account = {}
            for stock_id in self.dic_data.keys():
                dic_account[stock_id+"_shares"]=0
                dic_account[stock_id+"_value"]=0
            dic_account['cash']=self.init_cash
            dic_account['Total_banlance']=self.init_cash
            save_obj(dic_account, str(account_id))
        else:
            print('We have initialized your account information in the exchange')
            dic_account = {}
            for stock_id in self.dic_data.keys():
                dic_account[stock_id+"_shares"]=0
                dic_account[stock_id+"_value"]=0
            dic_account['cash']=self.init_cash
            dic_account['Total_banlance']=self.init_cash
            save_obj(dic_account, str(account_id))
    def get_close_price(self,time:pd.Timestamp)->dict:
        """
        To get the close price of each stock.
        :parameter
        :param time: The time.
        :return: It's a dictionary whose key is stock id and whose value is the close price of the stock.
        """
        dic_close_price={}
        for stock_id in self.dic_data.keys():
            dic_close_price[stock_id]=self.dic_data[stock_id].loc[time,'close']
        return dic_close_price

    def get_account_info(self):
        """
        To get the account information.
        :return: The dic account.
        """
        dic_account = load_obj(str(self.account_id))
        return dic_account


    def trade(self,order:dict,time:pd.Timestamp):
        """
        It will do the trading and update the account information.
        :param order: It's a dictionary whose key is the stock id and whose value a dictionary whose key is "type"
                       and "shares",the value is "buy" or "sell" or "Hold" and the num of shares.
        :param time: The trading time.
        """
        dic_account = load_obj(str(self.account_id))
        dic_close_price=Exchange.get_close_price(self,time)
        for stock_id in self.dic_data.keys():
            if order[stock_id]['type']=="buy":
                if not math.isnan(dic_close_price[stock_id]):
                    dic_account[stock_id+"_shares"]+=order[stock_id]['shares']
                    dic_account[stock_id+"_value"]=dic_close_price[stock_id]*dic_account[stock_id+"_shares"]
                    dic_account['cash']=dic_account['cash']-order[stock_id]['shares']*dic_close_price[stock_id]*(1+self.commision+self.slippage_rate)
                else:
                    dic_account[stock_id + "_value"]=0
            elif order[stock_id]['type']=='sell':
                if not math.isnan(dic_close_price[stock_id]):
                    dic_account[stock_id + "_shares"]=dic_account[stock_id + "_shares"]- order[stock_id]['shares']
                    dic_account[stock_id + "_value"] = dic_close_price[stock_id] * dic_account[stock_id + "_shares"]
                    dic_account['cash']=dic_account['cash']+order[stock_id]['shares']*dic_close_price[stock_id]*(1-self.commision-self.slippage_rate)
                else:
                    dic_account[stock_id + "_value"]=0
            else:
                if not math.isnan(dic_close_price[stock_id]):
                    dic_account[stock_id + "_value"] += dic_close_price[stock_id] * dic_account[stock_id + "_shares"]
                else:
                    dic_account[stock_id + "_value"]=0
        dic_account['Total_banlance']=0
        for stock_id in self.dic_data.keys():
            dic_account['Total_banlance']=dic_account['Total_banlance']+dic_account[stock_id+"_value"]
        dic_account['Total_banlance']=dic_account['Total_banlance']+dic_account['cash']
        save_obj(dic_account, str(self.account_id))







