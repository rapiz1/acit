import yaml
import argparse
import requests
import colorama
import dateutil.parser as dateparser
from termcolor import colored
from importlib import import_module
from bs4 import BeautifulSoup
parser = argparse.ArgumentParser('ACit', description='Print your submissions on Online Judge', epilog='By Rapiz')
parser.add_argument('command',  choices=['list', 'submissions'], help='list: print your configuration\n submisssions: print your submissions', type=str)
parser.add_argument('-t', '--target', metavar='OnlineJudge', help='specific target Online Judge', type=str)
parser.add_argument('-s', '--status', help='print submissions with specific status', choices=['ac', 'unac', 'wa', 're', 'pe', 'ce', 'tle'])
parser.add_argument('-v', '--verbose', help='print more information', action="count", default = 0)
args = parser.parse_args();

def get_local_config(key, oj):
    local_config = oj.copy()
    local_config['key'] = key
    for item in config['default']:
        if item not in oj:
            local_config[item] = config['default'][item]
    return local_config

def prettyprint_oj(config):
    if config['enable'] == False:
        out = colored(config['name'] + ' Disabled', 'white', attrs=['dark'])
    else:
        out = config['name']
        out += ' ' + colored('('+config['username']+')', 'cyan')
        if config and config['plugin']:
            out += ' ' + colored('Plugin', 'green', attrs=['reverse'])
    print(out)
def list_oj(config):
    for key, oj in config['online_judge'].items():
        local_config = get_local_config(key, oj)
        prettyprint_oj(local_config)

def uniform_submissions(submissions):
    for item in submissions:
        for k, v in item.items():
            item[k] = str(v).strip()
            if k == 'status':
                v = v.casefold()
                if 'wrong' in v:
                    item[k] = 'Wrong answer'
                elif 'runtime' in v:
                    item[k] = 'Runtime error'
                elif 'compi' in v:
                    item[k] = 'Comilation error'
                elif 'presen' in v:
                    item[k] = 'Presentation error'
                elif 'time' in v:
                    item[k] = 'Time Limit Exceed'
                elif 'mem' in v:
                    item[k] = 'Memory Limit Exceed'
                elif 'out' in v:
                    item[k] = 'Output Limit Exceed'
                elif 'ok' in v:
                    item[k] = 'Accepted'
        item['date'] = dateparser.parse(item['date'])
    return submissions

def shortstr(string, l):
    if len(string) > l:
        return string[:l-3]+'...'
    else:
        return string
def prettyprint_submissions(submissions):
    for item in submissions:
        out = str()
        for k, v in item.items():
            if len(out):
                out += ' '
            if k == 'date':
                out += v.isoformat(' ', timespec='minutes')
            elif k == 'status':
                color = 'white'
                if v == 'Wrong answer' or v == 'Unaccepted':
                    color = 'red'
                elif v == 'Accepted':
                    color = 'green'
                else:
                    color = 'cyan'
                out += colored(v, color)
            else:
                out += v;
        print(out)

def select_by_css(config):
    headers = {
        "User-Agent": 'acit/0.01'
    }
    url = oj['submissions'].format_map(local_config)
    soup = BeautifulSoup(requests.get(url, headers = headers).content, features='html5lib')
    selectors = oj['selectors']
    all_submissions = soup.select(selectors['submission'])
    if args.verbose >= 3:
        print(soup)
    if args.verbose >= 2:
        print(all_submissions)
    if args.verbose:
        print(selectors)
    ret = []
    for submission in all_submissions:
        record = {}
        for key, value in selectors.items():
            if key == 'submission':
                continue
            record[key] = submission.select_one(value).get_text().strip() + ' '
        ret.append(record)
    return ret
def select_by_plugins(config):
    plugin = import_module(f".{config['key']}", "plugins")
    return plugin.get_submissions(config)
def get_submissions(config):
    if config['plugin'] == True:
        submissions = select_by_plugins(config)
    else:
        submissions = select_by_css(config)
    return submissions
def get_status_by_abbrev(status):
    if status == 'ac':
        return 'Accepted'
    elif status == 'unac':
        return 'Unaccepted'
    elif status == 'wa':
        return 'Wrong answer'
    elif status == 're':
        return 'Runtime error'
    elif status == 'ce':
        return 'Comilation error'
    elif status == 'mle':
        return 'Memory Limit Exceed'
    elif status == 'tle':
        return 'Time Limit Exceed'
    elif status == 'ole':
        return 'Output Limit Exceed'
    elif status == 'pe':
        return 'Presentation error'
def filter_submissions_by_status(submissions, status):
    filtered_submissions = []
    for item in submissions:
        if item['status'] == status:
            filtered_submissions.append(item)
    return filtered_submissions
colorama.init()
# Load configuration
with open('config.yaml') as config_file:
    config = yaml.load(config_file.read(), Loader=yaml.CLoader)
if args.verbose:
    print('Verbosity:', args.verbose)
if args.command == 'list':
    list_oj(config)
elif args.command == 'submissions':
    for key, oj in config['online_judge'].items():
        if 'enable' in oj and oj['enable'] is False:
            continue
        if args.target:
            if key != args.target and oj['name'] != args.target:
                continue
        print(colored(oj['name'], attrs=['underline']))
        local_config = get_local_config(key, oj)
        submissions = uniform_submissions(get_submissions(local_config))
        if args.status:
            submissions = filter_submissions_by_status(submissions, get_status_by_abbrev(args.status))
        prettyprint_submissions(submissions)
