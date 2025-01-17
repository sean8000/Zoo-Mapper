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
from Moon_Scrape_Raw_Python import *

import pandas as pd
import csv
import subprocess
import multiprocessing
import threading
import re
import json
import os

import moon_scrape_home

#import Negating_row

LARGE_FONT = ("Bell Gothic Std Black", 40, 'bold')
MEDIUM_FONT = ("Bell Gothic Std Black", 25, 'bold')
BUTTON_FONT = ('Calibiri', 14, 'bold')
BACKGROUND_COLOR = '#407297'
LIGHT_BLUE = '#d4e1fa'

class Doc_To_Excel_Moon_Scrape_Page(tk.Frame):
	def __init__(self, parent, controller):
		def show_back():
			from moon_scrape_home import Moon_Scrape_Home_Page
			controller.show_frame(Moon_Scrape_Home_Page) 
		"""
		This function creates the landing page when users run Moon Scrapes.
		We will be able to select the file we want to run, allow us to select the 
		excel sheet we are grabbing data fom, inputting our columns and scraping 
		the moon data 
		Inputs:
			self: Represents the page that we have created
			parent:
			controller: 
		Results:
			The page will be up and ready for the user to interact with
		"""
		# Setting our variables
		self.filename = "None"           		# Variable will store the name of the file we want to oon scrape
		self.file_extension = "None"	 		# Variable that will store the extension of the file (must be .docx)
		self.info_page = "None"
		self.tmp = tk.StringVar()       		# setting self 

		self.tmp.set("hello")


		# Creating the title of the web page
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Scraping Moon Data From Doc to New Excel", font=MEDIUM_FONT)    		# Creates the title of the web pag
		label.pack(pady=10, padx=10)                                                # Padding the name

		# Creating Buttons for web page
		select_button = ttk.Button(self, text="Select File",
										command=lambda: self.select_file())         # Select File button, look to function select_file # 76 to see what it does   
		select_button.pack()        # called with keyword-option/value pairs that control where the widget is to appear within its container
									#and how it is to behave when the main application window is resized
		
		# Will begin the process of running the webpage
		options_button = ttk.Button(self, text="Run Moon Scrape",
									command=lambda: self.get_parameters())          # Taken from kde, repurposed
		options_button.pack()

		# Button that allows you to return the the homepage
		back_button = ttk.Button(self, text="Back to Moon Scrape Home",
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
		self.filename = askopenfilename(initialdir="", title="Select a File", filetypes=(("Doc Files", "*.docx*"), ("All Files", "*.*")))

		file_type = self.filename[self.filename.index('.'):] # grabbing the type of the filw

		# Checking to make sure the file is an .xslx 
		if file_type == ".docx":
			validFile = True
			file_extension = file_type

		# else: # presumabley to make sure that we are not allowing a file that is not valid to be saved
		#     errorMessage(Error.FILETYPE)
		#     self.filename = ""


	def get_parameters(self):
		"""
		grabbing all of the information and parameters from the file we have selected
		"""
		info_page = Params_Page(self.filename)
		info_page.wait_window(info_page)
			
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
		self.latitude= tk.StringVar()
		self.longitude= tk.StringVar()
		self.new_excel_name = tk.StringVar()


		self.filename.set(filename)         		# setting filename to the filename the user input

		# Grab Latitude
		latitude_label = tk.Label(self, text="Input Latitude", bg='white')
		latitude_label.pack()
		
		latitude_entry = ttk.Entry(self, textvariable=self.latitude)
		latitude_entry.pack(fill='x', expand=True)
		latitude_entry.focus()
  
		# Grab Longitude
		longitude_label = tk.Label(self, text="Input Longitude", bg='white')
		longitude_label.pack()
		
		longitude_entry = ttk.Entry(self, textvariable=self.longitude)
		longitude_entry.pack(fill='x', expand=True)
		longitude_entry.focus()

		# Grab new Excel File Name
		new_excel_label = tk.Label(self, text="Input Name of New Excel Sheet", bg='white')
		new_excel_label.pack()
		
		new_excel_entry = ttk.Entry(self, textvariable=self.new_excel_name)
		new_excel_entry.pack(fill='x', expand=True)
		longitude_entry.focus()

		# Press to run the Scrape
		tmp_button = tk.Button(self, text="Run Moon Scrape",
								command=lambda: self.run_scrape())
		tmp_button.pack()
	
	def run_scrape(self):
		print("Filename", self.filename.get())
		print("Latitude", self.latitude.get())
		print("Longitude", self.longitude.get())
		print("New Excel Name", self.new_excel_name.get())

		doc_to_excel_Moon_Data(self.filename.get(), self.latitude.get(), self.longitude.get(), self.new_excel_name.get())