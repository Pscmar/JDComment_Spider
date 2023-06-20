# -*- encoding: utf-8 -*-
from enum import Flag
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import numpy as np
import requests
import json
import csv
import io

import urllib3

urllib3.disable_warnings()

# 保存评论数据
def commentSave(list_comment):
    '''
    list_comment: 二维list,包含了多条用户评论信息
    '''
    file = io.open('data/JDComment_ThinkPadP15v_all.csv','w',encoding="utf-8",newline = '')
    # file = io.open('data/JDComment_HPzhan99_i7T600.csv','w',encoding="utf-8",newline = '')
    writer = csv.writer(file)
    writer.writerow(['用户ID','评论内容','购买时间','点赞数','回复数','评分','评价时间','产品型号'])#'用户位置',
    for i in range(len(list_comment)):
        writer.writerow(list_comment[i])
    file.close()
    print('存入成功')

def getCommentData(format_url,proc,i,maxPage):
    '''
    format_url: 格式化的字符串框架，在循环中给它添上参数
    proc: 商品的productID，标识唯一的商品号
    i: 商品评论的展示，例如全部商品、晒图、追评、好评等
    maxPage: 商品的评论最大页数
    '''
    sig_comment = []
    global list_comment
    cur_page = 0
    while cur_page < maxPage:
        
        # url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv%s&score=%s&sortType=5&page=%s&pageSize=10&isShadowSku=0&fold=1'%(proc,i,cur_page)
        url = format_url.format(proc,i,cur_page) # 给字符串添上参数
        try:
            response = requests.get(url=url, headers=headers, verify=False)
            time.sleep(np.random.rand()*2)
            jsonData = response.text
            startLoc = jsonData.find('{')
            #print(jsonData[::-1])//字符串逆序
            jsonData = jsonData[startLoc:]
            jsonData = json.loads(jsonData)
            pageLen = len(jsonData['comments'])
            print("当前第%s页"%cur_page)
            for j in range(0,pageLen):
                userId = jsonData['comments'][j]['id']#用户ID
                content = jsonData['comments'][j]['content']#评论内容
                boughtTime = jsonData['comments'][j]['referenceTime']#购买时间
                voteCount = jsonData['comments'][j]['usefulVoteCount']#点赞数
                replyCount = jsonData['comments'][j]['replyCount']#回复数目
                starStep = jsonData['comments'][j]['score']#评分
                creationTime = jsonData['comments'][j]['creationTime']#评价时间
                # location = jsonData['comments'][j]['location']#用户位置
                referenceName = jsonData['comments'][j]['referenceName']#笔记本型号
                sig_comment.append(userId)#每一行数据
                sig_comment.append(content)
                sig_comment.append(boughtTime)
                sig_comment.append(voteCount)
                sig_comment.append(replyCount)
                sig_comment.append(starStep)
                sig_comment.append(creationTime)
                # sig_comment.append(location)
                sig_comment.append(referenceName)
                list_comment.append(sig_comment)
                print(sig_comment)
                sig_comment = []
        except:
            time.sleep(5)
            cur_page -= 1
            print('网络故障或者是网页出现了问题，五秒后重新连接')
        cur_page += 1

