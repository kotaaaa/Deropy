
''' 定義されているもの
＜関数＞
- screenShotFull(driver, url, filename)
    フルページ スクリーンショット
'''

import common as cmn
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import subprocess


def get_driver(width=960, height=540):
    options = Options()
    options.binary_location = cmn.CHROME_CANARY
    options.add_argument('--headless')
    options.add_argument('--hide-scrollbars')
    options.add_argument('--window-size=' +
                         str(width) + ',' + str(height))
    driver = webdriver.Chrome(chrome_options=options)
    return driver


def screenShotFull(driver, filename, url=''):
    '''フルページ スクリーンショット (Winの場合は要chromeアドレス変更)'''
    # アクセス
    if url:
        driver.get(url)
    url = driver.current_url
    print('Capturing ' + url)

    # ページサイズ取得
    cw = driver.execute_script("return document.body.scrollWidth;")
    ch = driver.execute_script("return document.body.scrollHeight;")
    # Chrome Canary スクリーンショット
    cmd = '"' + cmn.CHROME_CANARY + '"' \
        + ' --headless' \
        + ' --hide-scrollbars' \
        + ' --screenshot=' + filename + '.png' \
        + ' --window-size=' + str(cw) + ',' + str(ch) \
        + ' ' + url
    subprocess.Popen(cmd, shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)


if __name__ == '__main__':
    print(cmn.CHROME_CANARY)
