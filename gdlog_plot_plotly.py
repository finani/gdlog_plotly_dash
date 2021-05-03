#!/usr/bin/env python3
 
import os
import sys
import signal
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

pd.set_option('display.max_seq_items', None)
        
def signal_handler(signal,frame):
    print('\npressed ctrl + c!!!\n')
    sys.exit(0)
signal.signal(signal.SIGINT,signal_handler)

class GDLOG_PLOTTER:
    def __init__(self, csv_path_):
        self.my_path = os.getcwd()
        self.csv_path = csv_path_
        self.csv_file_name = self.csv_path.split('/')[-1].split('.')[0]
        self.save_path = self.my_path + '/' + self.csv_file_name + '/'
        self.df = pd.read_csv(self.csv_path)
        self.df['dateTime'] = pd.to_datetime(self.df['rosTime'], unit='s') + pd.DateOffset(hours=9)
        self.df.columns = self.df.columns.str.strip()
        self.df_header_list = self.df.columns.tolist()
        self.df_header_dict = {}
        self.df_length = len(self.df)
        self.data_range = range(self.df_length)
        self.preset_dict = {
            'a' : ['rpy', 'velNed', 'posNed'],
            'b' : ['accBody', 'pqr'],
            'c' : ['vbxyz'],
            'px4' : ['fcMcMode', 'rpy', 'velNed', 'posNed']
        }
        self.fig_list = []

        self.header_list_to_dict()

    def df_picked_plot(self, title_, data_num_, fig_):
        plot_header = ['dateTime']
        if data_num_ == 1:
            if (self.df_header_dict[title_][1] == "None"):
                plot_header.append(title_)
            else:
                plot_header.append(title_+'_'+self.df_header_dict[title_][1])
        elif data_num_ > 1:
            for i in range(data_num_):
                if (self.df_header_dict[title_][1+i] == "None"):
                    plot_header.append(title_+'_'+str(i))
                else:
                    plot_header.append(title_+'_'+self.df_header_dict[title_][1+i]+'_'+str(i))
        else:
            print("Error: data_num_ is invaild")
        # df_picked = self.df.loc[self.data_range, plot_header]

        plot_header_x = plot_header[0]
        for plot_header_y in plot_header[1:]:
            fig_.add_trace(go.Scatter(x=self.df[plot_header_x], y=self.df[plot_header_y], name=plot_header_y))
        return fig_

    def df_picked_subplot(self, title_, data_num_, fig_, i_):
        plot_header = ['dateTime']
        if data_num_ == 1:
            if (self.df_header_dict[title_][1] == "None"):
                plot_header.append(title_)
            else:
                plot_header.append(title_+'_'+self.df_header_dict[title_][1])
        elif data_num_ > 1:
            for i in range(data_num_):
                if (self.df_header_dict[title_][1+i] == "None"):
                    plot_header.append(title_+'_'+str(i))
                else:
                    plot_header.append(title_+'_'+self.df_header_dict[title_][1+i]+'_'+str(i))
        else:
            print("Error: data_num_ is invaild")
        # df_picked = self.df.loc[self.data_range, plot_header]

        plot_header_x = plot_header[0]
        for plot_header_y in plot_header[1:]:
            fig_.add_trace(go.Scatter(x=self.df[plot_header_x], y=self.df[plot_header_y], name=plot_header_y), row=1+i_, col=1)
        return fig_

    def plot_using_data_name_list(self, title_list_):
        axes_length = len(title_list_)
        if axes_length == 1:
            fig = go.Figure()
            self.df_picked_plot(title_list_[0], self.df_header_dict[title_list_[0]][0], fig)
            # self.fig_list.append(fig)
            fig.update_layout(
                title_text=title_list_[0]+'     ['+str(self.data_range.start)+' - ' +str(self.data_range.stop)+']',
                xaxis_title="dateTime",
                xaxis=dict(
                    rangeslider=dict(
                        visible=True,
                        thickness=0.1
                    ),
                    type="date"
                )
            )
            fig.show(block=False)
        elif axes_length > 1:
            fig = make_subplots(
                rows=axes_length,
                cols=1,
                shared_xaxes=True
            )
            for i in range(axes_length):
                self.df_picked_subplot(title_list_[i], self.df_header_dict[title_list_[i]][0], fig, i)
            # self.fig_list.append(fig)
            fig.update_layout(
                title=dict(
                    text=title_list_[i]+'     ['+str(self.data_range.start)+' - ' +str(self.data_range.stop)+']'
                ),
                xaxis=dict(
                    title="dateTime",
                    type="date",
                    rangeslider=dict(
                        visible=True,
                        thickness=0.1
                    )
                )
            )
            fig.show(block=False)

    def plot_using_preset_name(self, title_):
        self.plot_using_data_name_list(self.preset_dict[title_])

    def header_list_to_dict(self):
        for title in self.df_header_list:
            title_splited = title.split('_')
            self.df_header_dict.setdefault(title_splited[0], [])
            len_title_splited = len(title_splited)
            if (len_title_splited == 1):
                self.df_header_dict[title_splited[0]].append(1)
                self.df_header_dict[title_splited[0]].append("None")
            elif (len_title_splited == 2):
                if title_splited[-1].isdigit():
                    try:
                        self.df_header_dict[title_splited[0]][0] += 1
                    except:
                        self.df_header_dict[title_splited[0]].append(1)
                    self.df_header_dict[title_splited[0]].append("None")
                else:
                    self.df_header_dict[title_splited[0]].append(1)
                    self.df_header_dict[title_splited[0]].append(title_splited[-1])
            elif (len_title_splited == 3):
                    try:
                        self.df_header_dict[title_splited[0]][0] += 1
                    except:
                        self.df_header_dict[title_splited[0]].append(1)
                    self.df_header_dict[title_splited[0]].append(title_splited[-2])
            else:
                print("CSV file includes invalid data_name: " + title)

    def show_preset(self):
        print("[preset_name]\n")
        for item in sorted(self.preset_dict.items()):
            print(item)
        print("")

    def show_log_data(self):
        print("\n[data_name]\n")
        column_count = 1
        key_previous = 'a'
        for key, value in sorted(self.df_header_dict.items()):
            if key[0] != key_previous[0]:
                key_previous = key
                print("")
                if (column_count != 1):
                    print("")
                column_count = 1
            if column_count < 3:
                print(key + ": " + str(value[0]), end='\t')
                if len(key) < 5:
                    print("", end='\t\t')
                elif len(key) < 13:
                    print("", end='\t')
                column_count += 1
            else:
                print(key + ": " + str(value[0]))
                column_count = 1
        print("\n")

    def show_guide(self):
        print("Welcome to gdlog_plotter\n")

        self.show_preset()
        self.show_log_data()

        print("\n\
[Command]\n\n\
\t[help] Open Guide\n\n\
\t[show] Plot preset\n\
\t\t[preset_name1] [preset_name2] ...\n\n\
\t[plot] Plot data from header\n\
\t\t[data_name1] [data_name2] ...\n\n\
\t[range] Set range   [cur] " + str(self.data_range.start) + "-" + str(self.data_range.stop)+", [max] " + str(self.df_length) + "\n\
\t\t[start_number] [end_number]\n\n\
\t[save] Save plot (.png)\n\
\t\t[all] save all figures\n\
\t\t[png_file_name_to_save] save the recent figure\n\n\
\t[clear] Clear plots\n\n\
\t[q] Close gdlog_plotter\n\n\
\n\tUsage: [show, plot, range, save, clear, q] sub_command_data\n\n")

    def show_debug_data(self):
        print("\n[data_name]\n")
        column_count = 1
        key_previous = 'a'
        for key, value in sorted(self.df_header_dict.items()):
            if key[0] != key_previous[0]:
                key_previous = key
                print("")
                if (column_count != 1):
                    print("")
                column_count = 1
            if column_count < 3:
                print(key + ": " + str(value), end='\t')
                if len(key) < 5:
                    print("", end='\t\t')
                elif len(key) < 13:
                    print("", end='\t')
                column_count += 1
            else:
                print(key + ": " + str(value))
                column_count = 1
        print("\n")

    def run(self):
        input_raw = input("plotter> ")
        input_list = input_raw.split(' ')
        data_length = len(input_list)-1

        if input_list[0] == 'help':
            self.show_guide()

        elif input_list[0] == 'show':
            if data_length > 0:
                try:
                    for i in range(data_length):
                        self.plot_using_preset_name(input_list[i+1])
                except:
                    self.show_preset()
                    print("invalid preset_name\n")
            else:
                self.show_preset()
                print("\tUsage: show [preset_name1] [preset_name2] ...\n")

        elif input_list[0] == 'plot':
            if data_length > 0:
                # try:
                self.plot_using_data_name_list(input_list[1:])
                # except:
                #     self.show_log_data()
                #     print("invalid data_name\n")
            else:
                self.show_log_data()
                print("\tUsage: plot [data_name1] [data_name2] ...")
                
        elif input_list[0] == 'range':
            if data_length == 2:
                self.data_range = range(int(input_list[1]),int(input_list[2]))
                print("Set range ["+str(self.data_range.start)+"-"+str(self.data_range.stop)+"]")
            else:
                self.data_range = range(self.df_length)
                print("\tUsage: range [start_number] [end_number]")
                print("Set default [0-"+str(self.df_length)+"]")

        elif input_list[0] == 'save':
            if len(self.fig_list) == 0:
                print("No figure in the self.fig_list")
                print("\tUsage: save [a]\n\t\tsave [png_file_name_to_save]")
            else:
                if not os.path.isdir(self.save_path): os.makedirs(self.save_path)
                if data_length == 1:
                    if input_list[1] == 'all':
                        for i in range(len(self.fig_list)):
                            self.fig_list[i].savefig(self.save_path + "fig_" + str(i) + ".png")
                            print("Saved: " + self.save_path + "fig_" + str(i) + ".png")
                    else:
                            self.fig_list[-1].savefig(self.save_path + input_list[1] + ".png")
                            print("Saved: " + self.save_path + input_list[1] + ".png")
                else:
                    self.fig_list[-1].savefig(self.save_path + "fig.png")
                    print("Saved: " + self.save_path + "fig.png")

        elif input_list[0] == 'clear':
            plt.close('all')
            self.fig_list.clear()
            print("Clear the self.fig_list")

        elif input_list[0] == 'debug':
            self.show_debug_data()
            print("Show debug data")

        elif ('q' in input_list[0]) or ('Q' in input_list[0]):
            plt.close('all')
            self.fig_list.clear()
            print("Clear the self.fig_list")
            print("Quit the gdlog_plot.py")
            exit()

        else:
            print("\tUsage: [show, plot, range, save, clear, q] sub_command_data")

if __name__ == '__main__':
    if len(sys.argv) == 1: # for test run
        csv_path = "gdLog_210323_172626.csv"
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
