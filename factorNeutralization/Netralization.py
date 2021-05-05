
import pandas as pd
import numpy as np
import pickle
from factorNeutralization.FactorProcessor import FactorProcessor
import warnings
warnings.filterwarnings("ignore")

def save_obj(path:str,obj:dict, name:str):
    """
    :parameter
    :param obj:The dictionary.
    :param name:The name of the dictionary you want to store.
    """
    with open(path+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(path:str,
             name:str):
    """
    :parameter
    :param name:The name of dictionary.
    :return: The dictionary.
    """
    with open(path+ name + '.pkl', 'rb') as f:
        return pickle.load(f)

class Neutralization:

    def __init__(self,
                 datelist:list,
                 stock_pool:pd.DataFrame,
                 path:str,
                 factor:str,
                 dic_date:str):
        """
        :parameter
        :param datelist:The datelist.
        :param stock_pool:A dataframe that includes the stock id.
        :param path: The path of the factor data that stores.
        :param factor: The factor name.
        :param dic_date: A dictionary whose key is datetime and value is a dataframe whose index is factor and colums are stock id.
        """
        self.datelist=datelist
        self.stock_pool=stock_pool
        self.path=path
        self.factor=factor
        self.dic_date=dic_date

    def neutralization(self):
        """
        将因子进行行业和市值中性化并将其储存到指定路径
        """
        factorprocessor=FactorProcessor(self.datelist,self.stock_pool,self.path)
        dic=factorprocessor.factorNeutral(self.factor,self.dic_date)
        save_obj(r'./因子//'+self.factor+'//', dic, 'dic_neutral_'+self.factor)
