import threading
import requests
import warnings
import pymysql
import random
import time
import json
from decrypt import encrypt as en

warnings.filterwarnings('ignore')
db = pymysql.connect(host='localhost', port=3306, user='root', password='1301207030Aa', database='topsports')
cursor = db.cursor()
token = ''
if token == '':
    sql = 'select token from users'
    cursor.execute(sql)
    token = str(cursor.fetchall()[0]).replace('(', '').replace(')', '').replace("'", "").replace('{', '').replace('}',
                                                                                                                  '').replace(
        ',', '')
num = 0
true_account = True


def get_challenge():  # 获取challenge，加入发送给解码平台的连接中
    global true_account
    _url = en('/order/confirmationOrder')
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': '*/*',
        'appId': 'wx71a6af1f91734f18',
        'Referer': 'https://servicewechat.com/wx71a6af1f91734f18/87/page-frame.html',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.9(0x1800092d) NetType/4G Language/zh_CN'
    }
    data = json.dumps({
        "merchantNo": "TS",
        "shippingId": "8a7a8eaf6fc5145e016fca58bd4f5dbb",
        "subOrderList": [{
            "shopNo": "NKNJA7",
            "expressType": 2,
            "commodityList": [{
                "productCode": "CV0612-015",
                "skuNo": "20211027000995",
                "sizeNo": "20160426000006",
                "sizeCode": "S",
                "num": 1,
                "assignProNo": "0",
                "itemFlag": 0,
                "liveType": 0,
                "roomId": "",
                "roomName": "",
                "shoppingcartId": "efe1625d88184fea86905fc4575ee5f8",
                "shopCommodityId": "cb89589a6412475fbe3fd56a693e7716"
            }],
            "remark": f"166{random.randint(200, 400)}89{random.randint(100, 200)}",
            "ticketCodes": []
        }],
        "purchaseType": 2,
        "usedPlatformCouponList": []
    })
    response = requests.post(url=_url, headers=headers, data=data, verify=False)
    if response.status_code == 200:
        if response.json()['code'] == 1:
            response = response.json()
            _challenge = response['data']['verificMap']['challenge']
            return _challenge
        else:
            print('Account Expired')
            true_account = False
            exit()
    else:
        print(response, 'error')
        exit()


def get_validate():  # 根据challenge获取validate
    global num
    x = True
    n = 0
    userkey = '4254d6ac36628f5e4dffec1b6e3b8604'
    gt = 'a53a5b6472732e344c776ba27d65302e'
    challenge = get_challenge()
    url = f'http://www.damagou.top/apiv1/jiyanRecognize.html?userkey={userkey}&gt={gt}&challenge={challenge}&type=1006&isJson=2'
    while x:
        res = requests.get(url, verify=False)
        if res.status_code == 200:
            res = res.json()
            if res['msg'] == 'success':
                data = res['data']
                challenge = str(data).split('|')[0]
                validate = str(data).split('|')[1]
                time_now = str(int(time.time()))
                add_sql = 'insert into captcha1(No,challenge, validate, create_time) values(null,%s,%s,%s)'
                _db = pymysql.connect(host='localhost', port=3306, user='root', password='1301207030Aa',database='topsports')
                _cursor = _db.cursor()
                _cursor.execute(add_sql, (challenge, validate, time_now))
                _db.commit()
                _cursor.close()
                _db.close()
                print(f'验证完成,validate--{validate}, Retry', n, 'times')
                num += 1
                x = False
            else:
                try:
                    print('验证失败, Retry', n, 'times,', 'code:', res['msg'])
                except Exception as e:
                    print('验证失败', e)
                x = False
        else:
            print(res.status_code)
            n += 1


def get_validates(n):  # 并发生成验证码
    Threads = []
    for i in range(n):
        thread = threading.Thread(target=get_validate)
        thread.start()
        Threads.append(thread)
    for thread in Threads:
        thread.join()


def serious_captcha(n):
    global num
    start = time.time()
    while num < n and true_account:
        get_validates(n - num)
    end = time.time()
    use = round((end - start) * 1000, 2)
    print(num, 'Captcha Finished in', use, 'ms')
    num = 0
