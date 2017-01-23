#-*- coding: utf-8 -*-
__author__ = 'Wu_cf'

import itertools
import os
import re
import sys
import urllib
import requests
from bs4 import BeautifulSoup

sys.path.append('PIL')
from PIL import Image as im


# 生成网址列表
def buildUrls(word):
    #底下这种用法是python3.x
   # word = urllib.parse.quote(word)
    #底下这种用法是python2.x
    word = urllib.quote(word)
    url = "https://www.google.co.jp/search?q={word}&biw=1056&bih=864&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjZr_OIt9XRAhWDU7wKHYfxDuUQ_AUICCgB"
    urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=60))
    return urls

# use BeautifulSoup to extracting images url from google
def resolveImgUrl(html):
    soup = BeautifulSoup(html, 'html.parser')
    imgUrls = []
    for tag in soup.findAll('img'):
        v = tag.get('src', tag.get('dfr-src'))
        imgUrls.append(v)
        print(tag['src'])
        if v is None:
            continue
            print ("v is None")
        return imgUrls


def downImg(imgUrl, dirpath, imgName):
    filename = os.path.join(dirpath, imgName)
    try:
        res = requests.get(imgUrl, timeout=15)
        if str(res.status_code)[0] == "4":
            print str(res.status_code), ":" , imgUrl
            return False
    except Exception as e:
        print "抛出异常：", imgUrl
        print e
        return False
    #图片写入文件
    with open(filename, "wb") as f:
        f.write(res.content)
    return True


def mkDir(dirName):
    dirpath = os.path.join(sys.path[0], dirName)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    return dirpath

def selectImg():
    # 这里路径换成你自己的
    path = '/Volumes/Transcend/git/vino-crawlers/Google/results'
    for x in os.listdir(path):
        if x.endswith('.jpg'):
            # file是图像对象，并没有close（）方法
             print "enter if flow"
             try:
                fp = open(path+x,'rb')
                file = im.open(fp)
             except Exception as e:
                 continue
        x1= file.size[0]
        y1= file.size[1]
        print x1,y1 ,x
        fp.close()
        if x1 < y1:
            try:
                os.remove(path+x)
                print "已删除 %s " % x
            except Exception as e:
                print "抛出异常："
                print e


if __name__ == '__main__':
    word = "v2ex"
    count = 2
    dirpath = mkDir("results")

    urls = buildUrls(word)
    index = 0
    flag = 1
    for url in urls:
        if flag == 2:
            break
        print "正在请求：", url
        html = requests.get(url, timeout=10).content
        imgUrls = resolveImgUrl(html)
        if len(imgUrls) == 0:  # 没有图片则结束
            break

        for url in imgUrls:
            if downImg(url, dirpath, str(index) + ".jpg"):
                index += 1
                if index > int(count):
                    flag = 2
                    break
                print "已下载 %s 张" % index
    print u'开始执行选择图片程序'
    selectImg()
