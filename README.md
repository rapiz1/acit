# Acit
![python](https://img.shields.io/badge/python-3-blue?style=for-the-badge&logo=python) ![Issues](https://img.shields.io/github/issues/rapiz1/acit?style=for-the-badge&logo=github) ![LICENSE](https://img.shields.io/github/license/Rapiz1/acit?style=for-the-badge&logo=gnu)

> A rich-featrued command line tool to count your submissions

## Features
* Built-in support for various OJs
* Easy to configure by YAML
* Easy to extend ( by CSS selectors or scripts)
* Colorful output
* *GUI ( pending )*

## Get Started
```shell
git clone https://github.com/Rapiz1/acit
cd acit
pip install -r requirements.txt
cp example.yaml config.yaml
```
And open `config.yaml` in your text editor.

Change `username` in the `default` section to your username on OJs.

If you have different username on some OJ, for exmaple, your generally use `jack123` as your username but have `jack321` for Codeforces. Your configuration should look like this:

```yaml
# Default configuration
default:
  username: jack123
  enable: true
  plugin: false

# Online Judge configuration
online_judge:
  codeforces:
    name: Codeforces
    username: jack321
    plugin: true
    submissions: http://codeforces.com/submissions/{username}
  luogu:
    name: 洛谷
    enable: true
    plugin: true
  vjudge:
    name: Virtual Judge
    plugin: true
  hdu:
    name: HDU Online Judge
    submissions: http://acm.hdu.edu.cn/status.php?user={username}
    selectors:
      submission: .table_text>tbody>tr~tr
      id: td:nth-child(4)
      date: td:nth-child(2)
      status: td:nth-child(3)
  bzoj:
    name: 大视野在线测评
    submissions: https://www.lydsy.com/JudgeOnline/status.php?user_id={username}
    selectors:
      submission: table[align] tr~tr
      id: td:nth-child(3)
      date: td:nth-child(9)
      status: td:nth-child(4)
  loj:
    name: LibreOJ
    plugin: true
```
### Usage
To get help information:
```c++
python acit.py -h
```

## TO-DO
- [ ] Improve luogo plugin
- [ ] Option for retrieving recent `n` or day/week/month/year submissions 
- [ ] Option for showing statistics
- [ ] List solved problems with duplicated AC submissions merged
- [ ] Show submissions from different submission in one list
- [ ] Better documents
