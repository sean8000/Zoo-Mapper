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

class Joins_Page_Both(tk.Frame):
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
		self.filename = "None"           # setting the file selection to None
		self.filename2 = "None"			 # Since you are joining 2 spreadsheets, you need to have 2 stored file names
		self.outputname = "None"          # Setting the outpot name of the file to NULL
		self.tmp = tk.StringVar()       
		self.tmp.set("hello")


		# Creating the title of the web page
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Data Transformations", font=MEDIUM_FONT)    # Creates the title of the web page
		label.pack(pady=10, padx=10)                                                # Padding the name

		# Creating Buttons for web page
		#Select light/temp file, select data file, run, and back to joins home page
		select_button = ttk.Button(self, text="Select Light/Temp File",
										command=lambda: self.select_file())         # Select File button, look to function select_file # 76 to see what it does   
		select_button.pack()        # called with keyword-option/value pairs that control where the widget is to appear within its container
									#and how it is to behave when the main application window is resized
		
		select_button2 = ttk.Button(self, text="Select Data File",
										command=lambda: self.select_file2())  
		select_button2.pack()

		options_button = ttk.Button(self, text="Run Transformations",
									command=lambda: self.get_parameters())          # Creates the options pop up pox
		options_button.pack()

		back_button = ttk.Button(self, text="Back to Joins",
							command=lambda: show_back())    # setting up the back to home button. goes back to start page for heat map
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
		This function is the same as above, it is just used to select the second file, could have been
		done with 1 function and an extra param, but whatever. 
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
		Different than the other ones, options box takes a second param which is the second file
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
			filename2: Filename of the second input file. 
		"""
		tk.Toplevel.__init__(self)  # constucting a main window of an application and making sure it is in the front of the screen
		self.attributes('-topmost', 'true')

		# We know what data we need for the calcularions so we are specifying the types they should all be
		self.filename = tk.StringVar()      # filename
		self.filename2 = tk.StringVar()  	# filename2
		self.outputname = tk.StringVar()    # Ouput directory
		self.lightDateTime = tk.StringVar()  	#DateTime column in the light/temp file
		self.rawDateTime = tk.StringVar()		#DateTime column in the data file
		self.categ = tk.StringVar()				#Type of behavior column (usually All Occurrence)
		self.channelType = tk.StringVar()		#Channel type column
		self.channelDuration = tk.StringVar()	#Channel duration column

		self.filename.set(filename)         # setting filename to the filename the user input
		self.filename2.set(filename2)		# set second filename
		self.headers = self.get_headers(self.filename.get())            #grabbing the names of the headers from the file we input
		self.headers2 = self.get_headers(self.filename2.get())

		#Create dropdown to select DateTime column from the light/temp excel sheet. 
		lightDateTime_label = tk.Label(self, text='Light Date Time Column', bg='white')       # Name of the column you want to invert
		lightDateTime_label.pack()                                                   # called with keyword-option/value pairs that control where the widget is to appear within its container
		lightDateTime_dropdown = tk.OptionMenu(self, self.lightDateTime, *self.headers)   # populating column with the data stored in the  column
		lightDateTime_dropdown.pack()
	   
	   #Create dropdown to select DateTime column from the data excel sheet.
		rawDateTime_label = tk.Label(self, text='Data Date Time Column', bg='white')       # Name of the column you want to invert
		rawDateTime_label.pack()                                                   # called with keyword-option/value pairs that control where the widget is to appear within its container
		rawDateTime_dropdown = tk.OptionMenu(self, self.rawDateTime, *self.headers2)   # populating column with the data stored in the  column
		rawDateTime_dropdown.pack()

		#Create dropdown to select the All Occurrence column from the data excel sheet.
		categ_label = tk.Label(self, text='All Occurrence Value Column', bg='white')       # Name of the column you want to invert
		categ_label.pack()                                                   # called with keyword-option/value pairs that control where the widget is to appear within its container
		categ_dropdown = tk.OptionMenu(self, self.categ, *self.headers2)   # populating column with the data stored in the  column
		categ_dropdown.pack()

		#Create dropdown to select the Channel Type column from the data excel sheet.
		channelType_label = tk.Label(self, text='Channel Type Column', bg='white')       # Name of the column you want to invert
		channelType_label.pack()                                                   # called with keyword-option/value pairs that control where the widget is to appear within its container
		channelType_dropdown = tk.OptionMenu(self, self.channelType, *self.headers2)   # populating column with the data stored in the  column
		channelType_dropdown.pack()

		#Create dropdown to select the Continuous Channel Duration column from the data excel sheet.
		channelDuration_label = tk.Label(self, text='Continuous Channel Duration Column', bg='white')       # Name of the column you want to invert
		channelDuration_label.pack()                                                   # called with keyword-option/value pairs that control where the widget is to appear within its container
		channelDuration_dropdown = tk.OptionMenu(self, self.channelDuration, *self.headers2)   # populating column with the data stored in the  column
		channelDuration_dropdown.pack()

		#Button that runs the join, inside the options box
		tmp_button = tk.Button(self, text="Run Join",
								command=lambda: self.run_join())
		tmp_button.pack()

	def get_headers(self, file):
		'''
		Gets the column headers for the excel file
		'''
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
		'''
		Params:
			df: The pandas dataframe (excel sheet)
			datetime: A datetime object passed into the function

		This function takes a datetime object passed in from a cell, and subtracts it with itself with a day
		offset to get a time delta of 1 day (a bit unnecessary but its already done)
		
		Iterates through the spreadsheet rows, if any datetime in a row is less than a day or the previous 
		minimum, and the row's all occurrence value is repetitive rubbing, it saves that time difference 
		and row number. 

		Essentially a min finding function but using datetime and timedeltas, returns -1 if no row was 
		within a day that was also repetive rubbing, otherwise returns the row number of that row (index)
		'''
		#This is the difference at the start, which is datetime - 1 day
		excelDateTime = self.rawDateTime.get()
		behavior = self.categ.get()
		time_difference = (datetime - (datetime - pd.DateOffset(1))).total_seconds() #Creates a time delta of 1 day in seconds
		returnIndex = -1

		#For loop that finds the minimum
		for i, row in df.iterrows():
			#Remember to convert time to datetime
			sub_time = abs((datetime - pd.to_datetime(row[excelDateTime])).total_seconds()) #Convert the time delta to total seconds
			#Only currently works with this specific 'Repetitive rubbing' string, case specific
			if sub_time < time_difference and row[behavior] == 'Repetitive rubbing': #must be rubbing
				time_difference = sub_time #setting time difference equal to found minimum
				returnIndex = i #row number returned
	
		return returnIndex
		
	def run_join(self):
		self.select_output()
		rawTime = self.rawDateTime.get()
		lightTime = self.lightDateTime.get()
		df_raw = pd.read_excel(self.filename2.get(), sheet_name=0) #read data excel
		df_light = pd.read_excel(self.filename.get(), sheet_name=0) #read light excel

		df_light= df_light.rename(columns={lightTime: 'rawDateTimeDup'}) #renaming columns

		df_raw[rawTime] = pd.to_datetime(df_raw[rawTime])
		df_light['rawDateTimeDup'] = pd.to_datetime(df_light['rawDateTimeDup'])

		#Rounded to the nearest 15 minutes because the datetime in the lighttemp file is in 15 minute intervals.
		df_raw['roundedDateTime'] = df_raw[rawTime].dt.round('15min') #Make a new column, round datetime to nearest 15 minutes
		df_light['roundedDateTime'] = df_light['rawDateTimeDup'].dt.round('15min') #Make a new column, round datetime to nearest 15 minutes

		#Does a left join from data spreadsheet onto light spreadsheet, matching entries on roundedDateTime 
		df_merged = pd.merge(df_raw, df_light, on='roundedDateTime', how="left")  
		df_merged = df_merged.drop('rawDateTimeDup', axis=1) #drop unnecessary column
		df_merged= df_merged.rename(columns={'#': 'Matching Row'})

		
		#Initial join above #deals with times in the light/temp spreadsheet
		#Second aspect of join below #deals with behaviors, the repetitive rubbing matching


		'''
		For loop that iterates through the rows, when it finds a row with a continuous value in the 
		channel type, when it finds a continuous row, it takes the value stored in channel duration
		and places it in the corresponding row that is returned from the find_closest_time() function

		If the return value is -1, then there was no value within a day that were repetitive rubbing, 
		so return a data joins failed message, otherwise store the value. If a value is already stored in that cell, 
		(2 times matched to that repetive rubbing behavior), concatenate that value to the end.
		'''
		for i, row in df_merged.iterrows():
			#Remember to convert time to datetime
			#Only works with continuous times
			channelType = self.channelType.get()
			channelDuration = self.channelDuration.get()
			excelDateTime = self.rawDateTime.get()
			if row[channelType] == 'Continuous':  #find continuous value at that row
				print("continuous at: ", i)
				#print("Keyval error at: ", i)
				stored_value = int (row[channelDuration])
				print("The stored value for the rubbing is: ", int(stored_value))
				timestamp = pd.to_datetime(row[excelDateTime])
				#print('before closest time')
				return_value = self.find_closest_time(df_merged, timestamp) #call function to find closest time
				#print("after closest time")
				print("Closest time returned: ", stored_value)
				if (return_value == -1):
					#print("There was nothing closest to this time, -1 returned ")
					
					#Raise an error and show that the data join failed because of date range
					messagebox.showinfo("Complete", "Data Joins failed due to range outside of a day")
					raise Exception("There is a spreadsheet entry with a continuous behavior, and no rubbing behavior within that day")
				else:
					print("The returned date time of this current column is: ", df_merged[excelDateTime][i])
					print("The returned time is: ", df_merged[excelDateTime][return_value])
					if pd.isnull(df_merged.loc[return_value, channelDuration]):
						#place stored_value at the returned row index in the channelDuration column
						df_merged.at[return_value, channelDuration] = stored_value
					else:
						#If a value is already stored there, concatenate the lastest value onto the end
						print("Adding second value...")
						df_merged.at[return_value, channelDuration] = str(df_merged.at[return_value, channelDuration]) + ", " + str(stored_value)

		#For some reason not working in applied version, but did in hardcoded version
		#df_merged = df_merged.drop('Unnamed: 0', axis=1)

		#Create the file name, write it to the output directory, show the complete message
		file_name = os.path.splitext(os.path.basename(self.filename2.get()))[0]
		outdir = self.outputname + "/" + file_name + "_Data_Join.xlsx"
		df_merged.to_excel(outdir)
		messagebox.showinfo("Complete", "Data Joins complete")