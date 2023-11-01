from tkinter.ttk import Style
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from tokenize import Double
from numpy import double, true_divide
import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects import NULL, pandas2ri
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

LARGE_FONT = ("Bell Gothic Std Black", 40, 'bold')      # setting for the large font
MEDIUM_FONT = ("Bell Gothic Std Black", 25, 'bold')     # settings for the medium fonts
BUTTON_FONT = ('Calibiri', 14, 'bold')                  # setting the font for the button
BACKGROUND_COLOR = '#407297'                            # background color for the button
LIGHT_BLUE = '#d4e1fa'                                  # background color for the site
JSON_PATH = os.getcwd() + '/kde_args.json'              # the path to the files we will use for the calculations


"""
Main page for KDE calculations
Allows user to select a file to run KDE calculations on
"""
class KDE_Page(tk.Frame):
    def __init__(self, parent, controller):
        """
        This function creates the landing page when users decide to run a KDE. We will be able to select the files we want to
        run in the KDE, Run the KDE itself and return to the home page
        Inputs:
            self: Represents the page that we have created
            parent:
            controller: 
        Results:
            The page will be up and ready for the user to interact with
        """
        # Setting our variables
        self.filename = NULL            # setting the file selection to NULL
        self.outputname = NULL          # Setting the outpot name of the file to NULL
        self.tmp = tk.StringVar()       
        self.tmp.set("hello")


        # Creating the title of the web page
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Kernel Density Estimate", font=MEDIUM_FONT)    # Creates the title of the web page
        label.pack(pady=10, padx=10)                                                # Padding the name

        # Creating Buttons for web page
        select_button = ttk.Button(self, text="Select File",
                                        command=lambda: self.select_file())         # Select File button, look to function select_file # 76 to see what it does   
        select_button.pack()        # called with keyword-option/value pairs that control where the widget is to appear within its container
                                    #and how it is to behave when the main application window is resized
        options_button = ttk.Button(self, text="Run KDE",
                                    command=lambda: self.get_parameters())          # Run the KDE , makes sure the parameters we were given were correct
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
        options_box = KDE_Calculation_Page(self.filename)
        options_box.wait_window(options_box)
        
        

