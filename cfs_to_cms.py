
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma

# conversion rate of cfs to cms
c = 35.315
new_csv_file = 'USGS_TGC_cms.csv'

# pull/read file
df = pd.read_csv("/home/kayleegross/Documents/Basins_streamflow/Tuolumne_data/tuol_hourly/USGS_TGC_H.csv", header = 0)

# print(DataFrame)

# make a new column in the dataframe and make it equal to cfs
df['cms'] = df['cfs']/c

dfnew = df.drop(columns=['cfs'])

# save it to a new csv with .to_csv()
dfnew.to_csv(new_csv_file)

# # define x,y for plot
# x_values = dfnew.datetime
# y_values = dfnew.cms
#
# #plotting and saving figure
# plt.plot(x_values, y_values)
# # plt.savefig("RCSF.png")
# plt.show()
