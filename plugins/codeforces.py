import requests
from datetime import datetime
url = "http://codeforces.com/api/user.status?handle={username}&from=1&count=20"
def get_submissions(config):
    data = requests.get(url.format_map(config)).json()['result']
    ret = []
    for x in data:
        item = {
            'id': str(x['contestId']) + x['problem']['index'],
            'date': datetime(1,1,1).fromtimestamp(x['creationTimeSeconds']).isoformat(),
            'status': x['verdict'],
        }
        ret.append(item)
    return ret
