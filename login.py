#-*- coding=utf-8 -*-

import requests
import re
import string
import getpass
import time

url = "http://gw.bupt.edu.cn/"
logout_url = "http://10.3.8.211/F.htm"
s = requests.Session()

def get_used_flow(text):
    pattern = "flow='(.*?)'"
    match = re.search(pattern, text, re.I)
    flow = string.atoi(match.group(1))

    flow0=flow%1024
    flow1=flow-flow0
    flow0=flow0*1000
    flow0=flow0-flow0%1024

    flow3='.'
    if(flow0/1024<10):
        flow3='.00'
    elif(flow0/1024<100):
        flow3='.0'

    s = u"已使用校外流量 Used internet traffic : "+ str(flow1/1024) + flow3 + str(flow0/1024) +" MByte"
    
    print s

def logout():
    r= s.get(logout_url)
    get_gw_state()

def login():
    option = raw_input("是否使用原账号登陆？[y/n]")
    if(option == 'y' or option == 'Y'):
        username = '*********'
        userpass = '*********'
    else:
        username = raw_input("请输入您的用户名")
        userpass = getpass.getpass("请输入您的密码")
    payload = {'DDDDD' : username, 'upass' : userpass, '0MKKey' : ''}
    r = s.post(url, data = payload)
    get_gw_state()

def get_gw_state():
    r = s.get(url)
    pattern = "login-button"
    match = re.search(pattern, r.text, re.I)
    if(match):
        print ("当前状态：您还未登陆网关")
        return False
    else:
        print("当前状态：您已经登陆网关")
        get_used_flow(r.text)
        return True

if __name__== "__main__":
    if(not get_gw_state()):
        option = raw_input("是否登陆网关？[y/n]")
        if(option == 'y' or option == 'Y'):
            login()
        else:
            print ("您并未选择登陆网关，当前处于断网状态")
    else:
        option = raw_input("是否登出网关？[y/n]")
        if(option == 'y' or option == 'Y'):
            logout()
        else:
            print ("您并未选择登出网关，请继续使用网络")
