import requests
from datetime import datetime
url = "https://vjudge.net/status/data/"
def get_submissions(config):
    form = {'un':config['username'], 'start': '0', 'length': '20'}
    data = requests.post(url, form).json()['data']
    ret = []
    for x in data:
        item = {
            'id': x['oj'] + x['probNum'],
            'date': datetime(1,1,1).fromtimestamp(x['time']/1000).isoformat(),
            'status': x['status'],
        }
        ret.append(item)
    return ret
