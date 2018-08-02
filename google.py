
import common as cmn

import os
import requests
from urllib import request as req
from urllib import parse
from tqdm import tqdm
import bs4


def get_images(keyword, result_dir, maximum=100):
    '''画像保存（上限100枚）'''
    cmn.make_dir(result_dir)

    # キーワードを"%??..."の形式に変換
    urlKeyword = parse.quote(keyword)

    url = 'https://www.google.com/search?hl=jp&q=' + \
        urlKeyword + '&btnG=Google+Search&tbs=0&safe=off&tbm=isch'
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"}
    html = requests.get(url=url, headers=headers).text
    soup = bs4.BeautifulSoup(html, "html.parser")
    elems = soup.select('.rg_meta.notranslate')

    count = 1
    for ele in tqdm(elems, total=maximum):
        # 数チェック
        if count > maximum:
            return

        ele = ele.contents[0].replace('"', '').split(',')
        eledict = dict()
        for e in ele:
            num = e.find(':')
            eledict[e[0:num]] = e[num + 1:]
        imageURL = eledict['ou']

        # ファイル拡張子
        exts = ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.gif']
        ext = os.path.splitext(imageURL)[1]
        if ext == '':
            ext = '.jpg'
        elif not ext in exts:
            continue

        try:
            filename = os.path.join(
                result_dir, keyword + '_' + str('%03d' % count) + ext)
            content = requests.get(imageURL).content
            with open(filename, 'wb') as f:
                f.write(content)
            count += 1
        except Exception as ex:
            continue


if __name__ == '__main__':
    get_images('ドラえもん', 'Test/ドラえもん/', maximum=5)
