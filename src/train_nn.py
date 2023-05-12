import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import sklearn as sk

from tools import *

filename = '../_data/filtered_data.csv'
data = pd.read_csv(filename)

X_train, X_test, y_train, y_test = model_preprocessing(dataset = data.drop(columns = ['Total'],axis = 1),
                                                       date_range = ("2012-01-01", "2029-01-01"),
                                                       test_size = 0.2)
    

#earling stopping
callback = keras.callbacks.EarlyStopping(monitor='loss', patience=3)

#model checkpoint
checkpoint_filepath = './_data/checkpoint/'
model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_filepath,
    save_weights_only=True,
    monitor='val_accuracy',
    mode='max',
    save_best_only=True)

model = tf.keras.models.Sequential()
model.add(keras.layers.Flatten(input_shape = X_train[0].shape))
model.add(tf.keras.layers.Dense(128, activation="relu6"))
model.add(keras.layers.Dropout(0.2) )
model.add(tf.keras.layers.Dense(3, activation="softmax"))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(X_train, 
          y_train, 
          epochs=60, 
          validation_split=0.1, 
          batch_size=60,
          callbacks=[callback,model_checkpoint_callback])
