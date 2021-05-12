# Monitor return of factors of the market

Assign2 aims to monitor the return of factors in the market. According to the 3-Factor model of Fama-French (there are also many other factor models), the return of the stocks can be 
explained by some factors like BP,size. Because of that, there are some trading strategies based on factors. 

But in the investment practice,there are many problems and one of them is that for one factor like BP, in some periods it's a good factor to invest but in some other periods it's
a really bad factors to invest in. So can we have some methods to monitor the performance of the factors.

I refrenced the famous paper of Fama-French, Common risk factors in the returns on stocks and bonds, and I think the method Fama used in this paper can help us to monitor
the perfomance of the factors, that is a long short portfolio. The reason that we use long short is that long short portfolio can remove the influence of beta.

## Function Introduction

 1. factor neutralization and standardization
    
    * It will neutralize log outstanding market capitalization and industry.
    * Use z score method to do standardization.
 

 2. Longshort portfolio net value calculation
    
    * You can upadte the data and monitor the net value of the longshort portfolio.
       
      * There is a package named data, in the package close data is the data of the price, factor data is the factor data.
      
      * In the main package there is a folders named "因子" and in this folder there are some folder named by the factor and after you run the longshort the net value data will be stored here and there will be picture shown.
      
## Enviroment prepared

 * The version of python: 3.8
 * We recommed you to use pycharm. After you download it and you can use pycharm to run it.

## Result 

 I test BP,EP and ROE_TTM factor and I have find some interesting phenomenon.
 
 * The following is the BP longshort net value and it's from 2005 to 2021.

<img src="https://github.com/algo21-220040002/Assign2/blob/master/Paper/BP_longshort_2005-2021.png" width="800" height="400" /><br/>

 * The following is the EP longshort net value and it's from 2005 to 2021. 

<img src="https://github.com/algo21-220040002/Assign2/blob/master/Paper/EP_longshort_2005-2021.png" width="800" height="400" /><br/>
 
 * The following is the ROE_TTM longshort net value and it's from 2005 to 2001.

<img src="https://github.com/algo21-220040002/Assign2/blob/master/Paper/ROE_TTM_longshort_2005-2021.png" width="800" height="400" /><br/>
 
      
    
    

