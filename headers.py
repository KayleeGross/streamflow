import pandas as pd
import datetime as datetime
import numpy as np
import matplotlib.pyplot as plt
import csv

# create a dictionary to write header for data
header_tuples = [('station_id','TUM'),
          ('station_name','tuolumne meadows'),
          ('easting','293306.56228591'),
          ('northing','4194327.33462844'),
          ('altitude','2621'),
          ('epsg','32611'),
          ('comment','discharge in m^3/s'),
          ('nodata','-999'),
          ('tz','-7'),
          ('fields','timestamp discharge'),
          ('[DATA]', "")]

header_list = []

for t in header_tuples:
    msg = "{0:<18}{1:<20}".format(t[0], "= " +  t[1])
    header_list.append({"[HEADER]":msg})

# mydict = [{'[HEADER]': 'station_id        = TUM'},
#           {'[HEADER]': 'station_name      = tuolumne meadows'},
#           {'[HEADER]': 'easting           = 293306.56228591'},
#           {'[HEADER]': 'northing          = 4194327.33462844'},
#           {'[HEADER]': 'altitude          = 2621'},
#           {'[HEADER]': 'epsg              = 32611'},
#           {'[HEADER]': 'comment           = discharge in m^3/s'},
#           {'[HEADER]': 'nodata            = -999'},
#           {'[HEADER]': 'tz                = -7'},
#           {'[HEADER]': 'fields            = timestamp discharge'},
#           {'[HEADER]': '[DATA]'}]

fields = ['[HEADER]']

# file paths
fname = 'TUM_edit.smet'
rawdata = '/home/kayleegross/Documents/Basins_streamflow/streamflow_data/cms_hourly_data/TUM_cms.csv'

# write and append df2 to new csv file
with open(fname, 'w+') as csvfile:
    csvfile.write("SMET 1.1 ASCII\n")
    writer = csv.DictWriter(csvfile, fieldnames = fields)
    writer.writeheader()
    writer.writerows(header_list)
    print(type(csvfile))
    csvfile.close()


df2 = pd.read_csv(rawdata,parse_dates=[0])


# use for nan values only
df3 = df2.fillna(value=-999)

# print(type(df3.iloc[1][0]))

df3.to_csv(fname, index=0, header=False, mode='a', date_format= '%Y-%m-%dT%H:%M:%S')


# use if data doesn't contain nan values
# df2.to_csv(fname, index=0, header=False, mode='a')
