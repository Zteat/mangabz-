import os
import time
import requests
from selenium import webdriver
from lxml import etree
import json
import re
import execjs
import urllib.parse


def getChapterUrl(url):
    headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
        }
    part_url = "http://www.mangabz.com"
    res = requests.get(url, headers=headers)
    html=res.text
    el = etree.HTML(html)
    a_list = el.xpath('//*[@class="detail-list-form-con"]/a')  #标签中class = container下的第二个div下所有a节点

    k=1
    for a in a_list:   #进每一章的具体网址
        #if(k<176):
        #    k=k+1
        #    continue

        print("start")
        list_title = a.xpath("./text()")[0].replace(' ','').replace('.','').replace('?','')
        page = a.xpath("./span/text()")[0].replace('P','').replace('（','').replace('）','')
        #list_file = "约定的梦幻岛"
        list_file = "ChainsawMan"
        getChapterFile(part_url + a.xpath("./@href")[0], list_file,list_title,page)


def getChapterFile(url,path1,path2,pages):#抓一章的图
    #漫画名称目录
    path=os.path.join(path1)

    session = requests.Session()
    if not os.path.exists(path):
        os.mkdir(path)
    #章节目录
    path=path+'\\'+path2
    if not os.path.exists(path):
        os.mkdir(path)
    headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
        }
    r = requests.get(url, headers=headers, timeout=10)
    mangabz_cid = re.findall("MANGABZ_CID=(.*?);", r.text)[0]
    mangabz_mid = re.findall("MANGABZ_MID=(.*?);", r.text)[0]
    page_total = re.findall("MANGABZ_IMAGE_COUNT=(.*?);", r.text)[0]
    mangabz_viewsign_dt = re.findall("MANGABZ_VIEWSIGN_DT=\"(.*?)\";", r.text)[0]
    mangabz_viewsign = re.findall("MANGABZ_VIEWSIGN=\"(.*?)\";", r.text)[0]

    for i in range(0, int(page_total)):
        #http://image.mangabz.com/1/83/113764/2_8011.jpg?cid=113764&key=8236f2fae2e13757561904696714ebef&uk=
        img_url = url + "chapterimage.ashx?" + "cid=%s&page=%s&key=&_cid=%s&_mid=%s&_dt=%s&_sign=%s" % (mangabz_cid, i, mangabz_cid, mangabz_mid, urllib.parse.quote(mangabz_viewsign_dt), mangabz_viewsign)
        
        r = session.get(img_url, headers=headers, timeout=10)
        headers["Referer"] = r.url
        imagelist = execjs.eval(r.text)
        if(imagelist):
            gett = requests.get(imagelist[0],headers=headers, timeout=10)
            with open(path+'\\'+str(i)+'.png', 'wb') as f:
                f.write(gett.content)
        if(i==int(page_total)-1):
            gett = requests.get(imagelist[1],headers=headers, timeout=10)
            with open(path+'\\'+str(i+1)+'.png', 'wb') as f:
                f.write(gett.content)
        #print(imagelist[0])    
    print('下载完成') 

if __name__ == '__main__':
    #getChapterUrl('http://www.mangabz.com/14862bz/')
    getChapterUrl('http://www.mangabz.com/577bz/')
    