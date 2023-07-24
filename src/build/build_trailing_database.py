#!/usr/bin/env python
import numpy as np
import pandas as pd
from tqdm import tqdm
from datetime import datetime

import sys
sys.path.insert(0, './src/misc')
from sql_tools import *
from webscraping_tools import *
from tools import *

seasons = season_range(2017,2022)

def build_trailing(db, seasons, n):


    master_boxscore = pd.DataFrame(read_database("./src/sql/database.db", f"boxscore_{seasons[0]}"))


    for season in seasons[1:]:
        master_boxscore = pd.concat([master_boxscore,read_database("./src/sql/database.db", f"boxscore_{season}")], axis=0)
        
    #ensure descending order in pulled database for safety
    master_boxscore = master_boxscore.sort_values(by = ['game_date'],ascending=False).reset_index(drop=True)
    master_odds = read_database("./src/sql/database.db", "odds").sort_values(by = ['game_date'],ascending=False).reset_index(drop=True)

    master_boxscore_data_only = master_boxscore.copy()

    #generate data only dataframe
    column_ind = [i for i in range(0,len(master_boxscore_data_only.dtypes)) if master_boxscore_data_only.dtypes[i] == 'object']
    master_boxscore_data_only = master_boxscore_data_only.drop(columns = master_boxscore_data_only.columns[column_ind], axis = 1)


    #generate trailing database by average past n games
    game_data_array = master_odds.values.tolist()

    row_list=[]

    for row in tqdm.tqdm(game_data_array):  
        team_temp = master_boxscore_data_only.loc[(master_boxscore['game_date'] <= row[1]) & (master_boxscore['teamAbbr']==row[2])][1:n+1].mean()
        team_temp.index ="team"+team_temp.keys()

        oppt_temp = master_boxscore_data_only.loc[(master_boxscore['game_date'] <= row[1]) & (master_boxscore['teamAbbr']==row[3])][1:n+1].mean()
        oppt_temp.index ="oppt"+oppt_temp.keys()

        row_list.append(pd.concat([team_temp, oppt_temp]).to_dict())

    trailing_dataset = master_odds.join(pd.DataFrame(row_list)).dropna()
    
    return trailing_dataset