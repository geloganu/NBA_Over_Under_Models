from nba_api.stats.endpoints import boxscoreadvancedv2
import pandas as pd
from tqdm import tqdm

def get_boxscore_dict(game_id):
    return boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=game_id).team_stats.get_dict()


def find_boxscore(dataframe):
    game_id_vals = dataframe['GAME_ID'].drop_duplicates()
    
    print(f'Finding boxscore for {len(game_id_vals)} games...')
    
    rows = []
    for id in tqdm(game_id_vals):
        rows.extend(get_boxscore_dict(game_id = id)['data'])
    
    headers = get_boxscore_dict(game_id = id)['headers']
        
    return pd.merge(dataframe, pd.DataFrame(data=rows,columns=headers), how = 'left',left_on=['GAME_ID','TEAM_ID'],right_on=['GAME_ID','TEAM_ID'])

