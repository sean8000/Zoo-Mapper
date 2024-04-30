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
#from joins_home import Joins_Home_Page
#import Negating_row

LARGE_FONT = ("Bell Gothic Std Black", 40, 'bold')
MEDIUM_FONT = ("Bell Gothic Std Black", 25, 'bold')
BUTTON_FONT = ('Calibiri', 14, 'bold')
BACKGROUND_COLOR = '#407297'
LIGHT_BLUE = '#d4e1fa'

class Joins_Page_Light(tk.Frame):
	'''
	Refer to joins_both.py for general documentation, this file is just a portion of joins_both
	It only does the light/temp portion of the join (1st half)
	'''
	def __init__(self, parent, controller):
		def show_back():
			from joins_home import Joins_Home_Page
			controller.show_frame(Joins_Home_Page) 
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
		self.filename2 = "None"
		self.outputname = "None"          # Setting the outpot name of the file to NULL
		self.tmp = tk.StringVar()       
		self.tmp.set("hello")


		# Creating the title of the web page
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Data Transformations", font=MEDIUM_FONT)    # Creates the title of the web page
		label.pack(pady=10, padx=10)                                                # Padding the name

		# Creating Buttons for web page
		select_button = ttk.Button(self, text="Select Light/Temp File",
										command=lambda: self.select_file())         # Select File button, look to function select_file # 76 to see what it does   
		select_button.pack()        # called with keyword-option/value pairs that control where the widget is to appear within its container
									#and how it is to behave when the main application window is resized
		
		select_button2 = ttk.Button(self, text="Select Data File",
										command=lambda: self.select_file2())  
		select_button2.pack()

		options_button = ttk.Button(self, text="Run Transformations",
									command=lambda: self.get_parameters())          # Taken from kde, repurposed
		options_button.pack()

		back_button = ttk.Button(self, text="Back to Joins",
							command=lambda: show_back())
		# setting up the back to home button. goes back to start page for heat map
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


	def select_file2(self):
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
		self.filename2 = askopenfilename(initialdir="", title="Select a File", filetypes=(("Excel Files", "*.xlsx*"), ("CSV Files", "*.csv*"), ("All Files", "*.*")))

		file_type = self.filename2[self.filename2.index('.'):] # grabbing the typr of the filw

		# Checking to make sure the file is an .xslx or a .csv
		if file_type == ".xlsx":
			validFile = True
		if file_type == ".csv":
			validFile = True

		# else: # presumabley to make sure that we are not allowing a file that is not valid to be saved
		#     errorMessage(Error.FILETYPE)
		#     self.filename2 = ""


	def get_parameters(self):
		"""
		grabbing all of the information and parameters from the file we have selected
		"""
		options_box = Params_Page(self.filename, self.filename2)
		options_box.wait_window(options_box)
		
		

"""
This page allows users to select parameters for KDE calculations and
run the KDE script
"""
class Params_Page(tk.Toplevel):
	def __init__(self, filename, filename2):
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
		self.filename2 = tk.StringVar()  
		self.outputname = tk.StringVar()    # unsure
		self.lightDateTime = tk.StringVar()   
		self.rawDateTime = tk.StringVar() 
		

		self.filename.set(filename)         # setting filename to the filename the user input
		self.filename2.set(filename2)
		self.headers = self.get_headers(self.filename.get())            #grabbing the names of the headers from the file we input
		self.headers2 = self.get_headers(self.filename2.get())

		lightDateTime_label = tk.Label(self, text='Light Date Time Column', bg='white')       # Name of the column you want to invert
		lightDateTime_label.pack()                                                   # called with keyword-option/value pairs that control where the widget is to appear within its container
		lightDateTime_dropdown = tk.OptionMenu(self, self.lightDateTime, *self.headers)   # populating column with the data stored in the  column
		lightDateTime_dropdown.pack()
	   
		rawDateTime_label = tk.Label(self, text='Data Date Time Column', bg='white')       # Name of the column you want to invert
		rawDateTime_label.pack()                                                   # called with keyword-option/value pairs that control where the widget is to appear within its container
		rawDateTime_dropdown = tk.OptionMenu(self, self.rawDateTime, *self.headers2)   # populating column with the data stored in the  column
		rawDateTime_dropdown.pack()

		tmp_button = tk.Button(self, text="Run Join",
								command=lambda: self.run_join())
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

	def find_closest_time(self, df, datetime):

		#This is the difference at the start, which is datetime - 1 day
		excelDateTime = self.rawDateTime.get()
		behavior = self.categ.get()
		time_difference = (datetime - (datetime - pd.DateOffset(1))).total_seconds()
		returnIndex = -1

		for i, row in df.iterrows():
			#Remember to convert time to datetime
			sub_time = abs((datetime - pd.to_datetime(row[excelDateTime])).total_seconds())
			#Only currently works with this specific 'Repetitive rubbing' string, case specific
			if sub_time < time_difference and row[behavior] == 'Repetitive rubbing':
				time_difference = sub_time
				returnIndex = i
	
		return returnIndex
		
	def run_join(self):
		self.select_output()
		rawTime = self.rawDateTime.get()
		lightTime = self.lightDateTime.get()
		df_raw = pd.read_excel(self.filename2.get(), sheet_name=0)
		df_light = pd.read_excel(self.filename.get(), sheet_name=0)

		df_light= df_light.rename(columns={lightTime: 'rawDateTimeDup'})

		df_raw[rawTime] = pd.to_datetime(df_raw[rawTime])
		df_light['rawDateTimeDup'] = pd.to_datetime(df_light['rawDateTimeDup'])
		df_raw['roundedDateTime'] = df_raw[rawTime].dt.round('15min')
		df_light['roundedDateTime'] = df_light['rawDateTimeDup'].dt.round('15min')

		df_merged = pd.merge(df_raw, df_light, on='roundedDateTime', how="left")  
		df_merged = df_merged.drop('rawDateTimeDup', axis=1)
		df_merged= df_merged.rename(columns={'#': 'Matching Row'})

		
		#Initial join above #deals with times
		
		file_name = os.path.splitext(os.path.basename(self.filename2.get()))[0]
		outdir = self.outputname + "/" + file_name + "_Data_Join.xlsx"
		df_merged.to_excel(outdir)
		messagebox.showinfo("Complete", "Data Light/Temp Join Complete")