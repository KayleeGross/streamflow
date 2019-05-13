import pandas as pd
from datetime import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

def get_hourly_Cdec(fname1):
    """
    Function retireves station info that is used to make headers for Cdec data.
    Args:
        fname: string to the path for the Cdec station csv
    """
    DatetimeFormat = "%Y-%m-%d %H"

    df = pd.read_csv(fname1, low_memory=False,
                 parse_dates=True, delimiter=',', index_col=[4], na_values=['BRT','ART','---'])
    df['VALUE'] = df['VALUE'].astype(float)

    result = df['VALUE'].resample('H').mean()

    return result


def get_hourly_additional(fname2):
    """
    Function retireves station info that is used to make headers for Cdec data.
    Args:
        fname: string to the path for the additional stations csv
    """
    DatetimeFormat = "%Y-%m-%d %H"

    df = pd.read_csv(fname2, low_memory=False,
                     parse_dates=True, delimiter=',', index_col=[0])


    columnNames = list(df.head(1))
    # print(columnNames)

    df[' Q6(cms)'] = df[' Q6(cms)'].astype(float)


    result = df[' Q6(cms)'].resample('H').mean()

    return result


def get_hourly_USGS(fname3):
    """
    Function retireves station info that is used to make headers for USGS data.
    Args:
    fname: string to the path for the USGS station csv
    """
    DatetimeFormat = "%Y-%m-%d %H"

    df = pd.read_csv(fname, low_memory=False,
                      parse_dates=True, delimiter=',', index_col=[4], na_values=[''])

    df['VALUE'] = df['VALUE'].astype(float)

    result = df['VALUE'].resample('H').mean()

    return result


# variables that will change with each new dataset
new_csv_file = 'Q6.csv'
fname1 = '/home/kayleegross/Documents/Basins_streamflow/Tuolumne_data/UCC_event.txt'
fname2 = '/home/kayleegross/Documents/Basins_streamflow/Tuolumne_data/Tuolumne_additional_6stations.csv'
fname3 = '/home/kayleegross/Documents/Basins_streamflow/Merced_data/USGS_HIB_event.txt'

# call function
# df = get_hourly_data(fname1)

df = get_hourly_additional(fname2)
#print(df[5084:5094])
df.to_csv(new_csv_file)
