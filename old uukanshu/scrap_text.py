from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
import re
import helper_func as hf

link = "https://www.uukanshu.com/b/28796/179659.html"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
req = Request(link, headers=headers)
html = urlopen(req)
page = html.read()

# def getChinese(context):
#     context = context.decode("utf-8") # convert context from str to unicode
#     filtrate = re.compile(u'[^\u4E00-\u9FA5]') # non-Chinese unicode range
#     context = filtrate.sub(r'', context) # remove all non-Chinese characters
#     context = context.encode("utf-8") # convert unicode back to str
#     return context

bsObj = BeautifulSoup(page, 'html.parser')
# print([tag.name for tag in bsObj.findAll()])
node = bsObj.find('div', attrs={'id':'contentbox'})
text = node.find_all(text = True, recursive = False)
text = "".join(text)
clean_text = text.encode('latin1').decode('gbk')

print(clean_text)
# tmp = re.sub(u'牋','', clean_text)

# print(tmp)

#######################################################################################################################################################################################################################
# Current Progress: 发现 uukanshu 网站的资源 有缺点:
#  1. 小说内容中 植入 广告, UU 看书.... 之类的 (数据清洗问题)
#  2. 网页结构不同章解有变化, 刚刚研究完了一个 个例的结构, 大部分的结构还没研究
# 
# Alternative: 发现 qu.la 网站比较 ok, 且有 github 能直接 下载 text 
# ###########################################################################################################################################################################################################################################