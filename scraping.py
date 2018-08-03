
'''
＜関数＞
- get_driver(width=960, height=540)
- save_images(url_list, basename)
- screenShotFull(driver, url, filename)
'''

import Deropy.common as cmn

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import os
import requests
from tqdm import tqdm
import subprocess


def get_driver(width=960, height=540):
    '''Chromeドライバー'''
    options = Options()
    options.binary_location = cmn.CHROME_CANARY
    options.add_argument('--headless')
    options.add_argument('--hide-scrollbars')
    options.add_argument('--window-size=' +
                         str(width) + ',' + str(height))
    driver = webdriver.Chrome(chrome_options=options)
    return driver


def save_images(url_list, basename, dir='./'):
    '''画像をインデックス付きでまとめて保存'''
    dir = os.path.join(dir, basename)
    cmn.make_dir(dir)
    for i, url in enumerate(tqdm(url_list)):
        cmn.make_dir(dir)
        ext = os.path.splitext(url)[1]
        filename = os.path.join(
            dir, basename + '_' + str('%03d' % (i + 1)) + ext)
        # 保存
        try:
            content = requests.get(url).content
            with open(filename, 'wb') as f:
                f.write(content)
        except Exception as ex:
            print(url, '\n->', ex)
            continue


def screenShotFull(driver, url, filename):
    '''フルページ スクリーンショット'''
    # アクセス
    if url:
        driver.get(url)
    url = driver.current_url
    print('Capturing ' + url)

    # ページサイズ取得
    cw = driver.execute_script("return document.body.scrollWidth;")
    ch = driver.execute_script("return document.body.scrollHeight;")
    # コマンド作成
    cmd = '"' + cmn.CHROME_CANARY + '"' \
        + ' --headless' \
        + ' --hide-scrollbars' \
        + ' --screenshot=' + filename + '.png' \
        + ' --window-size=' + str(cw) + ',' + str(ch) \
        + ' ' + url
    # コマンド実行
    subprocess.Popen(cmd, shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)


if __name__ == '__main__':
    print(cmn.CHROME_CANARY)
