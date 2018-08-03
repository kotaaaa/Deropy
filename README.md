# myTools
#Python
---

## 構成
* common.py
* scraping.py
* neural.py

---

## common.py
### 定数
	* `CHROME_CANARY_MAC`
	* `CHROME_WIN`
### 関数
	* `system()`
	* `system_func(mac, win, lin=None, others=None)`

---

## scraping.py
### 関数
	* `screenShotFull(driver, filename, url='')`
	フルページ スクリーンショット

---

## neural.py
### 関数
	* `shuffle_lists(x, y)`
	データ・ラベルをシャッフル
	* `save_model(model, model_name='model', dir='models')`
	モデル・重みの保存
	* `load_model(model_name='model', dir='models')`
	モデル・重みの読み込み
	* `save_hist(history, label, filename)`
	学習結果を保存
	* `plot_hist(files, result_file, items)`
	グラフ化

---

## google.py (Googleクラス)
### 関数
	* `Search(self, keyword, type='text', maximum=100)`
	Google検索して、検索結果をリストで返す。
	type -> ‘text’/’image’
	* `query_gen(self, keyword, type)`
	検索クエリ作成 (内部関数)
	* `text_result(self, query_gen, maximum)`
	テキスト検索 (内部関数)
	* `image_result(self, query_gen, maximum)`
	画像検索 (内部関数)
### 使用例
```py
google = Search(self, keyword, type='text', maximum=100)
result = google.Search('ドラえもん', type='image', maximum=55)
for url in result:
    (ダウンロード処理)
```
