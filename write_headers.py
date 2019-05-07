import pandas as pd
import datetime as datetime
import numpy as np
import matplotlib.pyplot as plt



def write_header(new_csv_file, data_fname, station_id, station_name, easting, northing, altitude, epsg, comment, nodata, tz, fields):

    """
    Function generates strings that will be used to rewrite the headers.
    Args:
        header: generates specific header names
    """

# using pandas to read csv and index data based on ID
    df = pd.read_csv(header_fname, index_col="ID")

# retrieving data by locating needed header
    data = df[["Station Name", "ElevationFeet", "Easting", "Northing"]].loc[station]


# generate header and write to new csv
    with open (new_csv_file,'w+') as path:

        station_id = df.get_value(idx, 'ID')
        station_name = df.getvalues(idx, 'Station Name')
        easting = df.getvalues(idx, 'Easting')
        northing = df.getvalues(idx, 'Northing')
        altitude = df.getvalues(idx, 'ElevationFeet')
        epsg = 32611
        comment = 'discharge in m^3/s'
        nodata = -999
        tz = -7
        fields = 'timestamp discharge'


        # Generate strings for header
        header = ("[HEADER]\n"
        "station_id = {}\n"
        "station_name = {}\n"
        "easting = {}\n"
        "northing = {}\n"
        "altitude = {}\n"
        "epsg = {}\n"
        "comment = {}\n"
        "nodata = {}\n"
        "tz = {}\n"
        "fields = {}\n"
        "[DATA]\n".format(station_id, station_name, easting, northing, altitude, epsg, comment, nodata, tz, fields))


        # Write your header
        path.write(header)
        # close
        path.close()

        return(header)

        print(header)



def join_data(df, data_fname, header_fname, new_csv_file):
    """
    Function joins the data with the header into a new csv file
    """

    df = pd.read_csv(data_fname)

    df.to_csv(new_csv_file)

    print(df)



data_fname = '/home/kayleegross/Documents/Basins_streamflow/Tuolumne_data/USGS_TGC_H.csv'
new_csv_file = 'TGC.csv'
header_fname = '/home/kayleegross/Documents/Basins_streamflow/Tuolumne_data/tuol_headers.csv'
station = 'FHH'

# call functions
write_header(station_id, station_name, easting, northing, altitude, epsg, comment, nodata, tz, fields, new_csv_file, data_fname,)

#join_data(data_fname, header_fname, new_csv_file)



# create new csv
df.to_csv(new_csv_file, mode='a')



# parse headers to make data easier to manipulate
#def parse_header(x):

    #pull_header_info = {'[HEADER]', 'station_id':'TGC', 'station_name': 'easting':37.916588, 'northing':-119.659897, 'altitude':3830, 'epsg':32611,
                        #'comment':'discharge in m^3/s', 'nodata':-999 , 'tz':-7, 'fields':'timestamp discharge'}


    #with open(x) as path:
        #lines = path.readlines()
        #path.close()

    # for loop through lines to extract data
    #for key in pull_header_info:
        #pull_header_info.values()

    # return the desired info.
    #return pull_header_info

    #print(pull_header_info)
