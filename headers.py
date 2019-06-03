import pandas as pd
import datetime as datetime
import numpy as np
import matplotlib.pyplot as plt
import csv


# create a dictionary to write header for data
mydict = [{'[HEADER]': '\n'},
          {'[HEADER]': 'station_name        = Tuolumne Meadows'},
          {'[HEADER]': 'station_id          = TUM'},
          {'[HEADER]': 'easting             = 293306.562'},
          {'[HEADER]': 'northing            = 4194327.335'},
          {'[HEADER]': 'altitude            = 2621'},
          {'[HEADER]': 'epsg                = 32611'},
          {'[HEADER]': 'comment             = discharge in m^3/s'},
          {'[HEADER]': 'nodata              = -999'},
          {'[HEADER]': 'tz                  = -7'},
          {'[HEADER]': 'fields              = timestamp discharge'},
          {'[HEADER]': '[DATA]'}]

fields = ['[HEADER]']

# file paths
fname = 'TUM.csv'
rawdata = '/home/kayleegross/Documents/Basins_streamflow/Tuolumne_data/complete/TUM_cms.csv'

# write and append df2 to new csv file
with open(fname, 'w+') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = fields, lineterminator = '\n')
    writer.writeheader()
    writer.writerows(mydict)
    csvfile.close()


df2 = pd.read_csv(rawdata)

# use for nan values only
df3 = df2.fillna(value=-999)

df3.to_csv(fname, index=0, header=False, mode='a')

# use if data doesn't contain nan values
# df2.to_csv(fname, index=0, header=False, mode='a')
