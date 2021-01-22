from keras.models import load_model
import tensorflow as tf
import matplotlib.pyplot as plt
from glob import glob
import numpy as np
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from tensorflow.keras.applications import DenseNet121
import tensorflow
from keras.models import Model
rom keras.layers import Input, Lambda, Dense, Flatten

# re-size all the images to this
IMAGE_SIZE = [224, 224]

train_path = 'Datasets/Train'
valid_path = 'Datasets/Test'

# add preprocessing layer to the front of resNet
dense_121 = DenseNet121(
    input_shape=IMAGE_SIZE + [3],
    weights='imagenet',
    include_top=False)

for layer in dense_121.layers:
    layer.trainable = False


# useful for getting number of classes
folders = glob('Datasets/Train/*')


# Number of layers - Add more if u want
x = Flatten()(dense_121.output)

prediction = Dense(len(folders), activation='softmax')(x)

# create a model object
model = Model(inputs=dense_121.input, outputs=prediction)

# view the structure of the model
model.summary()

# Compiling the model
model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)


train_datagen = ImageDataGenerator(rescale=1. / 255,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1. / 255)

training_set = train_datagen.flow_from_directory('Datasets/Train',
                                                 target_size=(224, 224),
                                                 batch_size=32,
                                                 class_mode='categorical')

test_set = test_datagen.flow_from_directory('Datasets/Test',
                                            target_size=(224, 224),
                                            batch_size=32,
                                            class_mode='categorical')


# fit the model
r = model.fit_generator(
    training_set,
    validation_data=test_set,
    epochs=5,
    steps_per_epoch=len(training_set),
    validation_steps=len(test_set)
)


model.save('final_file.h5')  # saving the model
