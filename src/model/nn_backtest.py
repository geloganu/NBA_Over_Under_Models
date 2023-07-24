import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import tensorflow as tf
from tensorflow import keras

import sys
sys.path.append('./src/misc')
import tools
import sql_tools

#importing file from SQL database

ntrail = int(input('Trail dataset (enter int): '))

path_to_data = "./src/sql/"
data = sql_tools.read_database(path_to_data+"trailing_database.db", f"{ntrail}_game_trailing")
data = data[data['O/U_line']!='']
data['O/U_result'] = data.apply(lambda row: tools.OU(row['O/U_line'],float(row['total'])),axis=1)

X,y = tools.model_preprocessing(data,("2017-01-10","2023-12-12"))

#earling stopping
callback = keras.callbacks.EarlyStopping(monitor='loss', patience=10)

model = tf.keras.models.Sequential()
model.add(keras.layers.Flatten(input_shape = X[0].shape))
model.add(tf.keras.layers.Dense(128, activation="relu6"))
model.add(keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Dense(3, activation="softmax"))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])


callback = keras.callbacks.EarlyStopping(monitor='loss', patience=5)

model.fit(X[301:], 
          y[301:], 
          epochs=100, 
          validation_split=0.1, 
          batch_size=100,
          verbose=0,
          callbacks=[callback])

n = 300
OU_results = list(y[-n:])
pred = []
acc_vals = []
print(f"Backtesting for {n} games...\n")

for i in tqdm(range(0,n)):
    #X_train = X[n+1-i:]
    #y_train = y[n+1-i:]

    if i%10:
        model.fit(X[n+1-i:], 
            y[n+1-i:], 
            epochs=100, 
            validation_split=0.1, 
            batch_size=100,
            verbose=0,
            callbacks=[callback])

    X_test = X[n-i]
    y_test = y[n-i]

    prediction_output = model.predict(X_test.reshape(1,-1),verbose=0)
    pred.append(tools.prediction_classifier(prediction_output)[0])

acc = tools.score_results(OU_results,pred)
acc_vals.append(acc)
  
overall_acc = sum(acc_vals)/len(acc_vals)
print(f"\nNeural network achieved {overall_acc*100}% overall accruacy for the past {n} games.")