"""
This page allows users to select parameters for KDE calculations and
run the KDE script
"""
class KDE_Calculation_Page(tk.Toplevel):
    def __init__(self, filename):
        tk.Toplevel.__init__(self)
        self.attributes('-topmost', 'true')

        self.filename = tk.StringVar()
        self.outputname = tk.StringVar()
        self.name_col = tk.StringVar()
        self.x_col = tk.StringVar()
        self.y_col = tk.StringVar()
        self.z_col = tk.StringVar()
        self.is_2d = tk.BooleanVar()
        self.is_2d.set(False)
        self.noise = tk.BooleanVar()
        self.noise.set(False)
        self.m = tk.IntVar()
        self.n = tk.IntVar()
        self.samse = tk.BooleanVar()
        self.samse.set(False)
        self.unconstr = tk.BooleanVar()
        self.unconstr.set(False)
        self.dscalar = tk.BooleanVar()
        self.dscalar.set(False)
        self.dunconstr = tk.BooleanVar()
        self.dunconstr.set(False)
        self.enclosure_depth = tk.StringVar()
        self.enclosure_depth.set('1.0')
        self.depth_sections = tk.StringVar()
        self.depth_sections.set('1.0')


        self.filename.set(filename)

        self.headers = self.get_headers(self.filename.get())
    
        name_col_label = tk.Label(self, text='Name Column', bg='white')
        name_col_label.pack()
        name_col_dropdown = tk.OptionMenu(self, self.name_col, *self.headers)
        name_col_dropdown.pack()

        x_col_label = tk.Label(self, text = "X Column", bg='white')
        x_col_label.pack()
        x_col_dropdown = tk.OptionMenu(self, self.x_col, *self.headers)
        x_col_dropdown.pack()

        y_col_label = tk.Label(self, text = "Y Column", bg='white')
        y_col_label.pack()
        y_col_dropdown = tk.OptionMenu(self, self.y_col, *self.headers)
        y_col_dropdown.pack()

        z_col_label = tk.Label(self, text = "Z Column", bg='white')
        z_col_label.pack()
        z_col_dropdown = tk.OptionMenu(self, self.z_col, *self.headers)
        z_col_dropdown.pack()

        m_label = tk.Label(self, text = "Scaling Factor (m)", bg='white')
        m_label.pack()
        m_slider = tk.Scale(self, from_=1, to=10, orient=HORIZONTAL, variable=self.m)
        m_slider.pack()

        n_label = tk.Label(self, text = "Stages in bandwith optimization (n)", bg='white')
        n_label.pack()
        n_slider = tk.Scale(self, from_=1, to=10, orient=HORIZONTAL, variable=self.n)
        n_slider.pack()

        # Select plugins
        plugins_label = tk.Label(self, text = "Select Plugins", bg = 'white')
        plugins_label.pack()
        samse_checkbox = tk.Checkbutton(self, text='samse', variable=self.samse)
        samse_checkbox.pack()
        unconstr_checkbox = tk.Checkbutton(self, text='unconstr', variable=self.unconstr)
        unconstr_checkbox.pack()
        dscalar_checkbox = tk.Checkbutton(self, text='dscalar', variable=self.dscalar)
        dscalar_checkbox.pack()
        dunconstr_checkbox = tk.Checkbutton(self, text='dunconstr', variable=self.dunconstr)
        dunconstr_checkbox.pack()

        # # Select contours
        contours_label = tk.Label(self, text = "Input Contours", bg='white')
        contours_label.pack()
        self.contours_textbox = tk.Text(self, height=1, width=20)
        self.contours_textbox.pack()
        
        is_2d_checkbox = tk.Checkbutton(self, text="Check here if data is 2D", variable=self.is_2d)
        is_2d_checkbox.pack()

        noise_checkbox = tk.Checkbutton(self, text='Add noise to data?', variable=self.noise)
        noise_checkbox.pack()

        depth_sections_label = tk.Label(self, text = "Number of Depth Sections", bg='white')
        depth_sections_label.pack()
        self.depth_sections_textbox = tk.Text(self, height=1, width=20)
        self.depth_sections_textbox.pack()

        depth_label = tk.Label(self, text="Enclosure Depth", bg='white')
        depth_label.pack()
        self.depth_textbox = tk.Text(self, height=1, width=20)
        self.depth_textbox.pack()
       
        tmp_button = tk.Button(self, text="Run KDE",
                                command=lambda: self.run_kde())
        tmp_button.pack()

    def get_headers(self, file):
        headers = list(pd.read_excel(file).columns)
        headers.append("N/A")
        return headers

    def create_options(self):
        options = {}
        options['name_col'] = self.name_col.get()

    def bool_to_str(self, b):
        if b:
            return 't'
        else:
            return 'f'

    def kde_thread_handler(self):
        kde_thread = multiprocessing.Process(target=self.run_kde)
        kde_thread.start()
        kde_thread.join()

    '''
    Selecting an output directory for the KDE calculations through python before the R script
    '''
    def select_output(self):
        validFile = False
        self.outputname = filedialog.askdirectory(title = "Select a Directory for Output")

    def get_contours(self):
        contours = self.contours_textbox.get(1.0, "end")
        contours = re.sub(","," ", contours)
        contours = re.sub("\s+", " ", contours)
        contours = re.sub("\s+\Z", "", contours)
        contours = re.split("\s", contours)

        contour_ints = []

        for c in contours:
            contour_ints.append(int(c))

        return contour_ints

    def set_enclosure_depth(self):
        self.enclosure_depth.set(self.depth_textbox.get(1.0, "end"))
    
    def set_depth_sections(self):
        self.depth_sections.set(self.depth_sections_textbox.get(1.0, "end"))

    # TODO: add contours and output path do dict
    def get_kde_args_dict(self) -> dict:
        kde_args = {}

        kde_args['filename'] = self.filename.get()
        kde_args['is2d'] = self.is_2d.get()
        kde_args['name_col'] = self.name_col.get()
        kde_args['x_col'] = self.x_col.get()
        kde_args['y_col'] = self.y_col.get()
        kde_args['z_col'] = self.z_col.get()
        kde_args['noise'] = self.noise.get()
        kde_args['m'] = self.m.get()
        kde_args['n'] = self.n.get()
        kde_args['samse'] = self.samse.get()
        kde_args['unconstr'] = self.unconstr.get()
        kde_args['dscalar'] = self.dscalar.get()
        kde_args['dunconstr'] = self.dunconstr.get()
        kde_args['enclosure_depth'] = self.enclosure_depth.get()
        kde_args['depth_sections'] = self.depth_sections.get()
        kde_args['output_dir'] = self.outputname
        kde_args['cs'] = self.get_contours()


        return kde_args

    def run_kde(self):

        self.select_output()

        kde_args = self.get_kde_args_dict()
        with open(JSON_PATH, "w") as outfile:
            json.dump(kde_args, outfile)

        subprocess.call(['Rscript', 'src/rscripts/3D_KDE_2021.R', JSON_PATH])

        # # Alert user that calculations are done
        messagebox.showinfo("Complete", "KDE calculations are complete")

