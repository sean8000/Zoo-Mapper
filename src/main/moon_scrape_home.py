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

from moon_scrape_doc_to_excel import Doc_To_Excel_Moon_Scrape_Page
from moon_scrape_excel_to_excel import Excel_To_Excel_Moon_Scrape_Page
from moon_scrape_excel_to_sheet import Excel_To_Sheet_Moon_Scrape_Page
import heatmappage

#import Negating_row

LARGE_FONT = ("Bell Gothic Std Black", 40, 'bold')
MEDIUM_FONT = ("Bell Gothic Std Black", 25, 'bold')
BUTTON_FONT = ('Calibiri', 14, 'bold')
BACKGROUND_COLOR = '#407297'
LIGHT_BLUE = '#d4e1fa'

class Moon_Scrape_Home_Page(tk.Frame):
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

		# Creating the title of the web page
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Moon Scrape", font=MEDIUM_FONT)    # Creates the title of the web page
		label.pack(pady=10, padx=10)                                                # Padding the name

		# Creating Buttons for web page
		joins_light = ttk.Button(self, text="Scrape Info from Google Doc to Excel Sheet",
							command=lambda: controller.show_frame(Doc_To_Excel_Moon_Scrape_Page))
		joins_light.pack()

		joins_rubbing = ttk.Button(self, text="Scrape Info from Excel and Create new Excel",
							command=lambda: controller.show_frame(Excel_To_Excel_Moon_Scrape_Page))
		joins_rubbing.pack()

		joins_both = ttk.Button(self, text="Scrape Info from Excel and add New Sheet to tht Excel",
							command=lambda: controller.show_frame(Excel_To_Sheet_Moon_Scrape_Page))
		joins_both.pack()

		back_button = ttk.Button(self, text="Back to Home",
							command=lambda: controller.show_frame(heatmappage.StartPage))    # setting up the back to home button. goes back to start page for heat map
		back_button.pack()
