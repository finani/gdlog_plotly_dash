#!/usr/bin/env python3
 
import sys
import signal
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_seq_items', None)
        
def signal_handler(signal,frame):
    print('\npressed ctrl + c!!!\n')
    sys.exit(0)
signal.signal(signal.SIGINT,signal_handler)

class GDLOG_PLOTTER:
    def __init__(self, csv_path_):
        self.csv_path = csv_path_
        self.df = pd.read_csv(self.csv_path)
        self.df.columns = self.df.columns.str.strip()
        self.df_length = len(self.df)
        self.data_range = range(self.df_length)
        self.fig_list = []

    def df_picked_plot(self, title_, data_num_):
        plot_header = ['rosTime']
        if data_num_ == 0:
            plot_header.append(title_)
        elif data_num_ > 0:
            for i in range(data_num_):
                plot_header.append(title_+'_'+str(i))
        else:
            print("Error: data_num_ is invaild")
        df_picked = self.df.loc[self.data_range, plot_header]

        df_picked_plot = df_picked.plot.line(
            sharex=True,
            grid=True,
            title=title_+'     ['+str(self.data_range.start)+' - ' +str(self.data_range.stop)+']',
            x='rosTime',
            linewidth=2
            )
        return df_picked_plot.get_figure()

    def df_picked_subplot(self, title_, data_num_, ax_):
        plot_header = ['rosTime']
        if data_num_ == 0:
            plot_header.append(title_)
        elif data_num_ > 0:
            for i in range(data_num_):
                plot_header.append(title_+'_'+str(i))
        else:
            print("Error: data_num_ is invaild")
        df_picked = self.df.loc[self.data_range, plot_header]

        df_picked_plot = df_picked.plot.line(ax=ax_,
            sharex=True,
            grid=True,
            title=title_+'     ['+str(self.data_range.start)+' - ' +str(self.data_range.stop)+']',
            x='rosTime',
            linewidth=2
            )

    def show_guide(self):
        print("Welcome to gdlog_plotter\n")
        print("[gdlog header]\n")
        print(type(df.columns)) # TODO: print data header names
        
        print("\
0. Open Guide\t[h], [help], [-h], [--help]\n\
1. Plot preset\n\
\t[a] rosTime, rpy, velNed, posNed\n\
\t[b] rosTime, accBody, pqr\n\
2. Plot data from header\n\
\t[data_name1] [data_name2] ...\n\
3. Set range [" + str(self.data_range.start) + "-" + str(self.data_range.stop)+"], [max] " + str(self.df_length) + "\n\
\t[start_number] [end_number]\n\
4. Save plot [default] " + self.csv_path.split('.')[0] + ".png\n\
\t[a] save all figures\n\
\t[png_file_name_to_save] save the recent figure\n\
5. Clean plots\n\n\
9. Close gdlog_plotter\t[q], [ctrl+c]\n\
\tUsage: [0-5,9] sub_command_data\n\n")

    def run(self):

        input_raw = input("plotter> ")

        input_list = input_raw.split(' ')
        data_length = len(input_list)-1
        if (input_list[0] == '0') or (input_list[0] == 'h') or (input_list[0] == 'help' or (input_list[0] == '-h') or (input_list[0] == '--help')):
            self.show_guide()
        elif input_list[0] == '1':
            if data_length > 0:
                for i in range(data_length):
                    if input_list[i+1] == 'a':
                        fig, axes = plt.subplots(nrows=3)
                        self.fig_list.append(fig)
                        self.df_picked_subplot('rpy', 3, axes[0])
                        self.df_picked_subplot('velNed', 3, axes[1])
                        self.df_picked_subplot('posNed', 3, axes[2])
                        plt.show(block=False)
                    elif input_list[i+1] == 'b':
                        fig, axes = plt.subplots(nrows=2)
                        self.fig_list.append(fig)
                        self.df_picked_subplot('accBody', 3, axes[0])
                        self.df_picked_subplot('pqr', 3, axes[1])
                        plt.show(block=False)
            else:
                print("\tUsage: 1 a b\n")
        elif input_list[0] == '2': # TODO: need to check data name is valid
            if data_length == 1:
                fig = self.df_picked_plot(input_list[1], 3) # TODO: 3 from enum using title(input_list[1])
                self.fig_list.append(fig)
                plt.show(block=False)
            elif data_length > 1:
                fig, axes = plt.subplots(nrows=data_length)
                self.fig_list.append(fig)
                for i in range(data_length):
                    self.df_picked_subplot(input_list[i+1], 3, axes[i]) # TODO: 3 from enum using title(input_list[1])
                plt.show(block=False)
            else:
                print("\tUsage: 2 rpy velNed")

        elif input_list[0] == '3':
            if data_length == 2:
                self.data_range = range(int(input_list[1]),int(input_list[2]))
                print("Set range ["+str(self.data_range.start)+"-"+str(self.data_range.stop)+"]")
            else:
                self.data_range = range(self.df_length)
                print("\tUsage: 3 start_number end_number")
                print("Set default [0-"+str(self.df_length)+"]")
        elif input_list[0] == '4':
            if len(self.fig_list) == 0:
                print("No figure in the self.fig_list")
            else:
                if data_length == 1:
                    if input_list[1] == 'a':
                        for i in range(len(self.fig_list)):
                            self.fig_list[i].savefig(self.csv_path.split('.')[0] + "_" + str(i) + ".png")
                            print("Saved: " + self.csv_path.split('.')[0] + "_" + str(i) + ".png")
                    else:
                            self.fig_list[-1].savefig(input_list[1] + ".png")
                            print("Saved: " + input_list[1] + ".png")
                else:
                    self.fig_list[-1].savefig(self.csv_path.split('.')[0] + ".png")
                    print("Saved: " + self.csv_path.split('.')[0] + ".png")
        elif input_list[0] == '5':
            plt.close('all')
            self.fig_list.clear()
            print("Clear the self.fig_list")
        elif (input_list[0] == '9') or (input_list[0] == 'q'):
            exit()
        elif input_list[0] == 'weebee':
            print("WeeBee~")
        else:
            print("\tUsage: [0-5,9] sub_command_data")

if __name__ == '__main__':
    if len(sys.argv) == 1: # for test run
        csv_path = "gdLog_210323_172626_edited.csv"
        print("Test run gdlog_plot.py using \'gdLog_210323_172626.csv\'\n")
        print("\tUsage: python3 gdlog_plot.py path_of_your_csv_file\n")
    elif len(sys.argv) == 2:
        csv_path = sys.argv[1]
    else:
        raise SystemExit('\tUsage: python3 %s path_of_your_csv_file' % sys.argv[0])

    gdlog_plotter = GDLOG_PLOTTER(csv_path)
    gdlog_plotter.show_guide()

    while(True):
        gdlog_plotter.run()

# TODO: show list of data
# TODO: get data number from enum class