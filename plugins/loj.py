import requests
import json
url = "https://loj.ac/submissions?submitter={username}"
def get_submissions(config):
    html = requests.get(url.format_map(config)).text.splitlines()
    for line in html:
        if 'itemList' in line:
            data = json.loads(line[line.find('['):line.rfind(']')+1])
            break
    ret = []
    for x in data:
        item = {
            'id': x['info']['problemId'],
            'date': x['info']['submitTime'],
            'status': x['result']['result'],
        }
        ret.append(item)
    return ret
