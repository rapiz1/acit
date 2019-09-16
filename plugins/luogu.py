import requests
import json
import os
from datetime import datetime
url = 'https://www.luogu.org/record/list?user={username}&_contentOnly=1'
headers = {
    "User-Agent": "acit/0.01"
}
def get_cookies():
    try:
        with open(os.path.dirname(os.path.abspath(__file__)) + '/luogu.json') as f:
            cookie = json.load(f)
    except:
        print('只有登录用户才能查看洛谷提交记录页面，请登录')
        username = input('用户名：')
        passoword = input('密码：')
    return cookie

def get_submissions(config):
    cookies = get_cookies()
    try:
        data = requests.get(url.format_map(config), cookies=cookies, headers = headers).json()['currentData']['records']['result']
    except:
        print('您的登录状态无效')
    ret = []
    for x in data:
        item = {
            "id": x['problem']['pid'],
            "date": datetime(1,1,1).fromtimestamp(x['submitTime']).isoformat(),
            "status": 'Accepted' if x['status'] == 12 else 'Unaccepted'
        }
        ret.append(item)
    return ret
