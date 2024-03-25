import tensorflow as tf
import tensorflow.keras.backend as K
from tensorflow.keras import regularizers
# to use InceptionV3 instead of MobileNetV2 :
#from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D, GlobalAveragePooling2D, AveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger
from tensorflow.keras.optimizers import SGD
#from tensorflow.keras.regularizers import l2
from tensorflow import keras
import numpy as np
import tensorflow as tf


### parameters
n_classes = 101 # dishes numbers form the dataset
img_width, img_height = 299, 299
train_data_dir = '../dataset/train'
validation_data_dir = '../dataset/test'
nb_train_samples = 75750   #101*750
nb_validation_samples = 25250   #101*250
batch_size = 20 # ???

### init
print(tf.__version__)
print(tf.test.gpu_device_name())
tf.config.run_functions_eagerly(False) ## force gpu usage on m1 mac
K.clear_session() #free memory previously used by keras

# datagen creation to train our model performing data augmentation (random transformations)
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)
# datagen creation to validate our model
test_datagen = ImageDataGenerator(rescale=1. / 255)
# training data creation from food101 dataset training data
train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical')
# validation data creation from food101 dataset validation data
validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical')

x = input('Do you want to load a saved model ? (y/n) ')
if x=='y':
    path = input('Enter path to model ')
    model = keras.models.load_model(path)
if x=='n':
    # model initialisation to MobileNetV2
    mbv2 = MobileNetV2(weights='imagenet', include_top=False, input_shape = (img_width,img_height,3))
    x = mbv2.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128,activation='relu')(x)
    x = Dropout(0.2)(x)
    predictions = Dense(101,kernel_regularizer=regularizers.l2(0.005), activation='softmax')(x)
    model = Model(inputs=mbv2.input, outputs=predictions)
    model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy', metrics=['accuracy'])

checkpointer = ModelCheckpoint(filepath='best_model_3class_sept.hdf5', verbose=1, save_best_only=True)
csv_logger = CSVLogger('history.log')

epochs_nb = int(input('How many epochs do you want to run ? (integer) '))
export_path = input('Enter path to saved model ')

### model training
history = model.fit_generator(train_generator,
                    steps_per_epoch = nb_train_samples // batch_size,
                    validation_data=validation_generator,
                    validation_steps=nb_validation_samples // batch_size,
                    epochs=epochs_nb,
                    verbose=1,
                    callbacks=[csv_logger, checkpointer])
model.save(export_path)
