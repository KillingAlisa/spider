import json

import requests  # 发送请求
from bs4 import BeautifulSoup  # 解析页面
import pandas as pd  # 存入csv数据
import os  # 判断文件存在
from time import sleep  # 等待间隔
import random  # 随机
import re  # 用正则表达式提取url
from flask import Flask,jsonify,request

app= Flask(__name__)

@app.route('/csdn',methods=['POST'])
def csdn_so():
    response_object = {'status': 'success'}
    post_data = request.get_json();
    query = post_data.get('query')
    #response_object['data'] = get_csdn_result(query)
    get_csdn_result(query)
    return jsonify(response_object)


def get_header():
    # 伪装浏览器请求头
    headers = {
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

def get_real_url(url):
    r = requests.get(url, headers=get_header(), allow_redirects=False)  # 不允许重定向
    if r.status_code == 302:  # 如果返回302，就从响应头获取真实地址
        real_url = r.headers.get('Location')
    else:  # 否则从返回内容中用正则表达式提取出来真实地址
        real_url = re.findall("URL='(.*?)'", r.text)[0]
    print('real_url is:', real_url)
    return real_url

def get_baidu_result():
    query = 'java'
    base_query = ' site:csdn.net'
    url = 'https://www.baidu.com/s?wd=' + query + base_query + '&pn=' + str(10)
    r = requests.get(url, headers=get_header())
    html = r.text
    print('响应码是:{}'.format(r.status_code))
    soup = BeautifulSoup(html, 'html.parser')
    result_list = soup.find_all(class_='result c-container new-pmd')
    print('正在爬取:{},共查询到{}个结果'.format(url, len(result_list)))

def get_csdn_result(query):
    url = 'https://so.csdn.net/so/search?q=' + query + '&t=&u=&urw='
    print(url)
    args = {
        'url': url,
        'timeout': 10,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    }
    r = query_by_splash(args)
    html = r.text
    #print(r.text)
    soup = BeautifulSoup(html, 'html.parser')
    #so_result = soup.find('div',class_='so-result-list min')
    so_result = soup.find(class_='so-list-detail')
    so_result = soup.find(class_='so-list-detail')
    print(so_result)
    index = 1
    #for tag in soup.find(class_='so-result-list min'):
     #   print(tag)
    return so_result

def query_by_splash(args):
    splash_url = 'http://localhost:8050/render.html'
    #response = requests.get(splash_url,data=json.dumps(args),headers={"content-type": "application/json"})
    response = requests.get(splash_url,params=args,headers={"content-type": "application/json"})
    return response

if __name__ == '__main__':
    app.run()

