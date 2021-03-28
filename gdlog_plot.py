#!/usr/bin/env python3
 
import sys
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_seq_items', None)

df = []
data_range = []

def df_picked_plot(df_, title_, data_num_, ax_):
    plot_header = ['rosTime']
    for i in range(data_num_):
        plot_header.append(title_+'_'+str(i))
    df_picked = df_.loc[data_range, plot_header]

    df_picked_plot = df_picked.plot.line(ax=ax_,
        sharex=True,
        grid=True,
        title='['+title_+']     ('+str(data_range.start)+' - ' +str(data_range.stop)+')', \
        x='rosTime',
        linewidth=2
        )

if __name__ == '__main__':
    if len(sys.argv) == 1: # for test run
        csv_path = "gdLog_210323_172626_edited.csv"
        print("Test run gdlog_plot.py using \'gdLog_210323_172626.csv\'\n")
        print("Usage: python3 gdlog_plot.py path_of_your_csv_file\n")
    elif len(sys.argv) == 2:
        csv_path = sys.argv[1]
    else:
        raise SystemExit('Usage: python3 %s path_of_your_csv_file' % sys.argv[0])

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()
    print(df.columns)

    data_range = range(0, 200)
    # data_range = range(len(df))

    fig, axes = plt.subplots(nrows=3)
    df_picked_plot(df, 'rpy', 3, axes[0])
    df_picked_plot(df, 'velNed', 3, axes[1])
    df_picked_plot(df, 'posNed', 3, axes[2])

    fig, axes = plt.subplots(nrows=2)
    df_picked_plot(df, 'accBody', 3, axes[0])
    df_picked_plot(df, 'pqr', 3, axes[1])

    plt.show()

# make interface
# show list of data
# get data number from enum class
# set plots from user input
# show
# loop