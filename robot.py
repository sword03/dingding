import requests
import json

class MessageFactory:
    @classmethod
    def make_a_message1(cls):
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "title",
                "text": "#### 解除警告：%s准备金恢复\n\
                    - 币种：btc\n\
                    - 用户存款：1234\n\
                    - 准备金：1111\n\
                    - 准备金率：100,1%%\n\
                    - 时间戳(UTC)：2019.01.01"
            },
            "at": {
                    "isAtAll": True
            }
        }

        return data

    @classmethod
    def make_a_message2(cls):
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "杭州天气",
                "text": "#### 杭州天气 @156xxxx8827\n" + "> 9度，西北风1级，空气良89，相对温度73%\n\n" +
                "> ![screenshot](https://gw.alipayobjects.com/zos/skylark-tools/public/files/84111bbeba74743d2771ed4f062d1f25.png)\n"
                + "> ###### 10点20分发布 [天气](http://www.thinkpage.cn/) \n"
            },
            "at": {
                "atMobiles": ["156xxxx8827", "189xxxx8325"],
                "isAtAll": False
            }
        }
        return data

    @classmethod
    def make_a_message3(cls):
        data = {
            "msgtype": "link",
            "link": {
                "text": "这个即将发布的新版本，创始人陈航（花名“无招”）称它为“红树林”。\
而在此之前，每当面临重大升级，产品经理们都会取一个应景的代号，这一次，为什么是“红树林”？",
                "title": "时代的火车向前开",
                "picUrl": "",
                "messageUrl": "https://news.sohu.com"
            }
        }
        return data

    @classmethod
    def make_a_message4(cls):
        data = {
            "actionCard": {
                "title": "乔布斯 20 年前想打造一间苹果咖啡厅，而它正是 Apple Store 的前身",
                "text": "![screenshot](serverapi2/@lADOpwk3K80C0M0FoA)\
                ### 乔布斯 20 年前想打造的苹果咖啡厅 \
                Apple Store 的设计正从原来满满的科技感走向生活化，而其生活化的走向其实可以追溯到\
            20年前苹果一个建立咖啡馆的计划",
                "hideAvatar": "0",
                "btnOrientation": "0",
                "singleTitle": "阅读全文",
                "singleURL": "https://www.dingtalk.com/"
            },
            "msgtype": "actionCard"
        }
        return data

    @classmethod
    def make_a_message5(cls):
        data = {
            "actionCard": {
                "title": "乔布斯 20 年前想打造一间苹果咖啡厅，而它正是 Apple Store 的前身",
                "text": "![screenshot](serverapi2/@lADOpwk3K80C0M0FoA) \
 ### 乔布斯 20 年前想打造的苹果咖啡厅 \
 Apple Store 的设计正从原来满满的科技感走向生活化，而其生活化的走向其实可以追溯到 20 年前苹果一个建立咖啡馆的计划",
                "hideAvatar": "0",
                "btnOrientation": "1",
                "btns": [
                    {
                        "title": "内容不错",
                        "actionURL": "https://www.dingtalk.com/"
                    },
                    {
                        "title": "不感兴趣",
                        "actionURL": "https://www.dingtalk.com/"
                    }
                ]
            },
            "msgtype": "actionCard"
        }
        return data

    @classmethod
    def make_a_message6(cls):
        data = {
            "feedCard": {
                "links": [
                    {
                        "title": "时代的火车向前开",
                        "messageURL": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI",
                        "picURL": "https://www.dingtalk.com/"
                    },
                    {
                        "title": "时代的火车向前开2",
                        "messageURL": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI",
                        "picURL": "https://www.dingtalk.com/"
                    }
                ]
            },
            "msgtype": "feedCard"
        }
        return data

import time
import hmac
import hashlib
import base64

def calculate_timestamp_sign(secret):
    timestamp = int(round(time.time() * 1000))
    # secret = 'this is secret'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code)
    print(timestamp)
    print(type(timestamp))
    print(sign)
    print(type(sign))
    return timestamp, sign


def notify(robot_url, access_token, info):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    params = {
        "access_token": access_token,
    }
    r = requests.post(robot_url, params=params, headers=headers, data=json.dumps(info))
    print(r.text)
    if r.status_code == 200:
        jo = json.loads(r.text)
        if jo['errcode'] == 0:
            return True
    return False

def notify_with_sig(robot_url, access_token, secret, info):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    timestamp, sign = calculate_timestamp_sign(secret)
    params = {
        "access_token": access_token,
        "timestamp": timestamp,
        "sign": sign
    }
    r = requests.post(robot_url, headers=headers, params=params, data=json.dumps(info))
    print(r.text)
    if r.status_code == 200:
        jo = json.loads(r.text)
        if jo['errcode'] == 0:
            return True
    return False


if __name__ == "__main__":
    msg1 = MessageFactory.make_a_message1()
    msg2 = MessageFactory.make_a_message2()
    msg3 = MessageFactory.make_a_message3()
    msg4 = MessageFactory.make_a_message4()
    msg5 = MessageFactory.make_a_message5()
    msg6 = MessageFactory.make_a_message6()

    # robot1
    robot_url = 'https://oapi.dingtalk.com/robot/send'
    access_token = "5b4243f85a7f72741ae8d4ba09021ee00d933ffe2efdd165cda2db7a58144d3d"
    notify(robot_url, access_token, msg1)
    notify(robot_url, access_token, msg2)
    notify(robot_url, access_token, msg3)
    notify(robot_url, access_token, msg4)
    notify(robot_url, access_token, msg5)
    notify(robot_url, access_token, msg6)

    # robot2, with signature
    access_token = "3aec9d508f8d677568bc7e60b32784ee3f6536646908b39eddee8c0b5e68ea81"
    secret = 'SECb4d978eff0597e2d2d9a69c883d7ac6734dfe48f105b3a40b6586a4b5625887a'
    notify_with_sig(robot_url, access_token, secret, msg6)
