from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from matplotlib.figure import figaspect
from netCDF4 import Dataset
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import datetime, timedelta
import os

import netCDF4 as nc

# from snowav.utils.wyhr import calculate_date_from_wyhr

# Read in the rainfall, AJ forecasts, and inflow as pandas dataframes.
df_ppt = pd.read_csv('/home/kayleegross/Documents/tuolumne_river_forecast/forecast_files/DP_precip_thru0625.csv', index_col=0, parse_dates=[0])
df_forecast = pd.read_csv('/home/kayleegross/Documents/tuolumne_river_forecast/forecast_files/CNRFC_AJ_forecast_thru0730.csv', index_col=0, parse_dates=[0])
df_runoff = pd.read_csv('/home/kayleegross/Documents/tuolumne_river_forecast/forecast_files/DP_AJ_runoff_thru0625.csv', index_col=0, parse_dates=[0], header=0)

# Read in updated swe and swi data
df_revised_swi = pd.read_csv('/home/kayleegross/Documents/tuolumne_river_forecast/forecast_files/revised_swi.csv', index_col=0, parse_dates=[0])
df_swe_swi = pd.read_csv('/home/kayleegross/Documents/tuolumne_river_forecast/forecast_files/swe_ytd_swi.csv', index_col=0, parse_dates=[0])
df_swe_runoff = pd.read_csv('/home/kayleegross/Documents/tuolumne_river_forecast/forecast_files/swe_ytd_runoff.csv', index_col=0, parse_dates=[0])


fig1 = plt.figure(figsize=(9.85, 7), dpi=150)
ax = fig1.add_subplot(111)
ax2 = ax.twinx()


# # plot CNRFC data
ax.plot(df_forecast.index, df_forecast['CNRFC 10%'], 'salmon', label='CNRFC 10%')
ax.plot(df_forecast.index, df_forecast['CNRFC 50%'], 'powderblue', label='CNRFC 50%')
ax.plot(df_forecast.index, df_forecast['CNRFC 90%'], 'yellowgreen', label='CNRFC 90%')

# # plot swi and swe
# df_swi['AF'].plot(kind='line', color='grey', ax=plt.gca(), label='SWI')
ax.plot(df_swe_swi.index, df_swe_swi['AF'], 'mediumpurple', label='Cumulative SWI+SWE')
ax.plot(df_swe_runoff.index, df_swe_runoff['current_swe_ytd_runoff'], 'darkgoldenrod', label='Cumulative Runoff+SWE')
ax.plot(df_revised_swi.index, df_revised_swi['normalized swi'], 'slategrey', label='Cumulative SWI')

# plot runoff
ax.plot(df_runoff.index, df_runoff, 'midnightblue', label='Cumulative Runoff')

# plot rainfall
ax2.bar(df_ppt.index, df_ppt["precip_in"].values, width=1,color='firebrick', label='Don Pedro Rainfall')
ax2.xaxis_date()


# set axis labels and ticks
ax.set_title('Tuolumne River Forecasts of April through July Runoff (AF)', fontsize=10, loc= 'center')
ax.set_xlabel('Date of Probabilistic Start', fontsize=10);
ax.set_ylabel('April through July Runoff (Acre-Feet)', fontsize=10);
ax2.set_ylabel('Rainfall [in.]', rotation=-90, fontsize=10)
ax2.yaxis.set_label_coords(1.07, 0.5)

# ax1.tick_params(axis='x', which='both', bottom=False, labelbottom=False)
ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
ax.set_yticks(125000+np.arange(0, 2625000, step=125000))
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))

# plt.setp(ax1.xaxis.get_majorticklabels(), rotation=-90 )
ax.tick_params(axis='x', which='minor', bottom=False)
ax.tick_params('x', rotation=-90, labelsize=7)
ax.tick_params('y', labelsize=7)
ax2.tick_params('y', labelsize=7)
# ax2.tick_params(axis='x', which='both', bottom=False, labelbottom=False)
ax.grid(linewidth=0.5, alpha=0.5)
# ax.legend(fontsize=7)

ax.set_xlim(pd.Timestamp('2018-10-01'), pd.Timestamp('2019-09-30'))
ax.set_ylim(0, 2625000)
ax2.set_ylim(0, 20)


# path to flights netcdf
file = '/mnt/snow_home/lidar_depths_wy2019.nc'

# open the file
ncf = nc.Dataset(file, 'r')

# get all of the water year hour numbers in the 'time' variable
times = ncf.variables['time'][:]

# close the file
ncf.close()

# get flight dates
def calculate_date_from_wyhr(wyhr, year):
    """
    Takes in the integer of water year hours and an integer year and
    returns the date
    """

    start = datetime(year=year-1, month=10, day=1)

    delta = timedelta(hours = wyhr)
    return start+delta

# convert each water year hour to a date and put them in a list
dates = []
for t in times:
    date = calculate_date_from_wyhr(int(t),2019)
    dates.append(date)

# loop through dates to plot lines
for i,date in enumerate(dates):
    if i == 0:
        lbl = 'Flight Dates'
    else:
        lbl = '__nolabel__'
    ax.axvline(x=date.date(), linestyle=':', linewidth=0.75, color='k', label=lbl)

fig1.legend(fontsize=6, loc="upper left", bbox_to_anchor=(0.75, 0.5))

plt.show()
plt.close()
