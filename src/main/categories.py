from tkinter.ttk import Style
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from tokenize import Double
from numpy import double, true_divide
import pandas as pd
import numpy as np
#import rpy2.robjects as robjects
#from rpy2.robjects import NULL, pandas2ri
#from rpy2.robjects import r
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import pandas as pd
import csv
import subprocess
import multiprocessing
import threading
import re
import json
import os


import heatmappage

#import Negating_row

LARGE_FONT = ("Bell Gothic Std Black", 40, 'bold')
MEDIUM_FONT = ("Bell Gothic Std Black", 25, 'bold')
BUTTON_FONT = ('Calibiri', 14, 'bold')
BACKGROUND_COLOR = '#407297'
LIGHT_BLUE = '#d4e1fa'

class Categories_Page(tk.Frame):
    def __init__(self, parent, controller):
        """
        This function creates the landing page when users decide to run Data Transformations.
        We will be able to select the file we want to
        run, run it and return to the home page
        Inputs:
            self: Represents the page that we have created
            parent:
            controller: 
        Results:
            The page will be up and ready for the user to interact with
        """
        # Setting our variables
        self.filename = "None"           # setting the file selection to NULL
        self.outputname = "None"          # Setting the outpot name of the file to NULL
        self.tmp = tk.StringVar()       
        self.tmp.set("hello")


        # Creating the title of the web page
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Data Transformations", font=MEDIUM_FONT)    # Creates the title of the web page
        label.pack(pady=10, padx=10)                                                # Padding the name

        # Creating Buttons for web page
        select_button = ttk.Button(self, text="Select File",
                                        command=lambda: self.select_file())         # Select File button, look to function select_file # 76 to see what it does   
        select_button.pack()        # called with keyword-option/value pairs that control where the widget is to appear within its container
                                    #and how it is to behave when the main application window is resized
        options_button = ttk.Button(self, text="Run Transformations",
                                    command=lambda: self.get_parameters())          # Taken from kde, repurposed
        options_button.pack()

        back_button = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(heatmappage.StartPage))    # setting up the back to home button. goes back to start page for heat map
        back_button.pack()

    def select_file(self):
        """
        This function is handling the selection of a file. We assume that the file is located inlocations specified by kde_args.json
        input: 
            self: The page itself

        result: 
            self.filename is set to the file that was selected 
        """
       # Tk.withdraw(self)
        validFile = False       # presuming that the file the user input is not valid, needs to be proven wrong

        # grabbing the filename + path of the file that the user want to une the KBE on 
        self.filename = askopenfilename(initialdir="", title="Select a File", filetypes=(("Excel Files", "*.xlsx*"), ("CSV Files", "*.csv*"), ("All Files", "*.*")))

        file_type = self.filename[self.filename.index('.'):] # grabbing the typr of the filw

        # Checking to make sure the file is an .xslx or a .csv
        if file_type == ".xlsx":
            validFile = True
        if file_type == ".csv":
            validFile = True

        # else: # presumabley to make sure that we are not allowing a file that is not valid to be saved
        #     errorMessage(Error.FILETYPE)
        #     self.filename = ""


    def get_parameters(self):
        """
        grabbing all of the information and parameters from the file we have selected
        """
        options_box = Params_Page(self.filename)
        options_box.wait_window(options_box)
        
        

"""
This page allows users to select parameters for KDE calculations and
run the KDE script
"""
class Params_Page(tk.Toplevel):
    def __init__(self, filename):
        """
        Initializing everything we will use for the KDE calculatiosn
        input:
            self
            filename: Filename of file where we will be grabbing our data from
        """
        tk.Toplevel.__init__(self)  # constucting a main window of an application and making sure it is in the front of the screen
        self.attributes('-topmost', 'true')

        # We know what data we need for the calcularions so we are specifying the types they should all be
        self.filename = tk.StringVar()      # filename
        self.outputname = tk.StringVar()    # unsure
        self.categ = tk.StringVar()    # the column you want to invert

        self.filename.set(filename)         # setting filename to the filename the user input

        self.headers = self.get_headers(self.filename.get())            #grabbing the names of the headers from the file we input
    
        categ_label = tk.Label(self, text='Behavior Desc. Column', bg='white')       # Name of the column you want to invert
        categ_label.pack()                                                   # called with keyword-option/value pairs that control where the widget is to appear within its container
        categ_dropdown = tk.OptionMenu(self, self.categ, *self.headers)   # populating column with the data stored in the  column
        categ_dropdown.pack()
       
        tmp_button = tk.Button(self, text="Run Transformations",
                                command=lambda: self.run_transformations())
        tmp_button.pack()

    def get_headers(self, file):
        headers = list(pd.read_excel(file).columns)
        headers.append("N/A")
        return headers

    '''
    Selecting an output directory for the KDE calculations through python before the R script
    '''

    def select_output(self):
        validFile = False
        self.outputname = filedialog.askdirectory(title = "Select a Directory for Output")

    def run_transformations(self):
        self.select_output()

        df = pd.read_excel(self.filename.get(), sheet_name=0)
        descCol = self.categ.get()

        listOfDesc = df[descCol].dropna().unique().tolist()
        listOfNumbers = []
        i = 1
        for elem in listOfDesc:
            listOfNumbers.append(i)
            i+=1
        print(listOfDesc)
        print(listOfNumbers)

        conditions = [df[descCol].values == desc for desc in listOfDesc]
        values = [num for num in listOfNumbers]
        df['Description_To_Number'] = np.select(conditions, values)

        df['Description_Legend'] = np.nan
        df['Description_Legend'][0] = "Empty Column = 0"
        j = 1
        for desc in listOfDesc:
            df['Description_Legend'][j] = listOfDesc[j-1] + " = " + str(listOfNumbers[j-1])
            j+=1
        file_name = os.path.splitext(os.path.basename(self.filename.get()))[0]
        outdir = self.outputname + "/" + file_name + "_Desc_To_Number.xlsx"
        df.to_excel(outdir)
        messagebox.showinfo("Complete", "Description to Number is Complete")