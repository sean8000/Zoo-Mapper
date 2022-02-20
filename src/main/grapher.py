import argparse
import tkinter

import matplotlib.pyplot as plt
import pandas as pd
import time

# Filters a pandas 'data_frame' for values with the date between 'start' and 'end'
# date_column is the name of the column storing the date (default 'Date')
# Returns the filtered data frame between the 2 given dates
def filter_date(data_frame, start=None, end=None, date_column='Date'):
    if start:
        data_frame = data_frame[data_frame[date_column] > start]
    if end:
        data_frame = data_frame[data_frame[date_column] < end]
    return data_frame

# Gets the frequencies of each unique value for the 'column' inside of the given 'data_frame'
# Returns the names, and frequencies
def create_frequency_data(data_frame, column):
    x = data_frame[column].value_counts().index
    y = data_frame[column].value_counts()
    return x, y

def heat_map_plot(file):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    data = pd.read_excel(file)
    #
    # root = tkinter.Tk()
    # dialog_box = dialogbox.DialogBox
    #
    # dialog_box.root = root
    #
    # D = {'user': 'Bob'}
    # string_var = tkinter.StringVar()
    #
    # b_login = tkinter.Button(root, text= 'Log in')
    # b_login['command'] = lambda: dialog_box('Name?', string_var, options=["Derek", "Bobby"])
    # b_login.pack()
    #
    # b_loggedin = tkinter.Button(root, text='Current User')
    # b_loggedin['command'] = lambda: dialog_box(string_var.get())
    # b_loggedin.pack()
    #
    # root.mainloop()
    #
    # print(D['user'])
    # print(data.index)
    # print("-------------------------------------")
    # print(data.columns)
    # print("-------------------------------------")
    # print(data.dtypes)
    # print("-------------------------------------")
    # print(data.info(verbose='True'))

    data = data.loc[(data['Channel Type'] == 'Interval') &
                    (pd.notnull(data['Space Use Coordinate X'])) &
                    (pd.notnull(data['Space Use Coordinate Y'])) &
                    (pd.notnull(data['Depth in Meters']))]

    x = data['Space Use Coordinate X'].values.flatten()
    y = data['Space Use Coordinate Y'].values.flatten()
    z = data['Depth in Meters'].values.flatten()

    print(x)
    print(y)
    print(z)

    ax.scatter(x, y, z)
    fig.show()
    return fig

# Filters the given data frame with entries only between start and end
# Creates a frequency bar plot and saves it with the given 'output' name
def create_frequency_figure(data_frame, column, start, end, output):
    df = filter_date(data_frame, start, end)
    title = '%s (%s to %s)' % (column, start, end) if start or end else column
    x, y = create_frequency_data(df, column)
    fig, ax = plt.subplots()
    bars = plt.bar(x, y)
    plt.title(title)
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, '%d' % int(height), ha='center', va='bottom')

    fig.savefig(output, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    heat_map_plot("MarinelandThru30June2020_FormattedWithDepth.xlsx")
    #
    # parser = argparse.ArgumentParser(description='Create a graph of data frequencies, filterable by date')
    # parser.add_argument('file', type=str, help='the path to the excel file')
    # parser.add_argument('column', type=str, help='the column name to collect data from in the excel file')
    # parser.add_argument('output', type=str, help='the path to the output image')
    # parser.add_argument('--start', type=str, help='the start date in the format: (d/m/y)')
    # parser.add_argument('--end', type=str, help='the end date in the format: (d/m/y)')
    # args = parser.parse_args()
    #
    # data = pd.read_excel(args.file)
    # create_frequency_figure(data, args.column, args.start, args.end, args.output)
    # print(args.output, "successfully generated.")
