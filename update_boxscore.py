#!/usr/bin/env pythons
import sys

import requests
import pandas as pd
from tqdm import tqdm

sys.path.insert(0, './src/misc')
from sql_tools import *
from webscraping_tools import *
from tools import *

tables = read_table_names("./src/sql/database.db")
tables = [t for t in tables if t.find('boxscore') != -1]

#retreive basic and advanced boxscore statistics from stats.nba.com
url = "https://stats.nba.com/stats/teamgamelogs"
request_headers = 'Accept|*/*&Accept-Encoding|gzip,deflate,br&Accept-Language|en-US,en;q=0.9&Connection|keep-alive&Host|stats.nba.com&Origin|https://www.nba.com&Referer|https://www.nba.com/&Sec-Fetch-Dest|empty&Sec-Fetch-Mode|cors&Sec-Fetch-Site|same-site&User-Agent|Mozilla/5.0(Macintosh;IntelMacOSX10_15_7) AppleWebKit/537.36(KHTML,like Gecko)Chrome/113.0.0.0 Safari/537.36&sec-ch-ua|"GoogleChrome";v="113","Chromium";v="113","Not-A.Brand";v="24"&sec-ch-ua-mobile|?0&sec-ch-ua-platform|"macOS"'
request_headers = clean_api_params(request_headers,"|","&")

season = tables[-1][-7::]

print("================================")
print("Updating advanced boxscore table...")
print("Fetching statistics from stats.nba.com...")

measure_type = ["Base","Advanced"]

params = query_string_parameters(measure_type[0],season)
params = clean_api_params(params,"=")

response = requests.get(url, headers=request_headers, params=params).json()
base_frame = pd.DataFrame(response['resultSets'][0]['rowSet'],columns = response['resultSets'][0]['headers'])

params = query_string_parameters(measure_type[1],season)
params = clean_api_params(params,"=")

response = requests.get(url, headers=request_headers, params=params).json()
adv_frame = pd.DataFrame(response['resultSets'][0]['rowSet'],columns = response['resultSets'][0]['headers'])

frame = base_frame.join(adv_frame.drop(columns=['SEASON_YEAR','TEAM_ID','TEAM_ABBREVIATION','TEAM_NAME','GAME_ID','GAME_DATE','MATCHUP','WL','MIN','GP_RANK', 'W_RANK', 'L_RANK', 'W_PCT_RANK', 'MIN_RANK']))

frame[["TEAM_ABBREVIATION","TEAM_NAME","MATCHUP"]] = frame.apply(lambda row: pd.Series(matchup_reformat(row["MATCHUP"])), axis=1) 
frame = frame.rename(columns={"TEAM_ABBREVIATION":"teamAbbr","TEAM_NAME":"opptAbbr","MATCHUP":"location","GAME_DATE":"game_date"})

#format cleaning up
frame["game_date"] = frame['game_date'].apply(lambda date: str(date).replace("T"," "))
frame['teamAbbr'] = frame['teamAbbr'].apply(lambda row: row.replace(" ",""))
frame['teamAbbr'] = frame['teamAbbr'].apply(lambda row: row.replace(" ",""))
frame['TEAM_ID'] = frame['TEAM_ID'].astype(str)

frame = frame.sort_values(by=["game_date"],ascending=False).reset_index(drop=True)

update_database("./src/sql/database.db",f"boxscore_{season}",frame)

print('Success!\n')    