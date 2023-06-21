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
    file = io.open('data/JDComment_ThinkPadP15v_全部_当前.csv','w',encoding="utf-8",newline = '')
    # file = io.open('data/JDComment_HPzhan99_全部_非时间.csv','w',encoding="utf-8",newline = '')
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
    # 只看当前商品
    format_url = 'https://api.m.jd.com/?appid=item-v3&functionId=pc_club_skuProductPageComments&client=pc&clientVersion=1.0.0&t=1686732829760&loginType=3&uuid=122270672.16803204500281358213226.1680320450.1686727382.1686730326.7&{0}&score={1}&sortType=6&page={2}&pageSize=10&isShadowSku=0&fold=1&bbtf=&shield='
    # # 页面所有商品
    # format_url = 'https://api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments&client=pc&clientVersion=1.0.0&t=1687240016464&loginType=3&uuid=122270672.1423320777.1687232969.1687232970.1687239468.2&{0}&score={1}&sortType=5&page={2}&pageSize=10&isShadowSku=0&fold=1&bbtf=&shield='
    
    #####################################################################

    # # HPzhan99_i7T600
    # # 只看当前商品
    # format_url = 'https://api.m.jd.com/?appid=item-v3&functionId=pc_club_skuProductPageComments&client=pc&clientVersion=1.0.0&t=1686732604299&loginType=3&uuid=122270672.16803204500281358213226.1680320450.1686727382.1686730326.7&{0}&score={1}&sortType=6&page={2}&pageSize=10&isShadowSku=0&fold=1&bbtf=&shield='
    # # 页面所有商品
    # format_url = 'https://api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments&client=pc&clientVersion=1.0.0&t=1687240517762&loginType=3&uuid=122270672.1423320777.1687232969.1687232970.1687239468.2&{0}&score={1}&sortType=5&page={2}&pageSize=10&isShadowSku=0&fold=1&bbtf=&shield='
    
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
    'cookie':'__jdv=76161171|baidu-search|t_262767352_baidusearch|cpc|304792255888_0_7e3dc46c1544410caf637a65e7256a0b|1687232969567; __jdu=1423320777; areaId=1; shshshfpa=632c45e6-710a-d84a-bea3-c8e217ec88a4-1687232970; shshshfpx=632c45e6-710a-d84a-bea3-c8e217ec88a4-1687232970; shshshfpb=vNWH0Uu37HttA3aDgEILhjA; ipLoc-djd=1-2800-55811-0; unpl=JF8EAIZnNSttX0NTVxoBHRMSSQlSW1kBQ0QGb2RQBloMHgBVTwVMQEJ7XlVdXxRKEB9sZxRUXFNLVw4aBisSEHteVVxdCU0fBmxkNWRVUCVUSBtsGHwQBhAZbl4IexcCX2cAV19aSFUDHQQrEyBLW2RubQl7FjNuV046XBVLUQYZABgTFk1bZF9tCw; PCSYCityID=CN_440000_440300_0; jsavif=1; __jda=122270672.1423320777.1687232969.1687249035.1687313527.4; __jdc=122270672; 3AB9D23F7A4B3C9B=4M6BQTUR6Z5K6LYYHEVPBGALIY4C3THJ37LPLSRXD7CQGKG7HDVNWZNC6AZHDM3CZ66ATOJAF3PI5PGPCWUDHADKPQ; token=d76955691c63b656a056d6d3dab71d28,2,937396; __tk=lcexjshiIzTojst1IsaEJsBiIDtxjpfojsezIvjyjpG,2,937396; shshshsID=243fcce5f8483b61d2ce51aed3a6e0fc_3_1687314599588; __jdb=122270672.4.1423320777|4.1687313527; 3AB9D23F7A4B3CSS=jdd034M6BQTUR6Z5K6LYYHEVPBGALIY4C3THJ37LPLSRXD7CQGKG7HDVNWZNC6AZHDM3CZ66ATOJAF3PI5PGPCWUDHADKPQAAAAMI3PEY5MYAAAAAD4MFQPECGCDZ4UX'
    }
    #手机四种颜色对应的产品id参数
    # productid = ['productId=100006795590','136061&productId=5089275','22778&productId=5475612','7021&productId=6784504']
    list_comment = [[]]
    sig_comment = []
    url = format_url.format('productId=100023130207',0,0) # lenovo
    # url = format_url.format('productId=100038768525',0,0) # HP
    print(url)
    try:
        response = requests.get(url=url, headers=headers, verify=False)
        jsonData = response.text
        startLoc = jsonData.find('{')
        jsonData = jsonData[startLoc:]
        jsonData = json.loads(jsonData)
        print("最大页数%s"%jsonData['maxPage'])
        getCommentData(format_url,'productId=100023130207',0,jsonData['maxPage'])#遍历每一页 # lenovo
        # getCommentData(format_url,'productId=100038768525',0,jsonData['maxPage'])#遍历每一页 # HP
    except Exception as e:
        print("the error is ",e)
        print("wating---")
        time.sleep(5)
        #commentSave(list_comment)
    print("---爬取结束，开始存储---")
    commentSave(list_comment)
    print("---存储完成---")
