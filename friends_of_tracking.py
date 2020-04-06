import json
import pandas
from pandas.io.json import json_normalize
import glob
from flatten_json import flatten
import numpy as np

competitions_df = pandas.read_json('/home/vivek/football/open-data/data/competitions.json')

matches_list = glob.glob('/home/vivek/football/open-data/data/matches/11/*.json')

matches_df = pandas.DataFrame()
for i in range (len(matches_list)):
    with open(matches_list[i]) as data_file:    
        data = json.load(data_file)
    data_flattened = [flatten(d) for d in data]
    data_flattened_df = pandas.DataFrame(data_flattened)
    data_flattened_df = data_flattened_df.replace(r'\s+', np.nan, regex=True)
    matches_df = matches_df.append(data_flattened_df)
matches_df = matches_df.dropna(axis='columns')