5
import pandas as pd
import numpy as np
from factorNeutralization.Netralization import Neutralization
from strategy.runLongShort import runLongShort
import pickle

def main():
    stock_pool = pd.read_excel(r'..\data\stock_pool\stock_pool_申万行业.xlsx', index_col=0)[0:616]
    factor = 'BP'

    #因子中性化和标准化
    # path = r'..\data\factor_data\\'
    # datelist = pd.date_range(start='2005-01-31', end='2021-03-31', freq='M')
    # with open(r'./因子//dic_date.pkl', 'rb') as f:
    #     dic_date=pickle.load(f)
    # neutralization=Neutralization(datelist,stock_pool,path,factor,dic_date)
    # neutralization.neutralization()

    #因子多空回测
    runlongshort=runLongShort(factor,10,stock_pool,"2005-01-31","2021-03-31")
    runlongshort.runlongshort(False)

if __name__=="__main__":
    main()