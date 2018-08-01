
'''
＜関数＞
- make_dir(dirname)
    ディレクトリ作成(再帰)
- system()
- system_func(mac, win, lin=None, others=None)

＜定数＞
- CHROME_CANARY_MAC
- CHROME_WIN
- CHROME_CANARY
'''

test

import os
import platform


def make_dir(dirname):
    '''ディレクトリ作成(再帰)'''
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def system():
    '''システム判定'''
    val = {'Darwin': 'm', 'Windows': 'w', 'Linux': 'l'}
    name = platform.system()
    if name in val.keys():
        return val[name]
    else:
        return ''


def system_func(mac, win, lin=None, others=None):
    '''システムに応じて戻り値を変える'''
    val = {'m': mac, 'w': win, 'l': lin, '': others}
    return val[system()]



# Chrome Canaryアドレス (Mac用)
CHROME_CANARY_MAC = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
CHROME_WIN = '"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
CHROME_CANARY = system_func(mac=CHROME_CANARY_MAC, win=CHROME_WIN)


if __name__ == '__main__':
    print(system_func(mac='yo', win='deso'))
