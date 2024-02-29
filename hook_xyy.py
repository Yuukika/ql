"""
cron: 30 */30 8-22 * * *
new Env('小阅阅阅读');
"""
# export xyyyd='备注#ysmuid#unionId#提现金额#wxpusherToken#topicId#支付宝姓名#支付宝账号&备注#ysmuid#unionId#提现金额#wxpusherToken#topicId#支付宝姓名#支付宝账号'
import hashlib  # line:28:import hashlib
import json  # line:29:import json
import math  # line:30:import math
import os  # line:31:import os
import random  # line:34:import random
import re  # line:35:import re
import time  # line:32:import time
from urllib.parse import (
    parse_qs,
    urlsplit,
)  # line:38:from urllib.parse import parse_qs, urlsplit
from urllib.parse import (
    quote,
    urlparse,
)  # line:36:from urllib.parse import quote, urlparse, parse_qs

import requests  # line:33:import requests
import urllib3  # line:37:import urllib3

urllib3.disable_warnings()  # line:40:urllib3.disable_warnings()
wxpusherAppToken = os.getenv("wxpusherAppToken") or ""
wxpusherTopicId = os.getenv("wxpusherTopicId") or ""
wechatBussinessKey = os.getenv("wechatBussinessKey") or ""

autman_push_config = os.getenv("autman_push_config") or ""


# autman 推送配置
# export autman_push_config='{
#     "url":"http://ip:port/push",
#     "token":"自定义token",
#     "plat":"wb",
#     "userId":"用户ID",
#     "groupCode":"群号"
# }'


def push(appToken, topicIds, title, link, text, type):
    datapust = {
        "appToken": appToken,
        "content": f"""<body onload="window.location.href='{link}'">出现检测文章！！！\n<a style='padding:10px;color:red;font-size:20px;' href='{link}'>点击我打开待检测文章</a>\n请尽快点击链接完成阅读\n备注：{text}</body>""",
        "summary": title or "小阅阅阅读",
        "contentType": 2,
        "topicIds": [int(topicIds)],
        "url": link,
    }  # line:56:}

    urlpust = "http://wxpusher.zjiecode.com/api/send/message"
    try:  # line:59:try:
        p = requests.post(url=urlpust, json=datapust, verify=False)
        print(datapust)
        print(p.text)
        if p.json()["code"] == 1000:
            print("✅ 推送文章到微信成功，请尽快前往点击文章，不然就黑号啦！")
            return True  # line:64:return True
        else:  # line:65:else:
            print("❌ 推送文章到微信失败，完犊子，要黑号了！")  # line:66:print("❌ 推送文章到微信失败，完犊子，要黑号了！")
            return False  # line:67:return False
    except:  # line:68:except:
        print("❌ 推送文章到微信失败，完犊子，要黑号了！")  # line:69:print("❌ 推送文章到微信失败，完犊子，要黑号了！")
        return False  # line:70:return False


def pushWechatBussiness(robotKey, link):
    datapust = {"msgtype": "text", "text": {"content": link}}
    urlpust = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + robotKey
    try:  # line:77:try:
        p = requests.post(url=urlpust, json=datapust, verify=False)
        if p.json()["errcode"] == 0:
            print("✅ 推送文章到企业微信成功！")  # line:81:print("✅ 推送文章到企业微信成功！")
            return True  # line:82:return True
        else:  # line:83:else:
            print("❌ 推送文章到企业微信失败！")  # line:84:print("❌ 推送文章到企业微信失败！")
            return False  # line:85:return False
    except:  # line:86:except:
        print("❌ 推送文章到企业微信失败！")  # line:87:print("❌ 推送文章到企业微信失败！")
        return False  # line:88:return False


def pushAutMan(link):
    if not autman_push_config or autman_push_config == "":
        print("❌ 推送文章到企业微信失败！")
        return
    config = json.loads(autman_push_config)
    print(config)
    datapust = {
        "token": config['token'],
        "plat": config['plat'],
        "groupCode": config['groupCode'],
        "userId": config['userId'],
        "title": "阅读检测推送【小阅阅】",
        "content": f"快点下方链接\n{link}\n等待时间：17秒 ,别耽搁时间了"
    }
    try:  # line:77:try:
        p = requests.post(url=config['url'], json=datapust, verify=False)
        if p.json()["ok"]:
            print("✅ 推送文章到autman成功！")  # line:81:print("✅ 推送文章到企业微信成功！")
            return True  # line:82:return True
        else:  # line:83:else:
            print("❌ 推送文章到autman失败！")  # line:84:print("❌ 推送文章到企业微信失败！")
            return False  # line:85:return False
    except:  # line:86:except:
        print("❌ 推送文章到autman失败！")  # line:87:print("❌ 推送文章到企业微信失败！")
        return False  # line:88:return False


