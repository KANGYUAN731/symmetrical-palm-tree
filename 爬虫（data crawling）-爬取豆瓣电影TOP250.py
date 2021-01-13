#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[17]:


# 构造分页数字列表
page_indexs = range(0, 250, 25) #豆瓣top250的分页构造0→25→50直到250


# In[18]:


list(page_indexs)


# In[19]:


def download_all_htmls():
    """
    下载所有列表页面的HTML，用于后续的分析
    """
    htmls = []
    for idx in page_indexs:
        url = f"https://movie.douban.com/top250?start={idx}&filter="  #讲豆瓣top250的分页参数替换成建构的list
        print("craw html:", url)
        #为了屏蔽豆瓣的反爬功能，增强headers
        r = requests.get(url,
                        headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"})
        if r.status_code != 200:
            raise Exception("error")
        htmls.append(r.text)
    return htmls


# In[20]:


# 执行爬取
htmls = download_all_htmls()


# In[21]:


htmls[0]


# In[28]:


def parse_single_html(html):  #传入一个html并返回数据
    """
    解析单个HTML，得到数据
    @return list({"link", "title", [label]})
    """
    soup = BeautifulSoup(html, 'html.parser')
    article_items = (
        soup.find("div", class_="article")  #对照html找出我们信息所在的位置及内容
            .find("ol", class_="grid_view")
            .find_all("div", class_="item")
    )
    datas = []
    for article_item in article_items:
        rank = article_item.find("div", class_="pic").find("em").get_text()
        info = article_item.find("div", class_="info")
        title = info.find("div", class_="hd").find("span", class_="title").get_text()
        stars = (
            info.find("div", class_="bd")
                .find("div", class_="star")
                .find_all("span")   #共4个span，所以使用find_all
        )
        rating_star = stars[0]["class"][0]  #class属性有多个，取第【0】个
        rating_num = stars[1].get_text()
        comments = stars[3].get_text()  #评价人数
        
        datas.append({
            "rank":rank,
            "title":title,
            "rating_star":rating_star.replace("rating","").replace("-t",""),  #去掉评级的前缀和后缀
            "rating_num":rating_num,
            "comments":comments.replace("人评价", "")  #去掉后缀“人评价”
        })
    return datas
    


# In[29]:


import pprint
pprint.pprint(parse_single_html(htmls[0]))


# In[31]:


#对页面进行再分析
all_datas = []
for html in htmls:
    all_datas.extend(parse_single_html(html))


# In[32]:


all_datas


# In[33]:


len(all_datas)


# In[35]:


#存入excel
import pandas as pd
df = pd.DataFrame(all_datas)
df


# In[36]:


df.to_excel("豆瓣电影TOP250.xlsx")


# In[ ]:




