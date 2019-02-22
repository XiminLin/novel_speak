from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
import time
import re

# encoding 和 decoding 的 学习
# headers 学习
# beautifulsoup parser
# findAll 的时候 确保 decoding 是一样的
# print([tag.name for tag in bsObj.findAll()]) 找到所有的 tag

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
req = Request("https://www.uukanshu.com/b/28796/", headers=headers)
html = urlopen(req)

page = html.read()
print(len(page))
bsObj = BeautifulSoup(page,"html.parser")

links = bsObj.findAll('a', attrs={'target':'_blank'}, text=re.compile('第'.encode('gbk').decode('latin1')))
for link in links[:100]:
    print(link.text.encode("latin1").decode("gbk"))

