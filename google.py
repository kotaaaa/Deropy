
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

    def Search(self, keyword, type = 'text', maximum = 100):
        print('Google', type.capitalize(), 'Search :', keyword)
        query=self.query_gen(keyword, type)
        if type == 'text':
            return self.text_result(query, maximum)
        elif type == 'image':
            return self.image_result(query, maximum)

    def text_result(self, query_gen, maximum):
        result=[]
        total=0
        while True:
            # 検索
            html=self.session.get(next(query_gen)).text
            soup=BeautifulSoup(html, 'lxml')
            elements=soup.select('.rc > .r > a')
            hrefs=[e['href'] for e in elements]

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
        result=[]
        total=0
        while True:
            # 検索
            html=self.session.get(next(query_gen)).text
            soup=BeautifulSoup(html, 'lxml')
            elements=soup.select('.rg_meta.notranslate')
            jsons=[json.loads(e.get_text()) for e in elements]
            imageURLs=[js['ou'] for js in jsons]

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

            # print(self.GOOGLE_SEARCH_URL + '?' + params)
            yield self.GOOGLE_SEARCH_URL + '?' + params
            page += 1


if __name__ == '__main__':
    google = Google()
    # result = google.Search('MyShin001', type='image', maximum=55)
    result = google.Search('ドラえもん', type='image', maximum=55)
    # result = google.Search('MyShin001', type='text', maximum=55)
    # result = google.Search('ドラえもん', type='text', maximum=55)
    [print(r) for r in result]
    print(len(result))
