import pandas as pd
from datetime import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

def get_hourly_data(fname, new_csv_file):
    """
    Function retireves station info that is used to make headers.
    Args:
        fname: string to the path for the station csv
        headers: uses indexing to
    """
    DatetimeFormat = "%Y-%m-%d %H"

    df = pd.read_csv(fname, low_memory=False,
                 parse_dates=True, delimiter=',', index_col=4) #na_values=['

    print(df["VALUE"])

    # Swap BRT out for NAN maybe
    #df.replace(to_replace = "BRT", value = "NaN")


#new = df.resample('H').mean()

    # save new hourly dataset
    #new.to_csv(new_csv_file)

    print(new)


new_csv_file = 'FHH_H.csv'
# make sure to change header place holders depending on USGS data or CDEC
headers = ['FHH','letter','sensor_no','sensor_type','datetime', 'cfs', 'units']
fname = '/home/kayleegross/Documents/Basins_streamflow/Tuolumne_data/FHH_event.txt'

# call function
get_hourly_data(fname, new_csv_file)
