
import pandas as pd
import numpy as np
import datetime
from sklearn.linear_model import LinearRegression
from scipy.stats.mstats import winsorize
import warnings
warnings.filterwarnings("ignore")

class FactorProcessor:
    """FactorProcessor
    It's used to process the factor including standardization and neutralization.
    """
    def __init__(self,
                 date_list:list,
                 stock_pool:pd.DataFrame,
                 path:str):
        """
        :parameter
        :param date_list:A list includes the timestamp.
        :param stock_pool:
        :param path:
        """
        self.date_list=date_list
        self.stock_pool=stock_pool
        self.path=path

    def dataPreprocessor(self,factor_list:list)->dict:
        """
        将数据按照日期整理到一起
        :return:A dictionary whose key is datetime and value is a dataframe whose index is factor including sector dummy
                and columns are the stock id.
        """
        dic_date={}
        for date in self.date_list:
            dic_date[date]=pd.DataFrame()

        stock_pool=self.stock_pool.join(pd.get_dummies(self.stock_pool.申万行业))   #将行业变成dummy变量
        stock_pool=stock_pool.set_index('stock_id')
        sector_dummy = stock_pool.columns.tolist()
        sector_dummy.remove('company_name')
        sector_dummy.remove('申万行业')

        for stock_id in stock_pool.index:  #遍历股票id
            factor_data=pd.read_excel(self.path +stock_id+".xlsx",index_col=0)  # 读取该股票的因子信息
            df = pd.DataFrame()
            df[stock_id] = stock_pool.loc[stock_id, sector_dummy]
            for date in self.date_list:
                Df=pd.DataFrame()
                Df[stock_id]=factor_data.loc[date,factor_list]
                dic_date[date][stock_id]=pd.concat([Df,df],axis=0)[stock_id]
        self.sector_dummy=sector_dummy
        return dic_date

    def factorNeutral(self,factor:str,dic_date:dict)->dict:
        """
        将因子进行中性化和标准化处理，并采用中位数填充空值
        :return: A dictionary whose key is date and value is dataframe whose index is factor and columns are stock id.
        """
        # dic_date=FactorProcessor.dataPreprocessor(self)   #调用dataPreprocessor函数得到整理好的数据
        # sector_dummy=self.sector_dummy

        stock_pool = self.stock_pool.join(pd.get_dummies(self.stock_pool.申万行业))  # 将行业变成dummy变量
        stock_pool = stock_pool.set_index('stock_id')
        sector_dummy = stock_pool.columns.tolist()
        sector_dummy.remove('company_name')
        sector_dummy.remove('申万行业')

        dic_date_factor = {}                   #存放中性化和标准化后的数据
        for date in self.date_list:
            dic_date_factor[date] = pd.DataFrame()

        for date in self.date_list:
            print(date)
            data=dic_date[date].T
            column_list=sector_dummy
            column_list.append('对数流通市值')
            column_list.append(factor)
            df=data[column_list]
            df=df.dropna()
            df1=df[[factor]]
            df1[factor]=winsorize(df1[factor], limits=[0.015, 0.015])   #对因子值进行缩尾处理
            Y=df1[[factor]].values
            column_list.remove(factor)
            X = df[column_list].values
            model_ols = LinearRegression()  #将因子对行业dummy和流通市值进行回归
            model_ols.fit(X, Y)
            df[factor]=Y-model_ols.predict(X)  #得到残差
            df[factor]=(df[factor]-df[factor].mean())/df[factor].std()    #对因子残差进行标准化
            data1=dic_date[date].T
            data1[factor]=df[factor]
            Df=data1[[factor]]
            Df.fillna(Df.median(),inplace=True) # 填充中位数
            dic_date_factor[date]=Df
        return dic_date_factor









