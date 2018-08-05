
import os
import random
import zipfile
import numpy as np
from PIL import Image


def shuffle_lists(list1, list2):
    '''リストをまとめてシャッフル'''
    zipped = list(zip(list1, list2))
    np.random.shuffle(zipped)
    x_result, y_result = zip(*zipped)
    return np.asarray(x_result), np.asarray(y_result)

def preprocess(*arrays, normalize=True, one_hot=True, flatten=False):

    for array in arrays:
        if normalize:  # 正規化
            array = array.astype(np.float32)
            array /= 255.0

        if one_hot:  # one-hot表現
            y_train = np_utils.to_categorical(y_train, class_num)

        if flatten:  # 一次元化
            x_train = x_train.reshape(-1, 150 * 150 * 3)



def Dogs_vs_Cats(num=1000, test_ratio=0.3):
    dir = os.path.expanduser('~/Datasets/Dogs_vs_Cats/')

    with zipfile.ZipFile(dir + 'train.zip', 'r') as z:
        # ファイル名取得 (0番はディレクトリ名)
        cat_files = random.sample(z.namelist()[1:12501], num // 2)
        dog_files = random.sample(z.namelist()[12501:], num - (num // 2))
        files = cat_files + dog_files
        # 正解ラベル
        label = [0 if i < num // 2 else 1 for i in range(num)]
        label = np.array(label, dtype='uint8')
        # シャッフル
        files, label = shuffle_lists(files, label)

        # 画像データ読み込み
        data = np.empty((0, 150, 150, 3), dtype='uint8')
        tmp = np.empty((0, 150, 150, 3), dtype='uint8')
        for i, file in enumerate(files):
            # ファイルを開いてtmpに格納
            with Image.open(z.open(file)) as img:
                img = img.resize((150, 150))
                img = np.array(img, dtype='uint8')
                img = img.reshape(1, 150, 150, 3)
                tmp = np.vstack((tmp, img))
            # dataに結合
            if i % 200 == 0:
                data = np.vstack((data, tmp))
                tmp = np.empty((0, 150, 150, 3), dtype='uint8')

    mid = int(num * test_ratio)
    return (data[mid:], label[mid:]), (data[:mid], label[:mid])


if __name__ == '__main__':
    Dogs_vs_Cats(num=200, test_ratio=0.3)
