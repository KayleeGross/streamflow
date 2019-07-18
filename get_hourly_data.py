import pandas as pd
from datetime import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import time

def get_hourly_Cdec(fname1):
    """
    Function converts Cdec event data to hourly data.
    Args:
    fname: string to the path for the Cdec station csv
    """
    DatetimeFormat = "%Y-%m-%d %H"

    df = pd.read_csv(fname1, low_memory=False,
                 parse_dates=True, delimiter=',', index_col=[2], na_values=['BRT','ART','---'])

    df['VALUE'] = df['VALUE'].astype(float)

    result = df['VALUE'].resample('H').mean()

    return result


def get_hourly_additional(fname2):
    """
    Function converts additional event data to hourly data.
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
    Function converts event data to hourly data.
    Args:
    fname3: string to the path for the USGS station csv
    """
    DatetimeFormat = "%Y-%m-%d %H"

    df = pd.read_csv(fname3, low_memory=False,
                             parse_dates=[0], delimiter=',', na_values=[''])
    df = df.set_index('dt')

    result = df.resample('H').mean()
    return result




# variables that will change with each new dataset
new_csv_file = 'USGS_11224000_H.csv'
fname1 = '/home/kayleegross/Documents/Basins_streamflow/streamflow_data/11206820_bksjd.csv'
fname2 = '/home/kayleegross/Documents/Basins_streamflow/Merced_data/USGS_HIB_event.csv'
fname3 = '/home/kayleegross/Documents/Basins_streamflow/streamflow_data/11224000_1.csv'

# call function

df = get_hourly_USGS(fname3)

df.to_csv(new_csv_file)
