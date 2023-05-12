import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def find_columns(columns, keyword):
    """retains and returns the columns (list) that contain the keyword (string).
    
    :columns: (array) list
    :keyword: (string) string to search and return associated columns.
    """
    
    retained_cols = []
    for feature in columns:
        if feature.find(keyword)!= -1:
            retained_cols.append(feature)
    
    print(f'Found {len(retained_cols)} columns with keyword {keyword}: {retained_cols}')
    
    return retained_cols

def OU(OUline, pts):
    """
    returns binary classification
    
    :OUline: (int/float) O/U line set by bookkeeper
    :pts: (int/float) total points scored by team
    """

    if pts > OUline:
        return 1
    elif pts < OUline:
        return 0
    elif pts == OUline:
        return 2

def model_preprocessing(dataset,date_range,test_size):
    """
    Takes filtered dataset and returns train_test_split dataset for training model. Removes columns of dtype == "object".
    
    :dataset: input dataset (pd.DataFrame type)
    :seasons: range of seasons eg. ("2016-01-01","2019-01-01")
    :test_size: validation set size
    """
    
    seasonal_data = dataset.loc[np.where((dataset['Date'] > date_range[0]) & (dataset['Date'] < date_range[1]))]
    
    column_ind = [i for i in range(0,len(dataset.dtypes)) if dataset.dtypes[i] == 'object']
    seasonal_data = seasonal_data.drop(columns = seasonal_data.columns[column_ind], axis = 1)
    
    OU_classification = np.asarray(seasonal_data['O/U'])
    
    seasonal_data = seasonal_data.drop(columns = ['O/U'], axis = 1)
    seasonal_data = np.asarray(seasonal_data, dtype = float)   
    seasonal_data = keras.utils.normalize(seasonal_data, axis=1)
     
    return train_test_split(seasonal_data, OU_classification, random_state=42,test_size = test_size)


def prediction_classifier(prediction):
    outcome=[]
    for pred in prediction:
        outcome.append(float(pred.argmax()))
        
    return outcome