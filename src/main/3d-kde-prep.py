from numpy import true_divide
import pandas as pd
#import rpy2.robjects as robjects
#from rpy2.robjects import pandas2ri
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas as pd
import csv

def get_file():
    """
    Grabbing the filetype and the filename
    """
    filetype = ''
    filename = ''
    while(filetype == ''):
        Tk().withdraw()
        filename = askopenfilename()
        
        if '.xlsx' in filename:
            filetype = '.xlsx'
        elif '.csv' in filename:
            filetype = '.csv'
        else:
            print("Unsupported file type. File type must be either .xlsx or .csv. Select a new file.")

    return filename, filetype

def get_names(file, type):
    if type == '.xlsx':
        names = pd.read_excel(file).columns
    elif type == '.csv':
        with open(file, 'r') as f:
            names = csv.DictReader(f).fieldnames

    return names

def print_names(names):
    print("Data Fields:")
    for name in names:
        print("\t" + name)

def get_param_string(param_name, names):
    flag = True
    val = ''
    while flag:
        print("Enter name of field for " + param_name)
        val = input()
        if val in names:
            flag = False
        else:
            print("Invalid name...")
    
    return val
    


def get_param_bool(param_name, names):
    flag = True
    while flag:
        print(param_name + "= [t/f]?")
        val = input()
        if val == 't':
            return True
        elif val == 'f':
            return False
        else:
            print("Invalid input, enter only t or f")

def get_params(names):
    # path, is_2d, name_col, x_col, y_col, z_col (if applicable)
    print_names(names)
    is_2d = get_param_bool("is_2D", names)
    name_col = get_param_string("name_col", names)
    x_col = get_param_string("x_col", names)
    y_col = get_param_string("y_col", names)
    if not is_2d:
        z_col = get_param_string("z_col", names)
    else:
        z_col = "NULL"

    return is_2d, name_col, x_col, y_col, z_col
    


def kde_prep():
    filename, filetype = get_file()
    names = get_names(filename, filetype)
    params = get_params(names)
    
    #r = robjects.R
    #r['source']('3D_KDE_2021.R')
    

if __name__ == '__main__':
    kde_prep()
