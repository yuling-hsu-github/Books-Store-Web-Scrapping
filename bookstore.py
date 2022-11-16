#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bookstore webscrapper
A bookstore from Taiwan, just for those people who are going to buy book, 
they could get exaustive info throught this code

@author: leahhsu
"""
import requests
from bs4 import BeautifulSoup
import random
import time
import pandas as pd
'''
Concept from beginning: selenium find the whole book and their categories
BeautifulSoup to translate the html to text then save them into a list
The final step info is going to save in excel

'''
#delaytime in case anti-webscapper
delay_choices = [8, 5, 10, 6, 20, 11]  #延遲的秒數
delay = random.choice(delay_choices)  #隨機選取秒數
time.sleep(delay)

bookname = []
article = []

price = []

book_dic = {"Japanese Literatrual":"https://www.books.com.tw/web/books_bmidm_0101/?o=1&v=1&page=", "Korean_book":"https://www.books.com.tw/web/sys_bbotm/books/010109/?o=1&v=1&page="}


for i in range(1,70):
    print("Page:",i)
    url = "https://www.books.com.tw/web/books_bmidm_0101/?o=1&v=1&page="+str(i+1)
    delay = random.choice(delay_choices)  #隨機選取秒數
    time.sleep(delay)
    r = requests.get(url)
    r.encoding = "utf-8"
    sp = BeautifulSoup(r.text, "lxml")

    #bug here
    top_bookname = sp.select('h4 a', limited = 25)
    for t in top_bookname:
        bookname.append(t.text.strip())
            
    name = sp.select('h4 a')

    #bug with publish and article together and lack the top info of top book
    articles = sp.select('li.info a')
    for a in articles:
        article.append(a.text.strip())
    #bug here
    prices = sp.select('li.set2 strong')
    for p in prices:
        price.append(p.text.strip())
#information split and put them in a variable
bookarticle = article[::2]
publish = article[1::2]
discount = price[::2]
bookprice = price[1::2]
#put info in an excel
df = pd.DataFrame(list(zip(bookname,bookarticle,publish,discount,bookprice)),columns =['Bookname', 'BookAuthor', 'Publisher','BookDiscount', 'BookPrice'])
filename = 'Bookstoreinfo.xlsx'
df.to_excel(filename)
print("Information archieve sucessfully!")
