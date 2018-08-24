#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import requests
import json
import time
import _thread
import itchat

from itchat.content import *

URL = 'http://qxu1606520315.my3w.com/'
jx3cw = {}
jx3cwUserName = ''
responseText = ''
#responseName = ''
FromUserName = ''
jx3GW = ''

def returnTips():
    return '格式错误，请输入 奇遇 或者 奇遇,雪山恩仇 或者 奇遇，雪山恩仇'

def returnPetTips():
    return '格式错误，请输入 宠物 或者 宠物,小叮当'

def getInfoString(name, last_time, cd_time, trigger):
    last_time_str = time.strftime("%m-%d %H:%M:%S", time.localtime(last_time / 1000))
    cd_time_str = ''
    if cd_time == 0:
        cd_time_str = '无内置cd'
    else:
        cd = int(time.time() - (last_time / 1000)) - cd_time * 60 * 60  # 秒为单位
        if abs(cd) // (3600) >= 24:
            cd_time_str = '%d天%d小时%d分%d秒' % \
                          (abs(cd) // (3600) // 24,
                           (abs(cd) - (abs(cd) // (3600) // 24) * 24 * 3600) // (3600),
                           (abs(cd) - abs(cd) // (3600) * 3600) // 60,
                           abs(cd) % 60)
        else:
            cd_time_str = '%d小时%d分%d秒' % \
                          (abs(cd) // (3600),
                           (abs(cd) - abs(cd) // (3600) * 3600) // 60,
                           abs(cd) % 60)
        if cd <= 0:
            cd_time_str = '还需' + cd_time_str
        else:
            cd_time_str = '已进' + cd_time_str
    reply = name + ' ' + trigger + ' ' + last_time_str + '(' + cd_time_str + ')'
    return  reply

def get_response(type, isname=0, name='雪山恩仇'):
    if type == '奇遇':
        if isname == 0:
            data = {
                'act': 'searchQiyuAll'
            }
        else:
            data = {
                'act': 'searchQiyuByName',
                'name': name
            }
    else:
        pass
    try:
        r = requests.post('http://qxu1606520315.my3w.com/query/controller.php',data=data).text
        rjson = json.loads(r)
        reply = ''
        if rjson['status'] == 1:
            if isname == 1:
                name = rjson['info']['name']
                last_time = int(rjson['info']['last_time'])
                cd_time = int(rjson['info']['cd_time'])
                trigger = rjson['info']['trigger']
                return getInfoString(name, last_time, cd_time, trigger)
            elif isname == 0:
                for x in rjson['info']:
                    name = x['name']
                    last_time = int(x['last_time'])
                    cd_time = int(x['cd_time'])
                    trigger = x['trigger']
                    reply += getInfoString(name, last_time, cd_time, trigger) +'\r\n'
                return reply
            else:
                pass
        else:
            return '查询失败，请重试或按正确格式查询，输入如 奇遇 或者 奇遇,雪山恩仇 或者 奇遇，雪山恩仇'
    except BaseException as e:
        return repr(e)

def get_cwresponse(petname=''):
    if petname == '':
        ret = itchat.send('梦江南', toUserName=jx3cwUserName)
        return
        # global responseText
        # text = responseText
        # if text == '':
        #     return '稍后再试'
        # else:
        #     responseText = ''
        #     return text
    else:
        ret = itchat.send('梦江南,'+petname, toUserName=jx3cwUserName)
        return
        # global responseText
        # text = responseText
        # if text == '':
        #     return '稍后再试'
        # else:
        #     responseText = ''
        #     return text

def get_reply(msg):
    msglist = msg.replace('，', ',').split(',')
    if len(msglist) == 1:
        if msglist[0] == '奇遇':
            #get_response(msglist[0])
            return '难产'
        elif msglist[0] == '宠物':
            return get_cwresponse()
        else:
            return
    elif len(msglist) == 2:
        if msglist[0] == '奇遇':
            #get_response(msglist[0], isname=1, name=msglist[1])
            return '难产'
        elif msglist[0] == '宠物':
            return get_cwresponse(msglist[1])
        else:
            return ''
    else:
        return

@itchat.msg_register([TEXT,NOTE,SHARING])
def text_reply(msg):
    global FromUserName
    if msg['MsgType'] == 49:
        print('FileName=%s \n url=%s' % (msg['FileName'], msg['Url']))
        return
    elif msg['MsgType'] == 1:
        FromUserName = msg['FromUserName']
        return get_reply(msg['Text'])
    return

@itchat.msg_register(TEXT, isGroupChat=True)
def text_groupReply(msg):
    global FromUserName
    FromUserName = msg['FromUserName']
    return get_reply(msg['Text'])

@itchat.msg_register([TEXT,NOTE,SHARING], isMpChat=True)
def text_groupReply(msg):
    if msg['FromUserName'] == jx3cwUserName:
        global responseText
        responseText= msg['Text']
        global FromUserName
        itchat.send_msg(responseText+'\n宠物查询数据 Powered by "鸭鸭全知道"', toUserName=FromUserName)
        FromUserName = ''
        responseText = ''
        return
    elif msg['FromUserName'] == jx3GW:
        if msg['MsgType'] == 49:
            print('FileName=%s \n url=%s'%(msg['FileName'], msg['Url']))
        return

# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
itchat.auto_login(hotReload=True)
mps = itchat.search_mps(name='剑三宠物查询')
jx3cwUserName = mps[0]['UserName']
jx3GW = itchat.search_mps(name='剑网3')[0]['UserName']
#jx3cw = itchat.search_mps(userName='剑三宠物查询')
itchat.run()
