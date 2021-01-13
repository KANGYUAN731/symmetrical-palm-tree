#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 


# In[94]:


from pandas_datareader import data   
kangyuanDict = {"特斯拉":"TSLA","达乐":"DG","苹果":"AAPL"}
start_date = "2019-12-31"
end_date = "2021-01-01"


# In[95]:


tesla = data.DataReader(kangyuanDict["特斯拉"],"yahoo",start_date,end_date)
dg = data.DataReader(kangyuanDict["达乐"],"yahoo",start_date,end_date)
aapl = data.DataReader(kangyuanDict["苹果"],"yahoo",start_date,end_date)
aapl.describe()


# In[106]:


import matplotlib.pyplot as plt


# In[98]:


plt.plot(tesla["Close"],label="tesla",color="blue")
plt.plot(dg["Close"],label="dg",color="red")
plt.plot(aapl["Close"],label="dg",color="yellow")

plt.title("3 stocks")
plt.show()


# In[100]:


aapl.head()


# In[101]:


'''
定义函数：计算机股票涨跌幅 ＝（现在股价－买入价格）/买入价格
输入参数：column 表示收盘价这一列数据
返回涨跌幅
'''

def change(column):
    # 买入价格 年初
    buyPrice = column[0]
    # 现在价格 年末
    curPrice = column[len(tesla)-1]
    changePrice = (curPrice - buyPrice)/buyPrice
    # 判断股价变化
    if changePrice > 0:
        print('股票累计上涨=',changePrice)
    elif changePrice == 0:
        print('股票累计没有变化=',changePrice)
    else:
        print('股票累计下跌=', changePrice)
    return changePrice


# In[77]:


tesladata = tesla[::-1]
change(tesla["Close"])


# In[84]:


dgdata = dg[::-1]
change(dg["Close"])


# In[102]:


aapldata = aapl[::-1]
change(aapl["Close"])


# In[ ]:




