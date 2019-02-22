#coding:utf-8
import re
import os
import glob
import queue
import time
from bs4 import BeautifulSoup
from urllib.request import Request
from urllib.request import urlopen
import threading

from scrap_text import get_text
from helper_func import create_direc
from helper_func import save_one_chapter
from helper_func import text_to_audio

headers = {
'Referer': 'https://sou.xanbhx.com/search?siteid=qula&q=%E4%BA%BA%E9%81%93%E8%87%B3%E5%B0%8A',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
url = 'https://www.qu.la/book/4310/'
bookname = u'人道至尊'
word_limit = 1024
audio_direc = u'人道至尊读出来'
exitFlag = 0

threadList = list(range(5))
queueLock = threading.Lock()
workQueue = queue.Queue(2000)
threads = []
threadID = 1

def save_book(url, bookname):
    req = Request(url, headers=headers)
    html = urlopen(req)
    page = html.read()

    bsObj = BeautifulSoup(page.decode('utf-8'), 'html.parser')

    all_chapters = bsObj.find('dt', text = re.compile(u'正文') )
    all_chapters = all_chapters.find_next_siblings('dd')

    direc = create_direc(bookname)

    for chapter in all_chapters:
        url = chapter.find('a')['href']
        chapter_name, chapter_text = get_text(''.join(['https://www.qu.la',url]))
        print(chapter_name)
        save_one_chapter(direc, chapter_name, chapter_text)

def chapter_to_audio(chapter):
    with open(os.path.join(bookname, chapter), 'rb') as f:
        text = f.read()
    text = text.decode('utf-8')
    st = 0
    audio = b''
    while st < len(text):
        end = text[:st+word_limit].rindex('\n')
        subtext = text[st:end]
        st = end + 1
        tmp = text_to_audio(subtext)
        if tmp is None: break
        audio += tmp
    with open(os.path.join(audio_direc, chapter[:-4]+'.mp3'), 'wb') as f:
        f.write(audio)

def book_to_audio(bookname):
    files = os.listdir(bookname)
    files = sorted(files, key=lambda x: int(x.split('_')[0]) )
    for chapter in files:
        print(chapter)
        chapter_to_audio(chapter)

class myThread (threading.Thread):
    def __init__(self, threadID, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.q = q

    def run(self):
        print("Starting " + str(self.threadID) )
        while not exitFlag:
            queueLock.acquire()
            if not workQueue.empty():
                chapter = self.q.get()
                queueLock.release()
                chapter_to_audio(chapter)
                print("Exiting " + str(self.threadID) + " " + chapter)
            else:
                queueLock.release()
                time.sleep(1)
                print("Exiting " + str(self.threadID) )
    

def book_to_audio_multi(bookname):
    global exitFlag
    files = os.listdir(bookname)
    files = sorted(files, key=lambda x: int(x.split('_')[0]) )
    files
    # Create new threads
    for threadID in threadList:
        thread = myThread(threadID, workQueue)
        thread.start()
        threads.append(thread)

    # Fill the queue
    queueLock.acquire()
    for word in files:
        workQueue.put(word)
    queueLock.release()

    # Wait for queue to empty
    while not workQueue.empty():
        pass

    # Notify threads it's time to exit
    exitFlag = 1

    # Wait for all threads to complete
    for t in threads:
        t.join()
    print ("Exiting Main Thread")

def sort_chapters():
    from shutil import copyfile
    ## sort these files
    files = os.listdir(bookname)
    files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(bookname, x)))
    for i, f in enumerate(files):
        newname = str(i+1) + '_' + f
        copyfile(os.path.join(bookname, f), os.path.join('tmp', newname))


if __name__ == '__main__':
    # save_book(url, bookname)
    book_to_audio_multi(bookname)

