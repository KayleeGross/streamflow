import pandas as pd
import datetime as datetime
import numpy as np
import matplotlib.pyplot as plt
import utm

# define function
def get_station_info(fname, station_ids):
    """
    Function retireves station info that is used to make headers.
    Args:
        data: locates specific rows and columns needed for header
    """
# using pandas to read csv and index data based on ID
    df = pd.read_csv(fname, index_col="ID")


# retrieving data by locating needed headers
    data = df[["Station Name", "Longitude", "Latitude", "ElevationFeet"]].loc[station_ids]

    return data


def get_utm(station_ids, df, new_csv_file):
    """
    Function converts a (lat, long) tuple from station id name into a UTM coordinate:
    Args:
        latlon: locates latlon data
        utm_conversion: converts latlon to utm
    """
    ds = df.copy()

    dutm = pd.DataFrame(columns=["Northing", "Easting", "station_id"])
    latlon = (ds[["Latitude", "Longitude"]].loc[station_ids])
    i = 0
    datax = []
    datay = []

    # for loop through latlon data
    for idx, row in latlon.iterrows():
        utm_conversion = utm.from_latlon(row['Latitude'], row['Longitude'])

        datax.append(utm_conversion[0])
        datay.append(utm_conversion[1])


    ds['Easting'] = datax
    ds['Northing'] = datay

    new = ds.drop(columns=['Longitude', 'Latitude'])

    # create new csv
    new.to_csv(new_csv_file)
    return new


# make some variables that will change with each station
new_csv_file = 'tuol_headers.csv'
fname = "/home/kayleegross/Documents/Basins_streamflow/station_info_TUOL.csv"
station_ids = ["FHH", "UCC", "TGC", "TUM"]

# call function
x = get_station_info(fname, station_ids)
y = get_utm(station_ids, x, new_csv_file)
print(y)