def getinfo(link):
    try:  # line:92:try:
        r = requests.get(link, verify=False)
        html = re.sub("\s", "", r.text)
        biz = re.findall('varbiz="(.*?)"\|\|', html)
        if biz != []:
            biz = biz[0]
        if biz == "" or biz == []:
            if "__biz" in link:
                biz = re.findall("__biz=(.*?)&", link)
                if biz != []:
                    biz = biz[0]
        nickname = re.findall('varnickname=htmlDecode\("(.*?)"\);', html)
        if nickname != []:
            nickname = nickname[0]
        user_name = re.findall('varuser_name="(.*?)";', html)
        if user_name != []:
            user_name = user_name[0]
        msg_title = re.findall("varmsg_title='(.*?)'\.html\(", html)
        if msg_title != []:
            msg_title = msg_title[0]
        text = f"公众号唯一标识：{biz}|文章:{msg_title}|作者:{nickname}|账号:{user_name}"
        print(text)
        return nickname, user_name, msg_title, text, biz
    except Exception as e:  # line:116:except Exception as e:
        print("❌ 提取文章信息失败")  # line:118:print("❌ 提取文章信息失败")
        return False  # line:119:return False


def ts():  # line:122:def ts():
    return (
            str(int(time.time())) + "000"
    )  # line:123:return str(int(time.time())) + "000"


checkDict = {
    "MzkxNTE3MzQ4MQ==": ["香姐爱旅行", "gh_54a65dc60039"],
    "Mzg5MjM0MDEwNw==": ["我本非凡", "gh_46b076903473"],
    "MzUzODY4NzE2OQ==": ["多肉葡萄2020", "gh_b3d79cd1e1b5"],
    "MzkyMjE3MzYxMg==": ["Youhful", "gh_b3d79cd1e1b5"],
    "MzkxNjMwNDIzOA==": ["少年没有乌托邦3", "gh_b3d79cd1e1b5"],
    "Mzg3NzUxMjc5Mg==": ["星星诺言", "gh_b3d79cd1e1b5"],
    "Mzg4NTcwODE1NA==": ["斑马还没睡123", "gh_b3d79cd1e1b5"],
    "Mzk0ODIxODE4OQ==": ["持家妙招宝典", "gh_b3d79cd1e1b5"],
    "Mzg2NjUyMjI1NA==": ["Lilinng", "gh_b3d79cd1e1b5"],
    "MzIzMDczODg4Mw==": ["有故事的同学Y", "gh_b3d79cd1e1b5"],
    "Mzg5ODUyMzYzMQ==": ["789也不行", "gh_b3d79cd1e1b5"],
    "MzU0NzI5Mjc4OQ==": ["皮蛋瘦肉猪", "gh_58d7ee593b86"],
    "Mzg5MDgxODAzMg==": ["北北小助手", "gh_58d7ee593b86"],
    "MzIzMDczODg4Mw==": ["有故事的同学Y", "gh_b8b92934da5f"],
    "MzkxNDU1NDEzNw==": ["小阅阅服务", "gh_e50cfefef9e5"],
}  # line:142:}


