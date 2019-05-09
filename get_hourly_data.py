import pandas as pd
from datetime import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

def get_hourly_data(fname):
    """
    Function retireves station info that is used to make headers for Cdec data.
    Args:
        fname: string to the path for the Cdec station csv
    """
    DatetimeFormat = "%Y-%m-%d %H"

    df = pd.read_csv(fname, low_memory=False,
                 parse_dates=True, delimiter=',', index_col=[4], na_values=['BRT','ART','---'])
    df['VALUE'] = df['VALUE'].astype(float)

    result = df['VALUE'].resample('H').mean()

    return result

# def get_hourly_USGS():
#         """
#         Function retireves station info that is used to make headers for USGS data.
#         Args:
#             fname: string to the path for the USGS station csv
#         """
#         DatetimeFormat = "%Y-%m-%d %H"
#
#         df = pd.read_csv(fname, low_memory=False,
#                      parse_dates=True, delimiter=',', index_col=[4], na_values=[''])
#         df['VALUE'] = df['VALUE'].astype(float)
#
#         result = df['VALUE'].resample('H').mean()
#
#         return result


# variables that will change with each new dataset
new_csv_file = 'TGC_H.csv'
fname = '/home/kayleegross/Documents/Basins_streamflow/Tuolumne_data/TGC_event.txt'

# call function
df = get_hourly_data(fname)
#print(df[5084:5094])
df.to_csv(new_csv_file)
