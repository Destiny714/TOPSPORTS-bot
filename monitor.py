from decrypt import encrypt_sign as es
import requests
import warnings
import pymysql
import time
import re
warnings.filterwarnings('ignore')
count = []
count_list = []


def match(txt):
    result = re.search(r'[Jj]ordan|[Dd]unk|[Rr]etro|JORDAN|DUNK|[Aa][Jj]|欧文|[Kk]yrie|35|[Cc][Uu][Tt]',txt)
    if result:
        return True
    else:
        return False


def bark_pusher(title,content):
    url = f'https://api.day.app/y67CydURc8wR9CVemagkYL/{title}/{content}'
    requests.get(url, verify=False)


def header(auth):  # 返回用户header
    headers = {
        'Authorization': '' + auth,
        'Content-Type': 'application/json',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': '*/*',
        'appId': 'wx71a6af1f91734f18',
        'Referer': 'https://servicewechat.com/wx71a6af1f91734f18/87/page-frame.html',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac'
    }
    return headers


def filter():  # 搜索对应货号返回匹配列表
    global count
    count = []
    headers = header('')
    keyword = ''
    pagesize = '20'
    shop = ''
    url = 'https://wxmall.topsports.com.cn/search/shopCommodity/list?searchKeyword={}&current=1&pageSize={}&sortColumn=upShelfTime&sortType=desc&filterIds=TS100101%2CTS300301&shopNo={}&tssign='.format(keyword,pagesize,shop) + es('/search/shopCommodity/list')
    try:
        r = requests.get(url=url, headers=headers, verify=False, timeout=2).json()
        good_list = r['data']['spu']['list']
        for good_detail in good_list:
            good_id = good_detail['id']
            good_code = good_detail['productCode']
            real_price = good_detail['salePrice']
            tag_price = good_detail['tagPrice']
            count_num = round((real_price / tag_price),4) *10
            good_name = good_detail['productName'].replace('#','')
            if match(good_name):
                is_match = True
            else:
                is_match = False
            good_shop = good_detail['shopName']
            good_count = good_detail['proName']
            if good_count:
                if (re.search(r'5折',good_count) or count_num <= 0.6) and good_id not in count_list and is_match:
                    count_list.append(good_id)
                    count.append({'name': good_name, 'shop': good_shop, 'id': good_id,'count':f'{count_num}折--{good_count}','price':real_price,'code':good_code})
            else:
                if count_num <= 0.6 and good_id not in count_list and is_match:
                    count_list.append(good_id)
                    count.append({'name': good_name, 'shop': good_shop, 'id': good_id,'count':count_num,'price':real_price,'code':good_code})
    except Exception as e:
        print(e)
        pass
    return count


if __name__ == '__main__':
    while True:
        search_match_id()
        if count:
            print(count)
            for i in count:
                bark_pusher(f"{i['shop']}--{i['price']}--{i['count']}",f"{i['code']}--{i['name']}")
        time.sleep(2)