class HHYD:  # line:145:class HHYD:
    def __init__(self, cg):
        self.unionId = cg["unionId"]
        self.ysm_uid = cg["ysm_uid"]
        self.txbz = cg["txbz"]
        self.topicIds = cg["topicIds"]
        self.appToken = cg["appToken"]
        global wechatBussinessKey
        self.wechatBussinessKey = wechatBussinessKey or ""
        global autman_push_config
        self.autman_push_config = autman_push_config or None
        self.aliAccount = cg["aliAccount"] or ""
        self.aliName = cg["aliName"] or ""
        self.name = cg["name"]
        self.domnainHost = "1698855139.hxiong.top"  # line:158:self.domnainHost = "1698855139.hxiong.top"
        self.exchangeParams = ""  # line:159:self.exchangeParams = ""
        self.headers = {
            "Connection": "keep-alive",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": f"http://{self.domnainHost}/",
            "Origin": f"http://{self.domnainHost}",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": f"ysm_uid={self.ysm_uid};",
        }  # line:172:}
        self.sec = requests.session()
        self.sec.verify = False  # line:174:self.sec.verify = False
        self.sec.headers = self.headers
        self.lastbiz = ""  # line:176:self.lastbiz = ""

    def user_info(self):  # line:178:def user_info(self):
        u = f"http://{self.domnainHost}/yunonline/v1/sign_info?time={ts()}&unionid={self.unionId}"  # line:179:u = f"http://{self.domnainHost}/yunonline/v1/sign_info?time={ts()}&unionid={self.unionId}"
        r = ""  # line:180:r = ""
        try:  # line:181:try:
            r = self.sec.get(u)
            rj = r.json()
            if rj.get("errcode") == 0:
                print(
                    f"账号[{self.name}]获取信息成功，当前阅读文章每篇奖励 {r.json()['data']['award']}个金币"
                )  # line:187:)
                return True  # line:188:return True
            else:  # line:189:else:
                print(f"账号[{self.name}]获取用户信息失败，账号异常 或者 ysm_uid无效，请检测ysm_uid是否正确")
                return False  # line:191:return False
        except:  # line:192:except:
            print(r.text)  # line:193:print(r.text)
            print(
                f"账号[{self.name}]获取用户信息失败,ysm_uid无效，请检测ysm_uid是否正确"
            )  # line:194:print(f"账号[{self.name}]获取用户信息失败,ysm_uid无效，请检测ysm_uid是否正确")
            return False  # line:195:return False

    def hasWechat(self):  # line:197:def hasWechat(self):
        r = ""  # line:198:r = ""
        try:  # line:199:try:
            u = f"http://{self.domnainHost}/yunonline/v1/hasWechat?unionid={self.unionId}"  # line:200:u = f"http://{self.domnainHost}/yunonline/v1/hasWechat?unionid={self.unionId}"
            r = self.sec.get(u)
            print(f"账号[{self.name}]判断公众号任务数量：{r.json()['data']['has']}")
        except:  # line:203:except:
            print(f"账号[{self.name}]判断是否有公众号任务失败：{r.text}")
            return False  # line:205:return False

    def gold(self):  # line:207:def gold(self):
        r = ""  # line:208:r = ""
        try:  # line:209:try:
            u = f"http://{self.domnainHost}/yunonline/v1/gold?unionid={self.unionId}&time={ts()}"  # line:210:u = f"http://{self.domnainHost}/yunonline/v1/gold?unionid={self.unionId}&time={ts()}"
            r = self.sec.get(u)
            rj = r.json()  # line:213:rj = r.json()
            self.remain = math.floor(
                int(rj.get("data").get("last_gold"))
            )  # line:214:self.remain = math.floor(int(rj.get("data").get("last_gold")))
            print(f'今日已经阅读了{rj.get("data").get("day_read")}篇文章,剩余{rj.get("data").get("remain_read")}未阅读，今日获取金币{rj.get("data").get("day_gold")}，剩余{self.remain}')  # line:217:)
        except:  # line:218:except:
            print(f"账号[{self.name}]获取金币失败")
            return False  # line:220:return False

    def getKey(self):  # line:222:def getKey(self):
        uk = ""  # line:223:uk = ""
        ukRes = None  # line:224:ukRes = None
        for i in range(10):  # line:225:for i in range(10):
            u = f"http://{self.domnainHost}/yunonline/v1/wtmpdomain"  # line:226:u = f"http://{self.domnainHost}/yunonline/v1/wtmpdomain"
            p = f"unionid={self.unionId}"  # line:228:p = f"unionid={self.unionId}"
            r = requests.post(u, headers=self.headers, data=p, verify=False)
            rj = r.json()  # line:231:rj = r.json()
            domain = rj.get("data").get("domain")
            pp = parse_qs(urlparse(domain).query)
            hn = urlparse(domain).netloc
            uk = pp.get("uk")[0]
            ukRes = r.text
            if uk:  # line:238:if uk:
                break  # line:239:break
        if uk == "":  # line:240:if uk == "":
            print(f"账号[{self.name}]获取uk失败，返回错误：{ukRes}")
            return  # line:242:return
        time.sleep(8)  # line:243:time.sleep(8)
        r = requests.get(
            domain,
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Host": f"{hn}",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
            },
            verify=False,
        )  # line:260:)
        print(f"账号[{self.name}] 阅读准备成功 即将开始阅读 ✅ ，阅读参数为：{uk}")
        h = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Host": "nsr.zsf2023e458.cloud",
            "Origin": f"https://{hn}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
        }  # line:274:}
        return uk, h  # line:275:return uk, h

    def read(self):  # line:277:def read(self):
        info = self.getKey()  # line:278:info = self.getKey()
        if len(info) == 0:  # line:279:if len(info) == 0:
            print(f"账号[{self.name}]获取阅读参数失败，停止往后阅读！⚠️ ")
            return  # line:281:return
        time.sleep(2)  # line:283:time.sleep(2)
        arctileTime = 1  # line:284:arctileTime = 1
        lastestArcticleId = ""  # line:285: = ""
        while True:  # line:286:while True:
            res = {"errcode": -1}  # line:287:res = {"errcode": -1}
            refreshTime = 0  # line:288:refreshTime = 0
            while (
                    res["errcode"] != 0
            ):  # line:289:while res["errcode"] != 0:
                timeStamp = str(ts())  # line:290:timeStamp = str(ts())
                psgn = hashlib.md5(
                    (
                            info[1]["Origin"].replace("https://", "")[:11]
                            + info[0]
                            + timeStamp
                            + "A&I25LILIYDS$"
                    ).encode()
                ).hexdigest()  # line:298:).hexdigest()
                self.params = {"uk": info[0], "time": timeStamp, "psgn": psgn}
                u = f"https://nsr.zsf2023e458.cloud/yunonline/v1/do_read"  # line:300:u = f"https://nsr.zsf2023e458.cloud/yunonline/v1/do_read"
                r = requests.get(
                    u,
                    headers=info[1],
                    params=self.params,
                    verify=False,
                    timeout=60,
                )  # line:303:)
                print("-" * 50)  # line:304:print("-" * 50)
                if r.text and r.json()["errcode"] == 0:
                    res = r.json()
                    print(f"账号[{self.name}]第[{refreshTime + 1}]次获取第[{arctileTime}]篇阅读文章[{info[0]}]跳转链接成功")  # line:313:)
                else:  # line:314:else:
                    decoded_str = json.loads(
                        r.text
                    )  # line:315:decoded_str = json.loads(r.text)
                    if decoded_str["msg"]:  # line:316:if decoded_str["msg"]:
                        print(f"账号[{self.name}]第[{refreshTime + 1}]次获取第[{arctileTime}]篇阅读文章[{info[0]}]跳转链接失败：{decoded_str['msg']}")  # line:319:)
                        return False  # line:320:return False
                    else:  # line:321:else:
                        print(f"账号[{self.name}]第[{refreshTime + 1}]次获取第[{arctileTime}]篇阅读文章[{info[0]}]跳转链接失败：{r.text}")  # line:324:)
                time.sleep(1.5)  # line:325:time.sleep(1.5)
                refreshTime = refreshTime + 1
                if refreshTime >= 5:  # line:327:if refreshTime >= 5:
                    print(f"⚠️ 账号[{self.name}]获取阅读第[{arctileTime}]篇文章[{info[0]}]超时……")
                    return  # line:329:return
            wechatPostLink = ""  # line:330:wechatPostLink = ""
            if res.get("errcode") == 0:
                returnLink = ""  # line:332:returnLink = ""
                try:  # line:333:try:
                    returnLink = res.get("data").get("link")
                except Exception as O0O000000O0O0000O:  # line:335:except Exception as e:
                    print(f"⚠️ 账号[{self.name}]获取阅读第[{arctileTime}]篇文章[{info[0]}]链接失败，疑似台子接口太垃圾，崩了，返回数据为：",res.get("data"))  # line:339:)
                    continue  # line:340:continue
                if "mp.weixin.qq.com" in returnLink:
                    print(f"账号[{self.name}] 阅读第[{arctileTime}]篇微信文章：{returnLink}")
                    wechatPostLink = returnLink
                else:  # line:344:else:
                    wechatPostLink = self.jump(returnLink)
                    print(f"账号[{self.name}] 阅读第[{arctileTime}]篇微信文章：{wechatPostLink}")
                print(f"账号[{self.name}] 阅读第[{arctileTime}]篇文章：{wechatPostLink}")
                a = getinfo(wechatPostLink)
                if not a:  # line:350:if a == False:
                    print(f"⚠️ 账号[{self.name}]因 获取公众号文章信息不成功，导致阅读第[{arctileTime}]篇文章[{info[0]}] 失败……")  # line:353:)
                    return False  # line:354:return False
                sleepTime = random.randint(7, 10)
                if checkDict.get(a[4]) is not None or (lastestArcticleId == wechatPostLink) or (
                        "&chksm=" in wechatPostLink):  # line:361:):
                    sleepTime = random.randint(15, 20)
                    print(
                        f"⚠️ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}] 检测到疑似检测文章，正在推送，等待过检测，等待时间：{sleepTime}秒。。。")  # line:365:)
                    if self.wechatBussinessKey:
                        pushWechatBussiness(self.wechatBussinessKey, wechatPostLink)
                    elif self.appToken:  # line:368:elif self.appToken:
                        push(
                            self.appToken,
                            self.topicIds,
                            "小阅阅阅读过检测",
                            wechatPostLink,
                            f"账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}] 正在等待过检测，等待时间：{sleepTime}秒\n提示：快点，别耽搁时间了！",
                            "xyyyd",
                        )  # line:376:)
                    if self.autman_push_config:  # line:377:else:
                        pushAutMan(wechatPostLink)
                        return False  # line:381:return False
                else:  # line:382:else:
                    print(f"✅ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}] 非检测文章，模拟读{sleepTime}秒")  # line:385:)
                lastestArcticleId = wechatPostLink
                self.lastbiz = a[4]
                time.sleep(sleepTime)  # line:388:time.sleep(sleepTime)
                u1 = f"http://nsr.zsf2023e458.cloud/yunonline/v1/get_read_gold?uk={info[0]}&time={sleepTime}&timestamp={ts()}"  # line:389:u1 = f"http://nsr.zsf2023e458.cloud/yunonline/v1/get_read_gold?uk={info[0]}&time={sleepTime}&timestamp={ts()}"
                r1 = requests.get(u1, headers=info[1], verify=False)
                if r1.text and r1.json():
                    try:  # line:392:try:
                        print(
                            f"✅ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]所得金币：{r1.json()['data']['gold']}个，账户当前金币：{r1.json()['data']['last_gold']}个，今日已读：{r1.json()['data']['day_read']}次，今日未读 {r1.json()['data']['remain_read']}篇文章")  # line:395:)
                    except Exception as e:  # line:396:except Exception as e:
                        print(
                            f"❌ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]异常：{r1.json().get('msg')}")  # line:399:)
                        if "本次阅读无效" in r1.json().get("msg"):
                            continue  # line:401:continue
                        else:  # line:402:else:
                            break  # line:403:break
                else:  # line:404:else:
                    print(f"❌ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]失败：{r1.text}")  # line:407:)
                    break  # line:408:break
            elif res.get("errcode") == 405:
                print(f"⚠️ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]阅读重复")
                time.sleep(1.5)  # line:411:time.sleep(1.5)
            elif res.get("errcode") == 407:
                print(f"⚠️ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]阅读结束")
                return True  # line:414:return True
            else:  # line:415:else:
                print(f"⚠️ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]未知情况")
                time.sleep(1.5)  # line:417:time.sleep(1.5)
            arctileTime = arctileTime + 1

    def jump(self, link):  # line:420:def jump(self, link):
        print(f"账号[{self.name}]开始本次阅读……")
        hn = urlparse(link).netloc
        h = {
            "Host": hn,
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh",
            "Cookie": f"ysm_uid={self.ysm_uid}",
        }  # line:432:}
        r = requests.get(link, headers=h, allow_redirects=False, verify=False)
        Location = r.headers.get("Location")
        print(f"账号[{self.name}]开始阅读文章 - {Location}")  # line:436:print(f"账号[{self.name}]开始阅读文章 - {Location}")
        return Location  # line:437:return Location

    def withdraw(self):  # line:439:def withdraw(self):
        if int(self.remain) < int(self.txbz):
            print(f"账号[{self.name}]没有达到提现标准")
            return False  # line:442:return False
        gold = int(int(self.remain) / 1000) * 1000
        print(f"账号[{self.name}]本次提现金币", gold)
        if gold:
            query = urlsplit(self.exchangeParams).query
            exchangeParams = parse_qs(query)  # line:447:
            for key, value in exchangeParams.items():
                exchangeParams[key] = value[0]
            u1 = f"http://{self.domnainHost}/yunonline/v1/user_gold"  # line:452:u1 = f"http://{self.domnainHost}/yunonline/v1/user_gold"
            p1 = f"unionid={exchangeParams['unionid']}&request_id={exchangeParams['request_id']}&gold={gold}"  # line:453:p1 = f"unionid={exchangeParams['unionid']}&request_id={exchangeParams['request_id']}&gold={gold}"
            r = requests.post(
                u1,
                data=p1,
                headers={
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Cookie": f"ysmuid={self.ysm_uid}; ejectCode=1",
                    "Host": f"{self.domnainHost}",
                    "Origin": f"http://{self.domnainHost}",
                    "Proxy-Connection": "keep-alive",
                    "Referer": f"http://{self.domnainHost}/yunonline/v1/exchange{self.exchangeParams}",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
                    "X-Requested-With": "XMLHttpRequest",
                },
                verify=False,
            )  # line:471:)
            try:  # line:472:try:
                res = r.json()  # line:473:res = r.json()
                if res.get("errcode") == 0:
                    print(f"✅ 账号[{self.name}]提现成功")  # line:475:print(f"✅ 账号[{self.name}]提现成功")
                    u = f"http://{self.domnainHost}/yunonline/v1/withdraw"  # line:476:u = f"http://{self.domnainHost}/yunonline/v1/withdraw"
                    p = f"unionid={exchangeParams['unionid']}&signid={exchangeParams['request_id']}&ua=0&ptype=0&paccount=&pname="  # line:477:p = f"unionid={exchangeParams['unionid']}&signid={exchangeParams['request_id']}&ua=0&ptype=0&paccount=&pname="
                    if self.aliAccount and self.aliName:
                        p = f"unionid={exchangeParams['unionid']}&signid={exchangeParams['request_id']}&ua=0&ptype=1&paccount={quote(self.aliAccount)}&pname={quote(self.aliName)}"  # line:479:p = f"unionid={exchangeParams['unionid']}&signid={exchangeParams['request_id']}&ua=0&ptype=1&paccount={quote(self.aliAccount)}&pname={quote(self.aliName)}"
                    r = requests.post(
                        u,
                        headers={
                            "Accept": "application/json, text/javascript, */*; q=0.01",
                            "Accept-Encoding": "gzip, deflate",
                            "Accept-Language": "zh-CN,zh;q=0.9",
                            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                            "Cookie": f"ysmuid={self.ysm_uid}; ejectCode=1",
                            "Host": f"{self.domnainHost}",
                            "Origin": f"http://{self.domnainHost}",
                            "Proxy-Connection": "keep-alive",
                            "Referer": f"http://{self.domnainHost}/yunonline/v1/exchange?unionid={self.unionId}&request_id={self.signid}&qrcode_number=16607864358145588",
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
                            "X-Requested-With": "XMLHttpRequest",
                        },
                        data=p,
                        verify=False,
                    )  # line:497:)
                    print(f"账号[{self.name}]提现结果", r.json())
                else:  # line:499:else:
                    print(f"账号[{self.name}]提现失败：", r.text, " 提现地址：", u1, " 提现参数：", p1)
            except Exception as e:  # line:501:except Exception as e:
                print(f"账号[{self.name}]提现失败：", r.text, " 提现地址：", u1, " 提现参数：", p1)

    def init(self):  # line:505:def init(self):
        try:  # line:506:try:
            res = requests.get(
                "https://nsr.zsf2023e458.cloud/yunonline/v1/getchatsite?t=1709019551&cid=785d878cb1e76a31cc1b52224d935ab7&code=081ktRFa1TM60H0gr4Ga1U6Pc10ktRFX&state=1",
                verify=False,
            )  # line:510:)
            self.domnainHost = res.json()["data"]["luodi"].split("/")[2]
            print(f"账号[{self.name}]提取到的域名：{self.domnainHost}")
            self.headers = {
                "Connection": "keep-alive",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"http://{self.domnainHost}/",
                "Origin": f"http://{self.domnainHost}",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Cookie": f"ysm_uid={self.ysm_uid};",
            }  # line:526:}
            self.signid = ""  # line:528:self.signid = ""
            for index in range(10):  # line:529:for i in range(10):
                res = requests.get(
                    f"http://{self.domnainHost}/",
                    headers={
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Cookie": f"ysmuid={self.ysm_uid}",
                    },
                    verify=False,
                )  # line:541:)
                htmltext = res.text  # line:542:htmltext = r.text
                res1 = re.sub("\s", "", htmltext)
                signidl = re.findall('\)\|\|"(.*?)";', res1)
                if signidl == []:  # line:546:if signidl == []:
                    continue  # line:547:continue
                else:  # line:548:else:
                    self.signid = signidl[
                        0
                    ]  # line:549:self.signid = signidl[0]
                    break  # line:550:break
            if self.signid == "":  # line:551:if self.signid == "":
                print(f"账号[{self.name}]初始化 requestId 失败,账号异常")
                return False  # line:553:return False
            res = requests.get(
                f"http://{self.domnainHost}/?cate=0",
                headers={
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cookie": f"ysmuid={self.ysm_uid}",
                },
                verify=False,
            )  # line:566:)
            htmltext = res.text
            res1 = re.sub("\s", "", htmltext)
            signidl = re.findall('/yunonline/v1/exchange(.*?)"', res1)
            if not signidl:
                print(f"账号[{self.name}]初始化 提现参数 失败,账号异常")
                return False  # line:573:return False
            else:  # line:574:else:
                self.exchangeParams = signidl[0]
            return True  # line:576:return True
        except Exception as e:  # line:577:except Exception as e:
            print(f"账号[{self.name}]初始化失败,请检查你的ck:{e}")
            return False  # line:580:return False

    def run(self):  # line:582:def run(self):
        if self.init():  # line:583:if self.init():
            self.user_info()  # line:584:self.user_info()
            self.hasWechat()  # line:585:self.hasWechat()
            self.gold()  # line:586:self.gold()
            self.read()  # line:587:self.read()
            time.sleep(3)  # line:588:time.sleep(3)
            self.gold()  # line:589:self.gold()
            time.sleep(3)  # line:590:time.sleep(3)
            self.withdraw()  # line:591:self.withdraw()


