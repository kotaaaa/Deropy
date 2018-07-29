

import os
from keras.models import model_from_json
import matplotlib.pyplot as plt
plt.switch_backend('agg')


def shuffle_lists(x_list, y_list):
    '''データ・ラベルをシャッフル'''
    zipped = list(zip(x_list, y_list))
    np.random.shuffle(zipped)
    x_result, y_result = zip(*zipped)
    return np.asarray(x_result), np.asarray(y_result)


def save_model(model, model_name='model', dir='models'):
    '''モデル・重みの保存'''
    make_dir(dir)
    model_name = os.path.join(dir, model_name)
    with open(model_name + '.json', 'w') as f:
        f.write(model.to_json())
    model.save_weights(model_name + '.h5')


def load_model(model_name='model', dir='models'):
    '''モデル・重みの読み込み'''
    model_name = os.path.join(dir, model_name)
    with open(model_name + '.json', 'r') as f:
        model = model_from_json(f.read())
    model.load_weights(model_name + '.h5')
    return model


def save_hist(history, label, filename):
    '''学習結果を保存'''
    loss = history.history['loss']
    acc = history.history['acc']
    val_loss = history.history['val_loss']
    val_acc = history.history['val_acc']
    nb_epoch = len(acc)

    with open(filename, "w") as f:
        f.write(label + '\n')
        f.write('epoch\tloss\tacc\tval_loss\tval_acc\n')
        for i in range(nb_epoch):
            f.write('%d\t%f\t%f\t%f\t%f\n' %
                    (i, loss[i], acc[i], val_loss[i], val_acc[i]))


def plot_hist(files, result_file, items):
    '''グラフ化'''
    # リスト出ない場合はリストに変換
    if isinstance(files, str):
        files = (files,)
    if isinstance(items, str):
        items = (items,)

    plt.figure()
    for filename in files:
        dic = load_hist(filename)
        for item in items:
            plt.plot(dic['epoch'], dic[item], marker='.',
                     label=f"{dic['label']}({item})")

    if items[0] in ('acc', 'val_acc'):
        plt.ylim((0, 1))
    plt.grid()
    plt.legend()
    plt.xlabel('epoch')
    plt.ylabel(','.join(items))
    plt.savefig(result_file)
