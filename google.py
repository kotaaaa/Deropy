
import myTools.common as cmn

import os
import requests
from urllib import parse
from tqdm import tqdm
from bs4 import BeautifulSoup
import json


class Google:
    def __init__(self):
        self.GOOGLE_SEARCH_URL = 'https://www.google.co.jp/search'
        self.session = requests.session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'})

    def query_gen(self, keyword, type='text'):
        '''検索クエリジェネレータ'''
        page = 0
        while True:
            if type == 'text':
                params = parse.urlencode({
                    'q': keyword,
                    'num': '100',
                    'start': str(page * 100)})
            elif type == 'image':
                params = parse.urlencode({
                    'q': keyword,
                    'tbm': 'isch',
                    'ijn': str(page)})

            print(self.GOOGLE_SEARCH_URL + '?' + params)
            yield self.GOOGLE_SEARCH_URL + '?' + params
            page += 1

    def get_images(self, keyword, result_dir, maximum=100,
                   jpg=True, png=True, gif=True):
        '''画像クロール'''
        cmn.make_dir(result_dir)
        exts = ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png']
        exts += ['.gif'] if gif else []

        query = self.query_gen(keyword, type='image')
        # headers = {'User-Agent':
        # 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'}

        save_num, page_num = 0, 0
        while save_num < maximum:
            print('Page', page_num + 1)

            # html = requests.get(query.__next__(), headers=headers).text
            html = self.session.get(query.__next__()).text
            soup = BeautifulSoup(html, 'lxml')
            elements = soup.select('.rg_meta.notranslate')
            imageURLs = [json.loads(e.get_text())['ou'] for e in elements]

            # 終了判定
            if not len(imageURLs):
                print('-> There is no more images')
                return

            for imageURL in tqdm(imageURLs):
                # 数チェック
                if save_num >= maximum:
                    print('-> Done')
                    return

                # 拡張子チェック
                ext = os.path.splitext(imageURL)[1]
                if not ext in exts:
                    continue

                # 保存
                filename = os.path.join(result_dir, keyword +
                                        '_' + str('%03d' % (save_num + 1)) + ext)
                try:
                    content = requests.get(imageURL).content
                    with open(filename, 'wb') as f:
                        f.write(content)
                    save_num += 1
                except Exception as ex:
                    continue

            page_num += 1

    def Search(self, keyword, type='text', maximum=10):
        print('Google', type.capitalize(), 'Search :', keyword)
        query = self.query_gen(keyword, type)
        if type == 'text':
            return self.text_result(query, maximum)
        elif type == 'image':
            return self.image_result(query, maximum)

    def text_result(self, query_gen, maximum):
        result = []
        total = 0
        while True:
            # 検索
            html = self.session.get(next(query_gen)).text
            soup = BeautifulSoup(html, 'lxml')
            elements = soup.select('.rc > .r > a')
            hrefs = [e['href'] for e in elements]

            # 検索結果の追加
            if not len(hrefs):
                print('-> No more results')
                break
            elif len(hrefs) > maximum - total:
                result += hrefs[:maximum - total]
                break
            else:
                result += hrefs
                total += len(hrefs)

        print('-> Finally got', str(len(result)), 'results')
        return result

    def image_result(self, query_gen, maximum):
        result = []
        total = 0
        while True:
            # 検索
            html = self.session.get(next(query_gen)).text
            soup = BeautifulSoup(html, 'lxml')
            print(soup.prettify())
            elements = soup.select('.rg_meta.notranslate')
            jsons = [json.loads(e.get_text()) for e in elements]
            imageURLs = [js['ou'] for js in jsons]

            # 検索結果の追加
            if not len(imageURLs):
                print('-> No more images')
                break
            elif len(imageURLs) > maximum - total:
                result += imageURLs[:maximum - total]
                break
            else:
                result += imageURLs
                total += len(imageURLs)

        print('-> Finally got', str(len(result)), 'images')
        return result


if __name__ == '__main__':
    # get_images('ドラえもん', 'Test/ドラえもん/', maximum=10, gif=False)

    google = Google()
    # google.get_images('ドラえもん', 'Test/ドラえもん/', maximum=10, gif=False)
    # result = google.Search('MyShin001', type='image', maximum=55)
    result = google.Search('ドラえもん', type='image', maximum=50)
    # print(result)
    # print(len(result))

    # result = google.Search('MyShin001', type='text', maximum=55)
    # result = google.Search('メントス', type='text', maximum=55)
    # result = google.Search('python', type='text', maximum=55)
    # [print(r) for r in result]
    # print(result)
    # print(len(result))
