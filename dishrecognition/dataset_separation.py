from shutil import copy
from collections import defaultdict
import os

#function to help preparing tarining set and test set....ONLY RUN ONCE
def prepare_data(filepath, src,dest):
  classes_images = defaultdict(list)
  with open(filepath, 'r') as txt:
      paths = [read.strip() for read in txt.readlines()]
      for p in paths:
        food = p.split('/')
        classes_images[food[0]].append(food[1] + '.jpg') #food[0]=nom food[1]=numero photo

  for food in classes_images.keys():
    print("\nCopying images into ",food)
    if not os.path.exists(os.path.join(dest,food)):
      os.makedirs(os.path.join(dest,food))
    for i in classes_images[food]:
      copy(os.path.join(src,food,i), os.path.join(dest,food,i))
  print("Copying Done!")

prepare_data('../dataset/meta/train.txt', '../dataset/images', '../dataset/train')
prepare_data('../dataset/meta/test.txt', '../dataset/images', '../dataset/test')