import os
from aip import AipSpeech

default_direc = "."
APP_ID = '15598362'
API_KEY = 'yOUSnEVqfQzG3zuyjzCknEDh'
SECRET_KEY = 'oZMNY8r4WlCVY3Yk6HwYMvY1DIqt4aL9'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def create_direc(book_name):
    direc = os.path.join(default_direc, book_name)
    try:
        os.mkdir(direc)
    finally:
        return direc

def save_one_chapter(direc, chapter_name, chapter_text):
    with open(os.path.join(direc,chapter_name+'.txt'), 'wb') as f:
        f.write(chapter_text.encode('utf-8'))


def text_to_audio(text):
    result  = client.synthesis(text, 'zh', 1, {
        'per': 3,
        'vol': 5,
        'pit': 5,
        'spd': 5
    })

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        return result
    else:
        print(result)
