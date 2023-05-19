import requests
import pandas as pd
import tqdm
import sqlite3

def clean_api_params(params,dict_divisor=":",line_divisor="&"):
    """
    Cleans params string and returns in dictionary format.
    
    :params: (dict) parameter string of website or endpoint.
    :dict_divisor: (str) symbol for sorting dictionary.
    """
    params_list = [x.split(dict_divisor) for x in params.split(line_divisor)]
    return {k:v for (k,v) in params_list}


def query_string_parameters(measure_type,season):
    """
    returns query string parameter for specific parameters
    """
    return f"DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType={measure_type}&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlusMinus=N&Rank=N&Season={season}&SeasonSegment=&SeasonType=&ShotClockRange=&VsConference=&VsDivision="

def season_range(min_year,max_year):
    return [str(year)+"-"+str(year+1)[-2:] for year in range(min_year,max_year+1)]

def request_data(url, headers, params, format):
    """
    Uses request library to retrieve endpoint data and returns in desired format (dict, json, dataframe).
    
    :url: (str) endpoint url
    :headers: (dict) endpoint request header dictionary.
    :params: (dict) endpoint query string parameters. 
    :format: (str) return format (dict, json, dataframe).
    """
    response = requests.get(url, headers=headers, params=params)
    response_json = response.json()
    if format == "json":
        return response_json
    elif format == "dataframe":
        frame = pd.DataFrame(response_json['resultSets'][0]['rowSet'])
        frame.columns = response_json['resultSets'][0]['headers']
        return frame
    elif format == "dict":
        frame = pd.DataFrame(response_json['resultSets'][0]['rowSet'])
        frame.columns = response_json['resultSets'][0]['headers']
        return frame.to_dict()
    else:
        raise Exception("Unknown format")
    
