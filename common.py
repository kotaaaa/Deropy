
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

str
import os
import re
import platform
from urllib.request import urlparse


def make_dir(dirname):
    '''ディレクトリ作成(再帰)'''
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def url2filename(url):
    '''urlからファイル名作成'''
    o = urlparse(url)
    filename = os.path.splitext(o.netloc + o.path)[0]
    filename = re.sub(r'[:*?"<>|/\\]', '_', filename)
    if filename[-1] == '_':
        filename += 'index'
    if len(filename) > 50:
        filename = filename[:50]
    return filename


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


def divide_df(df, ratio1, ratio2, shuffle=False):
    '''データフレームを任意の比で分割'''
    df_tmp = df.sample(frac=1) if shuffle else df
    middle = round(len(df) * ratio1 / (ratio1 + ratio2))
    return df_tmp[:middle].reset_index(drop=True), df_tmp[middle:].reset_index(drop=True)


# Chrome Canaryアドレス (Mac用)
CHROME_CANARY_MAC = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
CHROME_WIN = '"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
CHROME_CANARY = system_func(mac=CHROME_CANARY_MAC, win=CHROME_WIN)


if __name__ == '__main__':
    print(system_func(mac='Mac', win='Windows', lin='Linux', others='cannot identify your OS'))
