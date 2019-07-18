import pandas as pd
import datetime as datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv

# matplotlib format modules
from matplotlib.dates import DateFormatter

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# locate/format data
years = mdates.YearLocator()
months = mdates.MonthLocator()
myfmt = mdates.DateFormatter("%Y")

# read in data
df = pd.read_csv('/home/kayleegross/Documents/Basins_streamflow/Kings_data/DKS_cms.csv',
parse_dates = ["datetime"],
# skiprows = 11,
index_col = ["datetime"],
na_values = [-999])

# plot the data
fig, ax = plt.subplots(figsize = (13,8))
ax.plot(df.index.values, df.values)
ax.set(ylabel="cms")
ax.set(title="DKS")

# tell matplotlib to use the format specified above
ax.xaxis.set_major_formatter(myfmt);
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator())
mdates.MonthLocator()
ax.set_xlim(pd.Timestamp('2016-03-02'), pd.Timestamp('2019-03-28'))

# rotate and align the tick labels so they look better
fig.autofmt_xdate()
plt.grid(True)
plt.tight_layout()
plt.show()
plt.close()

















# replace -999 with nan to plot
# df = df.replace(-999, np.nan)
#
#
# print(df)
# plt.plot(df)
# plt.title("TGC")
# plt.xlabel("year")
#
#
# plt.ylabel("cms")
# plt.grid(True)
# plt.show()
# plt.tight_layout()
# # plt.savefig('Q01_fig.png')
# plt.close()
