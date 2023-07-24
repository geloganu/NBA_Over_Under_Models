import numpy as np
import pandas as pd
import keras


def season_format(season):
    """
    Returns season in terms of "2019_20" format
    
    :season: (int) season year 
    """
    season = int(season)
    return str(season)+'-'+str(season+1)[-2:]

def score_results(y,yhat):
    """
    Returns accuacy score for two lists
    """
    true = 0
    for i,j in zip(yhat,y):
        if i == j:
            true += 1
    
    return true/len(yhat)

def matchup_reformat(matchup):
    """
    Reads matchup information and sorts to home team, away team, and location
    
    :matchup: (str) matchup information eg:(CLE @ GSW)
    """
    if matchup.find("@") != -1:
        teamAbbr = matchup.split("@")[0]
        opptAbbr = matchup.split("@")[1]
        loc = "away"
    else:
        teamAbbr = matchup.split("vs.")[0]
        opptAbbr = matchup.split("vs.")[1]
        loc = "home"

    return teamAbbr, opptAbbr,loc

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
    OUline = float(OUline)
    pts = float(pts)
    
    if pts > OUline:
        return 1
    elif pts < OUline:
        return 0
    elif pts == OUline:
        return 2

def model_preprocessing(dataset,date_range):
    """
    Takes filtered dataset and returns train_test_split dataset for training model. Removes columns of dtype == "object".
    
    :dataset: input dataset (pd.DataFrame type)
    :seasons: range of seasons eg. ("2016-01-01","2019-01-01")
    """
    
    seasonal_data = dataset.iloc[np.where((dataset['game_date'] > date_range[0]) & (dataset['game_date'] < date_range[1]))]
    
    column_ind = [i for i in range(0,len(dataset.dtypes)) if dataset.dtypes[i] == 'object']
    seasonal_data = seasonal_data.drop(columns = seasonal_data.columns[column_ind], axis = 1)
    
    OU_classification = np.asarray(seasonal_data['O/U_result'])
    
    seasonal_data = seasonal_data.drop(columns = ['O/U_result'], axis = 1)
    seasonal_data = np.asarray(seasonal_data, dtype = float)   
    seasonal_data = keras.utils.normalize(seasonal_data, axis=1)
     
    return seasonal_data, OU_classification


def prediction_classifier(prediction):
    outcome=[]
    for pred in prediction:
        outcome.append(float(pred.argmax()))
        
    return outcome