
import myTools.common as cmn

import os
import requests
from urllib import parse
from tqdm import tqdm
from bs4 import BeautifulSoup
import json


def get_images(keyword, result_dir, maximum=100, gif=True):
    '''画像保存（上限100枚）'''
    cmn.make_dir(result_dir)

    # キーワードを"%??..."の形式に変換
    urlKeyword = parse.quote(keyword)
    url = 'https://www.google.com/search?tbm=isch&q=' + urlKeyword + '&ijn='
    headers = {'User-Agent':
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    exts = ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png']
    if gif:
        exts.append('.gif')

    save_num, page_num = 1, 1
    while save_num <= maximum:
        print('Page', page_num)

        url_tmp = url + str(page_num - 1)
        html = requests.get(url=url_tmp, headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        elements = soup.select('.rg_meta.notranslate')

        # 終了判定
        if not len(elements):
            print('-> There is no more images')
            return

        for element in tqdm(elements):
            # 数チェック
            if save_num > maximum:
                print('-> Already met your requirements')
                return

            # 画像url取得
            js = json.loads(element.get_text())
            imageURL = js['ou']

            # 拡張子チェック
            ext = os.path.splitext(imageURL)[1]
            if not ext in exts:
                continue

            # 保存
            filename = os.path.join(result_dir, keyword +
                                    '_' + str('%03d' % save_num) + ext)
            try:
                content = requests.get(imageURL).content
                with open(filename, 'wb') as f:
                    f.write(content)
                save_num += 1
            except Exception as ex:
                continue

        page_num += 1


if __name__ == '__main__':
    get_images('ドラえもん', 'Test/ドラえもん/', maximum=5, gif=False)