if __name__ == "__main__":
    global list_comment
    ua=UserAgent()
    # thinkpadP15v_i7T600
    # # 只看当前商品
    # format_url = 'https://api.m.jd.com/?appid=item-v3&functionId=pc_club_skuProductPageComments&client=pc&clientVersion=1.0.0&t=1686732829760&loginType=3&uuid=122270672.16803204500281358213226.1680320450.1686727382.1686730326.7&{0}&score={1}&sortType=5&page={2}&pageSize=10&isShadowSku=0&fold=1&bbtf=&shield='
    # 页面所有商品
    format_url = 'https://api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments&client=pc&clientVersion=1.0.0&t=1687240016464&loginType=3&uuid=122270672.1423320777.1687232969.1687232970.1687239468.2&{0}&score={1}&sortType=5&page={2}&pageSize=30&isShadowSku=0&fold=1&bbtf=&shield='
    
    #####################################################################

    # # HPzhan99_i7T600
    # # 只看当前商品
    # format_url = 'https://api.m.jd.com/?appid=item-v3&functionId=pc_club_skuProductPageComments&client=pc&clientVersion=1.0.0&t=1686732604299&loginType=3&uuid=122270672.16803204500281358213226.1680320450.1686727382.1686730326.7&{0}&score={1}&sortType=5&page={2}&pageSize=10&isShadowSku=0&fold=1&bbtf=&shield='
    # # 页面所有商品
    # format_url = 'https://api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments&client=pc&clientVersion=1.0.0&t=1687240517762&loginType=3&uuid=122270672.1423320777.1687232969.1687232970.1687239468.2&{0}&score={1}&sortType=5&page={2}&pageSize=20&isShadowSku=0&fold=1&bbtf=&shield='
    # 设置访问请求头
    headers = {
    'Accept': '*/*',
    'Authority':"api.m.jd.com",
    "User-Agent":ua.random,
    'Referer':"https://item.jd.com/",
    'sec-ch-ua':"\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"",
    'sec-ch-ua-mobile': '?0',
    'Sec-Fetch-Dest': 'script',
    'Sec-Fetch-Mode':'no-cors',
    'Sec-Fetch-Site':'same-site',
    'cookie':'__jdu=16803204500281358213226; shshshfpa=6aeff90d-1baa-510c-672e-9ae5e96ee79a-1615545459; shshshfpx=6aeff90d-1baa-510c-672e-9ae5e96ee79a-1615545459; jcap_dvzw_fp=fZdl7g6q1Ps9WwSkcjIJsc6_KgMKnmMz-PyDscKdrqvVjrU3L4u2_JIDl9h_1_bcJL8GIA==; whwswswws=; shshshfp=152866942b46e57e5069788500b03803; TrackID=1xHoWN1vj6YHJWemdayhu_ExIO5ojJGLysR7erhewv1H9qLp6ToPcDWkFXf-UK4nysSrn6BG52tDotlEbXAGO2Dwcu8yQD41pAiyzdBvkuGA; pinId=20Ng2tqKhhIdSFk2S27kurV9-x-f3wj7; areaId=1; ipLoc-djd=1-2800-55811-0; autoOpenApp_downCloseDate_jd_homePage=1686714550477_1; autoOpenApp_downCloseDate_auto=1686714567190_1800000; warehistory="100038768525,100038768525,"; __jdv=122270672%7Ciosapp%7Ct_335139774%7Cappshare%7CWxfriends%7C1686730356150; jsavif=1; __jda=122270672.16803204500281358213226.1680320450.1686727382.1686730326.7; __jdc=122270672; token=e753dfe6bcd3776bd13b3cc6614402d3,2,937072; __tk=20af941faa3ec55366036a424f1eafe3,2,937072; shshshsID=50e4ba3d5e2351ef73a78aaedee8c184_2_1686730704337; 3AB9D23F7A4B3C9B=VJQFZW3TIQKBU56EX3YIVXNUCZIC4Y5PB7QJ7O7YEJ2JCU6O3B67OMNDDBV3WHLVCVV25WNAOQGVO6SXHGUAV2ZWIQ; 3AB9D23F7A4B3CSS=jdd03VJQFZW3TIQKBU56EX3YIVXNUCZIC4Y5PB7QJ7O7YEJ2JCU6O3B67OMNDDBV3WHLVCVV25WNAOQGVO6SXHGUAV2ZWIQAAAAMIXECKZNIAAAAAD6N26XY33ZQG2YX; _gia_d=1; shshshfpb=se8OCKP6ahlSnl4%2B62bxuVg%3D%3D; __jdb=122270672.10.16803204500281358213226|7.1686730326'
    }
    #手机四种颜色对应的产品id参数
    # productid = ['productId=100006795590','136061&productId=5089275','22778&productId=5475612','7021&productId=6784504']
    list_comment = [[]]
    sig_comment = []
    url = format_url.format('productId=100023130207',0,0)
    # url = format_url.format('productId=100038768525',0,0)
    print(url)
    try:
        response = requests.get(url=url, headers=headers, verify=False)
        jsonData = response.text
        startLoc = jsonData.find('{')
        jsonData = jsonData[startLoc:]
        jsonData = json.loads(jsonData)
        print("最大页数%s"%jsonData['maxPage'])
        getCommentData(format_url,'productId=100023130207',0,jsonData['maxPage'])#遍历每一页
        # getCommentData(format_url,'productId=100038768525',0,jsonData['maxPage'])#遍历每一页
    except Exception as e:
        print("the error is ",e)
        print("wating---")
        time.sleep(5)
        #commentSave(list_comment)
    print("---爬取结束，开始存储---")
    commentSave(list_comment)
    print("---存储完成---")