def getNewInviteUrl():  # line:594:def getNewInviteUrl():
    r = requests.get("https://www.filesmej.cn/waidomain.php", verify=False).json()
    if r.get("code") == 0:  # line:596:if r.get("code") == 0:
        newEntryUrl = r.get("data").get("luodi")
        parsed_url = urlparse(newEntryUrl)
        host = parsed_url.hostname
        return f"https://u7ds.sy673.shop/yunonline/v1/auth/2639bb95daba1d99e5338a8c2e21e2f0?codeurl=u7ds.sy673.shop&codeuserid=2&time=1709021176".replace(
            "u7ds.sy673.shop", host or "u7ds.sy673.shop"
        )  # line:602:)
    else:  # line:603:else:
        return "https://osl4.f4135.shop/yunonline/v1/auth/c5c3f97ce3894f1c08593c4a6c54dbfe?codeurl=osl4.f4135.shop&codeuserid=2&time=1709089052"  # line:604:return "https://u7ds.sy673.shop/yunonline/v1/auth/2639bb95daba1d99e5338a8c2e21e2f0?codeurl=u7ds.sy673.shop&codeuserid=2&time=1709021176"


if __name__ == "__main__":  # line:607:if __name__ == "__main__":
    accounts = os.getenv("xyyyd")
    inviteUrl = 'https://osl4.f4135.shop/yunonline/v1/auth/c5c3f97ce3894f1c08593c4a6c54dbfe?codeurl=osl4.f4135.shop&codeuserid=2&time=1709089052'  # line:612:inviteUrl = getNewInviteUrl()
    if accounts is None:  # line:613:if accounts is None:
        print(f"你没有填入xyyyd，咋运行？\n走下邀请呗：{inviteUrl}")
    else:  # line:615:else:
        split_arr = ['&', "@", "\n"]
        accounts_list = []
        for split in split_arr:
            if split in accounts:
                accounts_list = accounts.split(split)
        num_of_accounts = len(accounts_list)
        print(
            f"当前脚本版本：魔改自用版 V1.32 \n提示：获取到 {num_of_accounts} 个账号\n注册地址：{inviteUrl}")  # line:623:)
        for i, account in enumerate(accounts_list, start=1):
            print("-" * 50)  # line:628:print("-" * 50)
            print(f"账号[{account.split('#')[0]}]开始执行任务 >>>")
            values = account.split("#")  # line:632:values = account.split("#")
            cg = {}  # line:634:cg = {}
            try:  # line:635:try:
                if len(values) == 3:  # line:636:if len(values) == 3:
                    cg = {
                        "name": values[0],
                        "ysm_uid": values[1],
                        "unionId": values[2],
                        "txbz": 3000,
                        "aliAccount": "",
                        "aliName": "",
                    }  # line:644:}
                else:  # line:645:else:
                    cg = {
                        "name": values[0],
                        "ysm_uid": values[1],
                        "unionId": values[2],
                        "txbz": values[3] or 3000,
                        "aliAccount": "",
                        "aliName": "",
                    }  # line:653:}
            except Exception as e:  # line:654:except Exception as e:
                print("逼逼叨:", "配置的啥玩意，缺参数了憨批，看清脚本说明！")
                continue  # line:657:continue
            cg["appToken"] = ""  # line:658:cg["appToken"] = ""
            if len(values) >= 5:  # line:660:if len(values) >= 5:
                if values[4]:  # line:661:if values[4]:
                    cg["appToken"] = values[4]  # line:662:cg["appToken"] = values[4]
            else:  # line:663:else:
                cg["appToken"] = wxpusherAppToken
            cg["topicIds"] = ""  # line:665:cg["topicIds"] = ""
            if len(values) >= 6:  # line:666:if len(values) >= 6:
                if values[5]:  # line:667:if values[5]:
                    cg["topicIds"] = values[5]  # line:668:cg["topicIds"] = values[5]
            else:  # line:669:else:
                cg["topicIds"] = wxpusherTopicId
            if len(values) >= 7:  # line:671:if len(values) >= 7:
                if values[6]:  # line:672:if values[6]:
                    cg["aliName"] = values[6]  # line:673:cg["aliName"] = values[6]
            if len(values) >= 8:  # line:674:if len(values) >= 8:
                if values[7]:  # line:675:if values[7]:
                    cg["aliAccount"] = values[7]
            try:  # line:677:try:
                if cg["appToken"].startswith("AT_") == False:
                    print(f"提示，账号[{account.split('#')[0]}] wxpush 配置错误，快仔细看头部说明！")
                    continue  # line:680:continue
                if cg["appToken"].startswith("AT_") == False or cg["topicIds"].isdigit() == False:  # line:683:):
                    print(f"提示，账号[{account.split('#')[0]}] wxpush 配置错误，快仔细看头部说明！")
                    continue  # line:685:continue
                api = HHYD(cg)  # line:686:api = HHYD(cg)
                if cg["aliName"] and cg["aliAccount"]:
                    print(
                        f"提示，账号[{account.split('#')[0]}] 采用了 支付宝提现，姓名：{cg['aliName']}，账户：{cg['aliAccount']}"
                    )  # line:690:)
                else:  # line:691:else:
                    print(f"提示，账号[{account.split('#')[0]}] 采用了 微信提现")
                api.run()  # line:693:api.run()
            except Exception as e:  # line:694:except Exception as e:
                if "Expecting value: line 1 column 1" in str(e):
                    print(f"提示，账号[{account.split('#')[0]}] 疑似 unionId出错，换一个吧！")
                elif "link' is not defined" in str(e):
                    print(f"提示，账号[{account.split('#')[0]}] 疑似 新号的某种原因导致的无法阅读，请手动阅读两篇再试试吧！")  # line:700:)
                else:  # line:701:else:
                    print(f"提示，账号[{account.split('#')[0]}] 出错啦，请将下面报错截图发到tg交流群:")
                raise e  # line:703:raise e
                continue  # line:704:continue
            print("-" * 50)  # line:706:print("-" * 50)
            print(f"账号[{account.split('#')[0]}]执行任务完毕！")
