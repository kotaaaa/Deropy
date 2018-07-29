
''' 定義されているもの
＜関数＞
- screenShotFull(driver, url, filename)
    フルページ スクリーンショット
'''

import common
import subprocess


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
    cmd = '"' + common.CHROME_CANARY + '"' \
        + ' --headless' \
        + ' --hide-scrollbars' \
        + ' --screenshot=' + filename + '.png' \
        + ' --window-size=' + str(cw) + ',' + str(ch) \
        + ' ' + url
    subprocess.Popen(cmd, shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)

if __name__ == '__main__':
    print(common.CHROME_CANARY)
