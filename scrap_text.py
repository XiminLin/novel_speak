from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

## charset 可以在 chrome 里面的 network 的 header 里面找 response 的 content-type
## headers 这里是 对应每个 chapter 网页的 header

text_headers = {
'Referer': 'https://www.qu.la/book/4310/',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

## return text of one chapter
def get_text(url):
    req = Request(url, headers = text_headers)
    html = urlopen(req)
    page = html.read()
    bsObj = BeautifulSoup(page, 'html.parser')

    ## get chapter name
    #### #wrapper <==> 'id'='wrapper'
    #### .content_read <==> 'class'='content_read'
    #### This is going down a path 
    #### returns a list
    chapter_name = bsObj.select('#wrapper .content_read .box_con .bookname h1')[0].text

    ## get chapter content
    chapter_text = bsObj.select('#wrapper .content_read .box_con #content')[0]
    for ss in chapter_text.select("script"):  # delete script...
        ss.decompose()

    ## change several spaces to line break
    #### \s+: regular expression for one or several spaces
    chapter_text = re.sub( r'\s+', '\n', chapter_text.text)

    return chapter_name, chapter_text