#!/usr/bin/env python
import sys

import requests
import pandas as pd
from tqdm import tqdm

sys.path.insert(0, './src/misc')
from sql_tools import *
from webscraping_tools import *
from tools import *

def access_nba_stats(season, measure_type):
    """
    Accesses stats.nba.com/stats/teamgamelogs for boxscore data for specified season and measure type.
    
    :season: (str) season year in the format '2017-18'.
    :measure_type: (str) boxscore measure type (Base, Advanced)
    """
    url = "https://stats.nba.com/stats/teamgamelogs"
    request_headers = 'Accept|*/*&Accept-Encoding|gzip,deflate,br&Accept-Language|en-US,en;q=0.9&Connection|keep-alive&Host|stats.nba.com&Origin|https://www.nba.com&Referer|https://www.nba.com/&Sec-Fetch-Dest|empty&c-Fetch-Mode|cors&Sec-Fetch-Site|same-site&User-Agent|Mozilla/5.0(Macintosh;IntelMacOSX10_15_7) AppSeleWebKit/537.36(KHTML,like Gecko)Chrome/113.0.0.0 Safari/537.36&sec-ch-ua|"GoogleChrome";v="113","Chromium";v="113","Not-A.Brand";v="24"&sec-ch-ua-mobile|?0&sec-ch-ua-platform|"macOS"'
    request_headers = clean_api_params(request_headers,"|","&")
    
    params = query_string_parameters(measure_type,season)
    params = clean_api_params(params,"=")

    
    response = requests.get(url, headers=request_headers, params=params).json()
    frame = pd.DataFrame(response['resultSets'][0]['rowSet'],columns = response['resultSets'][0]['headers'])
    
    return frame

def dataframe_cleaning(base_frame, adv_frame):
    """
    Cleans and joins base and advanced dataframe
    
    :base_frame: (Pandas DF) Raw base boxscore dataframe.
    :adv_frame: (Pandas DF) Raw advanced boxscore dataframe.
    """
    frame = base_frame.join(adv_frame.drop(columns=['SEASON_YEAR','TEAM_ID','TEAM_ABBREVIATION','TEAM_NAME','GAME_ID','GAME_DATE','MATCHUP','WL','MIN','GP_RANK', 'W_RANK', 'L_RANK', 'W_PCT_RANK', 'MIN_RANK']))

    frame[["TEAM_ABBREVIATION","TEAM_NAME","MATCHUP"]] = frame.apply(lambda row: pd.Series(matchup_reformat(row["MATCHUP"])), axis=1) 
    frame = frame.rename(columns={"TEAM_ABBREVIATION":"teamAbbr","TEAM_NAME":"opptAbbr","MATCHUP":"location","GAME_DATE":"game_date"})

    #format cleaning up
    frame["game_date"] = frame['game_date'].apply(lambda date: str(date).replace("T"," "))
    frame['teamAbbr'] = frame['teamAbbr'].apply(lambda row: row.replace(" ",""))
    frame['teamAbbr'] = frame['teamAbbr'].apply(lambda row: row.replace(" ",""))
    frame['TEAM_ID'] = frame['TEAM_ID'].astype(str)

    frame = frame.sort_values(by=["game_date"],ascending=False).reset_index(drop=True)
    
    return frame
    

def access_odds_data():
    """
    retreive historical and current odds data from rotowire.com/betting/nba/. Data is cleaned and formatted
    """
    url = "https://www.rotowire.com/betting/nba/tables/games-archive.php"

    #print("================================")
    #print("Building/updating odds table...")
    #print(f"Fetching historical odds rotowire.com/betting stats.nba.com...")
    odds_page = requests.get(url).json()
    odds_data = pd.DataFrame(odds_page,columns = odds_page[0].keys())

    odds_data = odds_data[['season','game_date','home_team_abbrev','visit_team_abbrev','total','game_over_under','spread']]
    odds_data['season'] = odds_data['season'].apply(lambda x: season_format(int(x)))

    odds_data = odds_data.rename(columns={"home_team_abbrev":"teamAbbr","visit_team_abbrev":"opptAbbr","game_over_under":"O/U_line"})
    
    return odds_data
    
def update_data(db, season):
    """
    Finds most recent boxscore data and updates table.
    
    :db: Sql database file for boxscore.
    """
    #retrieve and update boxscore for most recent season.

    base_frame = access_nba_stats(season, "Base")
    adv_frame = access_nba_stats(season, "Advanced")
    frame = dataframe_cleaning(base_frame, adv_frame)
    
    update_database(db,f"boxscore_{season}",frame)
    
    
