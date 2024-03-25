from dataset_separation import prepare_data
import shutil
import os

def test_prepare_data():
    shutil.rmtree('../dataset/train')
    prepare_data('../dataset/meta/train.txt', '../dataset/images', '../dataset/train')
    assert os.path.isfile('../dataset/train/apple_pie/134.jpg')
    assert os.path.isfile('../dataset/train/waffles/3919789.jpg')