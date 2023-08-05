import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import pytz
from influxdb import InfluxDBClient
import scipy as sp
import scipy.optimize as op
from scipy.stats import norm

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.ticker import AutoMinorLocator, MultipleLocator


# define ticks
def set_ticks(ax, xMaj, yMaj):
    ax.xaxis.set_major_locator(MultipleLocator(xMaj))
    ax.yaxis.set_major_locator(MultipleLocator(yMaj))
    ax.minorticks_on()
    ax.tick_params(which='major', width=1.0, length=8, direction='in', labelsize=14)
    ax.tick_params(which='minor', width=1.0, length=4, direction='in', labelsize=14)
    ax.yaxis.get_offset_text().set_fontsize(14)
    ax.xaxis.get_offset_text().set_fontsize(14)



def plot(x, y, save=True, debug=True):

    fig = plt.figure(figsize=(16, 8))
    gs = fig.add_gridspec(2, 2,  width_ratios=(8,2), height_ratios=(2,8),
                        left=0.1, right=0.9, bottom=0.1, top=0.9,
                        wspace=0.05, hspace=0.05)

    ax = fig.add_subplot(gs[1, 0])

    ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)

    x_data = x
    y_data = y

    # compute mean,max and min
    mean = np.mean(y_data)
    max_val = np.max(y_data)
    min_val = np.min(y_data)

    # --- Plot --- #
    #ax.plot(x_data, y_data, color='#004C97', linestyle='-', alpha = 0.8, lw=1)
    ax.plot(x_data, y_data, marker='o', markersize=4, color='#004C97',
            alpha=0.5, mec= 'none', linestyle='none')

    # number of ticks 
    n_ticks = 9
    step = int((max_val - min_val) / n_ticks)

    # ticks
    ax.yaxis.set_major_locator(MultipleLocator(step))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    # set formatter
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.minorticks_on()
    ax.tick_params(which='major', width=1.0, length=8, direction='in', labelsize=14)
    ax.tick_params(which='minor', width=1.0, length=4, direction='in', labelsize=14)

    ax_histy.yaxis.set_major_locator(MultipleLocator(step))
    #ax_histy.xaxis.set_major_locator(MultipleLocator(6))
    ax_histy.minorticks_on()
    ax_histy.tick_params(which='major', width=1.0, length=8, direction='in', labelsize=14)
    ax_histy.tick_params(which='minor', width=1.0, length=4, direction='in', labelsize=14)
    ax_histy.yaxis.set_label_position('right')
    ax_histy.yaxis.tick_right()

    # labels
    ax.set_xlabel('Time [h:m]', fontsize=14)
    ax.set_ylabel('Resistance [$\Omega $]', fontsize=14)
    ax.set_ylim(np.min(y_data)-6,np.max(y_data)+5)

    # text 
    today, _ = datetime.now().strftime('%Y%m%d %H:%M:%S').split()
    ax.text(0.018, 0.95, today, transform = ax.transAxes, fontsize=13, fontweight = 'bold')
    ax.text(0.2, 0.95, 'Mean = %1.1f $\Omega$' %mean, transform = ax.transAxes, fontsize=13)

    # --- Histogram --- #
    ax_histy.hist(y_data, bins=30, fc = '#004C97',alpha = 0.2, orientation='horizontal')
    n, bins , _ = ax_histy.hist(y_data, bins=30, histtype='step', ec = '#004C97',lw=2, 
                                            orientation='horizontal')

    # bin width 
    bin_width = bins[1] - bins[0]
    ax_histy.set_xlabel('Counts / %1.1f $\Omega$'%bin_width, fontsize=14)

    # no labels on histogram projections plot
    #ax_histy.tick_params(axis='y', labelleft=False)

    if save:
        fig.savefig('plots/' + today + '.png', dpi = 200)


    # open txt file to save data 
    if debug:
        path = '/home/acd/acdemo/gizmo-control/gizmo/'
        filename = 'summary.txt'

        if os.path.exists(path + filename):
            outfile = open(path + filename, 'a')
        else: 
            outfile = open(path + filename, 'a')
            outfile.write('Date\t\t' + 'Mean\t' + 'Max\t' + 'Min\t' + '\n')

        outfile.write(today + '\t' + '{:1.1f}'.format(mean) + '\t' + str(max_val) + '\t' + str(min_val) + '\n' )

        # close file
        outfile.close()



def main():
    
    '''Connect to the InfluxDB and read impedance data
       of the last 24 hours. Finally produce a plot.'''

    host = 'localhost'
    port = 8086

    dbname = 'gizmo'
    query = 'SELECT "Res" FROM "LArTF_monitor" WHERE time > now() - 24h'

    client = InfluxDBClient(host='localhost', port=8086, database = 'gizmo')

    print('Querying data: ' + query)
    result = client.query(query)

    date, impedance = [],[]
    for point in result.get_points():
        date_utc = datetime.strptime(point['time'], '%Y-%m-%dT%H:%M:%SZ')
        date.append(date_utc - timedelta(hours = 5))
        impedance.append(point['Res'])

    plot(date, impedance, True, True)


if __name__ == '__main__':
    main()



