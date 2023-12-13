from random import random
from pyquery import PyQuery as pq
import time, random
import requests
import threading
import json

# @variable timeLimit 访问次数限制。
# @variable timer 计时器。
# @variable requestsHeader 请求头。目前是按照cookie进行登陆的，日后考虑更换为移动端api进行登陆。
# @variable cookie cookie
# @variable user 登陆邮箱的账号名
# @variable password 登陆邮箱的密码
# @variable theHost 邮箱服务器主机
# @instance theServer 连接邮箱实例
# @instance theRequestConn requests实例，用于发起GET请求获取通知内容与页面内容。

global timeLimit
global timer
timeLimit = 0
timer = threading.Timer

requestsHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Connection": "keep-alive"
}

cookie = {
    'cookie': r''
}

user = ""
password = ""
theHost = ""


theRequestConn = requests.session()


# 去除网页不必要内容，返回内容主体
def getContent(oriDom: pq):
    oriDom("script").remove()
    oriDom("input").remove()
    oriDom("form").remove()
    return oriDom(".article")

def getRecommend(oriDom: pq):
    oriDom("script").remove()
    oriDom("input").remove()
    oriDom("form").remove()
    return oriDom(".topic-list")

def getRecommendList(oriDom:pq):
    topics = oriDom('li')

    result_list = []

    # 遍历每个 li 元素，提取信息
    for topic in topics.items():
        title = topic('a').attr('title')
        href = topic('a').attr('href')
        group_name = topic('.group-link').text()

        # 将提取的信息添加到结果列表中
        result_list.append({
            'title': title,
            'href': href,
            'group': group_name
        })

    return result_list

def getTime():
    return time.asctime(time.localtime(time.time()))

# 获取帖子内容，返回对应操作的dom实例
def provideContent(url):
    try:
        html = theRequestConn.get(
            url=url, headers=requestsHeaders, cookies=cookie).content
        dom = getRecommend(pq(html))
        fst = dom.eq(0)
        res = getRecommendList(fst)
        return res
    except Exception as e:
        print("[" + getTime() + "]" + "error occur when trying getting all content")
        print(e)
        return []


from flask import Flask,Response,jsonify
from flask_cors import cross_origin

app = Flask(__name__)


@app.route('/topic/<tid>')
@cross_origin()
def getTopicWithComments(tid):
    results = provideContent('https://www.douban.com/group/topic/{tid}/?_i=23859068DXfnFZ'.format(tid=tid))
    return jsonify(results)




if __name__ == "__main__":
    # 生产环境需要更改。
    app.run()